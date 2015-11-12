import os
import time
import hashlib

import yaml
import utils._yaml


def md5(text):
    m = hashlib.md5()
    m.update(text)
    return unicode(m.hexdigest())


def save_yaml(infodict, path, filename):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(yaml.dump(infodict))


def load_yaml(path, filename):
    with open(os.path.join(path, filename), 'r') as yf:
        yaml_data = yf.read()
    yaml_info = yaml.load(yaml_data, Loader=utils._yaml.Loader)
    return yaml_info


def strftime(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
