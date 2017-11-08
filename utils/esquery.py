import re


def match_gen(keywords):
    result = {'must': [], 'should': [], 'filter': []}
    match_str = re.sub('"(.*?)"', '', keywords)
    match_phrase_list = re.findall('"(.*?)"', keywords)
    if len(match_str.replace(' ', '')) > 0:
        result["should"] = [{
                "match_phrase": {
                    "content": {
                        "query": match_str,
                        "slop":  50}
                    }
            }]
        result['must'].append({"match": {"content": {"query": match_str,
                                                   "minimum_should_match": "30%"}}})
    for keyword in match_phrase_list:
        result['must'].append({"match_phrase": {"content": {"query": keyword}}})
    return result


def filter_gen(filterdict):
    result = {'must': [], 'should': [], 'filter': []}
    if 'date' in filterdict:
        for index in range(len(filterdict['date'])):
            filterdict['date'][index] = filterdict['date'][index].replace('-', '')
    for key, value in filterdict.items():
        if not value:
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


def request_gen(keywords=None, filterdict=None, ids=None):
    if keywords is None:
        keywords = ''
    if filterdict is None:
        filterdict = dict()
    if ids is not None:
        filterdict['_id'] = list(ids)
    querydict = {'query': {'bool': {}}}
    match_query = match_gen(keywords)
    filter_query = filter_gen(filterdict)
    if keywords:
        for each in match_query:
            if match_query[each]:
                if each not in querydict['query']['bool']:
                    querydict['query']['bool'][each] = list()
                querydict['query']['bool'][each].extend(match_query[each])
    if filterdict:
        for each in filter_query:
            if filter_query[each]:
                if each not in querydict['query']['bool']:
                    querydict['query']['bool'][each] = list()
                querydict['query']['bool'][each].extend(filter_query[each])
    return querydict


def scroll(esconn, indexname, kwargs, start=0, size=None):
    count = 0
    result = list()
    scroll = True if start + size > 10000 else False
    if scroll:
        start = 0
        kwargs['scroll'] = '1m'
    page = esconn.search(
            index=indexname,
            from_=start,
            size=size,
            request_timeout=30,
            **kwargs)
    if size is None or (size+start) > page['hits']['total']:
        size = page['hits']['total']-start

    while (len(page['hits']['hits']) > 0 and count < size):
        result.extend(page['hits']['hits'])
        count += len(page['hits']['hits'])
        if scroll:
            sid = page['_scroll_id']
            page = esconn.scroll(scroll_id = sid, scroll = '1m', request_timeout=30)
    return result


def count(esconn, indexname, kwargs):
    page = esconn.count(index=indexname, **kwargs)
    return page['count']
