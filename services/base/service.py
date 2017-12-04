import core.outputstorage


class Service(object):
    
    def get_id(self, name):
        return core.outputstorage.ConvertName(name).base

    @property
    def ids(self):
        try:
            return self._ids
        except AttributeError:
            return set()

    def names(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).md

    def yamls(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).yaml

    def exists(self, id):
        return self.get_id(id) in self.ids

    def unique(self, bsobj):
        id = bsobj.ID
        return not self.exists(id)

    def _add(self, name):
        id = self.get_id(name)
        self.ids.add(id)
        return True

    def _remove(self, name):
        id = self.get_id(name)
        self.ids.remove(id)
        return True

