import yaml
import os.path

import utils._yaml
import core.outputstorage
import services.base.storage


class People(services.base.storage.BaseStorage):

    commitinfo = 'People'

    def __init__(self, storage, path, name=None, iotype=None):
        self.storage = storage
        super(People, self).__init__(path, name=name, iotype=iotype)

    def exists(self, id):
        id_yaml = core.outputstorage.ConvertName(id).yaml
        return self.interface.exists(id_yaml)

    def getmd(self, id):
        info = self.getyaml(id)
        for id in info['cv']:
            if self.storage.exists(id):
                yield self.storage.getmd(id)

    def getinfo(self, id):
        info = self.getyaml(id)
        for id in info['cv']:
            if self.storage.exists(id):
                yield self.storage.getyaml(id)

    def add(self, peopobj, committer=None, unique=True, yamlfile=True, do_commit=True):
        name = core.outputstorage.ConvertName(peopobj.name)
        if unique is True and self.unique(peopobj) is False:
            savedobj = self.getyaml(name)
            if peopobj.metadata['cv'][0] in savedobj['cv']:
                return False
            peopobj.metadata['cv'] = savedobj['cv'] + peopobj.metadata['cv']
        message = "Add %s: %s metadata." % (self.commitinfo, name)
        self.interface.add(name.yaml, yaml.safe_dump(peopobj.metadata, allow_unicode=True),
                           message=message, committer=committer, do_commit=do_commit)
        self._nums += 1
        return True
