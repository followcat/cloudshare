# -*- coding: utf-8 -*-
import re
import string
import os.path
import functools
import extractor.unique_id
import extractor.education
import extractor.expectation
import extractor.utils_parsing
import extractor.extract_experience


cv_template = (
    ("id",                  str),
    ("name",                str),
    ("filename",            str),
    ("committer",           str),
    ("date",                int),
    ("origin",              str),
    ("originid",            str),
    ("phone",               str),
    ("email",               str),
    ("expectation",         dict),
    ("current",             dict),
    ("gender",              str),
    ("marital_status",      str),
    ("age",                 str),
    ("birthdate",           str),
    ("education_history",   list),
    ("education",           str),
    ("school",              str),
    ("company",             str),
    ("position",            str),
    ("experience",          dict),
    ("comment",             list),
    ("tag",                 list),
    ("tracking",            list),
)

co_template = (
    ("name",                str),
    ("product",             str),
    ("website",             str),
    ("conumber",            str),
    ("address",             str),
    ("introduction",        str),
    ("email",               str),
)

peo_template = (
    ("id",                  str),
    ("cv",                  list),
)


def generate_info_template(template):
    info = {}
    for each in template:
        info[each[0]] = each[1]()
    return info


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
    re_words = re.search(re_string, stream.replace(u'\xa0', ' '))
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


def get_education(stream, name=None):
    fix_func = {
        'default': extractor.education.fix,
        'jingying': extractor.education.fix_jingying,
        'liepin': extractor.education.fix_liepin,
        'yingcai': extractor.education.fix_yingcai,
        'zhilian': extractor.education.fix_zhilian,
    }
    try:
        assert name in fix_func
    except AssertionError:
        name = 'default'
    result = dict()
    education_result = fix_func[name](stream)
    result.update(education_result)
    if 'education_history' in education_result:
        highest_education = -1
        for edu in education_result['education_history']:
            if extractor.utils_parsing.education_rate(edu['education']) > highest_education:
                highest_education = extractor.utils_parsing.education_rate(edu['education'])
                result['education'] = edu['education']
                try:
                    result['school'] = edu['school']
                except KeyError:
                    pass
    return result


def get_expectation(stream):
    result = extractor.expectation.fix(stream)
    return result


def get_experience(stream, name=None):
    u"""
        >>> xp = get_experience(u"工作经历\\n2010.03 - 2015.05 公司")['experience']['company'][0]
        >>> xp['date_from'], xp['date_to']
        (u'2010.03', u'2015.05')
        >>> assert xp['name'] == u'公司'
        >>> xp = get_experience(u"工作经历\\n2010/03 - 2015/05 公司")['experience']['company'][0]
        >>> xp['date_from'], xp['date_to']
        (u'2010.03', u'2015.05')
        >>> assert xp['name'] == u'公司'
        >>> assert get_experience(u"2015/03 - 至今   XXCOM")
        >>> assert get_experience(u"2015/03 - 至今   XXCOM XXX")
    """

    fix_func = {
        'default': functools.partial(extractor.extract_experience.fix, stream, True),
        'cloudshare': functools.partial(extractor.extract_experience.fix, stream, True),
        'liepin': functools.partial(extractor.extract_experience.fix_liepin, stream),
        'jingying': functools.partial(extractor.extract_experience.fix_jingying, stream),
        'zhilian': functools.partial(extractor.extract_experience.fix_zhilian, stream),
        'yingcai': functools.partial(extractor.extract_experience.fix_yingcai, stream),
    }
    experiences = []
    current_company = None
    current_position = None
    try:
        assert name in fix_func
    except AssertionError:
        name = 'default'

    extracted_data = fix_func[name]()
    if extracted_data:
        (company, position) = extracted_data['experience']['company'], extracted_data['experience']['position']
        for c in company:
            current_positions = [p for p in position if p['at_company'] == c['id']]
            for p in current_positions:
                if (re.match(extractor.utils_parsing.TODAY, c['date_to']) or
                        re.match(extractor.utils_parsing.TODAY, p['date_to'])):
                    if current_company is None:
                        current_company = c['name']
                    if current_position is None:
                        current_position = p['name']
            else:
                if not len(current_positions):
                    if re.match(extractor.utils_parsing.TODAY, c['date_to']) is not None:
                        if current_company is None:
                            current_company = c['name']
    result = extracted_data
    if current_company is None:
        current_company = ''
    if current_position is None:
        current_position = ''
    if 'experience' not in result:
        result['experience'] = {}
    result['company'] = current_company
    result['position'] = current_position
    return result


