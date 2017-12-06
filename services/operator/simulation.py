import services.operator.split
import services.operator.checker
import services.base.kv_storage
import services.base.name_storage


class Simulation(services.operator.checker.Filter):
    """ Backward compatible definition of a simulation service,

    A simulation will:
        - filter ids based on nams.json
        - update kv data with content from YAML directory
    """
    def __init__(self, path, name, service, iotype='git'):
        operator_service = services.base.name_storage.NameStorage(path, name, iotype=iotype)
        data_service = services.operator.split.SplitData(
                services.base.kv_storage.KeyValueStorage(path, name, iotype=iotype),
                service)
        super(Simulation, self).__init__(data_service, operator_service)

    # TODO: check if at the right place (getmd)
    def dump(self, path):
        def writefile(filepath, stream):
            with open(filepath, 'w') as f:
                f.write(stream.encode('utf-8'))

        import os
        import utils.builtin
        import core.outputstorage

        if not os.path.exists(path):
            os.makedirs(path)
        for i in self.ids:
            name = core.outputstorage.ConvertName(i)
            try:
                mdpath = os.path.join(path, name.md)
                mdstream = self.getmd(i)
                writefile(mdpath, mdstream)
            except IOError:
                pass
            writefile(htmlpath, htmlstream)
            yamlinfo = self.getyaml(i)
            utils.builtin.save_yaml(yamlinfo, path, name.yaml)
