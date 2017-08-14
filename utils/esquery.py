import re


def match_gen(keywords):
    result = {'query': {'bool': {'must': [], 'should': []}}}
    match_str = re.sub('"(.*?)"', '', keywords)
    match_phrase_list = re.findall('"(.*?)"', keywords)
    if len(match_str.replace(' ', '')) > 0:
        result["query"]["bool"]["should"] = {
                "match_phrase": {
                    "content": {
                        "query": match_str,
                        "slop":  50}
                    }
            }
        result['query']['bool']['must'].append({"match": {"content": {"query": match_str,
                                                   "minimum_should_match": "30%"}}})
    for keyword in match_phrase_list:
        result['query']['bool']['must'].append({"match_phrase": {"content": {"query": keyword}}})
    return result


def filter_gen(filterdict):
    result = {'query': {'bool': {'filter': []}}}
    if 'date' in filterdict:
        for index in range(len(filterdict['date'])):
            filterdict['date'][index] = filterdict['date'][index].replace('-', '')
    mustlist = result['query']['bool']['filter']
    for key, value in filterdict.items():
        if not value:
            continue
        if key == 'date':
            if len(value[0]) > 0:
                daterange = {'range': {'date': {'gte': value[0], 'lte': value[1]}}}
                mustlist.append(daterange)
        elif key == 'age':
            if value[0] is not None or value[1] is not None:
                agerange = {'range': {'age': {'gte': str(value[0]) if value[0] else '0',
                                              'lte': str(value[1]) if value[1] else '99'}}}
                mustlist.append(agerange)
        elif key == 'expectation_places':
            mustlist.append({'terms': {'expectation.places': value}})
        elif key == 'current_places':
            mustlist.append({'terms': {'current.places': value}})
        elif key == 'business':
            mustlist.append({'terms': {'classify': value}})
        else:
            if isinstance(value, list):
                mustlist.append({'terms': {key.lower(): value}})
            else:
                mustlist.append({'term': {key.lower(): value}})
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
    querydict.update(match_query)
    querydict.update(filter_query)
    return querydict
