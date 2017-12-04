import services.operator.simulation


class SimulationCV(services.operator.simulation.Simulation):

    YAML_TEMPLATE = (
        ("committer",           str),
    )

    yaml_private_key = {
        "phone":                '[*****]',
        "email":                '[*****]',
        "name":                 '[*****]',
        "committer":            '[*****]',
        "origin":               '[*****]'
    }

    list_item = {}

    def __init__(self, path, name, service, iotype='git'):
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
        super(SimulationCV, self).__init__(path, name, service, iotype=iotype)

