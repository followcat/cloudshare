import core.outputstorage
import services.base.kv_storage
import services.operator.checker


class People(services.base.kv_storage.KeyValueStorage):

    def add(self, peopobj, committer=None, unique=True, kv_file=True, text_file=False, do_commit=True):
        name = core.outputstorage.ConvertName(peopobj.name)
        if unique is True and self.unique(peopobj) is False:
            savedobj = self.getyaml(name)
            if peopobj.metadata['cv'][0] in savedobj['cv']:
                return False
            peopobj.metadata['cv'] = savedobj['cv'] + peopobj.metadata['cv']
        return super(People, self).add(peopobj, committer, unique, kv_file, text_file, do_commit=do_commit)

class CVSelector(services.operator.checker.Selector):
    def selection(self, x):
        return self.operator_service.getyaml(x)['cv']

