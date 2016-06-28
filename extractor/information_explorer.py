# -*- coding: utf-8 -*-
import re
import os.path
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
        >>> company_restr = ur'[ \u3000:\uff1a]*([\S]*有限公司)'
        >>> assert get_infofromrestr(u'company: cat有限公司', company_restr)
    """
    regex = re.compile(restring, re.IGNORECASE)
    search_string = stream.replace(u'\xa0', ' ')
    result = re.findall(regex, search_string)
    return result


def get_experience(stream):
    u"""
        >>> get_experience(u"2015.03 - 2015.05   XXCOM")
        [(u'2015.03', u'2015.05', u'XXCOM')]
        >>> get_experience(u"2015/03 - 2015/05   XXCOM")
        [(u'2015/03', u'2015/05', u'XXCOM')]
        >>> assert get_experience(u"2015/03 - 至今   XXCOM")
        >>> assert get_experience(u"2015/03 - 至今   XXCOM XXX")
    """
    experiences = []
    extracted_data = extractor.extract_experience.fix(stream)
    RE = re.compile(extractor.utils_parsing.DURATION)
    if not extracted_data[1]:
        (company, position) = extracted_data[0]
        for (i,c) in enumerate(company):
            current_positions = [p for p in position if p[4] == i]
            for p in current_positions:
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
    return experiences


def info_by_re_iter(stream, restr):
    result_iter = iter(get_infofromrestr(stream, restr))
    try:
        result = ''.join(result_iter.next())
    except StopIteration:
        result = ''
    return result


def catch(stream, basename):
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
        "id":           '',
        "experience":   [],
        "comment":      [],
        "tag":          [],
        "tracking":     [],
        }
    organization = (u'有限公司', U'公司', u'集团', u'院')
    organization_restr = u'[ \u3000:\uff1a]*([（）()a-zA-Z0-9\u4E00-\u9FA5]+)('
    for each in organization:
        organization_restr += each + '|'
    organization_restr = organization_restr[:-1] + ')'

    school = (u'大学', u'学院', u'学校')
    school_restr = u'[ \u3000]*([a-zA-Z0-9\u4E00-\u9FA5]+)('
    for each in school:
        school_restr += each + '|'
    school_restr = school_restr[:-1] + ')'

    education = (u'博士', u'硕士', u'本科', u'大专')
    education_restr = u'('
    for each in education:
        education_restr += each + '|'
    education_restr = education_restr[:-1] + ')'

    age_chinese = u'岁'
    age_restr = u'[ \u3000]*(\d{2})' + age_chinese

    phone_restr = u'1\d{10}'

    email_restr = u'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'

    name = get_tagfromstring(u'姓名', stream)
    namelist = get_infofromrestr(name, u'^[\u4E00-\u9FA5\w]*$')
    if not namelist:
        name = ''
    info_dict["name"] = name

    age = info_by_re_iter(stream, age_restr)
    phone = info_by_re_iter(stream, phone_restr)
    email = info_by_re_iter(stream, email_restr)
    company = info_by_re_iter(stream, organization_restr)
    school_iter = iter(get_infofromrestr(stream, school_restr))
    try:
        school = ''.join(school_iter.next())
        while len(school) > 10:
            school = ''.join(school_iter.next())
    except StopIteration:
        school = ''

    info_dict["school"] = school
    info_dict["company"] = company
    info_dict["filename"] = basename
    info_dict["position"] = get_tagfromstring(u'所任职位', stream)[:25] or\
        get_tagfromstring(u'职位', stream)[:25]
    info_dict["education"] = get_tagfromstring(u'学历', stream) or\
        info_by_re_iter(stream, education_restr)
    info_dict["originid"] = get_tagfromstring(u'ID', stream, rule='a-zA-Z0-9')
    info_dict["age"] = get_tagfromstring(u'年龄', stream) or age
    info_dict["phone"] = get_tagfromstring(u'电话', stream, ur'\d\-－()（）') or phone
    info_dict["email"] = get_tagfromstring(u'邮件', stream, email_restr) or \
        get_tagfromstring(u'邮箱', stream) or email
    info_dict["experience"] = get_experience(stream)
    return info_dict
