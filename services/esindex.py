import math
import time
import collections

import elasticsearch.helpers

import utils.builtin
import utils.esquery


class ElasticsearchIndexing(object):

    doctype = 'index'
    index_config_CV = {
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
    index_config_CO = {
        "template": doctype,
        "mappings": {
            "_default_": {
                "dynamic_templates": [
                    {
                        "name": {
                            "match":              "name",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_smart"
                            }
                    }},
                    {
                        "introduction": {
                            "match":              "introduction",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_max_word"
                            }
                    }},
                    {
                        "clientcontact": {
                            "match":              "clientcontact",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_max_word"
                            }
                    }},
                    {
                        "reminder": {
                            "match":              "reminder",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_max_word"
                            }
                    }},
                    {
                        "id": {
                            "match":              "id",
                            "mapping": {
                                "type":           "keyword"
                            }
                    }},
                    {
                        "modifytime": {
                            "match":              "modifytime",
                            "mapping": {
                                "type":           "keyword"
                            }
                    }}
                ]
            }
        }
    }
    index_config_JD = {
        "template": doctype,
        "mappings": {
            "_default_": {
                "dynamic_templates": [
                    {
                        "name": {
                            "match":              "name",
                            "match_mapping_type": "string",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_max_word"
                            }
                    }},
                    {
                        "description": {
                            "match":              "description",
                            "match_mapping_type": "string",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_max_word"
                            }
                    }},
                    {
                        "followup": {
                            "match":              "followup",
                            "match_mapping_type": "string",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_max_word"
                            }
                    }},
                    {
                        "commentary": {
                            "match":              "commentary",
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
    def setup(self, esconn, config):
        self.config = config
        self.es = esconn
        for each in config:
            if each.startswith('CV'):
                self.es.indices.create(index=config[each],
                                       body=self.index_config_CV, ignore=400)
            elif each.startswith('CO'):
                self.es.indices.create(index=config[each],
                                       body=self.index_config_CO, ignore=400)
            elif each.startswith('JD'):
                self.es.indices.create(index=config[each],
                                       body=self.index_config_JD, ignore=400)

    def update(self, index, doctype, svcs, numbers=5000):
        for svc in svcs:
            self.updatesvc(index, doctype, svc, numbers=numbers)

    def genaction(self, index, doctype, id, data, info, content=True):
        _source = data
        if _source is None or content is False:
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

    def updatesvc(self, index, doctype, svc, content=True, numbers=5000):
        assert svc.name
        total, searchs = self.ESsearch(index=index, doctype=doctype)
        update_ids = set([item['_id'] for item in searchs])
        ACTIONS = list()
        times = 0
        count = 0
        for id in svc.ids-update_ids:
            try:
                geninfo = self.genindex(svc.getyaml(id))
            except Exception:
                print id
                continue
            data = svc.getmd(id)
            action = self.genaction(index, doctype, id, data, geninfo, content=content)
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

    def add(self, index, doctype, id, data, info, content=True):
        ACTIONS = list()
        geninfo = self.genindex(info)
        action = self.genaction(index, doctype, id, data, geninfo, content=content)
        ACTIONS.append(action)
        elasticsearch.helpers.bulk(self.es, ACTIONS,
                raise_on_error=False, raise_on_exception=False, stats_only=True)

    def upgrade(self, index, doctype, svcs, ids=None):
        for svc in svcs:
            self.upgradesvc(index, doctype, svc, ids=ids)

    def upgradesvc(self, index, doctype, svc, ids=None, content=True, numbers=5000):
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
            action = self.genaction(index, doctype, id, data, geninfo, content=content)
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
        kwargs['_source'] = source
        result = utils.esquery.scroll(self.es, kwargs, index=index, doctype=doctype,
                                      start=start, size=size)
        return result

    def count(self, index=None, doctype=None, filterdict=None,
              ids=None, kwargs=None, slop=50):
        result = 0
        querydict = utils.esquery.request_gen(self.es, index=index, doctype=doctype,
                                              filterdict=filterdict, ids=ids, slop=slop)
        if kwargs is None:
            kwargs = dict()
        kwargs.update({'body': querydict})
        result = utils.esquery.count(self.es, kwargs, index=index, doctype=doctype)
        return result

    def search(self, index=None, doctype=None, filterdict=None, ids=None, source=False,
               start=0, size=None, kwargs=None, onlyid=False, slop=50):
        results = (0, list())
        querydict = utils.esquery.request_gen(self.es, index=index, doctype=doctype,
                                              filterdict=filterdict, ids=ids, slop=slop)
        results = self.ESsearch(index=index, doctype=doctype, querydict=querydict,
                                kwargs=kwargs, source=source, start=start, size=size)
        if onlyid:
            total, searchs = results
            results = [each['_id'] for each in searchs]
        return results

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
