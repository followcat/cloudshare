import services.base.simulation
import services.curriculumvitae

import utils.pandocconverter
import extractor.information_explorer


class SimulationCV(services.base.simulation.Simulation,
                   services.curriculumvitae.CurriculumVitae):

    YAML_TEMPLATE = (
        ("committer",           str),
    )

    yaml_private_key = {
        "secrecy":              True,
        "phone":                '[*****]',
        "email":                '[*****]',
        "name":                 '[*****]',
        "committer":            '[*****]',
        "origin":               '[*****]'
    }

    list_item = {}

    def __init__(self, path, name, storages, iotype='git'):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> config.init_samplecv()
            >>> SVC_PRJ_TEST = config.SVC_PRJ_TEST
            >>> id = list(SVC_PRJ_TEST.cv_ids())[0]
            >>> SVC_PRJ_TEST.curriculumvitae.updateinfo(id, 'committer', 'dev', 'dev')
            {'committer': 'dev'}
            >>> config.destory()
        """
        super(SimulationCV, self).__init__(path, name, storages, iotype=iotype)

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        html = None
        for storage in self.storages:
            try:
                html = storage.gethtml(veren)
                break
            except IOError:
                continue
        return html

    def gethtml(self, id):
        result = None
        for storage in self.storages:
            try:
                result = storage.gethtml(id)
                break
            except IOError:
                continue
        return result

    def getuniqueid(self, id):
        result = None
        for storage in self.storages:
            try:
                result = storage.getuniqueid(id)
                break
            except IOError:
                continue
        return result

    def getmd(self, id):
        result = super(SimulationCV, self).getmd(id)
        return result

    def getyaml(self, id):
        result = super(SimulationCV, self).getyaml(id)
        return result

