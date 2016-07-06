# -*- coding: utf-8 -*-
import re


TODAY = u'((至今)|(目前)|(现在)|今|([Pp]resent)|([Nn]ow))'
CHNUMBERS = u'一二三四五六七八九十'
SP = u'\s\xa0\ufffd\u2028\u3000'
ASP = u'[' + SP + u']'
SEP = u'\-–—―\\\\·,~～/'
UNIBRALEFT = ur'[（\(\[【]'
UNIBRARIGHT = ur'[）\)\]】]'
DATESEP = u'['+SEP+SP+u'至]+'
DATE = ur'(?:(?:\d{4}'+ASP+u'?['+SEP+u'\.．年]'+ASP+u'{0,2}(?:(?:(?:(?:[01]\d{1})|(?:[1-9]{1}))('+ASP+u'?月)?)|(?:['+CHNUMBERS+u']{1,3}月)))|'+TODAY+')'
PERIOD = u'(?P<from>' + DATE + ur')' + DATESEP + ASP+ u'*(?P<to>' + DATE + ')'
DURATION = ur'(?P<duration>(\d{1,2}'+ASP+u'?年'+ASP+u'?(\d{1,2}'+ASP+u'?个月)?)|(\d{1,2}'+ASP+u'?个月))'
AGE = u'(?P<age>\d{2})'+ASP+u'?岁'
FULLDATE = u'(?:\d{4}[\.．年](?:(?:[01]\d{1})|(?:[1-9]{1}))[\.．月](?:(?:[0123]\d{1})|(?:[1-9]{1}))日)'
FIELDSEP = ur'、：:；;\|'
SENTENCESEP = FIELDSEP+ur'，。'

exclude_with_parenthesis = lambda x: u'('+UNIBRALEFT+u'[^（\(\[【' +x+ u']+?'+UNIBRARIGHT+ASP+u'*)'

CONTEXT = exclude_with_parenthesis(u'年月'+CHNUMBERS)
PREFIX = u'((\d+['+SENTENCESEP+u'\.]?'+ASP+u'*)|([◆·\?]+)|(\uf0d8\xa0))'

# Exclude date related characters to avoid eating duration
COMPANYTAIL = exclude_with_parenthesis(u'人年月')
# use re.DOTALL for better results
COMPANY = ur'[^' + SENTENCESEP + '=\n\*]+?('+COMPANYTAIL+u')?'
POSITION = ur'[^=\n\*：:\|]+'

education_list = {
    1: (u'中技', u'中专', u'高中'),
    2: (u'大专', ),
    #3: Show clearly step before graduate
    4: (u'本科', u'金融学学士', u'文学学士', u'全日制本科', u'统招本科', u'学士'),
    5: (u'在职硕士', ),
    6: (u'硕士', u'硕士研究生', u'研究生/硕士学位', u'MBA', u'MBA/EMBA'),
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
AGEANDBIRTH = AGE+ u'('+UNIBRALEFT+u'(?P<birthdate>' +FULLDATE+ u'|'+DATE+u')' +UNIBRARIGHT + u')?'

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

remove_escape = lambda x: x.group(1)
fix_escape = lambda x: re.compile(u'\\\\([_'+SEP+'])').sub(remove_escape, x)
fix_name = lambda x: re.compile(ASP+'+').sub(' ', fix_escape(x)).strip()
fix_duration = lambda x: re.compile(ASP+'+').sub('', x).strip()

ten_thousands = lambda x: re.compile(u'(?<=\d)'+ASP+u'*W').sub(u'万', x)
salary_unit = lambda x: re.compile(u'(?<=\d)/(?=[年月])').sub(u'元/', x)
fix_salary = lambda x: salary_unit(ten_thousands(re.compile(ASP+'+').sub('', x)))


WORKXP = PERIOD + ur'[:：\ufffd]?\s*' + UNIBRALEFT + DURATION + UNIBRARIGHT +ASP+ ur'*[：:\| ]*(?P<company>'+COMPANY+u')[：:\| ]*(?P<position>'+POSITION+u'?)$'
STUDIES = PERIOD+ ur'[:：\ufffd]?\s*' + u'(?P<school>'+COMPANY+u')[：:\| ]*(?P<major>'+POSITION+u'?)[：:\| ]*'+EDUCATION+u'?$'


