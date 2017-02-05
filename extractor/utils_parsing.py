# -*- coding: utf-8 -*-
import re
import time

import sources.industry_id


TODAY = u'(?:(?:至今)|(?:目前)|(?:现在)|今|(?:[Pp]resent)|(?:[Nn]ow))'
CHNUMBERS = u'一二三四五六七八九十'
SP = u'\s\xa0\ufffd\u2028\u3000'
ANL = u'(?:^>|\n)'
ESP = u'[' + SP + u']'
POESP = ESP.replace('\s', ' \t')
ASP = u'(?:^>|\\\\\n|[' + SP + u'])'
POASP = ASP.replace('\s', ' \t')
SEP = u'\-\uff0d\u2013\u2014\u2015\u4e00\\\\·,~～/'
UNIBRALEFT = u'(?:[（\(\[【]|\\\\[\(\[])'
UNIBRARIGHT = u'(?:[）\)\]】]|\\\\[\)\]])'
DATESEP = u'['+SEP+SP+u'至]+'
_CHPDATE = ur'(?:\d{4}'+ASP+u'?__DATE_SEP__'+ASP+u'{0,2}(?:(?:(?:(?:[01]\d{1})|(?:[1-9]{1}))(?:'+ASP+u'?月)?)|(?:['+CHNUMBERS+u']{1,3}月)))'
MONTH_MATCHING = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
        }
ENMONTH = r'(?:'+'|'.join(MONTH_MATCHING)+')'
ENPDATE = ur'(?:'+ENMONTH+ASP+'*\d{4})'
_PDATE = ur'(?:'+_CHPDATE+'|'+ENPDATE+'|'+TODAY+')'
FDSEP = u'(?P<fromsep>['+SEP+u'\.．年])'
DATE = _PDATE.replace('__DATE_SEP__', FDSEP.replace('P<fromsep>', ':'))
SDSEP = u'(?P=fromsep)'
PERIOD = u'(?P<from>' + _PDATE.replace('__DATE_SEP__', FDSEP) + ur')' + DATESEP + ASP+ u'*(?P<to>' + _PDATE.replace('__DATE_SEP__', SDSEP) + ')(?:'+UNIBRALEFT+u'含[^（\(\[【]+?期'+UNIBRARIGHT+u')?'
CHDURATION = ur'(?:(?:\-?\d{1,2}(?:\.\d)?'+ASP+u'?年'+ASP+u'?(?:\d{1,2}'+ASP+u'?个月)?)|(?:(?:(?:\d{1,2})|(?:['+CHNUMBERS+u']{1,3}))'+ASP+u'?个月内?))'
ENDURATION = ur'(?:(?:\d{1,2}'+ASP+u'?years?'+ASP+u'?)?(?:(?:\d{1,2})'+ASP+u'?months?))'
DURATION = ur'(?P<duration>'+CHDURATION+'|'+ENDURATION+')'
AGE = u'(?P<age>\d{2})'+ASP+u'?岁'
FULLDATE = u'(?:\d{4}[\.．年](?:(?:[01]\d{1})|(?:[1-9]{1}))[\.．月](?:(?:[0123]\d{1})|(?:[1-9]{1}))日)'
FIELDSEP = ur'、：:；;\|\uff5c'
ENDLINESEP = u'。'
SENTENCESEP = FIELDSEP+ENDLINESEP
EDUFIELDSEP = u'，'+FIELDSEP

exclude_with_parenthesis = lambda x: u'(?:'+UNIBRALEFT+u'[^（\(\[【' +x+ u']+?'+UNIBRARIGHT+ASP+u'*)'

CONTEXT = exclude_with_parenthesis(u'年月'+CHNUMBERS)
PREFIX = u'(?:(?:(?:\d+(?:['+SENTENCESEP+u'\.]|'+ASP+u'{2}))|\- {3}|#|◆|■|·|\?|\uf0d8\xa0|\uf0b7|\uf075|\u258c)|'+POASP+u')'

