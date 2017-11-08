import os
import subprocess

import utils.esquery


class NotImplementedInterface(Exception):
    pass

class Interface(object):

    def __init__(self, path, name, searchengine=None):
        self.path = path
        self.name = name
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

    def search(self, keywords=None, filterdict=None, ids=None, source=False,
               start=0, size=None, path='', files=None):
        if self.searchengine is None:
            result = self.grep(keywords, path=path, files=files)
        else:
            result = self.SEsearch(keywords=keywords, filterdict=filterdict, ids=ids,
                                   source=source, start=start, size=size)
        return result

    def search_yaml(self, keywords=None, filterdict=None, ids=None, source=False,
                    start=0, size=None, path='', files=None):
        if self.searchengine is None:
            result = self.grep_yaml(keywords, path=path, files=files)
        else:
            result = self.SEsearch_yaml(keywords=keywords, filterdict=filterdict, ids=ids,
                                        source=source, start=start, size=size)
        return result

    def grep(self):
        raise NotImplementedInterface

    def grep_yaml(self):
        raise NotImplementedInterface

    def SEquery(self, indexname, keywords=None, filterdict=None, ids=None,
                source=False, start=0, size=None):
        query_dict = utils.esquery.request_gen(keywords=keywords,
                                               filterdict=filterdict, ids=ids)
        kwargs = {
            '_source_include': 'file',
            'body': query_dict,
            '_source': 'false' if source is False else 'true'
        }
        result = utils.esquery.scroll(self.searchengine, indexname, kwargs,
                                      start=start, size=size)
        if source is False:
            result = map(lambda x: (x['_id'], x['_score']), result)
        return result

    def SEcount(self, keywords=None, filterdict=None, ids=None):
        kwargs = dict()
        indexname = ['.'.join([self.name])]
        if filterdict is not None:
            indexname.extend(["cloudshare.index"])
        querydict = utils.esquery.request_gen(keywords=keywords,
                                              filterdict=filterdict, ids=ids)
        kwargs.update({'body': querydict})
        result = utils.esquery.count(self.searchengine, indexname, kwargs)
        return result

    def SEcount_yaml(self, keywords=None, filterdict=None, ids=None):
        kwargs = dict()
        indexname = ['.'.join([self.name, 'yaml'])]
        if filterdict is not None:
            indexname.extend(["cloudshare.index"])
        querydict = utils.esquery.request_gen(keywords=keywords,
                                              filterdict=filterdict, ids=ids)
        kwargs.update({'body': querydict})
        result = utils.esquery.count(self.searchengine, indexname, kwargs)
        return result


    def SEsearch(self, keywords=None, filterdict=None, ids=None, source=False,
                 start=0, size=10):
        indexname = ['.'.join([self.name])]
        if filterdict is not None:
            indexname.extend(["cloudshare.index"])
        result = self.SEquery(indexname, keywords=keywords, filterdict=filterdict, ids=ids,
                              source=source, start=start, size=size)
        return result

    def SEsearch_yaml(self, keywords=None, filterdict=None, ids=None, source=False,
                      start=0, size=10):
        indexname = ['.'.join([self.name, 'yaml'])]
        if filterdict is not None:
            indexname.extend(["cloudshare.index"])
        result = self.SEquery(indexname, keywords=keywords, filterdict=filterdict, ids=ids,
                              source=source, start=start, size=size)
        return result

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
