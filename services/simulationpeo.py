import services.people
import services.base.simulation


class SimulationPEO(services.base.simulation.Simulation,
                    services.people.People):

    YAML_TEMPLATE = (
        ("committer",           str),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    list_item = {"tag", "comment", "tracking"}

    def __init__(self, path, name, peostorage, iotype='git'):
        super(SimulationPEO, self).__init__(path, name, peostorage, iotype)

    def getyaml(self, id):
        try:
            return super(SimulationPEO, self).getyaml(id)
        except IOError:
            yaml = {'id': id, 'cv': [id]}
            info = self.getinfo(id)
            yaml.update(info)
            return yaml
