import os
import time
import yaml
import ujson

import utils._yaml
import utils.issue
import utils.builtin
import interface.basefs
import core.outputstorage


class SimulationCV(object):

    ids_file = 'names.json'

    YAML_DIR = 'CV'
    YAML_TEMPLATE = (
        ("committer",           list),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    def __init__(self, path, cvstorage, storage=None):
        self.path = path
        self.cvids = set()
        self.cvstorage = cvstorage
        if storage is None:
            storage = interface.basefs.BaseFSInterface(path)
        self.interface = storage
        self.cvpath = self.YAML_DIR
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        self.cvids = set(utils.builtin.load_json(self.path, self.ids_file))

    def save(self):
        utils.builtin.save_json(sorted(self.cvids), self.path, self.ids_file,
                                indent=4)

    def add(self, id, committer, yamlfile=False):
        result = False
        if not self.exists(id):
            self._add(id)
            filenames = []
            filedatas = []
            filenames.append(bytes(self.ids_file))
            filedatas.append(ujson.dumps(sorted(self.cvids), indent=4))
            if yamlfile is True:
                info = self.generate_info_template()
                info['committer'] = committer
                name = core.outputstorage.ConvertName(id).yaml
                dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                                     allow_unicode=True, default_flow_style=False)
                filenames.append(bytes(os.path.join(self.cvpath, name)))
                filedatas.append(dumpinfo)
            self.interface.add_files(filenames, filedatas,
                                     message='Add new cv %s.'%id,
                                     committer=committer)
            utils.builtin.save_json(sorted(self.cvids), self.path, self.ids_file,
                                    indent=4)
            result = True
        return result

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

    def exists(self, name):
        id = core.outputstorage.ConvertName(name).base
        return id in self.cvids

    def _add(self, name):
        id = core.outputstorage.ConvertName(name).base
        self.cvids.add(id)

    def yamls(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).yaml

    def names(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).md

    def getmd(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.getmd(name)

    def getinfo(self, id):
        if not self.exists(id):
            return None
        name = core.outputstorage.ConvertName(id).yaml
        yamlstream = self.interface.get(os.path.join(self.cvpath, name))
        if yamlstream is None:
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

    def datas(self):
        for name in self.names():
            text = self.cvstorage.getmd(name)
            yield name, text

    @property
    def NUMS(self):
        return len(self.cvids)

    @utils.issue.fix_issue('issues/update_name.rst')
    def updateinfo(self, id, key, value, committer):
        data = None
        projectinfo = self.getinfo(id)
        baseinfo = self.getyaml(id)
        if projectinfo is not None and (key in projectinfo or key in baseinfo):
            data = { key: value }
            if key == 'tag':
                data = self.addtag(id, value, committer)
            elif key == 'tracking':
                data = self.addtracking(id, value, committer)
            elif key == 'comment':
                data = self.addcomment(id, value, committer)
            else:
                projectinfo[key] = value
                self.saveinfo(id, projectinfo,
                              'Update %s key %s.' % (id, key), committer)
        return data

    def _infoframe(self, value, username):
        data = {'author': username,
                'content': value,
                'date': time.strftime('%Y-%m-%d %H:%M:%S')}
        return data

    def addtag(self, id, tag, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(tag, committer)
        info['tag'].insert(0, data)
        self.saveinfo(id, info, 'Add %s tag.'%id, committer)
        return data

    def addcomment(self, id, comment, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(comment, committer)
        info['comment'].insert(0, data)
        self.saveinfo(id, info, 'Add %s comment.'%id, committer)
        return data

    def addtracking(self, id, tracking, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(tracking, committer)
        info['tracking'].insert(0, data)
        self.saveinfo(id, info, 'Add %s tracking.'%id, committer)
        return data

    def saveinfo(self, id, info, message, committer):
        name = core.outputstorage.ConvertName(id).yaml
        dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                             allow_unicode=True, default_flow_style=False)
        self.interface.modify(os.path.join(self.cvpath, name), dumpinfo,
                              message=message, committer=committer)
