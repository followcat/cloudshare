import services.base.kv_storage
import services.base.name_storage


class SelectionCustomer(services.base.name_storage.NameStorage):
    """"""
    ids_file = 'customers.json'


class SimulationCustomer(services.base.kv_storage.KeyValueStorage):

    YAML_DIR = 'CUSTOMER'
    YAML_TEMPLATE = (
    )

