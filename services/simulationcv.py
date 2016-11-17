import os
import time
import yaml
import ujson

import utils._yaml
import utils.issue
import utils.builtin
import interface.basefs
import core.outputstorage
import services.curriculumvitae


class SimulationCV(services.curriculumvitae.CurriculumVitae):

    ids_file = 'names.json'

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = (
        ("committer",           list),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    def __init__(self, path, name, cvstorage):
        super(SimulationCV, self).__init__(path, name)
        self._ids = None
        self.cvstorage = cvstorage
        self.yamlpath = self.YAML_DIR

    def add(self, cvobj, committer=None, unique=True, yamlfile=False):
        result = False
        id = cvobj.ID
        if (unique and not self.exists(id)) or not unique:
            self._add(id)
            filenames = []
            filedatas = []
            filenames.append(bytes(self.ids_file))
            filedatas.append(ujson.dumps(sorted(self.ids), indent=4))
            if yamlfile is True:
                if not os.path.exists(os.path.join(self.path, self.yamlpath)):
                    os.makedirs(os.path.join(self.path, self.yamlpath))
                info = self.generate_info_template()
                info['committer'] = committer
                name = core.outputstorage.ConvertName(id).yaml
                dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                                     allow_unicode=True, default_flow_style=False)
                filenames.append(bytes(os.path.join(self.yamlpath, name)))
                filedatas.append(dumpinfo)
            self.interface.add_files(filenames, filedatas,
                                     message='Add new cv %s.'%id,
                                     committer=committer)
            self.interface.modify(self.ids_file, ujson.dumps(sorted(self.ids), indent=4))
            result = True
        return result

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

    def _add(self, name):
        id = core.outputstorage.ConvertName(name).base
        self.ids.add(id)

    def search(self, keyword):
        results = set()
        allfile = self.cvstorage.search(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            if id in self.ids:
                results.add(id)
        return results

    def search_yaml(self, keyword):
        results = set()
        allfile = self.interface.grep(keyword, self.YAML_DIR)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def getmd(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.getmd(name)

    def getinfo(self, id):
        if not self.exists(id):
            return None
        name = core.outputstorage.ConvertName(id).yaml
        try:
            yamlstream = self.interface.get(os.path.join(self.yamlpath, name))
        except IOError:
            yamlstream = '{}'
        return yaml.load(yamlstream, Loader=utils._yaml.Loader)

    def getyaml(self, id):
        if not self.exists(id):
            return None
        yaml = self.cvstorage.getyaml(id)
        if yaml is not None:
            info = self.getinfo(id)
            yaml.update(info)
        return yaml

    def gethtml(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.gethtml(name)

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

    def saveinfo(self, id, info, message, committer):
        name = core.outputstorage.ConvertName(id).yaml
        dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                             allow_unicode=True, default_flow_style=False)
        self.interface.modify(os.path.join(self.yamlpath, name), dumpinfo,
                              message=message, committer=committer)

    def dump(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        def storage(filepath, stream):
            with open(filepath, 'w') as f:
                f.write(stream.encode('utf-8'))
        for i in self.ids:
            name = core.outputstorage.ConvertName(i)
            mdpath = os.path.join(path, name.md)
            mdstream = self.cvstorage.getmd(i)
            storage(mdpath, mdstream)
            htmlpath = os.path.join(path, name.html)
            htmlstream = self.cvstorage.gethtml(i)
            storage(htmlpath, htmlstream)
            yamlinfo = self.cvstorage.getyaml(i)
            utils.builtin.save_yaml(yamlinfo, path, name.yaml)
