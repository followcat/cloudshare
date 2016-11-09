# -*- coding: utf-8 -*-

import hashlib

import extractor.utils_parsing


is_education = lambda x:'education' in x
is_experience = lambda x:'name' in x


def experience_upto_date(date_to, to):
    u"""
        >>> date_to = '2014.04'
        >>> assert date_to == experience_upto_date(date_to, u'至今')
        >>> assert date_to == experience_upto_date(date_to, '2015.04')
        >>> assert date_to == experience_upto_date(date_to, '2014.04')
        >>> assert u'至今' == experience_upto_date(date_to, '2013.04')
    """
    if to == u'至今':
        return date_to
    (period_month, period_year) = extractor.utils_parsing.compute_period(to, date_to, today=to)
    if period_year < 0 or (period_year == 0 and period_month <= 0):
        return date_to
    else:
        return u'至今'
            
def predate(xp, to):
    u"""
        >>> ed = {
        ...     'date_from':  '2012.09',
        ...     'date_to':    '2016.06',
        ...     'education':  u'本科',
        ...     }
        >>> assert u'至今' == predate(ed, '2015.01')['date_to']
        >>> assert not u'至今' == predate(ed, u'至今')['date_to']
    """
    output = xp.copy()
    if extractor.utils_parsing.compute_period(output['date_to'], to, today=to)[-1] < 0:
        output['date_to'] = u'至今'
    return output

def acceptable_education(ed, to_date=u'至今', low_level=u'大专'):
    u"""
        >>> ed = {
        ...     'date_from':  '2014.01',
        ...     'date_to':    '2014.04',
        ...     'school':     'XXX',
        ...     'education':  u'中专',
        ...     }
        >>> assert not acceptable_education(ed)
        >>> assert acceptable_education(ed, low_level=u'中专')

        >>> ed['education'] = u'大专'
        >>> assert acceptable_education(ed)
        >>> assert not acceptable_education(ed, to_date='2013.01')
    """
    assert is_education(ed)
    try:
        (period_month, period_year) = extractor.utils_parsing.compute_period(ed['date_from'], to_date, today=to_date)
    except ValueError:
        return False
    if period_year < 0:
        return False
    return extractor.utils_parsing.education_rate(ed['education']) \
            >= extractor.utils_parsing.education_rate(low_level)

def acceptable_experience(xp, to_date=u'至今'):
    u"""
        >>> xp = {
        ...     'date_from':   '2014.01',
        ...     'date_to':     '2014.04',
        ...     'name':        'XXX'}
        >>> assert not acceptable_experience(xp)
        >>> xp['date_to'] = '2014.05'
        >>> assert acceptable_experience(xp)
        >>> xp['date_to'] = '1994.05'
        >>> assert not acceptable_experience(xp)
        >>> xp['date_to'] = '2016.01'
        >>> assert acceptable_experience(xp)
        >>> assert not acceptable_experience(xp, to_date='2014.04')
        >>> xp['date_from'] = u'至今'
        >>> assert not acceptable_experience(xp)
    """
    assert is_experience(xp)
    try:
        (period_month, period_year) = extractor.utils_parsing.compute_period(xp['date_from'], experience_upto_date(xp['date_to'], to_date), today=to_date)
    except ValueError:
        return False
    return period_year > 0 or (period_year == 0 and period_month > 3)

def order_history(history):
    return sorted(history, key=lambda x:x['date_from'])

def history(cv_yaml, to_date=u'至今'):
    u"""
        >>> import interface.gitinterface
        >>> import services.curriculumvitae
        >>> REPO_DB_NAME = 'repo'
        >>> REPO_DB = interface.gitinterface.GitInterface(REPO_DB_NAME)
        >>> SVC_CV_REPO = services.curriculumvitae.CurriculumVitae(REPO_DB, 'cloudshare')
        >>> yaml = SVC_CV_REPO.getyaml('0mlcw5kf.yaml')
        >>> assert yaml['education_history'][-1]['education'] == u'中专'
        >>> assert not is_education(history(yaml)[0])

        >>> cv = lambda xp: {'education_history': [], 'experience': {'company': [xp.copy()]}}
        >>> ed = {
        ...     'date_from':  '2010.01',
        ...     'date_to':    '2014.01',
        ...     'school':     u'科技大学',
        ...     'major':      u'光电工程',  
        ...     'education':  u'本科',
        ...     }
        >>> xp = {
        ...     'date_from':   '2014.01',
        ...     'date_to':     '2016.04',
        ...     'name':        u'有限公司'}
        >>> cv1 = cv(xp)
        >>> cv1.update({'education_history': [ed]})
        >>> assert is_education(history(cv1)[0])

        >>> xp['date_from'] = '2004.01'
        >>> cv2 = cv(xp)
        >>> cv2.update({'education_history': [ed]})
        >>> assert is_experience(history(cv2)[0])
        >>> assert history(cv2)[1] == history(cv1)[0]

        >>> xp = {
        ...     'date_from':   '2014.01',
        ...     'date_to':     '2016.04',
        ...     'name':        u'有限公司'}
        >>> assert history(cv(xp), '2015.01')[0]['date_to'] == u'至今'
    """
    try:
        history = [ed for ed in cv_yaml['education_history'] if acceptable_education(ed, to_date)]
    except KeyError:
        history = []
    try:
        for xp in cv_yaml['experience']['company']:
            output = xp.copy()
            if acceptable_experience(xp, to_date):
                output['date_to'] = experience_upto_date(xp['date_to'], to_date)
                history.append(output)
    except KeyError:
        pass
    return order_history(history)

