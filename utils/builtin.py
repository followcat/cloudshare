# -*- coding: utf-8 -*-
import os
import time
import ujson
import hashlib

import yaml
import utils._yaml

import jieba
import jieba.posseg


def industrytopath(industry):
    return industry.replace('/', '-')


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


def jieba_cut(text, pos=False, HMM=True):
    """
        >>> from utils.builtin import jieba_cut
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
        >>> s = '有较强的自学能力'
        >>> words = list(jieba_cut(s))
        >>> for _w in words:     
        ...     print(_w.encode('utf-8'))
        有
        较
        强
        的
        自学能力
        >>> words = list(jieba_cut(s, pos=True))
        >>> for _w in words:
        ...     print(_w.encode('utf-8'))
        有/v
        较强/a
        的/uj
        自学能力/l
    """
    if pos:
        return jieba.posseg.cut(text, HMM=HMM)
    return jieba.cut(text, HMM=HMM)

def pos_extract(words, flags):
    """
        >>> from services.mining import FLAGS
        >>> from utils.builtin import jieba_cut, pos_extract
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
        >>> s = "研究表明电子器件的失效中70%是由焊点失效引起的"
        >>> words = list(jieba_cut(s, pos=True))
        >>> for _w in words:
        ...     print(_w.encode('utf-8'))
        研究/vn
        表明/v
        电子器件/n
        的/uj
        失效/a
        中/ns
        70/m
        %/x
        是/v
        由/p
        焊点/n
        失效/a
        引起/v
        的/uj
        >>> words = pos_extract(words, FLAGS)
        >>> for _w in words:
        ...     print(_w.encode('utf-8'))
        研究
        表明
        电子器件
        的
        失效
        中
        是
        焊点
        失效
        引起
        的
    """
    return [word.word for word in words if word.flag not in flags]
