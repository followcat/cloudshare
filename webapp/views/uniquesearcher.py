import glob
import os.path

import utils.builtin


class UniqueSearcher(object):
    def __init__(self, path):
        """
            >>> import shutil
            >>> import webapp.views.cv
            >>> import webapp.views.uniquesearcher
            >>> import repointerface.gitinterface
            >>> repo_name = 'webapp/views/test_repo'
            >>> test_path = "webapp/views/test_output"
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> cv1 = webapp.views.cv.CurriculumVitaeObject('cv_1.doc', f1, test_path)
            >>> repocv = webapp.views.cv.RepoCurriculumVitae(interface)
            >>> cv1.result
            True
            >>> us = webapp.views.uniquesearcher.UniqueSearcher(repocv.repo_path)
            >>> us.unique(cv1.filepro.yamlinfo)
            True
            >>> repocv.add(cv1)
            True
            >>> us.unique(cv1.filepro.yamlinfo)
            True
            >>> us.reload()
            >>> us.unique(cv1.filepro.yamlinfo)
            False
            >>> repocv.add(cv1)
            False
            >>> f1.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        self.yaml_path = path
        self.yaml_datas = {}
        for f in glob.glob(os.path.join(self.yaml_path, '*.yaml')):
            data = utils.builtin.load_yaml("", f)
            base, suffix = os.path.splitext(f)
            self.yaml_datas[base] = data

    def unique(self, yamldict):
        phone = yamldict['phone']
        email = yamldict['email']
        if len(phone) == 0 and len(email) == 0:
            return False
        for each in self.yaml_datas.values():
            if (phone == each['phone'].encode('utf-8') and
                email == each['email'].encode('utf-8')):
                return False
        else:
            return True

    def reload(self):
        self.yaml_datas = {}
        for f in glob.glob(os.path.join(self.yaml_path, '*.yaml')):
            base, suffix = os.path.splitext(f)
            if base not in self.yaml_datas:
                data = utils.builtin.load_yaml("", f)
                self.yaml_datas[base] = data
