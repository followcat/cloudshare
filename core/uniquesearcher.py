import glob
import os.path

import utils.builtin


class UniqueSearcher(object):
    def __init__(self, path):
        """
            >>> import shutil
            >>> import core.basedata
            >>> import core.uniquesearcher
            >>> import interface.gitinterface
            >>> import services.curriculumvitae
            >>> import extractor.information_explorer
            >>> repo_name = 'core/test_repo'
            >>> test_path = 'core/test_output'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> fp1 = core.docprocessor.Processor(f1, 'cv_1.doc', test_path)
            >>> yamlinfo = extractor.information_explorer.catch_cvinfo(
            ...     fp1.markdown_stream.decode('utf8'), fp1.base.base, fp1.name.base)
            >>> cv1 = core.basedata.DataObject(fp1.name, fp1.markdown_stream, yamlinfo)
            >>> svc_cv = services.curriculumvitae.CurriculumVitae(interface.path)
            >>> fp1.result
            True
            >>> us = core.uniquesearcher.UniqueSearcher(svc_cv.path)
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
