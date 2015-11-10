import glob
import os.path

import yaml
import utils._yaml


class UniqueSearcher(object):
    def __init__(self, repo):
        """
            >>> import shutil
            >>> import core.converterutils
            >>> import repointerface.gitinterface
            >>> repo_name = 'core/test_repo'
            >>> basepath = 'core/test_output'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> cv1 = core.converterutils.FileProcesser('core/test',
            ... 'cv_1.doc', basepath)
            >>> cv1.convert()
            True
            >>> us = core.uniquesearcher.UniqueSearcher(interface)
            >>> us.unique(cv1.yamlinfo)
            True
            >>> cv1.storage(interface)
            True
            >>> us.unique(cv1.yamlinfo)
            True
            >>> us.reload()
            >>> us.unique(cv1.yamlinfo)
            False
            >>> cv1.storage(interface)  # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            DuplicateException: Duplicate files: cv_1
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(basepath)
        """
        self.yaml_path = repo.repo.path
        self.yaml_datas = {}
        for f in glob.glob(os.path.join(self.yaml_path, '*.yaml')):
            with open(f) as fp:
                data = yaml.load(fp.read(), Loader=utils._yaml.Loader)
            base, suffix = os.path.splitext(f)
            self.yaml_datas[base] = data

    def unique(self, yamldict):
        phone = yamldict['phone']
        email = yamldict['email']
        if len(phone) == 0 and len(email) == 0:
            return False
        for each in self.yaml_datas.values():
            if (phone and phone == each['phone'].encode('utf-8') or
                    email and email == each['email'].encode('utf-8')):
                return False
        else:
            return True

    def reload(self):
        self.yaml_datas = {}
        for f in glob.glob(os.path.join(self.yaml_path, '*.yaml')):
            base, suffix = os.path.splitext(f)
            if base not in self.yaml_datas:
                with open(f) as fp:
                    data = yaml.load(fp.read())
                self.yaml_datas[base] = data
