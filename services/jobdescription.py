import glob
import os.path

import yaml

import utils.builtin
import core.outputstorage
import services.operator.search
import services.base.kv_storage


class JobDescription(services.base.kv_storage.KeyValueStorage):

    commitinfo = 'JobDescription'

    YAML_DIR = '.'
    YAML_TEMPLATE = (
        ("name",            unicode),
        ("id",              str),
        ("company",         unicode),
        ("description",     unicode),
        ("committer",       str),
        ("commentary",      unicode),
        ("followup",        unicode),
        ("status",          str),
    )

    def __init__(self, path, name=None, iotype=None):
        """
            >>> import shutil
            >>> import services.jobdescription

            >>> path = 'services/test_repo'

            >>> svc_jd = services.jobdescription.JobDescription(path, 'testjd')
            >>> svc_jd.add('CompanyA', 'JD-A', 'JD-A description', 'Dever')
            True
            >>> results = list(svc_jd.interface.grep('JD-A'))
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description']
            'JD-A description'
            >>> svc_jd.modify(data['id'], 'JD-B description', 'Closed', '', '', 'Dever')
            True
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description']
            'JD-B description'
            >>> lists = list(svc_jd.datas())
            >>> lists[0][1]['company'], lists[0][1]['description']
            ('CompanyA', 'JD-B description')
            >>> svc_jd.add('CompanyC', 'JD-C', 'JD-C description', 'Dever',
            ...     commentary='this is JD-C commentary', followup='JD-C followup')
            True
            >>> results = list(svc_jd..interface.grep('JD-C'))
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description'], data['commentary']
            ('JD-C description', 'this is JD-C commentary')
            >>> svc_jd.modify(data['id'], 'JD-C description', 'Opening',
            ...     'this is UPDATED JD-C commentary', 'UPDATED JD-C followup', 'Dever')
            True
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description'], data['commentary'], data['followup']
            ('JD-C description', 'this is UPDATED JD-C commentary', 'UPDATED JD-C followup')
            >>> shutil.rmtree(path)
        """
        super(JobDescription, self).__init__(path, name=name, iotype=iotype)

    def _metadata(self, info):
        origin = self.generate_info_template()
        for key, datatype in self.YAML_TEMPLATE:
            if key in info and isinstance(info[key], datatype):
                origin[key] = info[key]
        origin['id'] = utils.builtin.genuuid()
        origin['status'] = 'Opening' if not origin['status'] else origin['status']
        return origin

    def baseobj(self, info):
        metadata = self._metadata(info)
        bsobj = core.basedata.DataObject(metadata=metadata, data=None)
        return bsobj

    def modify(self, id, description, status, commentary, followup, committer):
        data = self.getyaml(id)
        if data['description'] != description and data['committer'] != committer:
            return False
        data['status'] = status
        data['description'] = description
        data['commentary'] = commentary
        data['followup'] = followup
        dump_data = yaml.safe_dump(data, allow_unicode=True)
        name = core.outputstorage.ConvertName(id)
        super(JobDescription, self).modify(name.yaml, dump_data,
                                           message="Modify job description: " + name,
                                           committer=committer)
        return True

    def datas(self):
        for id in self.ids:
            result = self.getyaml(id)
            yield id, result


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
                        "modifytime": {
                            "match":              "modifytime",
                            "mapping": {
                                "type":           "keyword"
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
