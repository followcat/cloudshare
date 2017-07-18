import math
import time
import collections

import elasticsearch
import elasticsearch.helpers

import utils.builtin


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

    def setup(self):
        self.es = elasticsearch.Elasticsearch()
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
            yamlinfo = self.genindex(svc.getyaml(id))
            action = {
                "_op_type": "index",
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
                print("Add numbers %d to index."%(times*numbers))
        else:
            elasticsearch.helpers.bulk(self.es, ACTIONS,
                    raise_on_error=False, raise_on_exception=False, stats_only=True)
            print("Add numbers %d to index. And finished."%(times*numbers+len(ACTIONS)))

    def upgrade(self):
        for svc in self.cvs:
            self.upgradecv(svc)

    def upgradecv(self, sv, numbers=5000):
        assert svc.name
        ACTIONS = list()
        times = 0
        count = 0
        for id in svc.ids:
            yamlinfo = self.genindex(svc.getyaml(id))
            action = {
                "_op_type": "update",
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
        ids = set()
        page = self.es.search(
                doc_type = 'index',
                scroll = '1m',
                sort = '_doc',
                size = size,
                _source='false',
                index=self.indexname,
                **kwargs)
        ids.symmetric_difference_update(set([item['_id'] for item in page['hits']['hits']]))
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']

        while (scroll_size > 0):
            page = self.es.scroll(scroll_id = sid, scroll = '1m')
            sid = page['_scroll_id']
            scroll_size = len(page['hits']['hits'])
            ids.symmetric_difference_update(set([item['_id'] for item in page['hits']['hits']]))
        return ids

    def filter_ids(self, ids, filterdict, uses=None):
        if 'date' in filterdict:
            for index in range(len(filterdict['date'])):
                filterdict['date'][index] = filterdict['date'][index].replace('-', '')
        querydict = {'query': {'bool': {'must': []}}}
        mustlist = querydict['query']['bool']['must']
        for key, value in filterdict.items():
            if not value:
                continue
            if key == 'date':
                if len(value[0]) > 0:
                    daterange = {'range': {'date': {'gte': value[0], 'lte': value[1]}}}
                    mustlist.append(daterange)
            elif key == 'expectation_places':
                mustlist.append({'terms': {'expectation.places': value}})
            elif key == 'current_places':
                mustlist.append({'terms': {'current.places': value}})
            else:
                if isinstance(value, list):
                    mustlist.append({'terms': {key.lower(): value}})
                else:
                    mustlist.append({'term': {key.lower(): value}})
        if mustlist:
            filterset = self.get(querydict)
            ids = filter(lambda x: x in filterset or x[0] in filterset, ids)
        return ids

    def lastday(self):
        lastday = '19800101'
        date = self.es.search(index=self.indexname, doc_type=self.doctype,
                              sort='_score,date:desc', size = 1)
        try:
            lastday = x['hits']['hits'][0]['_source']['date']
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
