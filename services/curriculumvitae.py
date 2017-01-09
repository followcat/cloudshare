import yaml
import time
import os.path
import datetime

import core.exception
import core.docprocessor
import core.outputstorage
import services.base.storage


class CurriculumVitae(services.base.storage.BaseStorage):

    commitinfo = 'CurriculumVitae'

    def exists(self, id):
        mdname = core.outputstorage.ConvertName(id).md
        return os.path.exists(os.path.join(self.path, mdname))

    def add_md(self, cvobj, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import core.basedata
            >>> import services.curriculumvitae
            >>> import extractor.information_explorer
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> test_path = "services/test_output"
            >>> DIR = 'services/test_repo'
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(DIR)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> fp1 = core.docprocessor.Processor(obj, name, test_path)
            >>> yamlinfo = extractor.information_explorer.catch_cvinfo(
            ...     stream=fp1.markdown_stream.decode('utf8'), filename=fp1.base.base)
            >>> cv1 = core.basedata.DataObject(data=fp1.markdown_stream, metadata=yamlinfo)
            >>> svc_cv.add_md(cv1)
            True
            >>> md_files = glob.glob(os.path.join(svc_cv.path, '*.md'))
            >>> len(md_files)
            1
            >>> yaml_files = glob.glob(os.path.join(svc_cv.path, '*.yaml'))
            >>> len(yaml_files)
            0
            >>> obj.close()
            >>> shutil.rmtree(DIR)
            >>> shutil.rmtree(test_path)
        """
        name = core.outputstorage.ConvertName(cvobj.metadata['id'])
        self.interface.add(name.md, cvobj.data, committer=committer)
        return True

    def gethtml(self, name):
        htmlname = core.outputstorage.ConvertName(name).html
        try:
            result = self.interface.getraw(htmlname)
        except IOError:
            md = self.getmd(name)
            if md is not None:
                result = core.docprocessor.md_to_html(md)
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
            yamlfile=True, mdfile=True, contacts=True):
        if contacts and not bsobj.metadata['email'] and not bsobj.metadata['phone']:
            raise core.exception.NotExistsContactException
        return super(CurriculumVitae, self).add(bsobj, committer, unique,
                                                yamlfile, mdfile)

    def addcv(self, bsobj, rawdata=None):
        result = self.add(bsobj, contacts=False)
        if result is True:
            cn_id = core.outputstorage.ConvertName(bsobj.name)
            if rawdata is not None:
                self.interface.add(cn_id.html, rawdata)
        return result
