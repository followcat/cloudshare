import math
import time
import collections

import elasticsearch.helpers

import utils.builtin
import utils.esquery


class ElasticsearchIndexing(object):

    indexname = 'cloudshare.index'
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

    def __init__(self, cvsvcs):
        self.cvs = cvsvcs

    def setup(self, esconn):
        self.es = esconn
        self.es.indices.create(index=self.indexname, body=self.index_config_body, ignore=400)

    def update(self):
        for svc in self.cvs:
            self.updatecv(svc)

    def updatecv(self, svc, numbers=5000):
        assert svc.name
        update_ids = self.ESids({})
        cv_ids = svc.ids
        ACTIONS = list()
        times = 0
        count = 0
        for id in cv_ids-update_ids:
            info = svc.getyaml(id)
            geninfo = self.genindex(info)
            action = {
                "_op_type": "index",
                "_index": self.indexname,
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

    def add(self, id, info):
        ACTIONS = list()
        geninfo = self.genindex(info)
        action = {
            "_op_type": "index",
            "_index": self.indexname,
            "_type": 'index',
            "_source": geninfo,
            '_id': id
            }
        ACTIONS.append(action)
        elasticsearch.helpers.bulk(self.es, ACTIONS,
                raise_on_error=False, raise_on_exception=False, stats_only=True)

    def upgrade(self, selected, ids=None):
        for svc in self.cvs:
            self.upgradecv(svc, selected, ids=ids)

    def upgradecv(self, svc, selected, ids=None, numbers=5000):
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
                "_index": self.indexname,
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

    def get(self, querydict):
        kwargs={'body': querydict}
        results = self.ESids(kwargs)
        return results

    def ESids(self, kwargs, size=10000):
        kwargs['doc_type'] = 'index'
        kwargs['sort'] = '_doc'
        kwargs['_source'] = 'false'
        result = utils.esquery.scroll_ids(self.es, self.indexname, kwargs)
        ids = set([item['_id'] for item in result])
        return ids

    def filter(self, filterdict, ids=None):
        results = set()
        querydict = utils.esquery.request_gen(filterdict=filterdict, ids=ids)
        if querydict['query']['bool']['filter']:
            results = self.get(querydict)
        return results

    def filter_ids(self, source, filterdict, ids, uses=None):
        result = source
        if filterdict:
            if not isinstance(ids, set):
                ids = set(ids)
            filterset = self.filter(filterdict, ids=ids)
            result = filter(lambda x: x in filterset or x[0] in filterset, source)
        return result

    def lastday(self):
        lastday = '19800101'
        search_result = self.es.search(index=self.indexname, doc_type=self.doctype,
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
