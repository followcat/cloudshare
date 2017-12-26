import time
import datetime

import core.exception
import core.outputstorage
import utils.pandocconverter
import services.operator.split
import services.operator.search
import services.base.kv_storage
import services.base.text_storage
import extractor.information_explorer


class CV(services.base.kv_storage.KeyValueStorage):
    """"""
    YAML_TEMPLATE = extractor.information_explorer.cv_template

    yaml_private_key = {
        "phone":                '[*****]',
        "email":                '[*****]',
        "name":                 '[*****]',
        "committer":            '[*****]',
        "origin":               '[*****]'
    }

class CurriculumVitae(services.operator.split.SplitData):
    """ Backward compatible definition of curriculum service.

    The service will mix:
        - plain text content from markdown file
        - kv content from *local* yaml file

    This is the only service to use PlainTextStorage. The handling
    of this case is hardcoded, so that CurriculumVitae behaviour is
    a bit different from its base class SplitData.
    """

    commitinfo = 'CurriculumVitae'

    def __init__(self, path, name=None, iotype=None):
        data_service = services.base.text_storage.PlainTextStorage(path, name, iotype)
        operator_service = CV(path, name, iotype)
        super(CurriculumVitae, self).__init__(data_service, operator_service)

    def private_keys(self):
        return self.operator_service.private_keys()

    def add_md(self, cvobj, committer=None, do_commit=True):
        return self.add(cvobj, committer, unique=False, kv_file=False, text_file=True, do_commit=do_commit)

    def getuniqueid(self, id):
        info = self.getyaml(id)
        try:
            uniqueid = info['unique_id']
        except KeyError:
            uniqueid = info['id']
        return uniqueid

    def gethtml(self, name):
        htmlname = core.outputstorage.ConvertName(name).html
        try:
            result = self.interface.getraw(htmlname)
        except IOError:
            md = self.getmd(name)
            if md is not None:
                result = utils.pandocconverter.md_to_html(md)
        return result

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        return self.gethtml(veren)

    def timerange(self, start_y, start_m, start_d, end_y, end_m, end_d):
        start = time.mktime(datetime.datetime(start_y, start_m, start_d).timetuple())
        end = time.mktime(datetime.datetime(end_y, end_m, end_d).timetuple())
        for id in self.ids:
            info = self.getyaml(id)
            date = info['date']
            if start < date and date < end:
                yield id

    def add(self, bsobj, committer=None, unique=True,
            kv_file=True, text_file=True, contacts=True, do_commit=True):
        if contacts and not bsobj.metadata['email'] and not bsobj.metadata['phone']:
            raise core.exception.NotExistsContactException
        return super(CurriculumVitae, self).add(bsobj, committer, unique,
                                kv_file, text_file, do_commit=do_commit)

    def modify(self, *args, **kwargs):
        """ Plain text do not support modify() """
        return self.operator_service.modify(*args, **kwargs)

    def remove(self, *args, **kwargs):
        """ Do not remove a CurriculumVitae """
        return True

    def addcv(self, bsobj, rawdata=None, do_commit=True):
        result = self.add(bsobj, contacts=False)
        if result is True:
            cn_id = core.outputstorage.ConvertName(bsobj.name)
            if rawdata is not None:
                self.interface.add(cn_id.html, rawdata, do_commit=do_commit)
        return result

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
