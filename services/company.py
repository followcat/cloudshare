import core.basedata
import utils.companyexcel
import services.base.kv_storage
import services.operator.search
import extractor.information_explorer


class Company(services.base.kv_storage.KeyValueStorage):
    YAML_DIR = '.'
    YAML_TEMPLATE = extractor.information_explorer.co_template

    commitinfo = 'Company'

    def remove(self, *args, **kwargs):
        """ Do not remove a Company """
        return True


class SearchIndex(services.operator.search.SearchIndex):
    """"""
    doctype = 'index'
    index_config = {
        "template": doctype,
        "mappings": {
            "_default_": {
                "dynamic_templates": [
                    {
                        "id": {
                            "match":              "id",
                            "mapping": {
                                "type":           "keyword"
                            }
                    }},
                    {
                        "name": {
                            "match":              "name",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_smart"
                            }
                    }},
                    {
                        "business": {
                            "match":              "business",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "keyword"
                            }
                    }},
                    {
                        "description": {
                            "match":              "description",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_smart"
                            }
                    }},
                    {
                        "website": {
                            "path_match":         "website",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_smart"
                            }
                    }},
                    {
                        "project.name": {
                            "match":              "project.name",
                            "mapping": {
                                "type":           "text",
                                "analyzer":       "ik_smart",
                                "fielddata":       True,
                            }
                    }},
                    {
                        "type": {
                            "match":              "type",
                            "mapping": {
                                "type":           "keyword"
                            }
                    }},
                    {
                        "total_employees": {
                            "match":              "total_employees",
                            "mapping": {
                                "type":           "keyword"
                            }
                    }},
                    {
                        "place": {
                            "match":              "place",
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
