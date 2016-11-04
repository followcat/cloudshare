import os
import time
import yaml
import ujson

import utils._yaml
import utils.issue
import utils.builtin
import services.base
import interface.basefs
import core.outputstorage


class SimulationCV(services.base.Service):

    ids_file = 'names.json'

    SAVE_DIR = 'CV'
    YAML_DIR = 'YAML'
    YAML_TEMPLATE = (
        ("committer",           list),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    def __init__(self, path, name, cvstorage, storage=None):
        self.path = os.path.join(path, self.SAVE_DIR)
        super(SimulationCV, self).__init__(self.path, name)
        self.cvids = set()
        self.cvstorage = cvstorage
        self.yamlpath = os.path.join(self.path, self.YAML_DIR)
        if storage is not None:
            self.interface = storage
            self.path = os.path.join(self.interface.path, self.SAVE_DIR)
            self.yamlpath = os.path.join(self.SAVE_DIR, self.YAML_DIR)
            self.ids_file = os.path.join(self.SAVE_DIR, self.ids_file)
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        stream = self.interface.get(self.ids_file)
        self.cvids = ujson.loads(stream)

    def save(self):
        stream = ujson.dumps(sorted(self.cvids), indent=4)
        self.interface.add(self.ids_file, stream)

    def add(self, cvobj, committer=None, unique=True, yamlfile=False):
        result = False
        id = cvobj.ID
        if (unique and not self.exists(id)) or not unique:
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
                filenames.append(bytes(os.path.join(self.yamlpath, name)))
                filedatas.append(dumpinfo)
            self.interface.add_files(filenames, filedatas,
                                     message='Add new cv %s.'%id,
                                     committer=committer)
            self.interface.modify(self.ids_file, ujson.dumps(sorted(self.cvids), indent=4))
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

    def search(self, keyword):
        results = set()
        allfile = self.cvstorage.search(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            if id in self.cvids:
                results.add(id)
        return results

    def search_yaml(self, keyword):
        results = set()
        allfile = self.interface.grep(keyword, self.SAVE_DIR)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def yamls(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).yaml

    def names(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).md

    def history(self, author=None, entries=10, skip=0):
        return self.interface.history(author=author, max_commits=entries, skip=skip)

    def getmd(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.getmd(name)

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        return self.cvstorage.gethtml(veren)

    def getinfo(self, id):
        if not self.exists(id):
            return None
        name = core.outputstorage.ConvertName(id).yaml
        yamlstream = self.interface.get(os.path.join(self.yamlpath, name))
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
        self.interface.modify(os.path.join(self.yamlpath, name), dumpinfo,
                              message=message, committer=committer)

    def dump(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        def storage(filepath, stream):
            with open(filepath, 'w') as f:
                f.write(stream.encode('utf-8'))
        for i in self.cvids:
            name = core.outputstorage.ConvertName(i)
            mdpath = os.path.join(path, name.md)
            mdstream = self.cvstorage.getmd(i)
            storage(mdpath, mdstream)
            htmlpath = os.path.join(path, name.html)
            htmlstream = self.cvstorage.gethtml(i)
            storage(htmlpath, htmlstream)
            yamlinfo = self.cvstorage.getyaml(i)
            utils.builtin.save_yaml(yamlinfo, path, name.yaml)
