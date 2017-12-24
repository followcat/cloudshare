import extractor.information_explorer
import services.base.kv_storage
import services.operator.checker


class People(services.base.kv_storage.KeyValueStorage):
    """"""
    YAML_DIR = '.'
    YAML_TEMPLATE = extractor.information_explorer.peo_template

    commitinfo = 'People'

class CVSelector(services.operator.checker.Selector):
    def selection(self, x):
        return self.operator_service.getyaml(x)['cv']

