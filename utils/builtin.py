import os
import hashlib

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
