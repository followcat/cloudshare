import yaml
import os.path

import utils._yaml
import core.outputstorage
import services.base.storage


class People(services.base.storage.BaseStorage):

    commitinfo = 'People'

    def __init__(self, path, storages, iotype):
        super(People, self).__init__(path, iotype=iotype)
        self.storages = storages

    def exists(self, id):
        id_yaml = core.outputstorage.ConvertName(id).yaml
        return self.interface.exists(id_yaml)

    def getmd(self, id):
        info = self.getyaml(id)
        for id in info['cv']:
            for sto in self.storages:
                if sto.exists(id):
                    yield sto.getmd(id)
                    break

    def getinfo(self, id):
        info = self.getyaml(id)
        for id in info['cv']:
            for sto in self.storages:
                if sto.exists(id):
                    yield sto.getyaml(id)
                    break

    def add(self, peopobj, committer=None, unique=True, yamlfile=True, do_commit=True):
        name = core.outputstorage.ConvertName(peopobj.name)
        if unique is True and self.unique(peopobj.name) is not True:
            savedobj = self.getyaml(name)
            if peopobj.metadata['cv'][0] in savedobj['cv']:
                return False
            peopobj.metadata['cv'] = savedobj['cv'] + peopobj.metadata['cv']
        message = "Add %s: %s metadata." % (self.commitinfo, name)
        self.interface.add(name.yaml, yaml.safe_dump(peopobj.metadata, allow_unicode=True),
                           message=message, committer=committer, do_commit=do_commit)
        self._nums += 1
        return True
