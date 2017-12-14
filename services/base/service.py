import core.outputstorage


class Service(object):

    _nums = 0

    def get_id(self, name):
        return core.outputstorage.ConvertName(name).base

    @property
    def ids(self):
        if not hasattr(self, '_ids'):
            self._ids = set()
        return self._ids

    @property
    def NUMS(self):
        if not self._nums:
            self._nums = len(self.ids)
        return self._nums

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
        result = False
        if not self.exists(name):
            id = self.get_id(name)
            self.ids.add(id)
            self._nums += 1
            result = True
        return result

    def _remove(self, name):
        result = False
        try:
            id = self.get_id(name)
            self.ids.remove(id)
            self._nums -= 1
            result = True
        except KeyError:
            pass
        return result

