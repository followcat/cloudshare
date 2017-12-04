import os
import tarfile
import subprocess

import utils.esquery


class NotImplementedInterface(Exception):
    pass

class Interface(object):

    def __init__(self, path, name):
        self.path = path
        self.name = name

    def do_commit(self, filenames):
        raise NotImplementedInterface

    def get(self, filename):
        raise NotImplementedInterface

    def getraw(self, filename):
        raise NotImplementedInterface

    def add(self, filename, filedata):
        raise NotImplementedInterface

    def exists(self, filename):
        raise NotImplementedInterface

    def modify(self, filename, filedata):
        raise NotImplementedInterface

    def lsfiles(self):
        raise NotImplementedInterface

    def grep(self):
        raise NotImplementedInterface

    def grep_yaml(self):
        raise NotImplementedInterface

    def subprocess_grep(self, command, path, shell):
        grep_list = []
        greppath = os.path.join(self.path, path)
        if not os.path.exists(greppath):
            return grep_list
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             cwd=greppath, shell=shell)
        returncode = p.communicate()[0]
        for each in returncode.split('\n'):
            if each:
                grep_list.append((each, 1))
        return grep_list

    def delete(self):
        raise NotImplementedInterface

    def backup(self, path, git=False):
        tar=tarfile.open(os.path.join(path, 'backup.tar.gz'), 'w:gz')
        for root, dir, files in os.walk(self.path):
            if git is False and '.git' in root.split('/'):
                continue
            for file in files:
                fullpath=os.path.join(root, file)
                tar.add(fullpath, arcname=file)
        tar.close()