def get_classify(experience, company_knowledge=None):
    return extractor.extract_experience.match_classify(experience, company_knowledge)


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


all_selected = ('name', 'originid', 'age', 'phone', 'email', 'education', 'experience', 'expectation', 'classify')

def catch_selected(stream, selected, name=None):
    assert set(selected).issubset(set(all_selected))
    info_dict = dict()
    if 'name' in selected:
        info_dict["name"] = get_name(stream)
    if 'originid' in selected:
        info_dict["originid"] = get_originid(stream)
    if 'age' in selected:
        info_dict["age"] = get_age(stream)
    if 'phone' in selected:
        info_dict["phone"] = get_phone(stream)
    if 'email' in selected:
        info_dict["email"] = get_email(stream)
    if 'education' in selected:
        info_dict.update(get_education(stream, name))     # education_history, education, school
    if 'experience' in selected:
        info_dict.update(get_experience(stream, name))    # experience, company, position
    if 'expectation' in selected:
        info_dict.update(get_expectation(stream))   # expectation, current, gender, marital_status,
                                                    # age
    if 'classify' in selected:
        experience = get_experience(stream, name)
        info_dict["classify"] = get_classify(experience)
    return info_dict

catch = functools.partial(catch_selected, selected=all_selected)


def catch_cvinfo(stream, filename, catch_info=True):
    """
        >>> import core.outputstorage
        >>> st = 'curriculum vitea'
        >>> name = core.outputstorage.ConvertName('name.docx')
        >>> assert catch_cvinfo(stream=st, filename=name.base)['filename'] == name.base
    """
    info = generate_info_template(cv_template)
    if catch_info is True:
        catchinfo = catch(stream)
        info.update(catchinfo)
    extractor.unique_id.unique_id(info)
    try:
        info['id'] = info['unique_id']
    except KeyError:
        info['id'] = extractor.unique_id.cv_id(stream)
    info["filename"] = filename
    return info


def catch_coinfo(stream, name):
    """
        >>> intro = {'introduction': 'introduction'}
        >>> assert catch_coinfo(name='sgwgewtgqe', stream=intro)['id'] == '114efe82f552167a1ebdd98e65f3e66750ffe720'
    """
    info = generate_info_template(co_template)
    info['name'] = name
    info['id'] = extractor.unique_id.company_id(name)
    if isinstance(stream, dict):
        for key in info:
            if key in stream and stream[key]:
                info[key] = stream[key]
        for key in ('introduction', 'total_employees'):
            try:
                info[key] = stream[key]
            except KeyError:
                pass
        try:
            info['business'].append(stream['business'])
        except KeyError:
            pass
    return info

def catch_peopinfo(stream, name):
    """
        >>> intro = {'id': '00yd4ww2', 'unique_id': 'e16f06e87d38c195f0d61fb685ec559ca9cfd5b3'}
        >>> assert catch_peopinfo(stream=intro, name=intro['unique_id'])['id'] == 'e16f06e87d38c195f0d61fb685ec559ca9cfd5b3'
        >>> assert catch_peopinfo(stream=intro, name=intro['unique_id'])['cv'] == ['00yd4ww2']
    """
    info = generate_info_template(peo_template)
    info['id'] = name
    if isinstance(stream, dict):
        try:
            info['cv'].append(stream['id'])
        except KeyError:
            pass
    return info
