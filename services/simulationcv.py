import services.base.simulation
import services.curriculumvitae


class SimulationCV(services.base.simulation.Simulation,
                   services.curriculumvitae.CurriculumVitae):

    YAML_TEMPLATE = (
        ("committer",           str),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    list_item = {"tag", "comment", "tracking"}

    def __init__(self, path, name, cvstorage, iotype='git'):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> config.init_samplecv()
            >>> SVC_PRJ_MED = config.SVC_PRJ_MED
            >>> id = list(SVC_PRJ_MED.cv_ids())[0]
            >>> SVC_PRJ_MED.curriculumvitae.updateinfo(id, 'committer', 'dev', 'dev')
            {'committer': 'dev'}
            >>> data = SVC_PRJ_MED.curriculumvitae.updateinfo(id, 'tag', 'tag_v', 'dev')
            >>> data['content'], data['author']
            ('tag_v', 'dev')
            >>> rm_data = SVC_PRJ_MED.curriculumvitae.deleteinfo(id, 'tag',
            ...             'tag_v', 'dev', data['date'])
            >>> rm_data['date'] == data['date']
            True
            >>> data = SVC_PRJ_MED.curriculumvitae.updateinfo(id, 'tag', 'tag_v', 'dev')
            >>> rm_data = SVC_PRJ_MED.curriculumvitae.deleteinfo(id, 'tag',
            ...             'tag_v', 'robot', data['date'])
            >>> rm_data is None
            True
            >>> config.destory()
        """
        super(SimulationCV, self).__init__(path, name, cvstorage, iotype)

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        return self.cvstorage.gethtml(veren)

    def gethtml(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.gethtml(name)
