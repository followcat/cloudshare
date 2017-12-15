import core.exception
import services.base.kv_storage


class AccessStorage(services.base.kv_storage.KeyValueStorage):
    """ AccessStorage enforce existence check before execution """

    def getinfo(self, id):
        if self.exists(id):
            return super(AccessStorage, self).getinfo(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def getyaml(self, id):
        if self.exists(id):
            return super(AccessStorage, self).getyaml(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def getmd(self, id):
        if self.exists(id):
            return super(AccessStorage, self).getmd(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def remove(self, id, committer=None, do_commit=True):
        result = False
        if self.exists(id):
            self._remove(id)
            filenames = []
            filedatas = []
            filenames.append(bytes(self.ids_file))
            filedatas.append(ujson.dumps(sorted(self.ids), indent=4))
            yamlname = core.outputstorage.ConvertName(id).yaml
            filedir = os.path.join(self.yamlpath, yamlname)
            self.interface.delete(filedir, message='Remove user %s'%id,
                                  committer=committer, do_commit=do_commit)
            self.interface.add_files(filenames, filedatas,
                                     message='Remove %s in ids file.'%id,
                                     committer=committer, do_commit=do_commit)
            result = True
        return result
