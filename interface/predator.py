# -*- coding: utf-8 -*-
import re
import glob
import os.path
import subprocess

import yaml
import pypandoc

import utils.builtin
import interface.base


class PredatorLiteInterface(interface.base.Interface):

    yamldir = 'JOBTITLES'
    extension = '.yaml'
    
    def __init__(self, path):
        self.path = path
        self.yamlpath = os.path.join(self.path, self.yamldir)
        super(PredatorLiteInterface, self).__init__(path)

    def exists(self, filename):
        result = False
        name, extension = os.path.splitext(filename)
        path, str_id = os.path.split(name)
        yamlname = str_id + self.extension
        path_file = os.path.join(self.yamlpath, yamlname)
        if os.path.exists(path_file):
            result = True
        return result

    def get(self, filename):
        name, extension = os.path.splitext(filename)
        if extension == '.yaml':
            path, name = os.path.split(filename)
            yamlname = os.path.join(self.yamldir, name)
            return self._get_file(yamlname)
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
                os.path.join(self.yamlpath, '*.yaml'))]

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


class PredatorInterface(PredatorLiteInterface):

    cvdir = 'CV'
    extension = '.html'

    def __init__(self, path):
        super(PredatorInterface, self).__init__(path)
        self.cvpath = os.path.join(path, self.cvdir)

    def exists(self, filename):
        result = False
        name, extension = os.path.splitext(filename)
        cvname = filename.replace(extension, self.extension)
        path_file = os.path.join(self.cvpath, cvname)
        if os.path.exists(path_file):
            result = True
        return result

    def get(self, filename):
        """
        For an invalid filename, pandoc output back the filename
            >>> import random
            >>> import interface.predator
            >>> invalid = '/tmp/'+''.join(map(lambda x:str(random.randrange(10)), range(30)))+'.md'
            >>> pypandoc.convert(invalid, 'markdown', format='docbook')[:5]
            u'/tmp/'

        The interface is expected to return None
            >>> pred = interface.predator.PredatorInterface('/tmp')
            >>> assert pred.get(invalid) is None
        """
        name, extension = os.path.splitext(filename)
        if extension == '.yaml':
            path, name = os.path.split(filename)
            yamlname = os.path.join(self.yamldir, name)
            return self._get_file(yamlname)
        elif extension == '.md':
            cvname = filename.replace(extension, self.extension)
            input_file = os.path.join(self.path, cvname)
            if os.path.exists(input_file):
                return pypandoc.convert(input_file, 'markdown', format='docbook')
        else:
            return self._get_file(filename)
