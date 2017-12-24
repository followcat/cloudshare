import core.basedata
import utils.companyexcel
import services.base.kv_storage
import extractor.information_explorer


class Company(services.base.kv_storage.KeyValueStorage):
    YAML_DIR = '.'
    YAML_TEMPLATE = extractor.information_explorer.co_template

    commitinfo = 'Company'

