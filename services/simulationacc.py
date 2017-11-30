import os
import ujson

import core.exception
import core.outputstorage
import services.operator.simulation


class SimulationACC(services.operator.simulation.Simulation):

    YAML_TEMPLATE = (
        ("inviter",             str),
    )

    def __init__(self, path, name, storages, iotype='git'):
        super(SimulationACC, self).__init__(path, name, storages, iotype=iotype)

    def _templateinfo(self, committer):
        info = super(SimulationACC, self)._templateinfo(committer)
        info['inviter'] = committer
        return info

    def getinfo(self, id):
        if self.exists(id):
            return super(SimulationACC, self).getinfo(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def getyaml(self, id):
        if self.exists(id):
            return super(SimulationACC, self).getyaml(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def getid_byname(self, name):
        for storage in self.storages:
            if name in storage.USERS:
                return storage.USERS[name]['id']

    def getmd(self, id):
        if self.exists(id):
            return super(SimulationACC, self).getmd(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def remove(self, id, committer=None, do_commit=True):
        result = False
        committer_id = self.getid_byname(committer)
        if self.exists(id) and self.exists(committer_id):
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
