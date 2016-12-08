import time
import yaml
import os.path

import utils._yaml
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

    def modify(self, filename, stream, message=None, committer=None):
        self.interface.modify(filename, stream, message, committer)
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

    @utils.issue.fix_issue('issues/update_name.rst')
    def updateinfo(self, id, key, value, committer):
        data = None
        projectinfo = self.getinfo(id)
        baseinfo = self.getyaml(id)
        if projectinfo is not None and (key in projectinfo or key in baseinfo):
            data = { key: value }
            if key == 'tag':
                data = self.addtag(id, value, committer)
            elif key == 'tracking':
                data = self.addtracking(id, value, committer)
            elif key == 'comment':
                data = self.addcomment(id, value, committer)
            else:
                projectinfo[key] = value
                self.saveinfo(id, projectinfo,
                              'Update %s key %s.' % (id, key), committer)
        return data

    def _infoframe(self, value, username):
        data = {'author': username,
                'content': value,
                'date': time.strftime('%Y-%m-%d %H:%M:%S')}
        return data

    def addtag(self, id, tag, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(tag, committer)
        info['tag'].insert(0, data)
        self.saveinfo(id, info, 'Add %s tag.'%id, committer)
        return data

    def addcomment(self, id, comment, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(comment, committer)
        info['comment'].insert(0, data)
        self.saveinfo(id, info, 'Add %s comment.'%id, committer)
        return data

    def addtracking(self, id, tracking, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(tracking, committer)
        info['tracking'].insert(0, data)
        self.saveinfo(id, info, 'Add %s tracking.'%id, committer)
        return data

    def getinfo(self, id):
        return self.getyaml(id)

    def saveinfo(self, id, info, message, committer):
        name = core.outputstorage.ConvertName(id).yaml
        dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                             allow_unicode=True, default_flow_style=False)
        self.interface.modify(name, dumpinfo, message=message, committer=committer)

    def addcv(self, bsobj, rawdata=None):
        self.add(bsobj)
        cn_id = core.outputstorage.ConvertName(bsobj.name)
        if rawdata is not None:
            self.interface.add(cn_id.html, rawdata)
        return True
