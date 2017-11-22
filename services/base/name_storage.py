import os
import time

import yaml
import ujson

import utils._yaml
import core.outputstorage
import services.base.template_storage


class NameStorage(services.base.template_storage.TemplateStorage):
    """Manage cached id list and simulation data

    The id cache is stored as json in $ids_file.

    The simulation data is stored as yaml reusing TemplateStorage
    mechanism. The BaseStorage mechanism is not supported by this
    anymore (no storage of md file).
    """

    ids_file = 'names.json'

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = ()

    fix_item = {}
    list_item = {}

    def __init__(self, path, name, iotype='git'):
        super(NameStorage, self).__init__(path, name, iotype=iotype)
        self.yamlpath = self.YAML_DIR
        idsfile = os.path.join(path, NameStorage.ids_file)
        if not os.path.exists(idsfile):
            dumpinfo = ujson.dumps(sorted(self.ids), indent=4)
            self.interface.add(self.ids_file, dumpinfo, message="Init ids file.")

    @property
    def ids(self):
        try:
            return ujson.loads(self.interface.get(self.ids_file))
        except IOError:
            return []

    def saveids(self):
        self.interface.modify(self.ids_file, ujson.dumps(sorted(self.ids), indent=4))

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

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
        if (unique and self.unique(bsobj)) or not unique:
            id = bsobj.ID
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
            result = True
        return result

    def getinfo(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        try:
            yamlstream = self.interface.get(os.path.join(self.yamlpath, name))
        except IOError:
            yamlstream = '{}'
        return yaml.load(yamlstream, Loader=utils._yaml.Loader)

    def updateinfo(self, id, key, value, committer, do_commit=True):
        assert key not in self.fix_item
        result = None
        if key in [each[0] for each in self.YAML_TEMPLATE]:
            if key in self.list_item:
                result = self._addinfo(id, key, value, committer, do_commit=do_commit)
            else:
                result = self._modifyinfo(id, key, value, committer, do_commit=do_commit)
        return result

    def deleteinfo(self, id, key, value, committer, date, do_commit=True):
        assert key not in self.fix_item
        assert key in self.list_item
        projectinfo = self.getinfo(id)
        result = None
        if key not in projectinfo:
            return result
        result = self._deleteinfo(id, key, value, date, committer, do_commit=do_commit)
        return result

