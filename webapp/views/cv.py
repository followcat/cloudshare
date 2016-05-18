import time
import shutil
import codecs
import os.path

import utils.builtin
import core.exception
import core.outputstorage
import core.converterutils
import core.uniquesearcher


class RepoCurriculumVitae(object):

    path = 'CV'

    def __init__(self, repo):
        self.repo = repo
        self.repo_path = self.repo.repo.path + "/" + self.path
        self.info = ""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    def add(self, cvobj, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> import interface.gitinterface
            >>> repo_name = 'webapp/views/test_repo'
            >>> test_path = "webapp/views/test_output"
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> repocv = webapp.views.cv.RepoCurriculumVitae(interface)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> f2 = open('core/test/cv_2.doc', 'r')
            >>> cv1 = webapp.views.cv.CurriculumVitaeObject('cv_1.doc', f1, test_path)
            >>> cv2 = webapp.views.cv.CurriculumVitaeObject('cv_2.doc', f2, test_path)
            >>> repocv.add(cv1)
            True
            >>> repocv.add(cv2)
            True
            >>> md_files = glob.glob(os.path.join(repocv.repo_path, '*.md'))
            >>> len(md_files)
            2
            >>> yaml_files = glob.glob(os.path.join(repocv.repo_path, '*.yaml'))
            >>> len(yaml_files)
            2
            >>> repocv.add(cv1)
            False
            >>> repocv.info
            'Exists File'
            >>> f1.close()
            >>> f2.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        if cvobj.result is False:
            return False
        unique_checker = core.uniquesearcher.UniqueSearcher(self.repo_path)
        if unique_checker.unique(cvobj.filepro.yamlinfo) is False:
            self.info = "Exists File"
            return False
        shutil.copy(os.path.join(cvobj.filepro.markdown_path, cvobj.filepro.name.md),
                    os.path.join(self.repo_path, cvobj.filepro.name.md))
        cvobj.filepro.yamlinfo['committer'] = committer
        cvobj.filepro.yamlinfo['date'] = time.time()
        utils.builtin.save_yaml(cvobj.filepro.yamlinfo,
                                self.repo_path, cvobj.filepro.name.yaml)
        self.repo.add_files([
                       os.path.join(self.repo_path, cvobj.filepro.name.md),
                       os.path.join(self.repo_path, cvobj.filepro.name.yaml)],
                       committer=committer)
        return True

    def add_md(self, cvobj, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> import interface.gitinterface
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> test_path = "webapp/views/test_output"
            >>> repo_name = 'webapp/views/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> repocv = webapp.views.cv.RepoCurriculumVitae(interface)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> cv1 = webapp.views.cv.CurriculumVitaeObject(name, obj, test_path)
            >>> repocv.add_md(cv1)
            True
            >>> md_files = glob.glob(os.path.join(repocv.repo_path, '*.md'))
            >>> len(md_files)
            1
            >>> yaml_files = glob.glob(os.path.join(repocv.repo_path, '*.yaml'))
            >>> len(yaml_files)
            0
            >>> obj.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        if cvobj.result is False:
            return False
        shutil.copy(os.path.join(cvobj.filepro.markdown_path, cvobj.filepro.name.md),
                    os.path.join(self.repo_path, cvobj.filepro.name.md))
        self.repo.add_files([os.path.join(self.repo_path, cvobj.filepro.name.md)],
                       committer=committer)
        return True

    def yamls(self):
        yamls = self.repo.lsfiles(self.path, '*.yaml')
        results = [os.path.split(each)[-1] for each in yamls]
        return results

    def datas(self):
        for yaml in self.yamls():
            name = core.outputstorage.ConvertName(yaml)
            with open(os.path.join(self.repo_path, name.md)) as fp:
                text = fp.read()
            yield name, text

    def search(self, keyword):
        results = self.repo.grep(keyword, self.path)
        return results

    def search_yaml(self, keyword):
        results = self.repo.grep_yaml(keyword, self.path)
        return results


class CurriculumVitaeObject(object):

    def __init__(self, filename, fileobject, path):
        """
            >>> import os
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> obj = open(os.path.join(root, name))
            >>> test_path = "webapp/views/test_output"
            >>> os.makedirs(test_path)
            >>> up = webapp.views.cv.CurriculumVitaeObject(name, obj, test_path)
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

    def preview_markdown(self):
        output = core.converterutils.md_to_html(self.filepro.markdown_stream)
        return output

    def remove(self):
        """
            >>> import os
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> obj = open(os.path.join(root, name))
            >>> test_path = "webapp/views/test_output"
            >>> os.makedirs(test_path)
            >>> up = webapp.views.cv.CurriculumVitaeObject(name, obj, test_path)
            >>> fn = os.path.join(up.filepro.markdown_path, up.filepro.name.md)
            >>> os.path.exists(fn)
            True
            >>> up.remove()
            >>> os.path.exists(fn)
            False
            >>> shutil.rmtree(test_path)
        """
        self.filepro.deleteconvert()
