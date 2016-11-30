import services.base.simulation
import services.curriculumvitae


class SimulationCV(services.base.simulation.Simulation,
                   services.curriculumvitae.CurriculumVitae):

    ids_file = 'names.json'

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = (
        ("committer",           list),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    def __init__(self, path, name, cvstorage):
        super(SimulationCV, self).__init__(path, name, cvstorage)

    def getmd(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.getmd(name)

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        return self.cvstorage.gethtml(veren)

    def gethtml(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.gethtml(name)
