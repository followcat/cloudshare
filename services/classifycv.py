import os

import utils.builtin
import sources.industry_id
import services.simulationcv


class ClassifyCV(services.simulationcv.SimulationCV):

    config_file = 'config.yaml'

    def __init__(self, name, path, cvstorage):
        classifypath = utils.builtin.industrytopath(name)
        super(ClassifyCV, self).__init__(classifypath, path, cvstorage)
        self.name = name

    def setup(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.config['classify'] = self.name
            self.update()

    def update(self):
        for y in self.cvstorage.yamls():
            if not self.exists(y):
                info = SVC_CV_REPO.getyaml(y)
                if self.name in info['classify']:
                    self._add(y)
        self.save()

    def load(self):
        self.config = utils.builtin.load_yaml(self.path, self.config_file)
        self.cvids = set(utils.builtin.load_json(self.path, self.ids_file))

    def save(self):
        utils.builtin.save_yaml(self.config, self.path, self.config_file)
        utils.builtin.save_json(self.cvids, self.path, self.ids_file)
