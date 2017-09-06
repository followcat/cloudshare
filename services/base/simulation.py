import os
import time

import yaml
import ujson

import utils._yaml
import utils.builtin
import core.outputstorage
import services.memdatas
import services.base.storage


class Simulation(services.base.storage.BaseStorage):

    ids_file = 'names.json'

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = ()

    fix_item = {}
    list_item = {}

    @classmethod
    def autoservice(cls, path, name, storages, iotype='git'):
        if cls.check(path):
            return cls(path, name, storages, iotype=iotype)
        else:
            return cls.__bases__[1](path, name, iotype=iotype)

    @classmethod
    def check(cls, path):
        idsfile = os.path.join(path, Simulation.ids_file)
        return not os.path.exists(path) or (
            os.path.exists(path) and os.path.exists(idsfile))

    def __init__(self, path, name, storages, iotype='git'):
        super(Simulation, self).__init__(path, name, iotype=iotype)
        self._ids = None
        self.storages = storages
        self.yamlpath = self.YAML_DIR
        self.memdatas = services.memdatas.MemeryDatas(self)
        idsfile = os.path.join(path, Simulation.ids_file)
        if not os.path.exists(idsfile):
            dumpinfo = ujson.dumps(sorted(self.ids), indent=4)
            self.interface.add(self.ids_file, dumpinfo, message="Init ids file.")

    def saveids(self):
        self.interface.modify(self.ids_file, ujson.dumps(sorted(self.ids), indent=4))

    def exists(self, name):
        id = core.outputstorage.ConvertName(name).base
        return id in self.ids

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

    def _add(self, name):
        id = core.outputstorage.ConvertName(name).base
        self.ids.add(id)
        return True

    def _remove(self, name):
        id = core.outputstorage.ConvertName(name).base
        self.ids.remove(id)
        return True

    def _templateinfo(self, committer):
        info = self.generate_info_template()
        info['committer'] = committer
        info['modifytime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if 'date' not in info or not info['date']:
            info['date'] = time.time()
        return info

    def add(self, bsobj, committer=None, unique=True,
            yamlfile=True, mdfile=False, do_commit=True):
        result = False
        id = bsobj.ID
        if (unique and not self.exists(id)) or not unique:
            self._add(id)
            filenames = []
            filedatas = []
            filenames.append(bytes(self.ids_file))
            filedatas.append(ujson.dumps(sorted(self.ids), indent=4))
            if yamlfile is True:
                if not os.path.exists(os.path.join(self.path, self.yamlpath)):
                    os.makedirs(os.path.join(self.path, self.yamlpath))
                info = self._templateinfo(committer)
                name = core.outputstorage.ConvertName(id).yaml
                dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                                     allow_unicode=True, default_flow_style=False)
                filenames.append(bytes(os.path.join(self.yamlpath, name)))
                filedatas.append(dumpinfo)
            self.interface.add_files(filenames, filedatas,
                                     message='Add new data %s.'%id,
                                     committer=committer, do_commit=do_commit)
            self.memdatas.update('modifytime', id)
            result = True
        return result

    def getinfo(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        try:
            yamlstream = self.interface.get(os.path.join(self.yamlpath, name))
        except IOError:
            yamlstream = '{}'
        return yaml.load(yamlstream, Loader=utils._yaml.Loader)

    def getmd(self, id):
        md = None
        for storage in self.storages:
            try:
                md = storage.getmd(id)
                break
            except IOError:
                continue
        return md

    def getyaml(self, id):
        baseinfo = dict()
        for storage in self.storages:
            try:
                baseinfo = storage.getyaml(id)
                break
            except IOError:
                continue
        prjinfo = self.getinfo(id)
        basetime = baseinfo['modifytime'] if 'modifytime' in baseinfo else 0
        prjtime = prjinfo['modifytime'] if 'modifytime' in prjinfo else 0
        prjinfo.update(baseinfo)
        prjinfo['modifytime'] = max(basetime, prjtime)
        return prjinfo

    def updateinfo(self, id, key, value, committer, do_commit=True):
        assert key not in self.fix_item
        assert self.exists(id)
        projectinfo = self.getinfo(id)
        result = None
        if key in projectinfo:
            if key in self.list_item:
                result = self._addinfo(id, key, value, committer, do_commit=do_commit)
            else:
                result = self._modifyinfo(id, key, value, committer, do_commit=do_commit)
        return result

    def deleteinfo(self, id, key, value, committer, date, do_commit=True):
        assert key not in self.fix_item
        assert key in self.list_item
        assert self.exists(id)
        projectinfo = self.getinfo(id)
        result = None
        if key not in projectinfo:
            return result
        result = self._deleteinfo(id, key, value, date, committer, do_commit=do_commit)
        return result

    def saveinfo(self, id, info, message, committer, do_commit=True):
        result = super(Simulation, self).saveinfo(id, info, message, committer, do_commit)
        self.memdatas.update('modifytime', id)
        return result

    def search(self, keyword, selected=None):
        if selected is None:
            selected = [storage.name for storage in self.storages]
        results = set()
        allfile = set()
        for storage in self.storages:
            if isinstance(storage, Simulation):
                allfile.update(storage.search(keyword, selected=selected))
            elif storage.name in selected:
                allfile.update(storage.search(keyword))
        for result in allfile:
            id = core.outputstorage.ConvertName(result[0]).base
            if id in self.ids:
                results.add((id, result[1]))
        return results

    def search_yaml(self, keyword, selected=None):
        if selected is None:
            selected = [storage.name for storage in self.storages]
        results = set()
        allfile = set()
        for storage in self.storages:
            if isinstance(storage, Simulation):
                allfile.update(storage.search_yaml(keyword, selected=selected))
            elif storage.name in selected:
                allfile.update(storage.search_yaml(keyword))
        for result in allfile:
            id = core.outputstorage.ConvertName(result[0]).base
            if id in self.ids:
                results.add((id, result[1]))
        return results

    def search_key(self, key, value, ids=None):
        return self.memdatas.search_key(key, value, ids)

    def sorted_ids(self, key, ids=None, reverse=True):
        return self.memdatas.sorted_ids(key, ids=ids, reverse=reverse)

    @property
    def ids(self):
        if self._ids is None:
            try:
                stream = self.interface.get(self.ids_file)
                self._ids = set(ujson.loads(stream))
            except IOError:
                self._ids = set()
        return self._ids

    @property
    def NUMS(self):
        return len(self.ids)

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
