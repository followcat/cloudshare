# -*- coding: utf-8 -*-
import re

import jieba

from extractor.utils_parsing import *


WORKEXPE =  u'((((((\d{1,2}((\-\d{1,2})|(\.\d))?)|(['+CHNUMBERS+u']{1,3})) *(年|(个月))(以[上下])?)|无)'+u'工作经验)|(应届(毕业)?生('+ASP+u'*经验)?))'
GEN = re.compile(u'^'+ASP+u'*-{3}[\- ]*'+ASP+u'*((个人信息)|(基本资料)|(\S*个人简历))?\n+'+ASP+u'*(?P<general>姓'+ASP+u'*名[:：]?.+?性'+ASP+u'*别[:：]?.*?)(?=\n'+ASP+u'*-{3}[\- ]*)$', re.DOTALL+re.M)
REVGEN = re.compile(u'^'+ASP+u'*(?P<general>姓'+ASP+u'*名[:：].+?性'+ASP+u'*别[:：].*?'+ASP+u'*-{3}[\- ]*\n+'+ASP+u'*((联系电话)|(电子邮件)|(年龄))[:：].*?)(?=\n+'+ASP+u'*-{3}[\- ]*)$', re.DOTALL+re.M)

GENFIELDS = (WORKEXPE, GENDER, AGEANDBIRTH, MARITALSTATUS, u'\d{3}cm', EDUCATION)
PIPEGENSEP = ASP+u'*\|?'+ASP+u'*)|('
PIPEGEN = re.compile(u'^'+ASP+u'*(?P<general>(('+PIPEGENSEP.join(GENFIELDS)+ASP+u'*\|?'+ASP+u'*)){2,6})', re.M)

SPGENSEP = ASP+u'{3}'+ASP+u'*'
SPGENFIELDS = (GENDER, AGEANDBIRTH, WORKEXPE, EDUCATION, u'('+MARITALSTATUS+u')?')
SPACEGEN = re.compile(u'^(?P<general>'+SPGENSEP.join(SPGENFIELDS)+u')', re.M)

LBLPIPEGENSEP = ASP+u'*\|?'+ASP+u'*'
LBLPIPEGEN = re.compile(u'^'+ASP+u'*'+PREFIX+u'*'+ASP+u'*(?P<general>姓名[:：]'+ASP+u'*.*?\|'+ASP+u'*'+LBLPIPEGENSEP.join(
    [GENDER, WORKEXPE, EDUCATION])+u')', re.M)

NAMEHEADER = re.compile(u'^.+'+UNIBRALEFT+GENDER+u'['+SENTENCESEP+u']'+ASP+u'*(?P<age>\d{2})'+UNIBRARIGHT+ASP+u'*$', re.M)
EXPECTATION = re.compile(u'期望((薪资)|([年月]薪))(（税前）)?[:：]'+ASP+u'*(?P<salary_expectation>'+SALARY+u')', re.M)
SALARYCURRENT = re.compile(u'目前((薪资)|([年月]薪))(（税前）)?[:：]'+ASP+u'*(?P<salary_current>'+SALARY+u')', re.M)

PLACETARGET = re.compile(u'((目标)|(期望))(工作)?地点[:：]'+ASP+u'*((不限)|(?P<places>'+PLACES+u'))', re.M)
PLACECURRENT = re.compile(u'((目前)|(所在))(工作)?地点?[:：]'+ASP+u'*((不限)|(?P<places>'+PLACES+u'))', re.M)

LABELGEND = re.compile(u'性'+ASP+u'*别[:：]?'+ASP+u'*'+GENDER, re.M)
LABELMARITAL = re.compile(u'婚姻状况[:：]?'+ASP+u'*'+MARITALSTATUS, re.M)


def format_salary(result, groupdict):
    if 'salary_months' in groupdict and groupdict['salary_months']:
        result['salary'] = fix_salary(groupdict['salary'])
        result['salary_months'] = groupdict['salary_months']
    elif 'salary' in groupdict and groupdict['salary']:
        result['salary'] = fix_salary(groupdict['salary'])
    elif 'yearly' in groupdict and groupdict['yearly']:
        result['yearly'] = fix_salary(groupdict['yearly']+u'/年')
    return result

places = lambda expectation:expectation['places']
yearly = lambda salary: salary['yearly']
salary = lambda salary: salary['salary']
expectation = lambda general: general['expectation']
current = lambda general: general['current']
age = lambda general: int(general['age'])
gender = lambda general: general['gender']
marital_status = lambda general: general['marital_status']