LIST_SEPARATOR = u')|(?:'
COMPANY_BUSINESS_KEYWORD = u'((?:'
postfix = ''
for v in sources.industry_id.sources.values():
    COMPANY_BUSINESS_KEYWORD += postfix
    COMPANY_BUSINESS_KEYWORD += LIST_SEPARATOR.join([_.replace('(','\(').replace(')','\)') for _ in v])
    postfix = LIST_SEPARATOR
COMPANY_BUSINESS_KEYWORD += u'))'
BUSINESSTRAIL = u'[^\*\|\n\- （\(\[【]{1,11}'
COMPANY_BUSINESS = u'(?:(?P<business>(?:'+COMPANY_BUSINESS_KEYWORD+u'('+BUSINESSTRAIL+u')?(?:'+exclude_with_parenthesis(u'\|\n\- ')+u')?)+)|其他)'

COMPANY_TYPE_KEYWORD = u'外商|企业|外企|合营|事业单位|上市|机关|合资|国企|民营|外资\([非欧美]+\)|代表处|股份制'
COMPANY_TYPE = u'(?:(?:[^/\|\n\- ：]*?(('+COMPANY_TYPE_KEYWORD+u')[^\|\n\- ]*)+)|其他)'

# Exclude date related characters to avoid eating duration
COMPANYTAIL = u'(?:、[^' + SENTENCESEP + u'=\n\*\u2013◆■]+?)?'+exclude_with_parenthesis(u'人年月')
# use re.DOTALL for better results
# \u2014, \u2015 and \u4e00 are found in company
COMPANY = u'(?:\\\\\*|(?:[^' + SENTENCESEP + u'=\n\*\u2013◆■]+?(?:(?:\\\\)?\*(?=(?!'+POASP+u')))+)?(?:(?:(?:\\\\\*){3})|(?:[^' + SENTENCESEP + u'=\n\*\u2013◆■]+?))(?:'+COMPANYTAIL+u')?)'
SENTENCESEP = SENTENCESEP+ur'，'
POSITION = ur'[^=\n\*：:\|\u2013\u2015\u3002]+'

JYCVSRC = re.compile(u'^(英文简历\n)?(?: {2}\-{3,}\n)(?: {4}\-{3,}\n)(?: {6}\-{3,}\n)(?: {8}\-{3,}\n)(?: {8}精英网用户\n)?')
NLPCVSRC = re.compile(u'^'+ASP+u'*-{9}[-'+SP+u']+\n+(.+\n+)?简历编号：'+ASP+u'*\S+'+ASP+u'*最新登录：'+ASP+u'*\S+'+ASP+u'*-{9}[-'+SP+u']+\n')
LPCVSRC = re.compile(u'^(:?(个人信息\n(?:离职，正在找工作 ，|在职(，急寻新工作 ，|，看看新机会 ，|，暂无跳槽打算。)))|(Personal Information\n(On job, open for new job|Dimission, seeking for new job) ,)) ， ', re.M)
ZLCVSRC = re.compile(u'^\t*(简历ID：RCC|Resume ID：REC)00\d{8}\n'+ASP+u'*[^\n\uf0b7]')
YCCVSRC = re.compile(u'^更新时间：(\d{4}-\d{2}-\d{2}|今天|昨天)\n(简历编号：)?')

is_jycv = lambda cv:JYCVSRC.search(cv)
is_lpcv = lambda cv:LPCVSRC.search(cv)
is_nlpcv = lambda cv:NLPCVSRC.search(cv)
is_zlcv = lambda cv:ZLCVSRC.search(cv)
is_yccv = lambda cv:YCCVSRC.search(cv)

