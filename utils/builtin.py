import os
import hashlib

import yaml

import utils._yaml
import core.exception
import core.converterutils


def md5(text):
    m = hashlib.md5()
    m.update(text)
    return unicode(m.hexdigest())


def convert_folder(path, repo, temp_output):
    if not os.path.exists(temp_output):
        os.makedirs(temp_output)
    for root, dirs, files in os.walk(path):
        for name in files:
            processfile = core.converterutils.FileProcesser(root, name, temp_output)
            try:
                processfile.storage(repo)
            except core.exception.DuplicateException as error:
                continue


def save_yaml(infodict, path, filename):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(yaml.dump(infodict))


def load_yaml(path, filename):
    with open(os.path.join(path, filename), 'r') as yf:
        yaml_data = yf.read()
    yaml_info = yaml.load(yaml_data, Loader=utils._yaml.Loader)
    return yaml_info
