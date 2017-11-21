import time
import yaml
import os.path

import core.outputstorage
import services.base.storage


def yaml_to_doc(d):
    output = ''
    xp = ''
    #for k in ['company', 'school', 'education']:
    #    output += k + ' ' + d[k] + '\n'
    k = 'experience'
    for x in d[k]:
        xp += x[-1] + '\n'
    return output + k + '\n' + xp


class CandidateSummary(services.base.storage.BaseStorage):

    path = 'CV'

    def __init__(self, interface, name=None):
        super(CandidateSummary, self).__init__(interface, name)
        self.repo_path = self.interface.path + "/" + self.path
        self.info = ""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    def exists(self, filename):
        # FIXME check that filename is in interface yaml list
        return True

    def add(self, cvobj, committer=None):
        raise NotImplementedError

    def add_md(self, cvobj, committer=None):
        raise NotImplementedError

    def modify(self, filename, stream, message=None, committer=None):
        raise NotImplementedError

    def yamls(self):
        yamls = self.interface.lsfiles(self.path, '*.yaml')
        for each in yamls:
            yield os.path.split(each)[-1]

    def names(self):
        for each in self.yamls():
            yield each

    def datas(self):
        for name in self.names():
            text = self.getmd(name)
            yield name, text

    def search(self, keyword):
        results = self.interface.search(keyword, self.path)
        return results

    def search_yaml(self, keyword):
        results = self.interface.search_yaml(keyword, self.path)
        return results

    def getmd(self, name):
        return yaml_to_doc(self.getyaml(name))

    def getyaml(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        path_name = os.path.join(self.path, name)
        yaml_str = self.interface.get(path_name)
        if yaml_str is None:
            raise IOError
        return yaml.load(yaml_str)


