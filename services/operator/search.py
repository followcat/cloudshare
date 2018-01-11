import time

import elasticsearch.helpers

import utils.esquery
import services.operator.facade


class SearchIndex(services.operator.facade.Facade):

    doctype = 'index'
    index_config = {
        "template": doctype,
        "mappings": {
            "_default_": {
                "dynamic_templates": [
                ]
            }
        }
    }

    def add(self, bsobj, *args, **kwargs):
        try:
            doctype = kwargs.pop('doctype')
        except KeyError:
            return False
        result = self.data_service.add(bsobj, *args, **kwargs)
        if result:
            id = bsobj.ID
            try:
                md = self.data_service.getmd(id)
            except AttributeError:
                md = None
            yaml = self.data_service.getyaml(id)
            self.indexadd(index=self.config, doctype=doctype, id=id, data=md, info=yaml)
        return result

    def modify(self, bsobj, *args, **kwargs):
        try:
            doctype = kwargs.pop('doctype')
        except KeyError:
            return False
        result = self.data_service.modify(bsobj, *args, **kwargs)
        if result:
            id = bsobj.ID
            try:
                md = self.data_service.getmd(id)
            except AttributeError:
                md = None
            yaml = self.data_service.getyaml(id)
            self.indexadd(index=self.config, doctype=doctype, id=id, data=md, info=yaml)
        return result

    def kick(self, bsobj, *args, **kwargs):
        try:
            doctype = kwargs.pop('doctype')
        except KeyError:
            return False
        result = self.data_service.kick(bsobj, *args, **kwargs)
        if result:
            id = bsobj.ID
            try:
                md = self.data_service.getmd(id)
            except AttributeError:
                md = None
            yaml = self.data_service.getyaml(id)
            self.indexadd(index=self.config, doctype=doctype, id=id, data=md, info=yaml)
        return result

    def setup(self, esconn, config):
        self.config = config
        self.es = esconn
        self.es.indices.create(index=config, body=self.index_config, ignore=400)

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

    def updatesvc(self, index, doctype, content=True, numbers=5000):
        total, searchs = self.ESsearch(index=index, doctype=doctype, size=10000, scroll='1m')
        update_ids = set([item['_id'] for item in searchs])
        ACTIONS = list()
        times = 0
        count = 0
        for id in self.data_service.ids-update_ids:
            try:
                geninfo = self.genindex(self.data_service.getyaml(id))
            except Exception:
                print id
                continue
            data = self.data_service.getmd(id)
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

    update = updatesvc

    def indexadd(self, index, doctype, id, data, info, content=True):
        ACTIONS = list()
        geninfo = self.genindex(info)
        action = self.genaction(index, doctype, id, data, geninfo, content=content)
        ACTIONS.append(action)
        elasticsearch.helpers.bulk(self.es, ACTIONS,
                raise_on_error=False, raise_on_exception=False, stats_only=True)

    def upgradesvc(self, index, doctype, ids=None, content=True, numbers=5000):
        if ids is None:
            ids = self.data_service.ids
        else:
            ids = set(ids) & self.data_service.ids
        times = 0
        count = 0
        ACTIONS = list()
        for id in ids:
            geninfo = self.genindex(self.data_service.getyaml(id))
            data = self.data_service.getmd(id)
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

    upgrade = upgradesvc

    def ESsearch(self, index=None, doctype=None, querydict=None, kwargs=None,
                 source=False, start=0, size=None, scroll=None):
        if kwargs is None:
            kwargs = dict()
        kwargs.update({'body': querydict})
        kwargs['_source'] = source
        result = utils.esquery.scroll(self.es, kwargs, index=index, doctype=doctype,
                                      start=start, size=size, scroll=scroll)
        return result

    def count(self, index=None, doctype=None, filterdict=None,
              ids=None, kwargs=None, slop=0):
        result = 0
        querydict = utils.esquery.request_gen(self.es, index=index, doctype=doctype,
                                              filterdict=filterdict, ids=ids, slop=slop)
        if kwargs is None:
            kwargs = dict()
        kwargs.update({'body': querydict})
        result = utils.esquery.count(self.es, kwargs, index=index, doctype=doctype)
        return result

    def search(self, index=None, doctype=None, filterdict=None, ids=None, source=False,
               start=0, size=None, kwargs=None, onlyid=False, slop=0, scroll=None):
        results = (0, list())
        querydict = utils.esquery.request_gen(self.es, index=index, doctype=doctype,
                                              filterdict=filterdict, ids=ids, slop=slop)
        results = self.ESsearch(index=index, doctype=doctype, querydict=querydict,
                                kwargs=kwargs, source=source, start=start,
                                size=size, scroll=scroll)
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