education_list = {
    0: (u'初中', u'初中及以下'),
    1: (u'中技', u'中专', u'高中', u'高职'),
    2: (u'大'+POASP+u'{0,3}专', ),
    #3: Show clearly step before graduate
    4: (u'本'+POASP+u'{0,3}科', u'学'+POASP+u'士', u'\S{0,5}(?P<shorted4>学士)', u'全日制本科', u'统招本科', "Bachelor's degree", 'B.S.E'),
    5: (u'在职硕士', ),
    6: (u'硕'+POASP+u'{0,3}士', u'\S{0,5}(?P<shorted6>硕士)', u'硕士研究生', u'研究生/硕士学位', u'MBA', u'MBA/EMBA', u'EMBA', "Master's degree"),
    7: (u'博'+POASP+u'{0,3}士', u'\S{0,5}(?P<shorted7>博士)', u'博士研究生'),
    8: (u'博士后', )
    }

EDUCATION_LIST = {}
for k,v in education_list.items():
    EDUCATION_LIST[k] = re.compile(u'(?:(?:'+ LIST_SEPARATOR.join([_v+u'(学位)?' for _v in v]) +u'))')

def education_rate(education):
    u"""
        >>> assert 0 == education_rate(u'初中')
        >>> assert education_rate(u'本科') > education_rate(u'大专')
        >>> assert education_rate(u'硕士') == education_rate(u'EMBA')
    """
    for (k, RE) in EDUCATION_LIST.items():
        if RE.match(education):
            return k
    else:
        return 0

BROKENOLELINK = u'\[\]{#[^}]+}'
EDUCATION = u'(?P<education>(?:'+ LIST_SEPARATOR.join([u'(?:(?:'+ LIST_SEPARATOR.join([_v+u'(学位)?' for _v in v]) +u'))' for v in education_list.values()]) +u'))'
SCHOOL = u'(?:[^'+SP+EDUFIELDSEP+u']+['+EDUFIELDSEP+u'])?(?P<schbr>'+UNIBRALEFT+u')?(?P<school>(?(schbr)[^）\)\]】]+|((\s?\w)+|([^'+SP+EDUFIELDSEP+u'）\)\]】]+'+ASP+u'*'+exclude_with_parenthesis('')+u'?))))(?(schbr)'+UNIBRARIGHT+u')'+exclude_with_parenthesis(SP)+u'?'
MAJOR = u'(?P<majbr>'+UNIBRALEFT+u')?(?P<major>(?(majbr)[^）\)\]】]+|[^'+EDUFIELDSEP+u'\n）\)\]】]+?))(?(majbr)'+UNIBRARIGHT+u')'+exclude_with_parenthesis(SP)+u'?'

GENDER = u'(?P<gender>男|女)'
MARITALSTATUS = u'(?:(?P<marital_status>未婚|已婚)|保密)'
AGEANDBIRTH = u'('+AGE+ u'|((?P<abbr>'+UNIBRALEFT+u')?(?P<birthdate>' +FULLDATE+ u'|'+DATE+u')生?(?(abbr)' +UNIBRARIGHT + u')))+'

SALARY = u'(?:(?P<salarylabel>月薪(?:（税前）)?[:：]?)?'+ASP+u'*(?:(?P<salary>\d[\-到 \d\|]*(?:月/月)?(?(salarylabel)(?:(?:元'+ASP+u'*/'+ASP+u'*月)|>元|(?:/月))?|(?:(?:元'+ASP+u'*/'+ASP+u'*月)|元|(?:/月)))(?:以[上下])?)'+ASP+u'*(?:\\\\\*'+ASP+u'*(?P<salary_months>\d{1,2})'+ASP+u'?个月)?|保密)|(?:(?:年薪(?:（税前）)?[:：]?)?'+ASP+u'*(?P<salary_yearly>\d[\- \d\|]*[万W])'+ASP+u'*人民币))'

