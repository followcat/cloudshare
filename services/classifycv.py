import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.simulationcv


class ClassifyCV(services.simulationcv.SimulationCV):

    config_file = 'config.yaml'

    def __init__(self, name, path, cvstorage):
        classifypath = utils.builtin.industrytopath(name)
        super(ClassifyCV, self).__init__(name, os.path.join(path, classifypath), cvstorage)
        self.config = dict()

    def load(self):
        self.config = utils.builtin.load_yaml(self.path, self.config_file)
        super(ClassifyCV, self).load()

    def save(self):
        utils.builtin.save_yaml(self.config, self.path, self.config_file,
                                default_flow_style=False)
        super(ClassifyCV, self).save()

    def setup(self, update=True):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.config['classify'] = self.name
            if update:
                self.update()

    def update(self):
        for y in self.cvstorage.yamls():
            if not self.exists(y):
                info = self.cvstorage.getyaml(y)
                if self.name in info['classify']:
                    self._add(y)
        self.save()

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
