import yaml

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


def load_app_config(path):
    config = dict()
    try:
        stream = open(os.path.join(path, 'run.yaml')).read()
        config = yaml.load(stream)
    except IOError:
        pass
    return config


CONFIG_PATH = 'webapp/config'
UPLOAD_TEMP = config.storage_config['UPLOAD_TEMP']
RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}

SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
APP_CONFIG = load_app_config(CONFIG_PATH)
ACCESS = load_access_config(CONFIG_PATH)
