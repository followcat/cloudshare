import time
import yaml
import os.path

import utils._yaml
import services.base
import core.outputstorage
import core.converterutils
import core.uniquesearcher


class CurriculumVitae(services.base.Service):

    path = 'CV'

    def __init__(self, interface, name=None):
        super(CurriculumVitae, self).__init__(interface, name)
        self.repo_path = self.interface.path + "/" + self.path
        self.info = ""
        self._nums = 0
        self.updatenums()

    def exists(self, filename):
        path_name = os.path.join(self.path, filename)
        result = self.interface.exists(path_name)
        return result

    def add(self, cvobj, committer=None, unique=True):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import services.curriculumvitae
            >>> import interface.gitinterface
            >>> repo_name = 'services/test_repo'
            >>> test_path = 'services/test_output'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(interface)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> f2 = open('core/test/cv_2.doc', 'r')
            >>> cv1 = services.curriculumvitae.CurriculumVitaeObject('cv_1.doc', f1, test_path)
            >>> cv2 = services.curriculumvitae.CurriculumVitaeObject('cv_2.doc', f2, test_path)
            >>> svc_cv.add(cv1)
            True
            >>> svc_cv.add(cv2)
            True
            >>> md_files = glob.glob(os.path.join(svc_cv.repo_path, '*.md'))
            >>> len(md_files)
            2
            >>> yaml_files = glob.glob(os.path.join(svc_cv.repo_path, '*.yaml'))
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
        if cvobj.result is False:
            return False
        unique_checker = core.uniquesearcher.UniqueSearcher(self.repo_path)
        if unique is True and unique_checker.unique(cvobj.filepro.yamlinfo) is False:
            self.info = "Exists File"
            return False
        cvobj.filepro.yamlinfo['committer'] = committer
        cvobj.filepro.yamlinfo['date'] = time.time()
        self.interface.add(os.path.join(self.path, cvobj.filepro.name.md),
                           cvobj.markdown(), committer=committer)
        self.interface.add(os.path.join(self.path, cvobj.filepro.name.yaml),
                           yaml.safe_dump(cvobj.yaml(), allow_unicode=True),
                           committer=committer)
        self._nums += 1
        return True

    def add_md(self, cvobj, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import services.curriculumvitae
            >>> import interface.gitinterface
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> test_path = "webapp/views/test_output"
            >>> repo_name = 'webapp/views/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(interface)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> cv1 = services.curriculumvitae.CurriculumVitaeObject(name, obj, test_path)
            >>> svc_cv.add_md(cv1)
            True
            >>> md_files = glob.glob(os.path.join(svc_cv.repo_path, '*.md'))
            >>> len(md_files)
            1
            >>> yaml_files = glob.glob(os.path.join(svc_cv.repo_path, '*.yaml'))
            >>> len(yaml_files)
            0
            >>> obj.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        if cvobj.result is False:
            return False
        self.interface.add(os.path.join(self.path, cvobj.filepro.name.md),
                           cvobj.markdown(), committer=committer)
        return True

    def modify(self, filename, stream, message=None, committer=None):
        path_filename = os.path.join(self.path, filename)
        self.interface.modify(path_filename, stream, message, committer)
        return True

    def yamls(self):
        yamls = self.interface.lsfiles(self.path, '*.yaml')
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
        results = self.interface.grep(keyword, self.path)
        return results

    def search_yaml(self, keyword):
        results = self.interface.grep_yaml(keyword, self.path)
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
        result = unicode()
        md = core.outputstorage.ConvertName(name).md
        path_name = os.path.join(self.path, md)
        markdown = self.interface.get(path_name)
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
            >>> PS = services.curriculumvitae.CurriculumVitae(P)
            >>> PS.getyaml('CV.md')
            Traceback (most recent call last):
            ...
            IOError
        """
        name = core.outputstorage.ConvertName(id).yaml
        path_name = os.path.join(self.path, name)
        yaml_str = self.interface.get(path_name)
        if yaml_str is None:
            raise IOError
        return yaml.load(yaml_str, Loader=utils._yaml.SafeLoader)

    @property
    def NUMS(self):
        return self._nums

    def updatenums(self):
        self._nums = len(list(self.yamls()))


class CurriculumVitaeObject(object):

    def __init__(self, filename, fileobject, path):
        """
            >>> import os
            >>> import shutil
            >>> import os.path
            >>> import services.curriculumvitae
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> obj = open(os.path.join(root, name))
            >>> test_path = "webapp/views/test_output"
            >>> os.makedirs(test_path)
            >>> up = services.curriculumvitae.CurriculumVitaeObject(name, obj, test_path)
            >>> up.result
            True
            >>> up.remove()
            >>> shutil.rmtree(test_path)
        """
        self.result = False
        self.tmp_path = path
        self.convertname = core.outputstorage.ConvertName(
            filename.encode('utf-8'))
        self.filepro = core.converterutils.FileProcesser(fileobject,
                                                         self.convertname,
                                                         self.tmp_path)
        self.result = self.filepro.result
        if self.result is False:
            self.information = 'Can not Convert'
        else:
            self.information = 'Sucess'

    def markdown(self):
        return self.filepro.markdown_stream

    def yaml(self):
        return self.filepro.yamlinfo

    def preview_markdown(self):
        output = core.converterutils.md_to_html(self.filepro.markdown_stream)
        return output

    def remove(self):
        """
            >>> import os
            >>> import shutil
            >>> import os.path
            >>> import services.curriculumvitae
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> obj = open(os.path.join(root, name))
            >>> test_path = "webapp/views/test_output"
            >>> os.makedirs(test_path)
            >>> up = services.curriculumvitae.CurriculumVitaeObject(name, obj, test_path)
            >>> fn = os.path.join(up.filepro.markdown_path, up.filepro.name.md)
            >>> os.path.exists(fn)
            True
            >>> up.remove()
            >>> os.path.exists(fn)
            False
            >>> shutil.rmtree(test_path)
        """
        self.filepro.deleteconvert()