EMPLOYEES = u'((?:(?P<employees>(少于)?\d+([ '+SEP+u']+(?:(?<= )-0 )?\d+)?'+ASP+u'*人(以[上下])?)|未填写))'
BEMPLOYEES = u'('+ UNIBRALEFT +ASP+u'*' + EMPLOYEES + u'(['+FIELDSEP+u']('+COMPANY_TYPE+u'))?' +ASP+u'*' + UNIBRARIGHT +u')'
BEMPLOYEES = u'('+ BEMPLOYEES + u'('+BEMPLOYEES.replace('P<employees>', ':')+u')?)'
BDURATION = u'(((?P<br>(?P<dit>\*)?'+UNIBRALEFT+u')|(\*\-{3}\*))[\n'+SP+u']*' + DURATION + u'(?(br)[\n'+SP+u']*' +UNIBRARIGHT + u'(?(dit)\*)))'

PLACES = u'(?:(\S+)['+SENTENCESEP+SEP+']?)+'


MONTH_ID = re.compile('(?P<emonth>'+ENMONTH+')')

def date_to_ch(x):
    try:
        month, year = x.split(' ')
        return ' '.join((year, str(MONTH_MATCHING[MONTH_ID.search(month).group('emonth')])))
    except ValueError:
        return x
    except AttributeError:
        return x

asplstrip = lambda x: re.compile(u'^'+ASP+'+', re.M).sub('', x)
asprstrip = lambda x: re.compile(ASP+'+$', re.M).sub('', x)
aspstrip = lambda x: asprstrip(asplstrip(x))

month_to_str = lambda x: str.zfill(str(x), 2)
fix_today = lambda x: re.compile('^'+TODAY+'$').sub(u'至今', x)
fix_sep = lambda x: re.compile(u'['+SP+SEP+u'\.．年]+').sub('.', x)
fix_trail = lambda x: x.replace(u'月', '').strip()
zero_date = lambda x: month_to_str(x.group())
fix_trailing = lambda x: re.compile(ur'\d+$').sub(zero_date, x)
fix_date = lambda x: fix_trailing(fix_sep(date_to_ch(fix_trail(fix_today(x)))))

