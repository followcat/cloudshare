import os
import time

import yaml
import ujson

import utils._yaml
import utils.builtin
import core.outputstorage
import services.operator.facade
import services.base.name_storage


class Simulation(services.operator.facade.Facade):
    """"""
    def __init__(self, path, name, service, iotype='git'):
        super(Simulation, self).__init__(service)
        self._ids = None
        self.service = service
        self.storage = services.base.name_storage.NameStorage(path, name, iotype=iotype)

    def add(self, bsobj, committer=None, unique=True,
            yamlfile=True, mdfile=False, do_commit=True):
        result = False
        if self.storage(bsobj, committer, unique, yamlfile, mdfile, do_commit):
            result = True
        return result

    def getyaml(self, id):
        """Simulation done by merging service and template data"""
        baseinfo = super(Simulation, self).getyaml(id)
        prjinfo = self.storage.getinfo(id)
        basetime = baseinfo['modifytime'] if 'modifytime' in baseinfo else 0
        prjtime = prjinfo['modifytime'] if 'modifytime' in prjinfo else 0
        prjinfo.update(baseinfo)
        prjinfo['modifytime'] = max(basetime, prjtime)
        return prjinfo

    def updateinfo(self, id, key, value, committer, do_commit=True):
        assert self.exists(id)
        return self.storage.updateinfo(id, key, value, committer, do_commit)

    def deleteinfo(self, id, key, value, committer, date, do_commit=True):
        assert self.exists(id)
        return self.storage.updateinfo(id, key, value, committer, date, do_commit)

    def saveinfo(self, id, info, message, committer, do_commit=True):
        result = self.storage.saveinfo(id, info, message, committer, do_commit)
        return result

    @property
    def ids(self):
        if self._ids is None:
            try:
                self._ids = set(self.storage.ids)
            except IOError:
                self._ids = set()
        return self._ids

    @property
    def NUMS(self):
        return len(self.ids)

    # TODO: check if at the right place (getmd)
    def dump(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        def writefile(filepath, stream):
            with open(filepath, 'w') as f:
                f.write(stream.encode('utf-8'))
        for i in self.ids:
            name = core.outputstorage.ConvertName(i)
            try:
                mdpath = os.path.join(path, name.md)
                mdstream = self.getmd(i)
                writefile(mdpath, mdstream)
            except IOError:
                pass
            writefile(htmlpath, htmlstream)
            yamlinfo = self.getyaml(i)
            utils.builtin.save_yaml(yamlinfo, path, name.yaml)