def output_history(item):
    u"""
        >>> xp = {
        ...     'date_from':   '2014.01',
        ...     'date_to':     u'至今',
        ...     'name':        u'有限公司'}
        >>> assert len([h for h in output_history(xp)]) == 1
    """
    if is_education(item):
        experience = u'|'.join([item['education'], item['school'], item['major']])
    elif is_experience(item):
        experience = item['name']
    else:
        raise ValueError("history item must be education or experience")
    yield (item['date_from'], u'|'.join([item['date_from'], experience]))
    if not item['date_to'] == u'至今':
        yield (item['date_to'], u'|'.join([item['date_from'], item['date_to'], experience]))

def hash_history(cv_yaml, to_date=u'至今', mininum_xp=2):
    u"""
        >>> import itertools
        >>> cv = lambda xp: {'education_history': [], 'experience': {'company': [xp.copy()]}}
        >>> xp1 = {
        ...     'date_from':   '2014.01',
        ...     'date_to':     '2016.04',
        ...     'name':        u'有限公司'}
        >>> cv1 = cv(xp1)
        >>> assert [t for t in hash_history(cv1, '2013.01', mininum_xp=1)
        ...         ] == [t for t in hash_history(cv1, '2014.03', mininum_xp=1)]
        >>> assert [t for t in hash_history(cv1, '2014.06', mininum_xp=1)
        ...         ] == [t for t in hash_history(cv1, '2015.06', mininum_xp=1)]
        >>> assert not [t for t in hash_history(cv1, '2016.01', mininum_xp=1)
        ...         ] == [t for t in hash_history(cv1, '2016.11', mininum_xp=1)]

        >>> xp2 = {
        ...     'date_from':   '2014.01',
        ...     'date_to':     u'至今',
        ...     'name':        u'有限公司'}
        >>> cv2 = cv(xp2)
        >>> assert [t for t in hash_history(cv2, '2016.01', mininum_xp=1)
        ...         ] == [t for t in hash_history(cv2, '2016.11', mininum_xp=1)]

        >>> assert [t for t in hash_history(cv1, '2013.01', mininum_xp=1)
        ...         ] == [t for t in hash_history(cv2, '2013.01', mininum_xp=1)]
        >>> assert [t for t in hash_history(cv1, '2015.03', mininum_xp=1)
        ...         ] == [t for t in hash_history(cv2, '2015.03', mininum_xp=1)]
        >>> assert not [t for t in hash_history(cv1, u'至今', mininum_xp=1)
        ...         ] == [t for t in hash_history(cv2, u'至今', mininum_xp=1)]

        >>> ed = {
        ...     'date_from':  '2010.01',
        ...     'date_to':    '2014.01',
        ...     'school':     u'科技大学',
        ...     'major':      u'光电工程',  
        ...     'education':  u'本科',
        ...     }
        >>> cv1.update({'education_history': [ed]})
        >>> cv2.update({'education_history': [ed]})
        >>> assert [t for t in hash_history(cv1, '2015.03')] == [t for t in hash_history(cv2, '2015.03')]
    """
    previous = ''
    for i, h in enumerate(history(cv_yaml, to_date)):
        for (hashdate, output) in output_history(h):
            if i+1 >= mininum_xp:
                yield (hashdate, hashlib.sha1(previous+output.encode('utf8')).hexdigest())
            previous += output.encode('utf8') + '\n'

def unique_id(cv_yaml, to_date=u'至今'):
    u"""
        >>> cv = lambda xp: {'education_history': [], 'experience': {'company': [xp.copy()]}}
        >>> ed = {
        ...     'date_from':  '2010.01',
        ...     'date_to':    '2014.01',
        ...     'school':     u'科技大学',
        ...     'major':      u'光电工程',  
        ...     'education':  u'本科',
        ...     }
        >>> xp = {
        ...     'date_from':   '2014.01',
        ...     'date_to':     '2016.04',
        ...     'name':        u'有限公司'}
        >>> cv_yaml = cv(xp)
        >>> cv_yaml.update({'education_history': [ed]})
        >>> id = unique_id(cv_yaml)
        >>> assert 2 == len(id['unique_id_hash'])
        >>> assert id['unique_id'] ==  hashlib.sha1(
        ...     u'2010.01|本科|科技大学|光电工程\\n2010.01|2014.01|本科|科技大学|光电工程\\n2014.01|有限公司\\n2014.01|2016.04|有限公司'.encode(
        ...     'utf8')).hexdigest()
        >>> assert id['unique_id_hashdate'] == '2016.04'

        >>> cv_yaml = cv(xp)
        >>> cv_yaml.update({'education_history': [ed]})
        >>> id = unique_id(cv_yaml, '2015.01')
        >>> assert 1 == len(id['unique_id_hash'])
        >>> cv_yaml = cv(xp)
        >>> cv_yaml.update({'education_history': [ed]})
        >>> assert id == unique_id(cv_yaml, '2016.01')
    """
    if 'unique_id_hash' not in cv_yaml:
        cv_yaml['unique_id_hash'] = []
    for date, history in hash_history(cv_yaml, to_date):
        cv_yaml['unique_id_hash'].append((date, history))
    # Sort history hash value by hashdate
    if len(cv_yaml['unique_id_hash']) == 0:
        del cv_yaml['unique_id_hash']
    else:
        cv_yaml['unique_id_hash'] = sorted(cv_yaml['unique_id_hash'], key=lambda x: x[0])
    if 'unique_id' not in cv_yaml:
        try:
            cv_yaml['unique_id'] = cv_yaml['unique_id_hash'][-1][1]
            cv_yaml['unique_id_hashdate'] = cv_yaml['unique_id_hash'][-1][0]
        except KeyError:
            pass
        except IndexError:
            pass
    return cv_yaml