def extract_places(groupdict):
    u"""
        >>> assert u'珠海' == extract_places(PLACECURRENT.search(u'所在地：珠海').groupdict()).pop()
        >>> assert len(extract_places(PLACETARGET.search(u'目标地点：不限').groupdict())) == 0
        >>> assert u'北京' == extract_places(PLACETARGET.search(u'目标地点：北京').groupdict()).pop()
        >>> assert u'北京' == extract_places(PLACETARGET.search(u'目标地点：北京，上海').groupdict()).pop()
        >>> assert u'西安' == extract_places(PLACETARGET.search(u'目标地点：陕西-西安').groupdict()).pop()
        >>> assert u'东莞' == extract_places(PLACETARGET.search(u'目标地点：东莞-万江区').groupdict()).pop()
        >>> assert u'成都' == extract_places(PLACECURRENT.search(u'所在地：成都-双流县').groupdict()).pop()
        >>> assert u'苏州' == extract_places(PLACECURRENT.search(u'所在地：苏州-工业园').groupdict()).pop()

    In the following case, result from jieba cut is ('南', '城区'):
        >>> assert u'东莞' == extract_places(PLACETARGET.search(u'目标地点：东莞-南城区').groupdict()).pop()
    """
    places = set()
    check_next = False
    i = ''; j = ''
    if not groupdict['places']:
        return places
    for k in jieba.cut(groupdict['places']):
        if k == '-':
            check_next = True
            i = j
            j = ''
        elif k in SENTENCESEP+SEP:
            if check_next:
                if u'区' in j or u'县' in j:
                    places.add(i)
                elif u'省' in i:
                    places.add(j)
                elif len(j) > len(i):
                    places.add(i)
                else:
                    places.add(j)
                j = ''
                check_next = False
            elif j:
                places.add(j)
                j = ''
        else:
            j += k
    else:
        if check_next:
            if u'区' in j or u'县' in j:
                places.add(i)
            elif u'省' in i:
                places.add(j)
            elif len(j) > len(i):
                places.add(i)
            else:
                places.add(j)
        elif j:
            places.add(j)
    return places

def extract_general(groupdict):
    general = {}
    if 'age' in groupdict and groupdict['age']:
        general['age'] = groupdict['age']
    if 'birthdate' in groupdict and groupdict['birthdate']:
        general['birthdate'] = groupdict['birthdate']
    if 'gender' in groupdict and groupdict['gender']:
        general['gender'] = groupdict['gender']
    if 'marital_status' in groupdict and groupdict['marital_status']:
        general['marital_status'] = groupdict['marital_status']
    return general
    

