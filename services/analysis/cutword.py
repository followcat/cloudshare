import os
import ujson

import core.outputstorage
import services.base.storage


class Cutword(services.base.storage.BaseStorage):

    commitinfo = 'Cutword'

    def unique(docobj):
        return not self.exists(docobj.name)

    def datas(self):
        for id in self.ids:
            yield id, self.getyaml(id)

    def exists(self, id):
        infoname = core.outputstorage.ConvertName(id).yaml
        return os.path.exists(os.path.join(self.path, infoname))

    def getyaml(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        yaml_str = self.interface.get(name)
        return ujson.loads(yaml_str)

    def add(self, docobj, committer=None, unique=True, yamlfile=True):
        name = core.outputstorage.ConvertName(docobj.name)
        if unique is True and self.unique(docobj) is False:
            return False
        message = "Add %s: %s metadata." % (self.commitinfo, name)
        self.interface.add(name.yaml, ujson.dumps(docobj.metadata,
                           ensure_ascii=False),
                           message=message, committer=committer)
        self._nums += 1
        return True
