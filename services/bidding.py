import core.basedata
import utils.companyexcel
import services.base.kv_storage
import services.operator.search
import extractor.information_explorer


class Bidding(services.base.kv_storage.KeyValueStorage):
    """
        >>> import shutil
        >>> import services.company
        >>> import core.basedata
        >>> import extractor.information_explorer
        >>> path = 'services/test_repo'
        >>> svc_co = services.bidding.Bidding(path)
        >>> name, committer, introduction = 'CompanyA', 'tester', 'This is Co.A'
        >>> metadata = extractor.information_explorer.catch_biddinginfo({'introduction': introduction,
        ...                                                         'name': name})
        >>> coobj = core.basedata.DataObject(metadata, data=introduction)
        >>> svc_co.add(coobj, 'Dever')
        True
        >>> co = svc_co.getyaml(metadata['id'])
        >>> co['name']
        'CompanyA'
        >>> co['introduction']
        'This is Co.A'
        >>> svc_co.add(coobj, 'Dever')
        False
        >>> list(svc_co.ids)
        ['4de25a98bc371bf87220e500215317f4b2c24933']
        >>> svc_co.getyaml('CompanyB') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        IOError...
        >>> shutil.rmtree(path)
    """
    YAML_TEMPLATE = extractor.information_explorer.bidding_template

    commitinfo = 'Bidding'

    def compare_excel(self, stream, committer):
        output = list()
        return output


class SearchIndex(services.operator.search.SearchIndex):
    """"""
    doctype = 'index'
    index_config = {
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
                        "conumber": {
                            "match":              "conumber",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_smart"
                            }
                    }},
                    {
                        "content": {
                            "path_match":         "*.content",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_smart"
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

    def indexadd(self, *args, **kwargs):
        kwargs['index'] = self.config
        return super(SearchIndex, self).indexadd(*args, **kwargs)

    def search(self, *args, **kwargs):
        kwargs['index'] = self.config
        return super(SearchIndex, self).search(*args, **kwargs)
