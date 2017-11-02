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
                    "strings": {
                        "match_mapping_type": "string",
                            "mapping": {
                                "type": "keyword"
                            }
                        }
                    }
                ]
            }
        }
    }

    def setup(self, esconn, indexname):
        self.es = esconn
        self.es.indices.create(index=indexname, body=self.index_config_body, ignore=400)

    def update(self, indexname, svcs):
        for svc in svcs:
            self.updatesvc(indexname, svc)

    def updatesvc(self, indexname, svc, numbers=5000):
        assert svc.name
        update_ids = set([item['_id'] for item in self.ES(indexname, {})])
        ACTIONS = list()
        times = 0
        count = 0
        for id in svc.ids-update_ids:
            info = svc.getyaml(id)
            geninfo = self.genindex(info)
            action = {
                "_op_type": "index",
                "_index": indexname,
                "_type": 'index',
                "_source": geninfo,
                '_id': id
                }
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

    def add(self, indexname, id, info):
        ACTIONS = list()
        geninfo = self.genindex(info)
        action = {
            "_op_type": "index",
            "_index": indexname,
            "_type": 'index',
            "_source": geninfo,
            '_id': id
            }
        ACTIONS.append(action)
        elasticsearch.helpers.bulk(self.es, ACTIONS,
                raise_on_error=False, raise_on_exception=False, stats_only=True)

    def upgrade(self, indexname, svcs, selected, ids=None):
        for svc in svcs:
            self.upgradesvc(indexname, svc, selected, ids=ids)

    def upgradesvc(self, indexname, svc, selected, ids=None, numbers=5000):
        assert svc.name
        if ids is None:
            ids = svc.ids
        else:
            ids = set(ids) & svc.ids
        times = 0
        count = 0
        ACTIONS = list()
        for id in ids:
            yamlinfo = self.genindex(svc.getyaml(id))
            action = {
                "_op_type": 'index',
                "_index": indexname,
                "_type": 'index',
                "_source": yamlinfo,
                '_id': id
                }
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

    def get(self, indexname, querydict, source=False, pagesize=10000, start=0, size=None):
        kwargs={'body': querydict}
        results = self.ES(indexname, kwargs, source=source,
                          pagesize=pagesize, start=start, size=None)
        return results

    def ES(self, indexname, kwargs, source=False, pagesize=10000, start=0, size=None):
        kwargs['doc_type'] = 'index'
        kwargs['sort'] = '_doc'
        kwargs['_source'] = 'false' if source is False else 'true'
        result = utils.esquery.scroll(self.es, indexname, kwargs,
                                      pagesize=pagesize, start=start, size=size)
        return result

    def filter(self, indexname, filterdict, ids=None, source=False,
               pagesize=10000, start=0, size=None):
        results = set()
        querydict = utils.esquery.request_gen(filterdict=filterdict, ids=ids)
        if querydict['query']['bool']['filter']:
            results = self.get(indexname, querydict, source=source,
                               pagesize=pagesize, start=start, size=size)
        return results

    def filter_ids(self, indexname, ids, filterdict, source=False,
                   pagesize=10000, start=0, size=None):
        result = ids
        if filterdict:
            filterset = self.filter(indexname, filterdict, ids=ids, source=source,
                                    pagesize=pagesize, start=start, size=size)
            result = set([item['_id'] for item in filterset])
        return result

    def lastday(self, indexname):
        lastday = '19800101'
        search_result = self.es.search(index=indexname, doc_type=self.doctype,
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
