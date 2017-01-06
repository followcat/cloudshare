import os
import ujson
import hashlib

import core.outputstorage
import services.base.storage


class Cutword(services.base.storage.BaseStorage):

    commitinfo = 'Cutword'

    def unique(self, id, text):
        return not self.existswords(id, text)

    def getchecksum(self, text):
        m2 = hashlib.md5()
        try:
            m2.update(text)
        except UnicodeEncodeError:
            m2.update(text.encode('utf8'))
        return m2.hexdigest()

    def datas(self):
        for id in self.ids:
            yield id, self.getyaml(id)

    def exists(self, id):
        infoname = core.outputstorage.ConvertName(id).yaml
        return os.path.exists(os.path.join(self.path, infoname))

    def existswords(self, id, text):
        checksum = self.getchecksum(text)
        infoname = core.outputstorage.ConvertName(id).yaml
        try:
            with open(os.path.join(self.path, infoname)) as fp:
                return checksum in fp.read()
        except IOError:
            return False

    def getyaml(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        yaml_str = self.interface.get(name)
        return ujson.loads(yaml_str)

    def getwords(self, id, text):
        checksum = self.getchecksum(text)
        name = core.outputstorage.ConvertName(id).yaml
        yaml_str = self.interface.get(name)
        info = ujson.loads(yaml_str)
        return info['words'][checksum]

    def add(self, docobj, committer=None, unique=True, yamlfile=True):
        name = core.outputstorage.ConvertName(docobj.name)
        if unique is True and self.unique(docobj.name, docobj.data) is not True:
            return False
        checksum = self.getchecksum(docobj.data)
        message = "Add %s: %s checksum %s metadata." % (self.commitinfo, name, checksum)
        if not self.exists(docobj.name):
            info = {'id': docobj.metadata['id'],
                    'words': {checksum: docobj.metadata['words']}}
            self.interface.add(name.yaml, ujson.dumps(info, ensure_ascii=False),
                               message=message, committer=committer)
        else:
            info = getyaml(docobj.metadata['id'])
            info['words'][checksum] = docobj.metadata['words']
            self.interface.modify(name.yaml, ujson.dumps(info, ensure_ascii=False),
                               message=message, committer=committer)
        self._nums += 1
        return True
