import os
import time
import yaml

import utils._yaml
import core.outputstorage
import services.base.storage


class KeyValueStorage(services.base.storage.BaseStorage):

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = ()

    fix_item = {}
    list_item = {}

    def __init__(self, path, name=None, searchengine=None, iotype=None):
        super(KeyValueStorage, self).__init__(path, name, searchengine, iotype=iotype)
        self.yamlpath = self.YAML_DIR

    def _listframe(self, value, username, date=None):
        if date is None:
            date = time.strftime('%Y-%m-%d %H:%M:%S')
        data = {'author': username,
                'content': value,
                'date': date}
        return data

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

    def getinfo(self, id):
        info = self.generate_info_template()
        info.update(self.getyaml(id))
        return info

    def _modifyinfo(self, id, key, value, committer, do_commit=True):
        result = {}
        projectinfo = self.getinfo(id)
        if not projectinfo[key] == value:
            projectinfo[key] = value
            self.saveinfo(id, projectinfo,
                          'Modify %s key %s.' % (id, key), committer, do_commit=do_commit)
            result = {key: value}
        return result

    def _addinfo(self, id, key, value, committer, do_commit=True):
        projectinfo = self.getinfo(id)
        data = self._listframe(value, committer)
        projectinfo[key].insert(0, data)
        self.saveinfo(id, projectinfo,
                      'Add %s key %s.' % (id, key), committer, do_commit=do_commit)
        return data

    def _deleteinfo(self, id, key, value, date, committer, do_commit=True):
        projectinfo = self.getinfo(id)
        data = self._listframe(value, committer, date)
        if data in projectinfo[key]:
            projectinfo[key].remove(data)
            self.saveinfo(id, projectinfo,
                          'Delete %s key %s.' % (id, key), committer, do_commit=do_commit)
            return data

    def updateinfo(self, id, key, value, committer, do_commit=True):
        result = None
        if key in [each[0] for each in self.YAML_TEMPLATE]:
            result = self._modifyinfo(id, key, value, committer, do_commit=do_commit)
        return result

    def saveinfo(self, id, info, message, committer, do_commit=True):
        result = False
        baseinfo = self.getinfo(id)
        if not self.generate_info_template():
            keys = baseinfo.keys()+info.keys()
        else:
            keys = self.generate_info_template().keys()
        saveinfo = dict(filter(lambda k: k[0] in keys, info.items()))
        if baseinfo != saveinfo:
            name = core.outputstorage.ConvertName(id).yaml
            saveinfo['modifytime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            dumpinfo = yaml.dump(saveinfo, Dumper=utils._yaml.SafeDumper,
                                 allow_unicode=True, default_flow_style=False)
            self.interface.modify(os.path.join(self.yamlpath, name), dumpinfo,
                                  message=message, committer=committer, do_commit=do_commit)
            result = True
        if result:
            for k in keys:
                try:
                    del info[k]
                except KeyError:
                    continue
        return result

    def add(self, bsobj, committer=None, unique=True, kv_file=True, text_file=False, do_commit=True):
        if unique is True and self.unique(bsobj) is False:
            self.info = "Exists File"
            return False
        name = core.outputstorage.ConvertName(bsobj.name)
        if kv_file is True:
            if committer is not None:
                bsobj.metadata['committer'] = committer
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            return self.saveinfo(name, bsobj.metadata,
                            message, committer, do_commit)
        return True

    def getyaml(self, id):
        """
        Expects an IOError exception if file not found.
            >>> import services.base.kv_storage
            >>> DIR = 'services/test_repo'
            >>> SVC_BSSTO = services.base.kv_storage.KeyValueStorage(DIR)
            >>> SVC_BSSTO.getyaml('CV') # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            IOError...
        """
        name = core.outputstorage.ConvertName(id).yaml
        yaml_str = self.interface.get(name)
        return yaml.load(yaml_str, Loader=utils._yaml.SafeLoader)

    def search_yaml(self, keyword, selected=None):
        results = set()
        if selected and self.name in selected:
            allfile = self.interface.search_yaml(keyword)
            for result in allfile:
                id = core.outputstorage.ConvertName(result[0]).base
                results.add((id, result[1]))
        return results

    @property
    def ids(self):
        """
            >>> import services.base.kv_storage
            >>> DIR = 'repo/CV'
            >>> SVC_BSSTO = services.base.kv_storage.KeyValueStorage(DIR)
            >>> assert SVC_BSSTO.interface.lsfiles('.', 'blr6dter.yaml')
        """
        return set([os.path.splitext(f)[0]
                    for f in self.interface.lsfiles('.', '*.yaml')])

