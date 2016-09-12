import os
import time
import ujson
import hashlib

import yaml
import utils._yaml


def md5(text):
    m = hashlib.md5()
    m.update(text)
    return unicode(m.hexdigest())


def save_yaml(infodict, path, filename):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(yaml.dump(infodict, Dumper=utils._yaml.SafeDumper, allow_unicode=True))


def load_yaml(path, filename):
    with open(os.path.join(path, filename), 'r') as yf:
        yaml_data = yf.read()
    yaml_info = yaml.load(yaml_data, Loader=utils._yaml.Loader)
    return yaml_info


def save_json(data, path, filename):
    ujson.dump(data, open(os.path.join(path, filename), 'w'))


def load_json(path, filename):
    return ujson.load(open(os.path.join(path, filename)))


try:
    from subprocess import check_output
except ImportError:
    # Python < 2.7 fallback, stolen from the 2.7 stdlib
    def check_output(*popenargs, **kwargs):
        from subprocess import Popen, PIPE, CalledProcessError
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = Popen(stdout=PIPE, *popenargs, **kwargs)
        output, _ = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd, output=output)
        return output


def strftime(t, format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(t))
