import os
import subprocess


class NotImplementedInterface(Exception):
    pass

class Interface(object):

    def __init__(self, path, searchengine=None):
        self.path = path
        self.searchengine = searchengine

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

    def search(self, keywords, path='', files=None):
        if self.searchengine is None:
            result = self.grep(keywords, path=path, files=files)
        else:
            result = self.searchengine(keywords)
        return result

    def search_yaml(self, restrings, path='', files=None):
        if self.searchengine is None:
            result = self.grep_yaml(restrings, path=path, files=files)
        else:
            result = self.searchengine_yaml(keywords)
        return result

    def grep(self):
        raise NotImplementedInterface

    def grep_yaml(self):
        raise NotImplementedInterface

    def searchengine(self, keywords):
        raise NotImplementedInterface

    def searchengine_yaml(self, keywords):
        raise NotImplementedInterface

    def subprocess_grep(self, command, path, shell):
        grep_list = []
        greppath = os.path.join(self.repo.path, path)
        if not os.path.exists(greppath):
            return grep_list
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             cwd=greppath, shell=shell)
        returncode = p.communicate()[0]
        for each in returncode.split('\n'):
            if each:
                grep_list.append(each)
        return grep_list

    def delete(self):
        raise NotImplementedInterface
