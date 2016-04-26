import time
import shutil
import codecs
import os.path

import utils.builtin
import core.exception
import core.outputstorage
import core.uniquesearcher
import core.converterutils


class CurriculumVitaeObject(object):

    path = 'CV'

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

    def confirm(self, repo, committer=None):
        """
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> import repointerface.gitinterface
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> repo_name = 'webapp/views/test_repo'
            >>> test_path = "webapp/views/test_output"
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> up = webapp.views.cv.CurriculumVitaeObject(name, obj, test_path)
            >>> up.confirm(interface)
            True
            >>> up.confirm(interface)
            False
            >>> up.information
            'Exists File'
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        result = False
        try:
            self.storage(repo, committer=committer)
            result = True
        except core.exception.DuplicateException:
            self.information = 'Exists File'
        return result

    def confirm_md(self, repo, committer=None):
        """
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> import repointerface.gitinterface
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> repo_name = 'webapp/views/test_repo'
            >>> test_path = "webapp/views/test_output"
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> up = webapp.views.cv.CurriculumVitaeObject(name, obj, test_path)
            >>> up.confirm(interface)
            True
            >>> up.confirm_md(interface)
            True
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        self.storage_md(repo, committer=committer)
        return True

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

    def storage(self, repo, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> import repointerface.gitinterface
            >>> basepath = 'core/test_output'
            >>> repo_name = 'core/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> f2 = open('core/test/cv_2.doc', 'r')
            >>> cv1 = webapp.views.cv.CurriculumVitaeObject('cv_1.doc', f1, basepath)
            >>> cv2 = webapp.views.cv.CurriculumVitaeObject('cv_2.doc', f2, basepath)
            >>> cv1.storage(interface)
            True
            >>> cv2.storage(interface)
            True
            >>> md_list = []
            >>> for position in glob.glob(os.path.join(repo_name, '*.md')):
            ...     with open(position) as f:
            ...         md_list.append(f.read())
            >>> yaml_list = []
            >>> for position in glob.glob(os.path.join(repo_name, '*.yaml')):
            ...     with open(position) as f:
            ...         yaml_list.append(f.read())
            >>> len(yaml_list)
            2
            >>> f1.close()
            >>> f2.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(basepath)
        """
        if self.result is False:
            return False
        path = repo.repo.path
        unique_checker = core.uniquesearcher.UniqueSearcher(repo)
        if unique_checker.unique(self.filepro.yamlinfo) is False:
            error = 'Duplicate files: %s' % self.convertname.base
            raise core.exception.DuplicateException(error)
        shutil.copy(os.path.join(self.filepro.markdown_path, self.filepro.name.md),
                    os.path.join(path, self.filepro.name.md))
        self.filepro.yamlinfo['committer'] = committer
        self.filepro.yamlinfo['date'] = time.time()
        utils.builtin.save_yaml(self.filepro.yamlinfo, path, self.filepro.name.yaml)
        repo.add_files([self.filepro.name.md, self.filepro.name.yaml],
                       committer=committer)
        return True

    def storage_md(self, repo, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import webapp.views.cv
            >>> import repointerface.gitinterface
            >>> basepath = 'core/test_output'
            >>> repo_name = 'core/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> f = open('core/test/cv_1.doc', 'r')
            >>> cv1 = webapp.views.cv.CurriculumVitaeObject('cv_1.doc', f, basepath)
            >>> cv1.storage_md(interface)
            True
            >>> md_files = glob.glob(os.path.join(repo_name, '*.md'))
            >>> len(md_files)
            1
            >>> yaml_files = glob.glob(os.path.join(repo_name, '*.yaml'))
            >>> len(yaml_files)
            0
            >>> f.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(basepath)
        """
        if self.result is False:
            return False
        path = repo.repo.path
        shutil.copy(os.path.join(self.filepro.markdown_path, self.filepro.name.md),
                    os.path.join(path, self.filepro.name.md))
        repo.add_files([self.filepro.name.md],
                       committer=committer)
        return True

