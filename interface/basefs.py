# -*- coding: utf-8 -*-
import io
import os
import glob
import tarfile
import xml.etree.ElementTree

import interface.base


class BaseFSInterface(interface.base.Interface):

    rawextention = '.html'
    mdextention = '.md'
    yamlextention = '.yaml'
    
    def __init__(self, path, name=None):
        self.path = path
        super(BaseFSInterface, self).__init__(path, name=name)
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
        with open(path_file) as fp:
            data = fp.read()
        return data

    def getraw(self, filename):
        def get_namespaces(raw):
            namespaces = dict([
                node for _, node in xml.etree.ElementTree.iterparse(
                    io.BytesIO(raw), events=['start-ns']
                )
            ])
            return namespaces
        def remove_namespace(raw, namespaces):
            """Remove namespace in the passed document in place."""
            e = xml.etree.ElementTree.fromstring(raw)
            for name in namespaces:
                namespace = namespaces[name]
                ns = u'{%s}' % namespace
                nsl = len(ns)
                for elem in e.getiterator():
                    if elem.tag.startswith(ns):
                        elem.tag = elem.tag[nsl:]
            return xml.etree.ElementTree.tostring(e, encoding='utf-8')

        result = self.get(filename)
        if result is not None:
            try:
                namespaces = get_namespaces(result)
                if namespaces:
                    result = remove_namespace(result, namespaces)
            except xml.etree.ElementTree.ParseError:
                pass
            result = result.decode('utf-8')
        return result

    def modify(self, filepath, stream, message=None, committer=None, do_commit=True):
        result = False
        filepath = os.path.join(self.path, filepath)
        if os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(stream)
            result = True
        return result

    def lsfiles(self, prefix, filterfile):
        return [os.path.split(f)[1] for f in glob.glob(
                os.path.join(self.path, prefix, filterfile))]

    def grep(self, restrings, path='', files=None):
        if files is None:
            files = ['*']
        command = self.gencommand(restrings, files)
        result = self.subprocess_grep(command, path, shell=True)
        return result

    def grep_yaml(self, restrings, path='', files=None):
        if files is None:
            files = ['*.yaml']
        command = self.gencommand(restrings, files)
        result = self.subprocess_grep(command, path, shell=True)
        return result

    def gencommand(self, restrings, files):
        command = ''
        keywords = restrings.split()
        if keywords:
            command = 'grep -l '
            command += keywords[0].encode('utf-8')
            command += ' ' + ' '.join(files)
            for each in keywords[1:]:
                command += ' | grep '
                command += each.encode('utf-8')
        return command

    def do_commit(self, filenames, message=None, committer=None):
        return ''

    def add(self, filepath, filedate, message=None, committer=None, do_commit=True):
        path = os.path.join(self.path, filepath)
        with open(path, 'w') as f:
            f.write(filedate)
        return True

    def delete(self, filepath, message=None, committer=None, do_commit=True):
        path = os.path.join(self.path, filepath)
        os.remove(path)
        return True

    def add_files(self, filenames, filedatas, message=None, committer=None, do_commit=True):
        assert len(filenames) == len(filedatas)
        for filename, filedata in zip(filenames, filedatas):
            self.add(filename, filedata)

    def backup(self, path, bare=False):
        tar=tarfile.open(os.path.join(path, 'backup.tar.gz'), 'w:gz')
        for root, dir, files in os.walk(self.path):
            for file in files:
                fullpath=os.path.join(root, file)
                tar.add(fullpath, arcname=file)
        tar.close()
