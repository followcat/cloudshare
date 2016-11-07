import os

import utils.builtin
import core.basedata
import services.simulationcv


class ClassifyCV(object):

    config_file = 'config.yaml'

    def __init__(self, name, path, cvstorage):
        self.name = name
        self.path = os.path.join(path, utils.builtin.industrytopath(name))
        self.curriculumvitae = services.simulationcv.SimulationCV(self.path, name, cvstorage)
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        self.config = utils.builtin.load_yaml(self.path, self.config_file)

    def save(self):
        utils.builtin.save_yaml(self.config, self.path, self.config_file,
                                default_flow_style=False)

    def setup(self, update=True):
        if not os.path.exists(os.path.join(self.path, self.config_file)):
            self.config['classify'] = self.name
            self.save()
            if update:
                self.update()

    def update(self):
        for y in self.cvstorage.yamls():
            if not self.exists(y):
                data = self.cvstorage.getmd(y)
                matedata = self.cvstorage.getyaml(y)
                if self.name in info['classify']:
                    dataobj = core.basedata.DataObject(name, data, matedata)
                    self.add(dataobj, yamlfile=False)

    def add(self, dataobj, committer=None, unique=True, yamlfile=True):
        return self.curriculumvitae.add(dataobj, committer, unique, yamlfile)

    def exists(self, id):
        return self.curriculumvitae.exists(id)

    def yamls(self):
        return self.curriculumvitae.yamls()

    def names(self):
        return self.curriculumvitae.names()

    def datas(self):
        return self.curriculumvitae.datas()

    def getmd(self, id):
        return self.curriculumvitae.getmd(id)

    def getyaml(self, id):
        return self.curriculumvitae.getyaml(id)

    def gethtml(self, id):
        return self.curriculumvitae.gethtml(id)

    @property
    def NUMS(self):
        return self.curriculumvitae.NUMS

