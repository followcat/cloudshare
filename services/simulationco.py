import services.base.simulation
import services.company


class SimulationCO(services.base.simulation.Simulation,
                   services.company.Company):

    YAML_TEMPLATE = (
        ("position",           list),
        ("clientcontact",      list),
        ("caller",             list),
        ("progress",           list),
        ("updatednumber",      list),
    )

    list_item = {"position", "clientcontact", "caller", "progress", "updatednumber"}

    def __init__(self, path, name, cvstorage, iotype=None):
        super(SimulationCO, self).__init__(path, name, cvstorage, iotype)
