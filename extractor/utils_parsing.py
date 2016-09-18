# -*- coding: utf-8 -*-
import re
import time


TODAY = u'(?:(?:至今)|(?:目前)|(?:现在)|今|(?:[Pp]resent)|(?:[Nn]ow))'
CHNUMBERS = u'一二三四五六七八九十'
SP = u'\s\xa0\ufffd\u2028\u3000'
ASP = u'[' + SP + u']'
SEP = u'\-\u2013\u2014\u2015\u4e00\\\\·,~～/'
UNIBRALEFT = ur'[（\(\[【]'
UNIBRARIGHT = ur'[）\)\]】]'
DATESEP = u'['+SEP+SP+u'至]+'
_PDATE = ur'(?:(?:\d{4}'+ASP+u'?__DATE_SEP__'+ASP+u'{0,2}(?:(?:(?:(?:[01]\d{1})|(?:[1-9]{1}))(?:'+ASP+u'?月)?)|(?:['+CHNUMBERS+u']{1,3}月)))|'+TODAY+')'
FDSEP = u'(?P<fromsep>['+SEP+u'\.．年])'
DATE = _PDATE.replace('__DATE_SEP__', FDSEP.replace('P<fromsep>', ':'))
SDSEP = u'(?P=fromsep)'
PERIOD = u'(?P<from>' + _PDATE.replace('__DATE_SEP__', FDSEP) + ur')' + DATESEP + ASP+ u'*(?P<to>' + _PDATE.replace('__DATE_SEP__', SDSEP) + ')(?:'+UNIBRALEFT+u'含[^（\(\[【]+?期'+UNIBRARIGHT+u')?'
DURATION = ur'(?P<duration>(?:\-?\d{1,2}'+ASP+u'?年'+ASP+u'?(?:\d{1,2}'+ASP+u'?个月)?)|(?:(?:(?:\d{1,2})|(['+CHNUMBERS+u']{1,3}))'+ASP+u'?个月内?))'
AGE = u'(?P<age>\d{2})'+ASP+u'?岁'
FULLDATE = u'(?:\d{4}[\.．年](?:(?:[01]\d{1})|(?:[1-9]{1}))[\.．月](?:(?:[0123]\d{1})|(?:[1-9]{1}))日)'
FIELDSEP = ur'、：:；;\|'
ENDLINESEP = u'。'
SENTENCESEP = FIELDSEP+ENDLINESEP

exclude_with_parenthesis = lambda x: u'('+UNIBRALEFT+u'[^（\(\[【' +x+ u']+?'+UNIBRARIGHT+ASP+u'*)'

CONTEXT = exclude_with_parenthesis(u'年月'+CHNUMBERS)
PREFIX = u'((\d+['+SENTENCESEP+u'\.]?'+ASP+u'{2})|◆|·|\?|(\uf0d8\xa0)|\uf0b7|\uf075)'

# Exclude date related characters to avoid eating duration
COMPANYTAIL = exclude_with_parenthesis(u'人年月')
# use re.DOTALL for better results
# \u2014, \u2015 and \u4e00 are found in company
COMPANY = ur'([^' + SENTENCESEP + u'=\n\*\u2013]+?(\\\\\*)+)?(((\\\\\*){3})|([^' + SENTENCESEP + u'=\n\*\u2013]+?))('+COMPANYTAIL+u')?'
SENTENCESEP = SENTENCESEP+ur'，'
POSITION = ur'[^=\n\*：:\|\u2013\u2015]+'

education_list = {
    0: (u'初中', ),
    1: (u'中技', u'中专', u'高中', u'高职'),
    2: (u'大专', ),
    #3: Show clearly step before graduate
    4: (u'本科', u'金融学学士', u'文学学士', u'全日制本科', u'统招本科', u'学士'),
    5: (u'在职硕士', ),
    6: (u'硕士', u'硕士研究生', u'研究生/硕士学位', u'MBA', u'MBA/EMBA', u'EMBA'),
    7: (u'博士', u'博士研究生'),
    8: (u'博士后', )
    }

LIST_SEPARATOR = u')|(?:'
EDUCATION_LIST = {}
for k,v in education_list.items():
    EDUCATION_LIST[k] = re.compile(u'(?:(?:'+ LIST_SEPARATOR.join(v) +u'))')
