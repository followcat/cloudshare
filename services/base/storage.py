import os
import time
import yaml

import utils.issue
import utils._yaml
import core.outputstorage
import services.base.service
import interface.basefs
import interface.gitinterface


class BaseStorage(services.base.service.Service):

    commitinfo = 'BaseData'

    def __init__(self, path, name=None, iotype=None):
        self.path = path
        self.yamlpath = ''
        super(BaseStorage, self).__init__()
        self.unique_checker = None
        self.info = ""

        if name is None:
            self.name = path.split('/')[-1]
        else:
            self.name = name
        if iotype is None:
            if os.path.exists(os.path.join(path, '.git')):
                self.interface = interface.gitinterface.GitInterface(path, name)
            else:
                self.interface = interface.basefs.BaseFSInterface(path, name)
        elif iotype == 'git':
            self.interface = interface.gitinterface.GitInterface(path, name)
        elif iotype == 'base':
            self.interface = interface.basefs.BaseFSInterface(path, name)
        else:
            raise Exception("Not support iotype.")

    def exists(self, id):
        """
            >>> import services.base.storage
            >>> DIR = 'repo/CV'
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DIR)
            >>> assert SVC_BSSTO.exists('blr6dter')
        """
        return super(BaseStorage, self).exists(id)

    def unique(self, bsobj):
        """
            >>> import shutil
            >>> import core.basedata
            >>> import services.base.storage
            >>> import extractor.information_explorer
            >>> repo_name = 'core/test_repo'
            >>> test_path = 'core/test_output'
            >>> f1 = open('core/test/cv_1.docx', 'r')
            >>> fp1 = utils.docprocessor.libreoffice.LibreOfficeProcessor(f1, 'cv_1.docx', test_path)
            >>> yamlinfo = extractor.information_explorer.catch_cvinfo(
            ...     stream=fp1.markdown_stream.decode('utf8'), filename=fp1.base.base)
            >>> cv1 = core.basedata.DataObject(data=fp1.markdown_stream, metadata=yamlinfo)
            >>> svc_cv = services.base.storage.BaseStorage(repo_name)
            >>> fp1.result
            True
            >>> svc_cv.unique(cv1.name)
            True
            >>> svc_cv.add(cv1)
            True
            >>> svc_cv.unique(cv1.name)
            False
            >>> svc_cv.add(cv1)
            False
            >>> f1.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        return super(BaseStorage, self).unique(bsobj)

    def add(self, filename, stream, message=None, committer=None, do_commit=True):
        self.interface.add(filename, stream, message, committer, do_commit=do_commit)
        return True

    def modify(self, filename, stream, message=None, committer=None, do_commit=True):
        self.interface.modify(filename, stream, message, committer, do_commit=do_commit)
        return True

    def history(self, author=None, entries=10, skip=0):
        return self.interface.history(author=author, max_commits=entries, skip=skip)

    def backup(self, path, **kwargs):
        self.interface.backup(path, **kwargs)

