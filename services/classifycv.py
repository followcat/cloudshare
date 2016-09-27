import os
import yaml

import utils._yaml
import sources.industry_id
import services.simulationcv


class ClassifyCV(services.simulationcv.SimulationCV):

    INDUSTRY_DIR = "JOBTITLES"

    def __init__(self, name, path, cvstorage, rawdb):
        super(ClassifyCV, self).__init__(name, path, cvstorage)
        self.rawdb = rawdb

    def setup(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.config['classify'] = self.name
        self.update()

    def update(self):
        in_id = sources.industry_id.industryID[self.config['classify']]
        for dbname in self.rawdb:
            raw_db = self.rawdb[dbname]
            urls_str = raw_db.get(os.path.join(self.INDUSTRY_DIR, in_id+'.yaml'))
            if urls_str is None:
                continue
            results = yaml.load(urls_str, Loader=utils._yaml.Loader)['datas']
            ids = [id for id in results]
            results = None
            for id in (set(ids) & set(raw_db.lsid_raw()) & set(self.cvstorage.lsids())):
                if not self.exists(id):
                    self._add(id)
        self.save()
