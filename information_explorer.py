# -*- coding: utf-8 -*-
import re
import os.path

import yaml


def getTagFromString(tag, stream):
    """
        >>> import information_explorer
        >>> information_explorer.getTagFromString('姓名', '姓名:followcat ')
        u'followcat'
        >>> information_explorer.getTagFromString('姓名', '姓    名:followcat ')
        u'followcat'
        >>> information_explorer.getTagFromString('姓名', '姓名:    followcat ')
        u'followcat'
        >>> information_explorer.getTagFromString('姓名', '姓    名:    followcat ')
        u'followcat'
        >>> information_explorer.getTagFromString('姓名', '  姓    名:    followcat ')
        u'followcat'
    """
    name = ""
    re_string = ""
    for each in tag.decode('utf-8'):
        re_string += each
        re_string += ur"[ \u3000]*"
    re_string += ur"[ \u3000:\uff1a]+(?P<tag>[\S]+)\W"
    re_words = re.search(re_string, stream.decode('utf8'))
    if re_words is not None:
        name = re_words.group('tag')
    return name


def getInfoFromRestr(stream, restring):
    """
        >>> import information_explorer
        >>> email_restr = ur"[a-zA-Z0-9._\\%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
        >>> information_explorer.getInfoFromRestr('Mail followcat@gmail.com', email_restr)
        [u'followcat@gmail.com']
        >>> phone_restr = r'1\d{10}'
        >>> information_explorer.getInfoFromRestr('phone: 13123456789', phone_restr)
        [u'13123456789']
        >>> company_restr = ur'[ \u3000:\uff1a]*([\S]*\u6709\u9650\u516c\u53f8)'
        >>> information_explorer.getInfoFromRestr('company: cat有限公司', company_restr)
        [u'cat\u6709\u9650\u516c\u53f8']
    """
    regex = re.compile(restring, re.IGNORECASE)
    result = re.findall(regex, stream.decode('utf8'))
    return result


def save_yaml(infodict, path, filename):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(yaml.dump(infodict))


def catch(path, convertname, basename, output):
    company_restr = ur'[ \u3000:\uff1a]*([\S]*\u6709\u9650\u516c\u53f8)'
    with open(os.path.join(path, convertname.md), 'r') as f:
        stream = f.read()
        info_dict = {
            "filename":     basename.decode('utf-8'),
            "name":         getTagFromString('姓名', stream),
            "education":    getTagFromString('学历', stream),
            "age":          getTagFromString('年龄', stream),
            "position":     getTagFromString('职位', stream),
            "company":      getInfoFromRestr(stream, company_restr)[0],
            }
        save_yaml(info_dict, output, convertname.yaml)
