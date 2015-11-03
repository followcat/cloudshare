# -*- coding: utf-8 -*-
import re
import os.path

import yaml


def getTagFromString(tag, stream):
    """
        >>> import core.information_explorer
        >>> core.information_explorer.getTagFromString('姓名', '姓名:followcat ')
        u'followcat'
        >>> core.information_explorer.getTagFromString('姓名', '姓    名:followcat ')
        u'followcat'
        >>> core.information_explorer.getTagFromString('姓名', '姓名:    followcat ')
        u'followcat'
        >>> core.information_explorer.getTagFromString('姓名', '姓    名:    followcat ')
        u'followcat'
        >>> core.information_explorer.getTagFromString('姓名', '  姓    名:    followcat ')
        u'followcat'
    """
    name = ""
    re_string = ""
    for each in tag.decode('utf-8').replace(u'\xa0', ' '):
        re_string += each
        re_string += ur"[ \u3000]*"
    re_string += ur"[ \u3000:\uff1a]+(?P<tag>[\S]+)\W"
    re_words = re.search(re_string, stream.decode('utf8'))
    if re_words is not None:
        name = re_words.group('tag')
    return name


def getInfoFromRestr(stream, restring):
    """
        >>> import core.information_explorer
        >>> email_restr = ur"[a-zA-Z0-9._\\%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
        >>> core.information_explorer.getInfoFromRestr(
        ... 'Mail followcat@gmail.com', email_restr)
        [u'followcat@gmail.com']
        >>> phone_restr = r'1\d{10}'
        >>> core.information_explorer.getInfoFromRestr(
        ... 'phone: 13123456789', phone_restr)
        [u'13123456789']
        >>> company_restr = ur'[ \u3000:\uff1a]*([\S]*\u6709\u9650\u516c\u53f8)'
        >>> core.information_explorer.getInfoFromRestr(
        ... 'company: cat有限公司', company_restr)
        [u'cat\u6709\u9650\u516c\u53f8']
    """
    regex = re.compile(restring, re.IGNORECASE)
    search_string = stream.decode('utf8').replace(u'\xa0', ' ')
    result = re.findall(regex, search_string)
    return result


def save_yaml(infodict, path, filename):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(yaml.dump(infodict))


def info_by_re_iter(stream, restr):
    result_iter = iter(getInfoFromRestr(stream, restr))
    try:
        result = ''.join(result_iter.next())
    except StopIteration:
        result = ''
    return result


def catch(path, convertname, basename, output):
    organization = (u'有限公司', U'公司', u'集团', u'院')
    organization_restr = u'[ \u3000:\uff1a]*([()a-zA-Z0-9\u4E00-\u9FA5]+)('
    for each in organization:
        organization_restr += each + '|'
    organization_restr = organization_restr[:-1] + ')'

    school = (u'大学', u'学院', u'学校')
    school_restr = u'[ \u3000]*([a-zA-Z0-9\u4E00-\u9FA5]+)('
    for each in school:
        school_restr += each + '|'
    school_restr = school_restr[:-1] + ')'

    age_chinese = u'岁'
    age_restr = u'[ \u3000]*(\d{2})' + age_chinese

    phone_restr = u'\b1\d{10}\b'

    email_restr = u'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b'

    with open(os.path.join(path, convertname.md), 'r') as f:
        stream = f.read()

        name = getTagFromString('姓名', stream)
        namelist = getInfoFromRestr(name.encode('utf-8'), u'^[\u4E00-\u9FA5\w]*$')
        if not namelist:
            name = ''

        age = info_by_re_iter(stream, age_restr)
        phone = info_by_re_iter(stream, phone_restr)
        email = info_by_re_iter(stream, email_restr)
        company = info_by_re_iter(stream, organization_restr)
        school_iter = iter(getInfoFromRestr(stream, school_restr))
        try:
            school = ''.join(school_iter.next())
            while len(school) > 10:
                school = ''.join(school_iter.next())
        except StopIteration:
            school = ''

        info_dict = {
            "filename":     basename.decode('utf-8'),
            "name":         name,
            "education":    getTagFromString('学历', stream),
            "age":          getTagFromString('年龄', stream) or age,
            "position":     getTagFromString('职位', stream),
            "company":      company,
            "school":       school,
            "phone":        getTagFromString('电话', stream) or phone,
            "email":        getTagFromString('邮件', stream) or email,
            "comment":      [],
            "tag":          [],
            "tracking":     [],
            }
        save_yaml(info_dict, output, convertname.yaml)
