import os
import time
import yaml

import utils.issue
import utils._yaml
import core.outputstorage
import services.base.service


class BaseStorage(services.base.service.Service):

    SAVE_DIR = ''
    commitinfo = 'BaseData'

    def __init__(self, path, name=None):
        self.path = os.path.join(path, self.SAVE_DIR)
        super(BaseStorage, self).__init__(self.path, name)
        self.unique_checker = None
        self.info = ""
        self._nums = 0

    def exists(self, id):
        """
            >>> import interface.basefs
            >>> import services.base.storage
            >>> services.base.storage.BaseStorage.SAVE_DIR = 'CV'
            >>> DIR = 'repo'
            >>> DB = interface.basefs.BaseFSInterface(DIR)
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DB.path, 'repo')
            >>> assert SVC_BSSTO.exists('blr6dter')

            >>> import interface.gitinterface
            >>> DB = interface.gitinterface.GitInterface(DIR)
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DB.path, 'repo')
            >>> assert SVC_BSSTO.exists('blr6dter')
            >>> services.base.storage.BaseStorage.SAVE_DIR = ''
        """
        return id in self.ids

    def unique(self, baseobject):
        name = core.outputstorage.ConvertName(baseobject.name)
        return not self.exists(name.base)

    def add(self, bsobj, committer=None, unique=True, yamlfile=True):
        if unique is True and self.unique(bsobj) is False:
            self.info = "Exists File"
            return False
        name = core.outputstorage.ConvertName(bsobj.name)
        message = "Add %s: %s data." % (self.commitinfo, name)
        self.interface.add(name.md, bsobj.data, message=message, committer=committer)
        if yamlfile is True:
            bsobj.metadata['committer'] = committer
            bsobj.metadata['date'] = time.time()
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            self.interface.add(name.yaml, yaml.safe_dump(bsobj.metadata, allow_unicode=True),
                               message=message, committer=committer)
        self._nums += 1
        return True

    def getmd(self, name):
        """
            >>> import interface.basefs
            >>> import services.base.storage
            >>> services.base.storage.BaseStorage.SAVE_DIR = 'CV'
            >>> DIR = 'repo'
            >>> DB = interface.basefs.BaseFSInterface(DIR)
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DB.path, 'repo')
            >>> assert SVC_BSSTO.getmd('blr6dter.yaml')

            >>> import interface.gitinterface
            >>> DB = interface.gitinterface.GitInterface(DIR)
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DB.path, 'repo')
            >>> assert SVC_BSSTO.getmd('blr6dter.yaml')
            >>> services.base.storage.BaseStorage.SAVE_DIR = ''
        """
        result = unicode()
        md = core.outputstorage.ConvertName(name).md
        markdown = self.interface.get(md)
        if markdown is None:
            result = None
        elif isinstance(markdown, unicode):
            result = markdown
        else:
            result = unicode(str(markdown), 'utf-8')
        return result

    def search(self, keyword):
        results = set()
        allfile = self.interface.grep(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def search_yaml(self, keyword):
        results = set()
        allfile = self.interface.grep_yaml(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def names(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).md

    def yamls(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).yaml

    def datas(self):
        for id in self.ids:
            name = core.outputstorage.ConvertName(id).md
            text = self.getmd(id)
            yield name, text

    @property
    def ids(self):
        """
            >>> import interface.basefs
            >>> import services.base.storage
            >>> services.base.storage.BaseStorage.SAVE_DIR = 'CV'
            >>> DIR = 'repo'
            >>> DB = interface.basefs.BaseFSInterface(DIR)
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DB.path, DIR)
            >>> assert SVC_BSSTO.interface.lsfiles('.', 'blr6dter.yaml')

            >>> import interface.gitinterface
            >>> DB = interface.gitinterface.GitInterface(DIR)
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DB.path, DIR)
            >>> assert SVC_BSSTO.interface.lsfiles('.', 'blr6dter.yaml')
            >>> services.base.storage.BaseStorage.SAVE_DIR = ''
        """
        return [os.path.splitext(f)[0]
                for f in self.interface.lsfiles('.', '*.yaml')]

    @property
    def NUMS(self):
        if not self._nums:
            self._nums = len(self.ids)
        return self._nums

