import math
import time
import collections

import elasticsearch

import utils.builtin


class ElasticsearchIndexing(object):

    indexname = 'cloudshare.index'
    doctype = 'index'
    index_config_body = {
      "settings": {
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "ik_max_word",
                },
                "content":{
                    "type":"custom",
                    "tokenizer":"whitespace",
                }
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

    def updatecv(self, svc):
        assert svc.name
        update_ids = self.ESids({})
        cv_ids = svc.ids
        for id in cv_ids-update_ids:
            yamlinfo = self.genindex(svc.getyaml(id))
            try:
                self.es.index(index=self.indexname, doc_type='index',
                              id=id, body=yamlinfo)
            except Exception as e:
                print(e)
                print(yamlinfo)

    def upgrade(self):
        for svc in self.cvs:
            self.upgradecv(svc, selected)

    def upgradecv(self, sv):
        assert svc.name
        update_ids = self.ESids({})
        cv_ids = svc.ids
        for id in cv_ids-update_ids:
            yamlinfo = self.genindex(svc.getyaml(id))
            self.es.update(index=self.indexname, doc_type='index',
                           id=id, body=yamlinfo)

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
            else:
                if isinstance(value, list):
                    mustlist.append({'terms': {key.lower(): [v.lower() for v in value]}})
                else:
                    mustlist.append({'term': {key.lower(): value.lower()}})
        print querydict
        if mustlist:
            filterset = self.get(querydict)
            ids = filter(lambda x: x in filterset or x[0] in filterset, ids)
        return ids

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
