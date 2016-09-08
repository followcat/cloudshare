# -*- coding: utf-8 -*-
import glob
import os.path
import subprocess

import interface.base


class BaseFSInterface(interface.base.Interface):

    rawextention = '.html'
    mdextention = '.md'
    yamlextention = '.yaml'
    
    def __init__(self, path):
        self.path = path
        super(BaseFSInterface, self).__init__(path)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def exists(self, filename):
        result = False
        path_file = os.path.join(self.path, filename)
        if os.path.exists(path_file):
            result = True
        return result

    def get(self, filename):
        data = None
        path_file = os.path.join(self.path, filename)
        if os.path.exists(path_file):
            with open(path_file) as fp:
                data = fp.read()
        return data

    def modify(self, filepath, stream, message=None, committer=None):
        result = False
        filepath = os.path.join(self.path, filepath)
        if os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(stream)
            result = True
        return result

    def lsfiles(self, *args, **kwargs):
        return [os.path.split(f)[1] for f in glob.glob(
                os.path.join(self.path, '*'+self.yamlextention))]

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
        grep_list = []
        keywords = restrings.split()
        if keywords:
            command = 'grep -l '
            command += keywords[0].encode('utf-8')
            command += ' *.yaml'
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

    def add(self, filepath, filedate):
        with open(filepath, 'w') as f:
            f.write(filedate)
        return True
