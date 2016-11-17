import yaml
import os.path

import utils._yaml
import core.outputstorage
import services.base.storage


class People(services.base.storage.BaseStorage):

    commitinfo = 'People'

    def add(self, peopobj, committer=None, unique=True, yamlfile=True):
        name = core.outputstorage.ConvertName(peopobj.name)
        if self.unique(peopobj) is not True:
            savedobj = self.getyaml(name)
            if peopobj.metadata['cv'][0] in savedobj['cv']:
                return False
            peopobj.metadata['cv'] = savedobj['cv'] + peopobj.metadata['cv']
        message = "Add %s: %s metadata." % (self.commitinfo, name)
        self.interface.add(name.yaml, yaml.safe_dump(peopobj.metadata, allow_unicode=True),
                           message=message, committer=committer)
        self._nums += 1
        return True
