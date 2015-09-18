# -*- coding: utf-8 -*-
import re
import os.path

import yaml


def getNameFromString(stream):
    """
        >>> import information_explorer
        >>> information_explorer.getNameFromString('姓名:followcat ')
        u'followcat'
        >>> information_explorer.getNameFromString('姓    名:followcat ')
        u'followcat'
        >>> information_explorer.getNameFromString('姓名:    followcat ')
        u'followcat'
        >>> information_explorer.getNameFromString('姓    名:    followcat ')
        u'followcat'
        >>> information_explorer.getNameFromString('  姓    名:    followcat ')
        u'followcat'
    """
    name = ""
    re_words = re.search(ur"\u59d3[\xa0 ]*\u540d[\xa0 :\uff1a]*"
                         "(?P<name>[\S]*)\W", stream.decode('utf8'))
    if re_words is not None:
        name = re_words.group('name')
    return name


def getPhoneNumFromString(stream):
    """
        >>> import information_explorer
        >>> information_explorer.getPhoneNumFromString('phone: 13123456789')
        ['13123456789']
    """
    regex = re.compile(r'1\d{10}', re.IGNORECASE)
    phonenums = re.findall(regex, stream)
    return phonenums


def getMailAddFromString(stream):
    """
        >>> import information_explorer
        >>> information_explorer.getMailAddFromString('Mail: followcat@gmail.com')
        ['followcat@gmail.com']
    """
    regex = re.compile(r"\b[a-zA-Z0-9._\\%+-]+"
                       r"@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b",
                       re.IGNORECASE)
    mails = re.findall(regex, stream)
    return mails


def save_yaml(infodict, path, filename):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(yaml.dump(infodict))


def catch(path, convertname, output):
    with open(os.path.join(path, convertname.md), 'r') as f:
        stream = f.read()
        info_dict = {
            "name": getNameFromString(stream),
            "mail": getMailAddFromString(stream),
            "phone": getPhoneNumFromString(stream)
            }
        save_yaml(info_dict, output, convertname.yaml)
