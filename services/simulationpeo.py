import services.people
import services.operator.simulation


class SimulationPEO(services.operator.simulation.Simulation):

    YAML_TEMPLATE = (
        ("committer",           str),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    list_item = {"tag", "comment", "tracking"}

    def __init__(self, path, name, storages, iotype='git'):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> config.init_samplecv()
            >>> SVC_PRJ_TEST = config.SVC_PRJ_TEST
            >>> id = list(SVC_PRJ_TEST.people.ids)[0]
            >>> SVC_PRJ_TEST.people.updateinfo(id, 'committer', 'dev', 'dev')
            {'committer': 'dev'}
            >>> data = SVC_PRJ_TEST.people.updateinfo(id, 'tag', 'tag_v', 'dev')
            >>> data['content'], data['author']
            ('tag_v', 'dev')
            >>> rm_data = SVC_PRJ_TEST.people.deleteinfo(id, 'tag',
            ...             'tag_v', 'dev', data['date'])
            >>> rm_data['date'] == data['date']
            True
            >>> data = SVC_PRJ_TEST.people.updateinfo(id, 'tag', 'tag_v', 'dev')
            >>> rm_data = SVC_PRJ_TEST.people.deleteinfo(id, 'tag',
            ...             'tag_v', 'robot', data['date'])
            >>> rm_data is None
            True
            >>> config.destory()
        """
        super(SimulationPEO, self).__init__(path, name, storages, iotype=iotype)

    def getyaml(self, id):
        try:
            return super(SimulationPEO, self).getyaml(id)
        except IOError:
            yaml = {'id': id, 'cv': [id]}
            info = self.getinfo(id)
            yaml.update(info)
            return yaml
