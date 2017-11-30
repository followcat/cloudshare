import os

import ujson

import services.base.storage


class NameStorage(services.base.storage.BaseStorage):

    ids_file = 'names.json'

    def __init__(self, path, name, iotype='git'):
        super(NameStorage, self).__init__(path, name, iotype=iotype)
        idsfile = os.path.join(path, NameStorage.ids_file)
        if not os.path.exists(idsfile):
            dumpinfo = ujson.dumps(sorted(self.ids), indent=4)
            self.interface.add(self.ids_file, dumpinfo, message="Init ids file.")

    @property
    def ids(self):
        try:
            return self._ids
        except AttributeError:
            try:
                return ujson.loads(self.interface.get(self.ids_file))
            except IOError:
                return super(NameStorage, self).ids

    def saveids(self):
        self.interface.modify(self.ids_file, ujson.dumps(sorted(self.ids), indent=4))

    def add(self, bsobj, committer=None, unique=True,
            kv_file=False, text_file=True, do_commit=True):
        result = False
        if (unique and self.unique(bsobj)) or not unique:
            id = bsobj.ID
            self._add(id)
            return self.interface.modify(self.ids_file, ujson.dumps(sorted(self.ids), indent=4),
                                     message='Add new data %s.'%id,
                                     committer=committer, do_commit=do_commit)
        return result

    def remove(self, bsobj, committer=None, unique=True,
            kv_file=False, text_file=True, do_commit=True):
        result = False
        id = bsobj.ID
        if self.exists(id):
            self._remove(id)
            return self.interface.modify(self.ids_file,
                              ujson.dumps(sorted(self.ids), indent=4),
                              message="Delete id: " + id,
                              committer=committer, do_commit=do_commit)
        else:
            result = True
        return result