decimal_repl = lambda x: compute_duration('0.0',str(round(float(x.group('year'))/10*12-float(x.group('year'))//1*.2,1)))
fix_decimal = lambda x: re.compile(u'(?P<year>\d+\.\d)年').sub(decimal_repl, x)
duration_to_ch = lambda x: re.compile('months?').sub(u'个月', re.compile('years?').sub(u'年',x))
fix_duration = lambda x: re.compile(ASP+'+').sub('', fix_decimal(duration_to_ch(x)))

fix_prefix = lambda x: aspstrip(re.compile(PREFIX).sub('', x)).strip('*')
fix_star = lambda x: x.replace('\*', '*')
remove_escape = lambda x: x.group(1)
fix_escape = lambda x: re.compile(u'\\\\([_'+SEP+'])').sub(remove_escape, fix_star(x))
fix_name = lambda x: re.compile(ASP+'+').sub(' ', aspstrip(fix_escape(x)))
fix_position = lambda x: fix_name(x).replace('*', '')

range_repl = lambda x: x.group('low')+'-'+x.group('high')+u'元/月'
salary_range = lambda x: re.compile(u'(?P<low>\d+)到(?P<high>\d+)').sub(range_repl, x)
ten_thousands = lambda x: re.compile(u'(?<=\d)'+ASP+u'*W').sub(u'万', x)
salary_unit = lambda x: re.compile(u'(?<=\d)/(?=[年月])').sub(u'元/', x.replace(u'月/月', ''))
fix_salary = lambda x: salary_unit(ten_thousands(salary_range(aspstrip(x).replace(' ', ''))))

fix_range = lambda x: x.replace(' -0 ', '')
fix_people = lambda x: re.compile(ASP+u'+人').sub(u'人', x)
fix_employees = lambda x: re.compile(u'[ '+SEP+u']+').sub(u'-', fix_people(fix_range(x)))

fix_education = lambda x: re.compile(ASP+'+').sub('', aspstrip(x))

WORKXP = PERIOD + ur'[:：\ufffd]?\s*' + UNIBRALEFT + DURATION + UNIBRARIGHT +ASP+ ur'*[：:\| ]*(?P<company>'+COMPANY+u')[：:\| ]*(?P<position>'+POSITION+u'?)$'
STUDIES = PERIOD+ ur'[:：\ufffd]?\s*' + u'(?P<school>'+COMPANY+u')[：:\| ]*(?P<major>'+POSITION+u'?)[：:\| ]*'+EDUCATION+u'?$'

heading = lambda x: x+u'(?:\n-{3,}$)?'


break_date = lambda x: tuple([int(i) for i in x.split('.')])

def returns_with_time(command, name, arg):
    try:
        start = time.time()
        command(arg)
        return time.time() - start
    except KeyboardInterrupt:
        end = time.time()
        raise Exception("Command with arg '%s' interrupted after: %i min %i sec" %
                (name, divmod(end-start,60)[0], divmod(end-start,60)[1]))
        return 0.

def compute_period(date_from, date_to, today=u'至今'):
    u"""
        >>> assert (11, -1) == compute_period('2002.08', '2002.07')
        >>> assert (2, 4) == compute_period('2002.08', '2006.10')
        >>> assert (0, -1) == compute_period(u'至今', '2006.10')
    """
    if date_from == u'至今':
        if date_to == u'至今':
            return (0, 0)
        else:
            return (0, -1)
    if '.' not in date_from:
        date_from += '.09'
    time_from = time.mktime(break_date(date_from)+(1,0,0,0,0,0,0))
    if date_to == u'至今':
        if today == u'至今':
            time_to = time.time()
        else:
            time_to = time.mktime(break_date(today)+(1,0,0,0,0,0,0))
    else:
        if '.' not in date_to:
            date_to += '.06'
        time_to = time.mktime(break_date(date_to)+(1,0,0,0,0,0,0))
    duration_tuple = time.gmtime(time_to - time_from)
    zerotime_tuple = time.gmtime(0)
    if zerotime_tuple[1] > duration_tuple[1]:
        year_offset = 1
        period_month = duration_tuple[1]+12 - zerotime_tuple[1]
    else:
        year_offset = 0
        period_month = duration_tuple[1] - zerotime_tuple[1]
    period_year = duration_tuple[0] -  zerotime_tuple[0] - year_offset
    return (period_month, period_year)


def compute_duration(date_from, date_to):
    u"""
        >>> print(compute_duration(u'至今', '2006.10'))
        一个月内
        >>> print(compute_duration('2002.08', '2006.10'))
        4年2个月
        >>> print(compute_duration('2014.08', u'至今')) #doctest: +ELLIPSIS
        2年...
        >>> print(compute_duration('2011.09', '2014.08'))
        2年11个月
        >>> print(compute_duration('2012.12', '2013.09'))
        9个月
        >>> print(compute_duration('2014.03', '2016.03'))
        2年
    """
    (period_month, period_year) = compute_period(date_from, date_to)
    if period_year < 0:
        duration = u'一个月内'
    elif period_year == 0:
        if period_month <= 0:
            duration = u'一个月内'
        else:
            duration = u'%d个月' % period_month
    else:
        if period_month <= 0:
            duration = u'%d年' % period_year
        else:
            duration = u'%d年%d个月' % (period_year, period_month)
    return duration

def add_months(date, increment):
    u"""
        >>> assert u'至今' == add_months(u'至今', 3)
        >>> assert '2017.02' == add_months('2016.11', 3)
        >>> assert '2016.02' == add_months('2014.11', 15)
    """
    if date == u'至今':
        return date
    if '.' not in date:
        date += '.01'
    year, month = break_date(date)
    year_inc, month_inc = divmod(increment, 12)
    month += month_inc
    year += year_inc
    if month > 12:
        month -= 12
        year += 1
    return '.'.join((str(year), month_to_str(month)))
