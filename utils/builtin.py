import os
import hashlib

import yaml


def md5(text):
    m = hashlib.md5()
    m.update(text)
    return unicode(m.hexdigest())


def save_yaml(infodict, path, filename):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(yaml.dump(infodict))
