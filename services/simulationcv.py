import services.base.kv_storage
import services.base.name_storage


class SelectionCV(services.base.name_storage.NameStorage):

    ids_file = 'names.json'


class SimulationCV(services.base.kv_storage.KeyValueStorage):

    YAML_DIR = 'YAML'
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

