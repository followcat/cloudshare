# -*- coding: utf-8 -*-
import re


def convert_filterdict(keywords):
    result = dict()
    convert_dict = {
        u'简历ID':    'id',
        u'上传人':     'committer',
        u'姓名':      'name',
        u'邮箱':      'email',
        u'性别':      'gender',
        u'手机':      'phone',
        u'年龄':      'age',
        u'学历':      'education',
        u'职位':      'position',
        u'公司':      'experience.company.name',
        u'最近公司':    'company',
        u'行业':      'classify',
        u'来源':      'origin',
        u'婚姻状况':    'marital_status'
    }
    filter_list = re.findall(u'([\u4E00-\u9FA5A-Za-z0-9_]+)[:：]([\u4E00-\u9FA5A-Za-z0-9_]+)',
                             keywords)
    keywords = re.sub(u'([\u4E00-\u9FA5A-Za-z0-9_]+)[:：]([\u4E00-\u9FA5A-Za-z0-9_]+)',
                      '', keywords)
    for each in filter_list:
        key, value = each
        if key in convert_dict:
            result[convert_dict[key]] = value
    return keywords, result


def match_gen(key, keywords, must=True, slop=0):
    result = {'must': [], 'should': [], 'filter': []}
    match_str = re.sub('"(.*?)"', '', keywords)
    match_phrase_list = re.findall(u'[“"](.*?)["”]', keywords)
    if len(match_str.replace(' ', '')) > 0:
        result["should"] = [{
                "match_phrase": {
                    key: {
                        "query": match_str,
                        "slop":  slop}
                    }
            }]
        if must is True:
            result['must'].append({"match": {key: {"query": match_str,
                                                   "minimum_should_match": "30%"}}})
    for keyword in match_phrase_list:
        result['must'].append({"match_phrase": {key: {"query": keyword}}})
    return result


def filter_gen(filterdict):
    result = {'must': [], 'should': [], 'filter': []}
    if 'date' in filterdict:
        for index in range(len(filterdict['date'])):
            filterdict['date'][index] = filterdict['date'][index].replace('-', '')
    for key, value in filterdict.items():
        if value is None:
            continue
        if key == 'date':
            if len(value[0]) > 0:
                daterange = {'range': {'date': {'gte': value[0], 'lte': value[1]}}}
                result['filter'].append(daterange)
        elif key == 'age':
            if value[0] is not None or value[1] is not None:
                agerange = {'range': {'age': {'gte': str(value[0]) if value[0] else '0',
                                              'lte': str(value[1]) if value[1] else '99'}}}
                result['filter'].append(agerange)
        elif key == 'expectation_places':
            result['filter'].append({'terms': {'expectation.places': value}})
        elif key == 'current_places':
            result['filter'].append({'terms': {'current.places': value}})
        elif key == 'business':
            result['filter'].append({'terms': {'classify': value}})
        else:
            if isinstance(value, list):
                result['filter'].append({'terms': {key.lower(): value}})
            else:
                result['filter'].append({'term': {key.lower(): value}})
    return result


def getmappings(esconn, fields, index=None, doctype=None):
    results = dict()
    try:
        mapping = esconn.indices.get_field_mapping(fields=fields, index=index, doc_type=doctype)
    except Exception as e:
        if e.status_code == 404:
            mapping = {}
        else:
            raise e
    for index in mapping:
        for mapid in mapping[index]['mappings']:
            for name in mapping[index]['mappings'][mapid]:
                fullname = mapping[index]['mappings'][mapid][name]['full_name']
                for key in mapping[index]['mappings'][mapid][name]['mapping']:
                    if fullname in results:
                        continue
                    results[fullname] = mapping[index]['mappings'][mapid]\
                                   [name]['mapping'][key]['type']
    return results


def request_gen(esconn, index=None, doctype=None, filterdict=None, ids=None, slop=0):
    querydict = dict()
    if filterdict is None:
        filterdict = dict()
    if ids is not None:
        filterdict['_id'] = ids
    if filterdict:
        querydict = {'query': {'bool': {}}}
        mappings = getmappings(esconn, fields=filterdict.keys(),
                               index=index, doctype=doctype)
        if '*' in filterdict:
            allshould = filterdict['*']
            filterdict.pop('*')
        for key in mappings:
            must = True
            if mappings[key] != 'text':
                continue
            keywords, str_filter = convert_filterdict(filterdict[key])
            filterdict[key] = keywords
            filterdict.update(str_filter)
        mappings = getmappings(esconn, fields=filterdict.keys(),
                               index=index, doctype=doctype)
        for key in mappings:
            must = True
            if mappings[key] != 'text':
                continue
            if key not in filterdict:
                must = False
                filterdict[key] = allshould
            match_query = match_gen(key, filterdict[key], must=must, slop=slop)
            for each in match_query:
                if match_query[each]:
                    if each not in querydict['query']['bool']:
                        querydict['query']['bool'][each] = list()
                    querydict['query']['bool'][each].extend(match_query[each])
            filterdict.pop(key)
        filter_query = filter_gen(filterdict)
        for each in filter_query:
            if filter_query[each]:
                if each not in querydict['query']['bool']:
                    querydict['query']['bool'][each] = list()
                querydict['query']['bool'][each].extend(filter_query[each])
    return querydict


def scroll(esconn, kwargs, index=None, doctype=None, start=0, size=None, scroll=None):
    count = 0
    result = list()
    if size is None:
        size = 10000
    if scroll is not None:
        kwargs['scroll'] = scroll
    if 'sort' in kwargs:
        sort = kwargs.pop('sort')
        if 'body' not in kwargs:
            kwargs['body'] = dict()
        kwargs['body']['sort'] = sort
    page = esconn.search(
            index=index,
            doc_type=doctype,
            from_=start,
            size=size,
            request_timeout=30,
            **kwargs)
    total = page['hits']['total']
    if scroll is not None or total < size:
        size = page['hits']['total']

    while (len(page['hits']['hits']) > 0 and count < size):
        result.extend(page['hits']['hits'])
        count += len(page['hits']['hits'])
        if scroll:
            sid = page['_scroll_id']
            page = esconn.scroll(scroll_id = sid, scroll = '1m', request_timeout=30)
    return total, result


def count(esconn, kwargs, index=None, doctype=None):
    page = esconn.count(index=index, doc_type=doctype, **kwargs)
    return page['count']
