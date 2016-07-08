# -*- coding: utf-8 -*-
import re
import glob
import os.path
import subprocess

import yaml

import utils.builtin
import interface.base


class PredatorLiteInterface(interface.base.Interface):

    cvdir = 'CV'
    rawdir = 'RAW'
    rawextention = '.html'
    mdextention = '.md'
    yamlextention = '.yaml'
    
    def __init__(self, path):
        self.path = path
        self.cvpath = os.path.join(self.path, self.cvdir)
        self.rawpath = os.path.join(self.path, self.rawdir)
        super(PredatorLiteInterface, self).__init__(path)
        if not os.path.exists(self.cvpath):
            os.makedirs(self.cvpath)

    def exists(self, filename):
        result = False
        path_file = os.path.join(self.cvpath, filename)
        if os.path.exists(path_file):
            result = True
        return result

    def get(self, filename):
        name, extension = os.path.splitext(filename)
        if extension == self.yamlextention:
            return self._get_file(filename)
        else:
            return None

    def _get_file(self, filename):
        data = None
        path_file = os.path.join(self.path, filename)
        if os.path.exists(path_file):
            with open(path_file) as fp:
                data = fp.read()
        return data

    def lsfiles(self, *args, **kwargs):
        return [os.path.split(f)[1] for f in glob.glob(
                os.path.join(self.cvpath, '*'+self.yamlextention))]

    def grep(self, restrings, path):
        grep_list = []
        keywords = restrings.split()
        if keywords:
            command = 'grep -l '
            command += keywords[0].encode('utf-8')
            command += ' *'
            for each in keywords[1:]:
                command += ' | grep '
                command += each.encode('utf-8')
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=os.path.join(self.path, path), shell=True)
            returncode = p.communicate()[0]
            for each in returncode.split('\n'):
                if each:
                    grep_list.append(each)
        return grep_list

    def grep_yaml(self, restrings, path):
        return []

    def lsid_md(self):
        return [os.path.splitext(os.path.split(f)[1])[0] for f in glob.glob(
                os.path.join(self.cvpath, '*'+self.mdextention))]

    def lsid_yaml(self):
        return [os.path.splitext(os.path.split(f)[1])[0] for f in glob.glob(
                os.path.join(self.cvpath, '*'+self.yamlextention))]

    def lsid_raw(self):
        return [os.path.splitext(os.path.split(f)[1])[0] for f in glob.glob(
                os.path.join(self.rawpath, '*'+self.rawextention))]

    def getraw(self, filename):
        rawname = os.path.join(self.rawdir, filename)
        return self._get_file(rawname)

    def addcv(self, id, data, yamldata):
        self.addmd(id, data)
        self.addyaml(id, yamldata)
        return True

    def addmd(self, id, data):
        filename = id + self.mdextention
        filepath = os.path.join(self.cvpath, filename)
        self._add(filepath, data)
        return True

    def addyaml(self, id, data):
        filename = id + self.yamlextention
        filepath = os.path.join(self.cvpath, filename)
        self._add(filepath, data)
        return True

    def _add(self, filepath, filedate):
        with open(filepath, 'w') as f:
            f.write(filedate)
        return True

class PredatorInterface(PredatorLiteInterface):

    def get(self, filename):
        """
        For an invalid filename
            >>> import random
            >>> invalid = '/tmp/'+''.join(map(lambda x:str(random.randrange(10)), range(30)))+'.md'

        The interface is expected to return None
            >>> import interface.predator
            >>> pred = interface.predator.PredatorInterface('/tmp')
            >>> assert pred.get(invalid) is None
        """
        return self._get_file(filename)
