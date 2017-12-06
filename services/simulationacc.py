import os
import ujson

import core.exception
import core.outputstorage
import services.operator.simulation

import services.base.kv_storage
import services.base.name_storage


class SelectionACC(services.base.name_storage.NameStorage):

    ids_file = 'names.json'


class SimulationACC(services.base.kv_storage.KeyValueStorage):

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = (
        ("inviter",             str),
    )

    def _templateinfo(self, committer):
        info = super(SimulationACC, self)._templateinfo(committer)
        info['inviter'] = committer
        return info

    def getid_byname(self, name):
        raise NotImplementedError('# FIXME: SimulationACC.getid_byname()')
        for storage in self.storages:
            if name in storage.USERS:
                return storage.USERS[name]['id']

    def remove(self, id, committer=None, do_commit=True):
        result = False
        try:
            committer_id = self.getid_byname(committer)
            if self.exists(committer_id):
                result = super(SimulationACC, self).remove(id, committer, do_commit=do_commit)
        except NotImplementedError:
            # FIXME: SimulationACC.getid_byname()
            result = super(SimulationACC, self).remove(id, committer, do_commit=do_commit)
        return result

