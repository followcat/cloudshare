import time
import yaml
import os.path

import utils._yaml
import services.base
import core.outputstorage
import core.converterutils
import core.uniquesearcher


class CurriculumVitae(services.base.Service):

    YAML_DIR = 'CV'

    def __init__(self, path, name=None):
        self.path = os.path.join(path, self.YAML_DIR)
        super(CurriculumVitae, self).__init__(self.path, name)
        self.unique_checker = None
        self.info = ""
        self._nums = 0

    def exists(self, id):
        """
            >>> import interface.basefs
            >>> import services.curriculumvitae
            >>> DIR = 'repo'
            >>> DB = interface.basefs.BaseFSInterface(DIR)
            >>> SVC_CV = services.curriculumvitae.CurriculumVitae(DB.path, 'repo')
            >>> assert SVC_CV.exists('blr6dter.yaml')

            >>> import interface.gitinterface
            >>> DB = interface.gitinterface.GitInterface(DIR)
            >>> SVC_CV = services.curriculumvitae.CurriculumVitae(DB.path, 'repo')
            >>> assert SVC_CV.exists('blr6dter.yaml')
        """
        yamlname = core.outputstorage.ConvertName(id).yaml
        result = self.interface.exists(yamlname)
        return result

    def add(self, cvobj, committer=None, unique=True, yamlfile=True):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import core.basedata
            >>> import core.converterutils
            >>> import services.curriculumvitae
            >>> import interface.gitinterface
            >>> repo_name = 'services/test_repo'
            >>> test_path = 'services/test_output'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(interface.path)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> f2 = open('core/test/cv_2.doc', 'r')
            >>> fp1 = core.converterutils.FileProcesser(f1, 'cv_1.doc', test_path)
            >>> fp2 = core.converterutils.FileProcesser(f2, 'cv_2.doc', test_path)
            >>> cv1 = core.basedata.DataObject(fp1.name, fp1.markdown_stream, fp1.yamlinfo)
            >>> cv2 = core.basedata.DataObject(fp2.name, fp2.markdown_stream, fp2.yamlinfo)
            >>> svc_cv.add(cv1)
            True
            >>> svc_cv.add(cv2)
            True
            >>> md_files = glob.glob(os.path.join(svc_cv.path, '*.md'))
            >>> len(md_files)
            2
            >>> yaml_files = glob.glob(os.path.join(svc_cv.path, '*.yaml'))
            >>> len(yaml_files)
            2
            >>> svc_cv.add(cv1)
            False
            >>> svc_cv.info
            'Exists File'
            >>> f1.close()
            >>> f2.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        if self.unique_checker is None:
            self.unique_checker = core.uniquesearcher.UniqueSearcher(self.path)
        self.unique_checker.update()
        if unique is True and self.unique_checker.unique(cvobj.metadata) is False:
            self.info = "Exists File"
            return False
        name = core.outputstorage.ConvertName(cvobj.name)
        message = "Add CV: %s data." % name
        self.interface.add(name.md, cvobj.data, message=message, committer=committer)
        if yamlfile is True:
            cvobj.metadata['committer'] = committer
            cvobj.metadata['date'] = time.time()
            message = "Add company: %s metadata." % name
            self.interface.add(name.yaml, yaml.safe_dump(cvobj.metadata, allow_unicode=True),
                               message=message, committer=committer)
        self._nums += 1
        return True

    def add_md(self, cvobj, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import core.basedata
            >>> import services.curriculumvitae
            >>> import interface.gitinterface
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> test_path = "webapp/views/test_output"
            >>> repo_name = 'webapp/views/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(interface.path)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> fp1 = core.converterutils.FileProcesser(obj, name, test_path)
            >>> cv1 = core.basedata.DataObject(fp1.name, fp1.markdown_stream, fp1.yamlinfo)
            >>> svc_cv.add_md(cv1)
            True
            >>> md_files = glob.glob(os.path.join(svc_cv.path, '*.md'))
            >>> len(md_files)
            1
            >>> yaml_files = glob.glob(os.path.join(svc_cv.path, '*.yaml'))
            >>> len(yaml_files)
            0
            >>> obj.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        name = core.outputstorage.ConvertName(cvobj.name)
        self.interface.add(name.md, cvobj.data, committer=committer)
        return True

    def modify(self, filename, stream, message=None, committer=None):
        self.interface.modify(filename, stream, message, committer)
        return True

    def yamls(self):
        """
            >>> import interface.basefs
            >>> import services.curriculumvitae
            >>> DIR = 'repo'
            >>> DB = interface.basefs.BaseFSInterface(DIR)
            >>> SVC_CV = services.curriculumvitae.CurriculumVitae(DB.path, DIR)
            >>> assert SVC_CV.interface.lsfiles('.', 'blr6dter.yaml')

            >>> import interface.gitinterface
            >>> DB = interface.gitinterface.GitInterface(DIR)
            >>> SVC_CV = services.curriculumvitae.CurriculumVitae(DB.path, DIR)
            >>> assert SVC_CV.interface.lsfiles('.', 'blr6dter.yaml')
        """
        yamls = self.interface.lsfiles('.', '*.yaml')
        for each in yamls:
            yield os.path.split(each)[-1]

    def names(self):
        for each in self.yamls():
            yield core.outputstorage.ConvertName(each).md

    def datas(self):
        for name in self.names():
            text = self.getmd(name)
            yield name, text

    def search(self, keyword):
        results = set()
        allfile = self.interface.grep(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def search_yaml(self, keyword):
        results = set()
        allfile = self.interface.grep_yaml(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def gethtml(self, name):
        htmlname = core.outputstorage.ConvertName(name).html
        result = self.interface.getraw(htmlname)
        if result is None:
            md = self.getmd(name)
            if md is not None:
                result = core.converterutils.md_to_html(md)
        return result

    def getmd(self, name):
        """
            >>> import interface.basefs
            >>> import services.curriculumvitae
            >>> DIR = 'repo'
            >>> DB = interface.basefs.BaseFSInterface(DIR)
            >>> SVC_CV = services.curriculumvitae.CurriculumVitae(DB.path, 'repo')
            >>> assert SVC_CV.getmd('blr6dter.yaml')

            >>> import interface.gitinterface
            >>> DB = interface.gitinterface.GitInterface(DIR)
            >>> SVC_CV = services.curriculumvitae.CurriculumVitae(DB.path, 'repo')
            >>> assert SVC_CV.getmd('blr6dter.yaml')
        """
        result = unicode()
        md = core.outputstorage.ConvertName(name).md
        markdown = self.interface.get(md)
        if markdown is None:
            result = None
        elif isinstance(markdown, unicode):
            result = markdown
        else:
            result = unicode(str(markdown), 'utf-8')
        return result


    def getyaml(self, id):
        """
        MultiCV expects an IOError exception if file not found.
            >>> import interface.predator
            >>> import services.curriculumvitae
            >>> P = interface.predator.PredatorInterface('/tmp')
            >>> PS = services.curriculumvitae.CurriculumVitae(P.path)
            >>> PS.getyaml('CV.md')
            Traceback (most recent call last):
            ...
            IOError
        """
        name = core.outputstorage.ConvertName(id).yaml
        yaml_str = self.interface.get(name)
        if yaml_str is None:
            raise IOError
        return yaml.load(yaml_str, Loader=utils._yaml.SafeLoader)

    @property
    def NUMS(self):
        if not self._nums:
            self._nums = len(list(self.yamls()))
        return self._nums

    @property
    def cvids(self):
        return [os.path.splitext(f)[0]
                for f in self.interface.lsfiles('.', '*.yaml')]

    def addcv(self, id, data, yamldata, rawdata=None):
        cn_id = core.outputstorage.ConvertName(id)
        self.interface.add(cn_id.md, data)
        self.interface.add(cn_id.yaml, yamldata)
        if rawdata is not None:
            self.interface.add(cn_id.html, rawdata)
        return True
