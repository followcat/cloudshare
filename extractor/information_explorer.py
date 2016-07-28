# -*- coding: utf-8 -*-
import re
import os.path
import functools
import extractor.education
import extractor.expectation
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
    result = dict(education='', school='', education_history=[])
    education_result = extractor.education.fix(stream)
    result.update(education_result)
    if 'education_history' in education_result:
        for edu in education_result['education_history']:
            result['education'] = edu['education']
            result['school'] = edu['school']
            break
    return result


def get_expectation(stream):
    result = extractor.expectation.fix(stream)
    return result


def get_experience(stream, name=None):
    u"""
        >>> get_experience(u"2015.03 - 2015.05   XXCOM")['experience']
        [(u'2015.03', u'2015.05', u'XXCOM')]
        >>> get_experience(u"2015/03 - 2015/05   XXCOM")['experience']
        [(u'2015/03', u'2015/05', u'XXCOM')]
        >>> assert get_experience(u"2015/03 - 至今   XXCOM")
        >>> assert get_experience(u"2015/03 - 至今   XXCOM XXX")
    """

    fix_func = {
        'default': functools.partial(extractor.extract_experience.fix, stream, True),
        'cloudshare': functools.partial(extractor.extract_experience.fix, stream, True),
        'liepin': functools.partial(extractor.extract_experience.fix_liepin, stream),
        'jingying': functools.partial(extractor.extract_experience.fix_jingying, stream),
        'zhilian': functools.partial(extractor.extract_experience.fix_zhilian, stream)
    }
    experiences = []
    current_company = None
    current_position = None
    if name is None:
        name = 'default'
    assert name in fix_func

    extracted_data = fix_func[name]()
    if extracted_data:
        (company, position) = extracted_data['experience']['company'], extracted_data['experience']['position']
        for (i,c) in enumerate(company):
            current_positions = [p for p in position if p['at_company'] == i]
            for p in current_positions:
                if (re.match(extractor.utils_parsing.TODAY, c['date_to']) or
                        re.match(extractor.utils_parsing.TODAY, p['date_to'])):
                    if current_company is None:
                        current_company = c['name']
                    if current_position is None:
                        current_position = p['name']
                if 'duration' in c and c['duration']:
                    if len(current_positions) == 1: 
                        if 'duration' in p and p['duration']:
                            experiences.append((p['date_from'], p['date_to'], c['name']+'|'+p['name']+'('+p['duration']+')'))
                        else:
                            experiences.append((p['date_from'], p['date_to'], c['name']+'|'+p['name']+'('+c['duration']+')'))
                    else:
                        if 'duration' in p and p['duration']:
                            experiences.append((p['date_from'], p['date_to'], c['name']+'('+c['duration']+')'+'|'+p['name']+'('+p['duration']+')'))
                        else:
                            experiences.append((p['date_from'], p['date_to'], c['name']+'('+c['duration']+')'+'|'+p['name']))
                elif 'duration' in p and p['duration']:
                    experiences.append((p['date_from'], p['date_to'], c['name']+'|'+p['name']+'('+p['duration']+')'))
                else:
                    experiences.append((p['date_from'], p['date_to'], c['name']+'|'+p['name']))
            else:
                if not len(current_positions):
                    if re.match(extractor.utils_parsing.TODAY, c['date_to']) is not None:
                        if current_company is None:
                            current_company = c['name']
                    if 'duration' in c and c['duration']:
                        experiences.append((c['date_from'], c['date_to'], c['name']+'('+c['duration']+')'))
                    else:
                        experiences.append((c['date_from'], c['date_to'], c['name']))
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


def catch(stream, name=None):
    info_dict = dict()
    info_dict["name"] = get_name(stream)
    info_dict["originid"] = get_originid(stream)
    info_dict["age"] = get_age(stream)
    info_dict["phone"] = get_phone(stream)
    info_dict["email"] = get_email(stream)
    info_dict.update(get_education(stream))     # education_history, education, school
    info_dict.update(get_experience(stream, name))    # experience, company, position
    info_dict.update(get_expectation(stream))   # expectation, current, gender, marital_status,
                                                # age
    return info_dict

def catch_selected(stream, selected, name=None):
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
        info_dict.update(get_education(stream))
    if 'experience' in selected:
        info_dict.update(get_experience(stream, name))
    if 'expectation' in selected:
        info_dict.update(get_expectation(stream))
    return info_dict
