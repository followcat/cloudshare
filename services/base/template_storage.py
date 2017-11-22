import os
import time
import yaml

import utils.issue
import utils._yaml
import core.outputstorage
import services.base.storage


class TemplateStorage(services.base.storage.BaseStorage):
    """Manage data based on template

    The data is stored as yaml is a mechanism that is independent
    from BaseStorage.
    """

    commitinfo = 'TemplateStorage'
    YAML_TEMPLATE = ()

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

    def _listframe(self, value, username, date=None):
        if date is None:
            date = time.strftime('%Y-%m-%d %H:%M:%S')
        data = {'author': username,
                'content': value,
                'date': date}
        return data

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

    @utils.issue.fix_issue('issues/update_name.rst')
    def updateinfo(self, id, key, value, committer, do_commit=True):
        result = None
        if key in key in [each[0] for each in self.YAML_TEMPLATE]:
            result = self._modifyinfo(id, key, value, committer, do_commit=do_commit)
        return result

    def saveinfo(self, id, info, message, committer, do_commit=True):
        result = False
        baseinfo = self.getinfo(id)
        saveinfo = dict(filter(lambda k: k[0] in baseinfo.keys()+
                                                 self.generate_info_template().keys(),
                                                 info.items()))
        if baseinfo != saveinfo:
            name = core.outputstorage.ConvertName(id).yaml
            saveinfo['modifytime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            dumpinfo = yaml.dump(saveinfo, Dumper=utils._yaml.SafeDumper,
                                 allow_unicode=True, default_flow_style=False)
            self.interface.modify(os.path.join(self.yamlpath, name), dumpinfo,
                                  message=message, committer=committer, do_commit=do_commit)
            result = True
        return result

    def getinfo(self, id):
        info = self.generate_info_template()
        info.update(self.getyaml(id))
        return info

