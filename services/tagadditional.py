import os

import core.basedata
import services.simulationcv


class TagsCurriculumVitae(services.simulationcv.SimulationCV):

    def setup(self, selected):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.config['selected'] = selected
        self.update()

    def update(self):
        for id in self.cvstorage.ids:
            if not self.exists(id):
                data = self.cvstorage.getyaml(id)
                metadata = self.cvstorage.getyaml(id)
                key = self.config['selected']['key']
                values_set = self.config['selected']['value']
                if key in yamlinfo:
                    keyset = set()
                    for each in yamlinfo[key].values():
                        keyset.update(each)
                    if keyset.intersection(values_set):
                        dataobj = core.basedata.DataObject(metadata, data)
                        self.add(dataobj)
        self.save()
