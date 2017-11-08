import math
import time
import collections

import elasticsearch.helpers

import utils.builtin
import utils.esquery


class ElasticsearchIndexing(object):

    doctype = 'index'
    index_config_body = {
        "template": doctype,
        "mappings": {
            "_default_": {
                "dynamic_templates": [
                    {
                        "content": {
                            "match":              "content",
                            "match_mapping_type": "string",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_max_word"
                            }
                    }},
                    {
                        "strings": {
                            "match_mapping_type": "string",
                                "mapping": {
                                    "type":       "keyword"
                                }
                    }}
                ]
            }
        }
    }

    def setup(self, esconn, index):
        self.es = esconn
        self.es.indices.create(index=index, body=self.index_config_body, ignore=400)

    def update(self, index, doctype, svcs, numbers=5000):
        for svc in svcs:
            self.updatesvc(index, doctype, svc, numbers=numbers)

    def genaction(self, index, doctype, id, data, info):
        _source = data
        if _source is None:
            _source = ''
        info.update({"content": _source})
        action = {
            "_op_type": 'index',
            "_index": index,
            "_type": doctype,
            "_source": info,
            "_id": id
            }
        return action

    def updatesvc(self, index, doctype, svc, numbers=5000):
        assert svc.name
        update_ids = set([item['_id'] for item in self.ESsearch(index=index, doctype=doctype )])
        ACTIONS = list()
        times = 0
        count = 0
        for id in svc.ids-update_ids:
            geninfo = self.genindex(svc.getyaml(id))
            data = svc.getmd(id)
            action = self.genaction(index, doctype, id, data, geninfo)
            ACTIONS.append(action)
            count += 1
            if count%numbers == 0:
                times += 1
                elasticsearch.helpers.bulk(self.es, ACTIONS,
                    raise_on_error=False, raise_on_exception=False, stats_only=True)
                ACTIONS = list()
                print("Add numbers %d to index."%(times*numbers))
        else:
            elasticsearch.helpers.bulk(self.es, ACTIONS,
                    raise_on_error=False, raise_on_exception=False, stats_only=True)
            print("Add numbers %d to index. And finished."%(times*numbers+len(ACTIONS)))

    def add(self, index, doctype, id, data, info):
        ACTIONS = list()
        geninfo = self.genindex(info)
        action = self.genaction(index, doctype, id, data, geninfo)
        ACTIONS.append(action)
        elasticsearch.helpers.bulk(self.es, ACTIONS,
                raise_on_error=False, raise_on_exception=False, stats_only=True)

    def upgrade(self, index, doctype, svcs, ids=None):
        for svc in svcs:
            self.upgradesvc(index, doctype, svc, ids=ids)

    def upgradesvc(self, index, doctype, svc, ids=None, numbers=5000):
        assert svc.name
        if ids is None:
            ids = svc.ids
        else:
            ids = set(ids) & svc.ids
        times = 0
        count = 0
        ACTIONS = list()
        for id in ids:
            geninfo = self.genindex(svc.getyaml(id))
            data = svc.getmd(id)
            action = self.genaction(index, doctype, id, data, geninfo)
            ACTIONS.append(action)
            count += 1
            if count%numbers == 0:
                times += 1
                elasticsearch.helpers.bulk(self.es, ACTIONS,
                    raise_on_error=False, raise_on_exception=False, stats_only=True)
                ACTIONS = list()
                print("Update numbers %d to index."%(times*numbers))
        else:
            elasticsearch.helpers.bulk(self.es, ACTIONS,
                    raise_on_error=False, raise_on_exception=False, stats_only=True)
            print("Update numbers %d to index. And finished."%(times*numbers+len(ACTIONS)))

    def ESsearch(self, index=None, doctype=None, querydict=None, kwargs=None,
                 source=False, start=0, size=None):
        if kwargs is None:
            kwargs = dict()
        kwargs.update({'body': querydict})
        kwargs['sort'] = '_doc' if 'sort' not in kwargs else kwargs['sort']
        kwargs['_source'] = 'false' if source is False else 'true'
        result = utils.esquery.scroll(self.es, kwargs, index=index, doctype=doctype,
                                      start=start, size=size)
        return result

    def count(self, index=None, doctype=None, keywords=None, filterdict=None,
              ids=None, kwargs=None):
        result = 0
        querydict = utils.esquery.request_gen(keywords=keywords,
                                              filterdict=filterdict, ids=ids)
        if kwargs is None:
            kwargs = dict()
        kwargs.update({'body': querydict})
        if ('filter' in querydict['query']['bool'] and querydict['query']['bool']['filter']) or\
            ('must' in querydict['query']['bool'] and querydict['query']['bool']['must']):
            result = utils.esquery.count(self.es, kwargs, index=index, doctype=doctype)
        return result

    def filter(self, index=None, doctype=None, keywords=None, filterdict=None, ids=None,
               source=False, start=0, size=None, kwargs=None):
        results = set()
        querydict = utils.esquery.request_gen(keywords=keywords,
                                              filterdict=filterdict, ids=ids)
        if ('filter' in querydict['query']['bool'] and querydict['query']['bool']['filter']) or\
            ('must' in querydict['query']['bool'] and querydict['query']['bool']['must']):
            results = self.ESsearch(index=index, doctype=doctype, querydict=querydict,
                                    kwargs=kwargs, source=source, start=start, size=size)
        return results

    def filter_ids(self, index=None, doctype=None, keywords=None, filterdict=None,
                   ids=None, source=False, start=0, size=None, kwargs=None):
        result = ids
        if filterdict:
            filterset = self.filter(index=index, doctype=doctype, keywords=keywords,
                                    filterdict=filterdict, ids=ids, source=source,
                                    start=start, size=size, kwargs=kwargs)
            result = set([item['_id'] for item in filterset])
        return result

    def lastday(self, index=None, doctype=None):
        lastday = '19800101'
        search_result = self.es.search(index=index, doc_type=doctype,
                                       sort='_score,date:desc', size = 1)
        try:
            lastday = search_result['hits']['hits'][0]['_source']['date']
        except IndexError:
            pass
        return lastday

    def genindex(self, yamlinfo):
        yamlinfo = self._date(yamlinfo)
        yamlinfo = self._tags(yamlinfo)
        yamlinfo = self._experience(yamlinfo)
        # yamlinfo = self._null(yamlinfo)
        return yamlinfo

    def _null(self, yamlinfo):
        output = dict()
        for each in yamlinfo:
            if yamlinfo[each]:
                output[each] = yamlinfo[each]
        return output

    def _experience(self, yamlinfo):
        if '_experience' in yamlinfo:
            if isinstance(yamlinfo['_experience'], list):
                yamlinfo.pop('_experience')
        return yamlinfo

    def _tags(self, yamlinfo):
        if 'tags' in yamlinfo:
            for tag in yamlinfo['tags']:
                yamlinfo['tags'][tag] = list(yamlinfo['tags'][tag])
        return yamlinfo

    def _date(self, yamlinfo):
        if 'date' in yamlinfo and yamlinfo['date']:
            ste_date = time.strftime('%Y%m%d', time.localtime(yamlinfo['date']))
            yamlinfo['date'] = ste_date
        return yamlinfo
