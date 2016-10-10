import os

import services.simulationcv


class TagsCurriculumVitae(services.simulationcv.SimulationCV):

    def setup(self, selected):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.config['selected'] = selected
        self.update()

    def update(self):
        for yamlname in self.cvstorage.yamls():
            if not self.exists(yamlname):
                yamlinfo = self.cvstorage.getyaml(yamlname)
                key = self.config['selected']['key']
                values_set = self.config['selected']['value']
                if key in yamlinfo:
                    keyset = set()
                    for each in yamlinfo[key].values():
                        keyset.update(each)
                    if keyset.intersection(values_set):
                        self._add(yamlname, name)
        self.save()
