# -*- coding: utf-8 -*-
import os
import time
import hashlib

import yaml
import utils._yaml

import jieba
import jieba.posseg


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


def jieba_cut(text, pos=False):
    """
        >>> from services.mining import *
        >>> s = "测试计量技术及仪器"
        >>> for _w in jieba_cut(s):
        ...     print(_w.encode('utf-8'))
        测试
        计量
        技术
        及
        仪器
        >>> for _w in jieba_cut(s, pos=True):
        ...     print(_w.encode('utf-8'))
        测试/vn
        计量/n
        技术/n
        及/c
        仪器/n
    """
    if pos:
        return jieba.posseg.cut(text)
    return jieba.cut(text)

def pos_extract(words, flags):
    """
        >>> from services.mining import *
        >>> s = "◆负责产品环境、电磁兼容、可靠性、安规等测试；"
        >>> words = list(jieba_cut(s, pos=True))
        >>> for _w in words:
        ...     print(_w.encode('utf-8'))
        ◆/x
        负责/v
        产品/n
        环境/n
        、/x
        电磁兼容/l
        、/x
        可靠性/n
        、/x
        安规/nr
        等/u
        测试/vn
        ；/x
        >>> words = pos_extract(words, FLAGS)
        >>> for _w in words:
        ...     print(_w.encode('utf-8'))
        负责
        产品
        环境
        电磁兼容
        可靠性
        测试
    """
    return [word.word for word in words if word.flag not in flags]
