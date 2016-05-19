import glob
import os.path

import utils.builtin


class UniqueSearcher(object):
    def __init__(self, path):
        """
            >>> import shutil
            >>> import services.curriculumvitae
            >>> import core.uniquesearcher
            >>> import interface.gitinterface
            >>> repo_name = 'webapp/views/test_repo'
            >>> test_path = "webapp/views/test_output"
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> cv1 = services.curriculumvitae.CurriculumVitaeObject('cv_1.doc', f1, test_path)
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(interface)
            >>> cv1.result
            True
            >>> us = core.uniquesearcher.UniqueSearcher(svc_cv.repo_path)
            >>> us.unique(cv1.filepro.yamlinfo)
            True
            >>> svc_cv.add(cv1)
            True
            >>> us.unique(cv1.filepro.yamlinfo)
            True
            >>> us.reload()
            >>> us.unique(cv1.filepro.yamlinfo)
            False
            >>> svc_cv.add(cv1)
            False
            >>> f1.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        self.yaml_path = path
        self.yaml_datas = {}
        for f in glob.glob(os.path.join(self.yaml_path, '*.yaml')):
            path, name = os.path.split(f)
            data = utils.builtin.load_yaml(path, name)
            base, suffix = os.path.splitext(name)
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
            path, name = os.path.split(f)
            base, suffix = os.path.splitext(name)
            if base not in self.yaml_datas:
                data = utils.builtin.load_yaml(path, name)
                self.yaml_datas[base] = data
