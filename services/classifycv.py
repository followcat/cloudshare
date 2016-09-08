import os

import utils.builtin
import core.outputstorage
import sources.industry_id


class ClassifyCV(object):

    INDUSTRY_DIR = "JOBTITLES"

    config_file = 'config.yaml'
    ids_file = 'names.yaml'

    def __init__(self, name, path, cvstorage, rawdb):
        self.name = name
        self.path = os.path.join(path, name)
        self.cvids = list()
        self.config = dict()
        self.cvstorage = cvstorage
        self.rawdb = rawdb
        try:
            self.load()
        except IOError:
            pass

    def setup(self, classify):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.config['classify'] = classify
        self.update()

    def load(self):
        self.config = utils.builtin.load_yaml(self.path, self.config_file)
        self.cvids = utils.builtin.load_yaml(self.path, self.ids_file)

    def update(self):
        in_id = sources.industry_id.industryID[self.config['classify']]
        for dbname in self.rawdb:
            raw_db = self.rawdb[dbname]
            urls_str = raw_db.get(os.path.join(self.INDUSTRY_DIR, in_id+'.yaml'))
            results = yaml.load(urls_str, Loader=utils._yaml.Loader)['datas']
            ids = [id for id in results]
            results = None
            for id in set(self.cvstorage.lsids())-
                         (set(ids) & set(raw_db.lsid_raw())):
                self._add(yamlname, name)
        utils.builtin.save_yaml(self.config, self.path, self.config_file)
        utils.builtin.save_yaml(self.cvids, self.path, self.ids_file)

    def exists(self, name):
        id = core.outputstorage.ConvertName(name)
        return id in self.cvids

    def _add(self, name, svccv_name):
        id = core.outputstorage.ConvertName(name).base
        self.cvids.append(id)

    def yamls(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).yaml

    def names(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).md

    def getmd(self, name):
        return self.cvstorage.getmd(name)

    def getyaml(self, name):
        return self.cvstorage.getyaml(name)

    def gethtml(self, name):
        return self.cvstorage.gethtml(name)

    def datas(self):
        for id in self.cvids:
            text = self.cvstorage.getmd(id)
            yield id, text

    @property
    def NUMS(self):
        return len(self.cvids)
