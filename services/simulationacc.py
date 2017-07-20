import core.exception
import services.base.simulation


class SimulationACC(services.base.simulation.Simulation):

    YAML_TEMPLATE = (
        ("inviter",             str),
    )

    def __init__(self, path, name, storage, iotype='git'):
        super(SimulationACC, self).__init__(path, name, storage, iotype=iotype)

    def getinfo(self, id):
        if self.exists(id):
            return super(SimulationACC, self).getinfo(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def getyaml(self, id):
        if self.exists(id):
            return super(SimulationACC, self).getyaml(id)
        else:
            raise core.exception.NotExistsIDException(id)

    def getmd(self, id):
        if self.exists(id):
            return super(SimulationACC, self).getmd(id)
        else:
            raise core.exception.NotExistsIDException(id)
