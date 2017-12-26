import os
import time
import yaml

import utils._yaml
import core.basedata
import core.outputstorage
import services.base.storage


class KeyValueStorage(services.base.storage.BaseStorage):
    """ Backward compatible definition of kv storage service.
    """

    YAML_DIR = '.'
    YAML_TEMPLATE = ()

    fix_item = {}
    MUST_KEYS = []

    yaml_private_key = {}

    def __init__(self, path, name=None, iotype=None):
        self.yamlpath = self.YAML_DIR
        super(KeyValueStorage, self).__init__(os.path.join(path, self.yamlpath), name, iotype=iotype)

    @property
    def list_item(self):
        return set([k for k,v in filter(lambda x: x[1] is list, self.YAML_TEMPLATE)])

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

    def private_keys(self):
        return self.yaml_private_key

    def getinfo(self, id):
        info = self.generate_info_template()
        try:
            info.update(self.getyaml(id))
        except IOError:
            pass
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
        assert key not in self.fix_item
        result = None
        if key in [each[0] for each in self.YAML_TEMPLATE]:
            if key in self.list_item:
                result = self._addinfo(id, key, value, relation,
                                       committer, do_commit=do_commit)
            else:
                result = self._modifyinfo(id, key, value, committer, do_commit=do_commit)
        return result

    def deleteinfo(self, id, msgid, committer, do_commit=True):
        result = self._deleteinfo(id, msgid, committer, do_commit=do_commit)
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
            result = self.interface.modify(name, dumpinfo,
                                  message=message, committer=committer, do_commit=do_commit)
        return result

    def add(self, bsobj, committer=None, unique=True, kv_file=True, text_file=False, do_commit=True):
        result = False
        if unique is True and self.unique(bsobj) is False:
            self.info = "Exists File"
            return False
        name = core.outputstorage.ConvertName(bsobj.name)
        if kv_file is True:
            assert set(self.MUST_KEY).issubset(set(bsobj.metadata.keys()))
            if committer is not None:
                bsobj.metadata['committer'] = committer
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            name = core.outputstorage.ConvertName(bsobj.name).yaml
            saveinfo = {'modifytime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
            saveinfo.update(bsobj.metadata)
            dumpinfo = yaml.dump(saveinfo, Dumper=utils._yaml.SafeDumper,
                                 allow_unicode=True, default_flow_style=False)
            result = self.interface.add(name, dumpinfo,
                            message, committer, do_commit=do_commit)
        return result

    def modify(self, bsobj, committer=None, unique=True, kv_file=True, text_file=False, do_commit=True):
        result = False
        name = core.outputstorage.ConvertName(bsobj.name)
        info = self.getinfo(name)
        if kv_file is True:
            assert set(self.MUST_KEY).issubset(set(bsobj.metadata.keys()))
            for key in self.generate_info_template():
                if key in self.list_item:
                    try:
                        if not bsobj.metadata[key]:
                            continue
                        elif isinstance(bsobj.metadata[key], (list, set, tuple, dict)):
                            info[key].extend(bsobj.metadata[key])
                        else:
                            info[key].append(bsobj.metadata[key])
                    except KeyError:
                        pass
                else:
                    try:
                        info[key] = bsobj.metadata[key]
                    except KeyError:
                        pass
            if committer is not None:
                info['committer'] = committer
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            saveinfo = {'modifytime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
            saveinfo.update(info)
            dumpinfo = yaml.dump(saveinfo, Dumper=utils._yaml.SafeDumper,
                                 allow_unicode=True, default_flow_style=False)
            result = self.interface.modify(name.yaml, dumpinfo,
                            message, committer, do_commit=do_commit)
        return result

    def remove(self, id, committer=None, do_commit=True):
        name = core.outputstorage.ConvertName(id).yaml
        return self.interface.delete(name, message='Remove user %s'%id,
                              committer=committer, do_commit=do_commit)

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

    getkv = getyaml

    def datas(self):
        for id in self.ids:
            yield id, self.getkv(id)

    @property
    def ids(self):
        """
            >>> import services.base.kv_storage
            >>> DIR = 'repo/CV'
            >>> SVC_BSSTO = services.base.kv_storage.KeyValueStorage(DIR)
            >>> assert SVC_BSSTO.interface.lsfiles('.', 'blr6dter.yaml')
        """
        if not hasattr(self, '_ids'):
            self._ids = set([os.path.splitext(f)[0]
                        for f in self.interface.lsfiles('.', '*.yaml')])
        return self._ids

