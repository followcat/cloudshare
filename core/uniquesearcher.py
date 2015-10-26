import glob
import os.path

import yaml


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
            >>> us = core.uniquesearcher.UniqueSearcher(interface)
            >>> us.unique_name('cv_1')
            True
            >>> cv1.storage(interface)
            True
            >>> us.unique_name('cv_1')
            True
            >>> us.reload()
            >>> us.unique_name('cv_1')
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
                data = yaml.load(fp.read())
            base, suffix = os.path.splitext(f)
            self.yaml_datas[base] = data

    def unique_name(self, name):
        for each in self.yaml_datas.values():
            if ('filename' in each and
                    name == each['filename'].encode('utf-8')):
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