def fix(d):
    u"""
        >>> assert u'元' in salary(salary(expectation(fix(u'期望月薪： 8000/月'))))
        >>> assert u'年' in yearly(salary(current(fix(u'目前薪资： 年薪 30-40万 人民币'))))
        >>> assert u'万' in yearly(salary(current(fix(u'目前薪资： 15-30W人民币'))))
        >>> assert u'元' in salary(salary(current(fix(u'目前薪资：月薪（税前）：25000 元 \* 15 个月'))))
        >>> assert not fix(u'期望地点：不限')
        >>> assert len(places(expectation(fix(u'3.  期望地点：湖南-长沙')))) == 1
        >>> assert len(places(expectation(fix(u'期望地点：   南昌,深圳,上海,广州')))) == 4
        >>> assert len(places(expectation(fix(u'目标地点： 东莞-南城区，东莞-莞城区，东莞-东城区，东莞-万江区')))) == 1
        >>> assert u'深圳' == places(current(fix(u'目前状态：   在职，看看新机会   所在地点：   深圳-南山区'))).pop()
        >>> assert gender(fix(u'''----\\n姓名：�  李  性别：�  男�\\n年龄：� 29 婚姻状况：�   已婚\\n----''')) == u'男'
        >>> assert gender(fix(u'''----\\n个人信息\\n姓名：     马        性别：       女\\n----''')) == u'女'
        >>> assert gender(fix(u'''----\\n基本资料\\n姓    名：    黄             性    别：    男\\n----''')) == u'男'
        >>> assert gender(fix(u'''----\\n罗个人简历\\n姓名    罗              性别       男      出生年月   1990年3月\\n----''')) == u'男'
        >>> assert gender(fix(u'''----\\n姓名：徐  性别：男\\n联系电话：10000000000  年龄： 27\\n----''')) == u'男'
        >>> assert gender(fix(u'姓名：苏  性别：女\\n------\\n联系电话：\\n----')) == u'女'
        >>> assert gender(fix(u'姓名：刘  性别：女\\n----\\n电子邮件：\\n----')) == u'女'
        >>> assert gender(fix(u'姓    名：   徐               性    别：   女\\n----\\n电子邮件：\\n----')) == u'女'
        >>> assert marital_status(fix(u'''姓名：赵 性别：男\\n----\\n联系电话：\\n婚姻状况：已婚\\n----''')) == u'已婚'
        >>> assert marital_status(fix(u'''----\\n姓名：常 性别：女\\n联系电话： \\n婚姻状况：已婚\\n----''')) == u'已婚'
        >>> assert gender(fix(u'5-7年工作经验 | 女 |  28岁（1988年1月4日）')) == u'女'
        >>> assert age(fix(u'16个月工作经验 | 女 |  24岁（1990年8月6日）')) == 24
        >>> assert gender(fix(u'三年以上工作经验 | 女 |  28岁（1986年3月15日）')) == u'女'
        >>> assert gender(fix(u'女 | 已婚 | 1982 年10月生')) == u'女'
        >>> assert gender(fix(u'男 | 1988年3月1日生 | 现居住于广东广州 | 中共党员')) == u'男'
        >>> assert marital_status(fix(u'女|6年工作经验|1989年8月|已婚')) == u'已婚'
        >>> assert marital_status(fix(u'10年以上工作经验 | 男 |  39岁（1976年4月4日） |  已婚 |  170cm |  无党派人士')) == u'已婚'
        >>> assert marital_status(fix(u'应届毕业生 | 男 |  22岁（1992年9月25日） |  未婚 |  170cm |  中共党员')) == u'未婚'
        >>> assert age(fix(u'应届生 经验 | 本科 | 男 | 未婚 | 24 岁 | 170cm | 团员 | 汉 |')) == 24
        >>> assert gender(fix(u'男    33岁(1983年12月)    9年工作经验    本科   ')) == u'男'
        >>> assert marital_status(fix(u'女    26岁(1990年7月)    4年工作经验    本科    未婚')) == u'未婚'
        >>> assert age(fix(u'  男    38岁(1977年6月)    12年工作经验    硕士    已婚')) == 38
        >>> assert gender(fix(u'姓名： 徐   |  男  |  15 年工作经验   | 硕士')) == u'男'
        >>> assert gender(fix(u'1.  姓名： 张   |  女  |  11 年工作经验   | MBA')) == u'女'
        >>> assert gender(fix(u'    1.  姓名： 蒋   |  女  |  7 年工作经验   | 硕士')) == u'女'
        >>> assert gender(fix(u'2.  3.  姓名： 杨   |  男  |  11 年工作经验   | 大专')) == u'男'
        >>> try:
        ...     assert not fix('?'*10000)
        ... except:
        ...     raise Exception("LBLPIPEGEN failed on time for fix('?'*10000)")
        >>> assert gender(fix(u'男 | 24岁(1990年6月17日) | 1年工作经验 | 173cm')) == u'男'
        >>> assert gender(fix(u'男 | 23岁(1991年2月14日) | 本科| 1年工作经验')) == u'男'
        >>> assert marital_status(fix(u'男 | 28岁(1986年10月5日) | 硕士| 一年以下工作经验 | 176cm | 未婚')) == u'未婚'
        >>> assert gender(fix(u'男 | 23岁(1991年7月12日) | 1年工作经验 | 未婚 |  O型')) == u'男'
        >>> assert age(fix(u'杨伟东 （男，26）\\n中山大学\\n')) == 26
        >>> assert marital_status(fix(u'杨伟东 （男，26）\\n中山大学\\n3.  婚姻状况：未婚')) == u'未婚'
        >>> assert not fix(u'·······························')
    """
    def fix_output(processed):
        result = processed
        return result

    current = {}
    processed = {}
    expectation = {}
    res = GEN.search(d)
    if res:
        m = LABELGEND.search(res.group('general'))
        if m:
            processed['gender'] = m.group('gender')
        m = LABELMARITAL.search(res.group('general'))
        if m:
            processed['marital_status'] = m.group('marital_status')
    elif REVGEN.search(d):
        m = LABELGEND.search(REVGEN.search(d).group('general'))
        if m:
            processed['gender'] = m.group('gender')
        m = LABELMARITAL.search(REVGEN.search(d).group('general'))
        if m:
            processed['marital_status'] = m.group('marital_status')
    if EXPECTATION.search(d):
        salary = {}
        expectation['salary'] = format_salary(salary, EXPECTATION.search(d).groupdict())
    if PLACETARGET.search(d):
        places = extract_places(PLACETARGET.search(d).groupdict())
        if places:
            expectation['places'] = list(places)
    if expectation:
        processed['expectation'] = expectation

    if SALARYCURRENT.search(d):
        salary = {}
        current['salary'] = format_salary(salary, SALARYCURRENT.search(d).groupdict())
    if PLACECURRENT.search(d):
        places = extract_places(PLACECURRENT.search(d).groupdict())
        if places:
            current['places'] = list(places)
    if current:
        processed['current'] = current

    if NAMEHEADER.search(d):
        processed.update(extract_general(NAMEHEADER.search(d).groupdict()))
        res = LABELMARITAL.search(d)
        if res:
            processed.update(extract_general(res.groupdict()))
    elif LBLPIPEGEN.search(d):
        processed.update(extract_general(LBLPIPEGEN.search(d).groupdict()))
    elif PIPEGEN.search(d):
        processed.update(extract_general(PIPEGEN.search(d).groupdict()))
    elif SPACEGEN.search(d):
        processed.update(extract_general(SPACEGEN.search(d).groupdict()))
    return fix_output(processed)
