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
            >>> repo_name = 'core/test_repo'
            >>> test_path = 'core/test_output'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> fp1 = core.converterutils.FileProcesser(f1, 'cv_1.doc', test_path)
            >>> cv1 = services.curriculumvitae.CurriculumVitaeObject(fp1.name,
            ...         fp1.markdown_stream, fp1.yamlinfo)
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(interface)
            >>> fp1.result
            True
            >>> us = core.uniquesearcher.UniqueSearcher(svc_cv.repo_path)
            >>> us.unique(cv1.metadata)
            True
            >>> svc_cv.add(cv1)
            True
            >>> us.unique(cv1.metadata)
            True
            >>> us.reload()
            >>> us.unique(cv1.metadata)
            False
            >>> svc_cv.add(cv1)
            False
            >>> f1.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        self.yaml_path = path
        self.yaml_datas = {}
        self.reload()

    def update(self):
        for f in glob.glob(os.path.join(self.yaml_path, '*.yaml')):
            path, name = os.path.split(f)
            base, suffix = os.path.splitext(name)
            if base not in self.yaml_datas:
                data = utils.builtin.load_yaml(path, name)
                self.yaml_datas[base] = data

    def reload(self):
        self.yaml_datas = {}
        self.update()

    def unique(self, yamldict):
        phone = yamldict['phone']
        email = yamldict['email']
        if len(phone) == 0 and len(email) == 0:
            return False
        for each in self.yaml_datas.values():
            if ((phone and phone == each['phone']) or
                (email and email == each['email'])):
                return False
        else:
            return True
