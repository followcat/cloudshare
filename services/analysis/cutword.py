import os
import ujson

import utils.builtin
import core.outputstorage
import services.base.storage


class Cutword(services.base.storage.BaseStorage):

    commitinfo = 'Cutword'

    def unique(self, docobj):
        return not self.exists(self.filename(docobj.name).base)

    def datas(self):
        for id in self.ids:
            yield id, self.getyaml(id)

    def exists(self, id):
        filename = self.filename(id)
        return os.path.exists(os.path.join(self.path, filename.yaml))

    def getyaml(self, id):
        filename = self.filename(id)
        yaml_str = self.interface.get(filename.yaml)
        return ujson.loads(yaml_str)

    def add(self, docobj, committer=None, unique=True, yamlfile=True):
        filename = self.filename(docobj.name)
        if unique is True and self.unique(docobj) is False:
            return False
        message = "Add %s: %s metadata." % (self.commitinfo, filename.base)
        try:
            self.interface.add(filename.yaml, ujson.dumps(docobj.metadata,
                               ensure_ascii=False),
                               message=message, committer=committer)
            result = True
            self._nums += 1
        except IOError:
            result = False
        return result

    def filename(self, name):
        name = core.outputstorage.ConvertName(utils.builtin.industrytopath(name))
        return name
