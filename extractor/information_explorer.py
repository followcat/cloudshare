# -*- coding: utf-8 -*-
import re
import os.path
import extractor.education
import extractor.utils_parsing
import extractor.extract_experience


def get_tagfromstring(tag, stream, rule=None):
    u"""
        >>> get_tagfromstring(u'姓名', u'姓名:followcat ')
        u'followcat'
        >>> get_tagfromstring(u'姓名', u'姓    名:followcat ')
        u'followcat'
        >>> get_tagfromstring(u'姓名', u'姓名:    followcat ')
        u'followcat'
        >>> get_tagfromstring(u'姓名', u'姓    名:    followcat ')
        u'followcat'
        >>> get_tagfromstring(u'姓名', u'  姓    名:    followcat ')
        u'followcat'
    """
    if rule is None:
        rule = '\S'
    name = ""
    re_string = ""
    for each in tag.replace(u'\xa0', ' '):
        re_string += each
        re_string += ur"[ \u3000]*"
    re_string += ur"[ \u3000:\uff1a]+(?P<tag>[%s]+)\W" % rule
    re_words = re.search(re_string, stream)
    if re_words is not None:
        name = re_words.group('tag')
    return name


def get_infofromrestr(stream, restring):
    u"""
        >>> email_restr = ur"[a-zA-Z0-9._\\%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
        >>> get_infofromrestr('Mail followcat@gmail.com', email_restr)
        [u'followcat@gmail.com']
        >>> phone_restr = ur'1\d{10}'
        >>> get_infofromrestr(u'phone: 13123456789', phone_restr)
        [u'13123456789']
    """
    regex = re.compile(restring, re.IGNORECASE)
    search_string = stream.replace(u'\xa0', ' ')
    result = re.findall(regex, search_string)
    return result


def info_by_re_iter(stream, restr):
    result_iter = iter(get_infofromrestr(stream, restr))
    try:
        result = ''.join(result_iter.next())
    except StopIteration:
        result = ''
    return result


def get_education(stream):
    result = dict(education='', school='')
    result['education'] = extractor.education.fix(stream)
    if 'education_history' in result['education']:
        for edu in result['education']['education_history']:
            result['school'] = edu['school']
            break
    return result


def get_experience(stream):
    u"""
        >>> get_experience(u"2015.03 - 2015.05   XXCOM")['experience']
        [(u'2015.03', u'2015.05', u'XXCOM')]
        >>> get_experience(u"2015/03 - 2015/05   XXCOM")['experience']
        [(u'2015/03', u'2015/05', u'XXCOM')]
        >>> assert get_experience(u"2015/03 - 至今   XXCOM")
        >>> assert get_experience(u"2015/03 - 至今   XXCOM XXX")
    """
    experiences = []
    current_company = None
    current_position = None

    extracted_data = extractor.extract_experience.fix(stream)
    RE = re.compile(extractor.utils_parsing.DURATION)
    if not extracted_data[1]:
        (company, position) = extracted_data[0]
        for (i,c) in enumerate(company):
            current_positions = [p for p in position if p[4] == i]
            for p in current_positions:
                if re.match(extractor.utils_parsing.TODAY, p[1]) is not None:
                    if current_company is None:
                        current_company = c[2]
                    if current_position is None:
                        current_position = p[2]
                if c[3] and len(current_positions) == 1 and not RE.search(p[2]):
                    experiences.append((p[0], p[1], c[2]+'|'+p[2]+'('+c[3]+')'))
                elif c[3]:
                    experiences.append((p[0], p[1], c[2]+'('+c[3]+')'+'|'+p[2]))
                else:
                    experiences.append((p[0], p[1], c[2]+'|'+p[2]))
            else:
                if not len(current_positions):
                    experiences.append((c[0], c[1], c[2]))
    if not experiences:
        restr = ur"(\d{4}[/.\\年 ]+\d{1,2}[月]*)[-– —]*(\d{4}[/.\\年 ]+\d{1,2}[月]*|至今)[：: ]*([^\n,，.。（（:]*)"
        result = get_infofromrestr(stream, restr)
        for each in result:
            if each[0] and each[1] and len(each[2]) > 1:
                experiences.append(each)
    result = dict(experience=experiences,
                  company=current_company,
                  position=current_position)
    if result['company'] is None:
        result['company'] = ''
    if result['position'] is None:
        result['position'] = ''
    return result


def get_name(stream):
    name = get_tagfromstring(u'姓名', stream)
    namelist = get_infofromrestr(name, u'^[\u4E00-\u9FA5\w]*$')
    if not namelist:
        name = ''
    return name


def get_email(stream):
    email_restr = u'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
    email = info_by_re_iter(stream, email_restr)
    result = get_tagfromstring(u'邮件', stream, email_restr) or \
        get_tagfromstring(u'邮箱', stream) or email
    return result


def get_originid(stream):
    result = get_tagfromstring(u'ID', stream, rule='a-zA-Z0-9')
    return result


def get_phone(stream):
    phone_restr = u'1\d{10}'
    phone = info_by_re_iter(stream, phone_restr)
    result = get_tagfromstring(u'电话', stream, ur'\d\-－()') or phone
    return result


def get_age(stream):
    age_chinese = u'岁'
    age_restr = u'[ \u3000]*(\d{2})' + age_chinese
    age = info_by_re_iter(stream, age_restr)
    result = get_tagfromstring(u'年龄', stream) or age
    return result


def catch(stream, basename=None):
    info_dict = {
        "filename":     '',
        "name":         '',
        "education":    '',
        "age":          '',
        "position":     '',
        "company":      '',
        "school":       '',
        "phone":        '',
        "email":        '',
        "origin":       '',
        "originid":     '',
        "id":           '',
        "experience":   [],
        "comment":      [],
        "tag":          [],
        "tracking":     [],
        }
    if basename is not None:
        info_dict["filename"] = basename
    info_dict["name"] = get_name(stream)
    info_dict["originid"] = get_originid(stream)
    info_dict["age"] = get_age(stream)
    info_dict["phone"] = get_phone(stream)
    info_dict["email"] = get_email(stream)
    info_dict.update(get_education(stream)) # experience, company, position
    info_dict.update(get_experience(stream)) # education, school
    return info_dict
