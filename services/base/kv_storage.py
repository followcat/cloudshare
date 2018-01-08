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
    MUST_KEY = []

    yaml_private_key = {}

    def __init__(self, path, name=None, iotype=None):
        self.yamlpath = self.YAML_DIR
        super(KeyValueStorage, self).__init__(os.path.join(path, self.yamlpath), name, iotype=iotype)

    @property
    def list_item(self):
        return set([k for k,v in filter(lambda x: x[1] is list, self.YAML_TEMPLATE)])

    def build_frame(self, **kwargs):
        return kwargs

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

    def merge_info(self, info, bsobj):
        for key in self.generate_info_template():
            if key in self.fix_item and info[key]:
                try:
                    assert info[key] == bsobj.metadata[key], 'Attempt at changing %s fixed key' %(key)
                except KeyError:
                    continue
            if key in self.list_item:
                try:
                    if not bsobj.metadata[key]:
                        continue
                    elif isinstance(bsobj.metadata[key], (list, set, tuple)):
                        if isinstance(info[key], set):
                            info[key].update(bsobj.metadata[key])
                        else:
                            info[key].extend(bsobj.metadata[key])
                    elif isinstance(bsobj.metadata[key], dict):
                        data = self.build_frame(**bsobj.metadata[key])
                        if data not in info[key]:
                            info[key].insert(0, data)
                    else:
                        if isinstance(info[key], set):
                            info[key].add(bsobj.metadata[key])
                        else:
                            info[key].append(bsobj.metadata[key])
                except KeyError:
                    pass
            else:
                try:
                    info[key] = bsobj.metadata[key]
                except KeyError:
                    pass


    def save_info(self, info, bsobj):
        assert set(self.MUST_KEY).issubset(set(bsobj.metadata.keys()))
        for key in self.generate_info_template():
            if key in self.fix_item and info[key]:
                try:
                    assert info[key] == bsobj.metadata[key], 'Attempt at changing %s fixed key' %(key)
                except KeyError:
                    continue
            try:
                info[key] = bsobj.metadata[key]
            except KeyError:
                pass

    def add(self, bsobj, committer=None, unique=True, kv_file=True, text_file=False, do_commit=True):
        assert set(self.MUST_KEY).issubset(set(bsobj.metadata.keys()))
        result = False
        if unique is True and self.unique(bsobj) is False:
            self.info = "Exists File"
            return False
        if kv_file is True:
            if committer is not None:
                bsobj.metadata['committer'] = committer
            name = core.outputstorage.ConvertName(bsobj.name)
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            info = self.generate_info_template()
            info.update({'modifytime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
            self.merge_info(info, bsobj)
            dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                                 allow_unicode=True, default_flow_style=False)
            result = self.interface.add(name.yaml, dumpinfo,
                            message, committer, do_commit=do_commit)
            if result:
                super(KeyValueStorage, self)._add(bsobj.ID)
        return result

    def modify(self, bsobj, committer=None, unique=True, kv_file=True, text_file=False, do_commit=True):
        result = False
        if kv_file is True:
            if committer is not None:
                bsobj.metadata['committer'] = committer
            name = core.outputstorage.ConvertName(bsobj.name)
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            info = self.getinfo(name)
            info.update({'modifytime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
            self.merge_info(info, bsobj)
            dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                                 allow_unicode=True, default_flow_style=False)
            result = self.interface.modify(name.yaml, dumpinfo,
                            message, committer, do_commit=do_commit)
        return result

    def save(self, bsobj, committer=None, unique=True, kv_file=True, text_file=False, do_commit=True):
        result = False
        if kv_file is True:
            if committer is not None:
                bsobj.metadata['committer'] = committer
            name = core.outputstorage.ConvertName(bsobj.name)
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            info = self.getinfo(name)
            info.update({'modifytime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
            self.save_info(info, bsobj)
            dumpinfo = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
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

