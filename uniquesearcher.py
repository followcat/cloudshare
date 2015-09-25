import glob
import os.path

import yaml

import outputstorage


class UniqueSearcher(object):
    def __init__(self):
        """
        >>> import shutil
        >>> import os.path
        >>> import outputstorage
        >>> import converterutils
        >>> import uniquesearcher
        >>> output_backup = outputstorage.OutputPath._output
        >>> outputstorage.OutputPath._output = 'test_output'
        >>> cv1 = converterutils.FileProcesser('./test', 'cv_1.doc')
        >>> us = uniquesearcher.UniqueSearcher()
        >>> us.unique_name('cv_1')
        True
        >>> cv1.convert()
        True
        >>> us.unique_name('cv_1')
        True
        >>> us.reload()
        >>> us.unique_name('cv_1')
        False
        >>> shutil.rmtree('test_output')
        >>> outputstorage.OutputPath._output = output_backup
        """
        self.yaml_path = outputstorage.OutputPath.yaml
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
