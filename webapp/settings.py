import webapp.jsonencoder
from baseapp.settings import *
from baseapp.loader import config


def load_access_config(path):
    config = dict()
    try:
        stream = open(os.path.join(path, 'access.yaml')).read()
        config = yaml.load(stream)
    except IOError:
        pass
    return config


def load_server_config(path):
    config = {
        'APP_CONFIG': {
            'host': 'localhost',
            'port': 4888,
            'threaded': True
        }
    }
    try:
        stream = open(os.path.join(path, 'run.yaml')).read()
        config.update(yaml.load(stream))
    except IOError:
        pass
    return config


CONFIG_PATH = 'webapp/config'
UPLOAD_TEMP = config.storage_config['UPLOAD_TEMP']
RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}
