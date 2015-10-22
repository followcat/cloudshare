import glob
import os.path

import yaml


class UniqueSearcher(object):
    def __init__(self, path):
        """
        >>> import shutil
        >>> import os.path
        >>> import core.outputstorage
        >>> import core.converterutils
        >>> import core.uniquesearcher
        >>> basepath = 'core/test_output'
        >>> outputpath = core.outputstorage.OutputPath(basepath)
        >>> cv1 = core.converterutils.FileProcesser('core/test', 'cv_1.doc',
        ... basepath)
        >>> us = core.uniquesearcher.UniqueSearcher(cv1.yaml_path)
        >>> us.unique_name('cv_1')
        True
        >>> cv1.convert()
        True
        >>> us.unique_name('cv_1')
        True
        >>> us.reload()
        >>> us.unique_name('cv_1')
        False
        >>> shutil.rmtree(basepath)
        """
        self.yaml_path = path
        self.yaml_datas = {}
        for f in glob.glob(os.path.join(self.yaml_path, '*.yaml')):
            with open(f) as fp:
                data = yaml.load(fp.read())
            base, suffix = os.path.splitext(f)
            self.yaml_datas[base] = data

    def unique_name(self, name):
        for each in self.yaml_datas.values():
            if name == each['filename'].encode('utf-8'):
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
