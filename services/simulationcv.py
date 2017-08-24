import services.base.simulation
import services.curriculumvitae


class SimulationCV(services.base.simulation.Simulation,
                   services.curriculumvitae.CurriculumVitae):

    YAML_TEMPLATE = (
        ("committer",           str),
    )

    yaml_private_key = {
        "phone": str(),
        "email": str()
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
        self.yaml_private_default = True

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
        html = None
        for storage in self.storages:
            try:
                html = storage.gethtml(id)
                break
            except IOError:
                continue
        return html

    def getuniqueid(self, id):
        result = None
        for storage in self.storages:
            try:
                result = storage.getuniqueid(id)
                break
            except IOError:
                continue
        return result

    def getyaml(self, id, private=None):
        if private is None:
             private = self.yaml_private_default
        result = super(SimulationCV, self).getyaml(id)
        if private is True and self.exists(id) is False:
            result.update(self.yaml_private_key)
        return result

    def getprivatekeys(self):
        return self.yaml_private_key.keys()