EDUCATION = u'(?P<education>(?:'+ LIST_SEPARATOR.join([u'(?:(?:'+ LIST_SEPARATOR.join(v) +u'))' for v in education_list.values()]) +u'))'
SCHOOL = u'(?P<school>(\s?\w)+|([^'+SP+FIELDSEP+u']+'+ASP+u'*'+exclude_with_parenthesis('')+u'?))'

GENDER = u'(?P<gender>男|女)'
MARITALSTATUS = u'(?P<marital_status>(未婚)|(已婚))'
AGEANDBIRTH = u'('+AGE+ u'|((?P<abbr>'+UNIBRALEFT+u')?(?P<birthdate>' +FULLDATE+ u'|'+DATE+u')生?(?(abbr)' +UNIBRARIGHT + u')))+'

SALARY = u'((月薪(（税前）)?[:：]?)?'+ASP+u'*((?P<salary>\d[\- \d\|]*(月/月)?((元/月)|元|(/月))(以[上下])?)'+ASP+u'*(\\\\\*'+ASP+u'*(?P<salary_months>\d{1,2})'+ASP+u'?个月)?)|((年薪(（税前）)?[:：]?)?'+ASP+u'*(?P<yearly>\d[\- \d\|]*[万W])'+ASP+u'*人民币))'
EMPLOYEES = u'((?P<employees>(少于)?\d[\d '+SEP+u']*人(以[上下])?)([' + SENTENCESEP + u'].*?)?)'
BEMPLOYEES = u'('+ UNIBRALEFT +ASP+u'*' + EMPLOYEES + UNIBRARIGHT +u')'
BDURATION = u'(((?P<br>(?P<dit>\*)?'+UNIBRALEFT+u')|(\*\-{3}\*))[\n'+SP+u']*' + DURATION + u'(?(br)[\n'+SP+u']*' +UNIBRARIGHT + u'(?(dit)\*)))'

PLACES = u'(?:(\S+)['+SENTENCESEP+SEP+']?)+'

fix_today = lambda x: re.compile('^'+TODAY+'$').sub(u'至今', x)
fix_sep = lambda x: re.compile(u'['+SP+SEP+u'\.．年]+').sub('.', x)
fix_trail = lambda x: x.replace(u'月', '').strip()
zero_date = lambda x: str.zfill(str(x.group()), 2)
fix_trailing = lambda x: re.compile(ur'\d+$').sub(zero_date, x)
fix_date = lambda x: fix_trailing(fix_sep(fix_trail(fix_today(x))))

fix_star = lambda x: x.replace('\*', '*')
remove_escape = lambda x: x.group(1)
fix_escape = lambda x: re.compile(u'\\\\([_'+SEP+'])').sub(remove_escape, fix_star(x))
fix_name = lambda x: re.compile(ASP+'+').sub(' ', fix_escape(x)).strip()
fix_duration = lambda x: re.compile(ASP+'+').sub('', x).strip()

ten_thousands = lambda x: re.compile(u'(?<=\d)'+ASP+u'*W').sub(u'万', x)
salary_unit = lambda x: re.compile(u'(?<=\d)/(?=[年月])').sub(u'元/', x)
fix_salary = lambda x: salary_unit(ten_thousands(re.compile(ASP+'+').sub('', x)))


WORKXP = PERIOD + ur'[:：\ufffd]?\s*' + UNIBRALEFT + DURATION + UNIBRARIGHT +ASP+ ur'*[：:\| ]*(?P<company>'+COMPANY+u')[：:\| ]*(?P<position>'+POSITION+u'?)$'
STUDIES = PERIOD+ ur'[:：\ufffd]?\s*' + u'(?P<school>'+COMPANY+u')[：:\| ]*(?P<major>'+POSITION+u'?)[：:\| ]*'+EDUCATION+u'?$'

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
    if date_from == u'至今':
        return u'一个月内'
    break_date = lambda x: tuple([int(i) for i in x.split('.')])
    time_from = time.mktime(break_date(date_from)+(1,0,0,0,0,0,0))
    if date_to == u'至今':
        time_to = time.time()
    else:
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
    if period_year < 0:
        duration = None
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

