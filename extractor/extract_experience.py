# -*- coding: utf-8 -*-
import re
import functools
try:
    import regex
except ImportError:
    setattr(re, 'ASCII', 0)
    regex = re

import sources.industry_id

from extractor.utils_parsing import *
import extractor.project
import extractor.unique_id


BTXPSEP = ASP+u'*'
BTXP = re.compile(u'^(?:'+BTXPSEP.join((u'工作经历', u'工作时间', u'单位名称', u'职位名称', u'所属部门'))+u')'+ASP+u'*(?P<expe>.*?)(?:培训经历|教育情况)', re.M+re.DOTALL)
XPTITLE = TITLE('experience')
XP = re.compile(SECTION('experience')+u'(?=^'+PREFIX+u'*'+REMAINING_SECTIONS('experience') +u')', re.DOTALL+re.M)
AXP = re.compile(ur'^'+SECTION('experience'), re.DOTALL+re.M)
TXP = re.compile(ur'-{9}[\-'+SP+u']*(?P<expe>'+PERIOD+ur'.*?)(?=-{9}[\-'+SP+u']*)', re.DOTALL)
PRXP = re.compile(ur'^'+PREFIX+u'*'+ XPTITLE +POASP+u'*\n+'+BORDERTOP('xpborder')+u'?(?P<expe>.*?)'+BORDERBOTTOM('xpborder')+u'^'+PREFIX+u'*(?='+POASP+u'*'+ BRACKETTOP('xptrailparens') +u'?\**((项'+POASP+u'?目经[验历]'+POASP+u'*'+ASP+u'+'+ANONPERIOD+u')|(((教'+POASP+u'?育)|(培'+POASP+u'?训))'+POASP+u'?((经'+POASP+u'?[历验])|(背景)|((?P<slash>/)?培训(?(slash)背景))))|Resume)'+ POASP +'*\**' + BRACKETBOTTOM('xptrailparens') +u'[:：]?'+POASP+u'*$' +u')', re.DOTALL+re.M)

PXP = re.compile(ur'^'+PREFIX+u'*'+ BRACKETTOP('projparens') +u'?\**项目经历'+ BRACKETBOTTOM('projparens') +u'(?P<expe>.*?)^'+PREFIX+u'*(?='+ BRACKETTOP('projtrailparens') +u'?\**(((教'+POASP+u'?育))'+POASP+u'?((经'+POASP+u'?[历验])|(背景)|(培训)))'+ POASP +'*\**' + BRACKETBOTTOM('projtrailparens') +u')', re.DOTALL+re.M)
EXP = re.compile(ur'^'+PREFIX+u'*'+ASP+u'*'+ BRACKETTOP('xpparens') +u'?\**(?:Work )?Experience\**'+ BRACKETBOTTOM('xpparens') +u'(?P<expe>.*?)^'+PREFIX+u'*'+ASP+u'*(?='+ BRACKETTOP('xptrailparens') +u'?(?:Languages|Skills|Education)'+ BRACKETBOTTOM('xptrailparens') +u')', re.DOTALL+re.M)


no_project_detail = lambda STR: u'(?<!(?:(?:职责|工作)(?:描述|内容)|项目成就)：\n{2})' + STR + u'(?!\n{2}['+SP+u']{2,}主要成就：)'

# Allow multiline once in company name when duration is present
# As company has at least one char, need to handle break just as company tail
# Catching all employees is too expensive on parenthesis repetition, some will be post processed
ECO = re.compile(u'^'+heading(PREFIX+u'*(?P<position>(\S[\S ]+\n)*)\n+')+heading(PREFIX+u'*(?P<company>(\S[\S ]+\n)*)\n+') + PERIOD +ASP+u'*' + BDURATION, re.M+re.DOTALL)
CO = re.compile(heading(PERIOD+ur'\**(('+ASP+u'?[:：'+SP+u'])|([:：]?))(?:'+ASP+u'*'+BROKENOLELINK+u')?'+ASP+u'*\**(?P<company>'+COMPANY+u'(\n'+COMPANYTAIL+u')?)\**'+POASP+u'*'+BEMPLOYEES+'?\**'+ASP+u'*\**'+BDURATION+POASP+u'*\**'+POASP+u'*$(?=(?<!\\\\)\n)'), re.DOTALL+re.M)
CCO = re.compile(heading(PERIOD+ur'\**(('+ASP+u'?[:：'+SP+u'])|([:：]?))(?:'+ASP+u'*'+BROKENOLELINK+u')?'+ASP+u'*\**(?P<company>'+COMPANY+u'(\n'+COMPANY+u')?)\**'+POASP+u'*'+BEMPLOYEES+'?\**'+ASP+u'*\**'+BDURATION+POASP+u'*\**'+POASP+u'*$(?=(?<!\\\\)\n)'), re.DOTALL+re.M)
TCO = re.compile(no_project_detail(u'^'+heading(PREFIX+u'*'+CONTEXT+u'?'+POASP+u'*\**'+PERIOD+ur'\**(('+ASP+u'?[:：'+SP+u'])|([:：]?))(?:'+ASP+u'*'+BROKENOLELINK+u')?'+ASP+u'*\**(?P<company>'+COMPANY+u')\**'+POASP+u'*'+BEMPLOYEES+'?\**('+ASP+u'*\**'+BDURATION+'\**)?'+POASP+u'*$(?=(?<!\\\\)\n)')), re.DOTALL+re.M)
PCO = re.compile(heading(PERIOD+ur'(('+ASP+u'?[:：'+SP+u']'+ASP+u'*)|([:：]?'+ASP+u'*\**))(?P<company>'+COMPANY+u'(\n(('+COMPANY+u')|('+COMPANYTAIL+u')))?)\**'+ASP+u'*\|('+ASP+u'*(?P<dpt>\S+)'+ASP+u'*\|)?'+ASP+u'*(?P<position>'+POSITION+u'?)'+ASP+u'*'+BDURATION+u'(?:\\\\)?$'), re.DOTALL+re.M)

PJCO = re.compile(u'^'+PREFIX+u'*'+PERIOD+ASP+u'*(?P<project>'+PROJECT+u')\n('+ASP+u'*项目职务[:：]?'+ASP+u'*(?P<position>'+POSITION+u'))?'+ASP+u'*所在公司[:：]?'+ASP+u'*(?P<company>'+COMPANY+u')(?:\\\\)?$', re.M)

# Avoid conflict in group names when combining *CO and *PO
AEMPLOYEES = EMPLOYEES.replace('employees', 'aemployees')
APERIOD = PERIOD.replace('from', 'afrom').replace('to', 'ato')
ASALARY = SALARY.replace('salary', 'asalary')
ACOMPANY_BUSINESS = COMPANY_BUSINESS.replace('business', 'abusiness')
ABDURATION = BDURATION.replace('duration', 'aduration').replace('br', 'abr').replace('dit', 'adit')

AAEMPLOYEES = EMPLOYEES.replace('employees', 'aaemployees')
AASALARY = SALARY.replace('salary', 'aasalary')

__PROJECT__ = u'\**(?:项目经验)[:：]\**'
__ACHIEVEMENT__ = u'\**(?:(?:主要)?工作|重点)业绩(?:[及和]成果|Performance|Main Achievements)?[:：]?\**'
__DEPARTMENT__ = u'\**(?:所[属在]部'+POASP+u'*门|科室|Department)[:：]?\**'
__CODESCRIPTION__ = u'(?P<desclabel>(?:公司|企业)(?:描述|介绍|简介|背景)[:：]?)'
__CODEPARTMENT__ = u'(?P<codptlbl>'+__DEPARTMENT__+u')'
__COEMPLOYEES__ = u'(?P<employlabel>(公司)?规模[:：]?)'
__POSALARY__ = u'\**(?:薪酬[情状]况|(?:职位)?月薪(?:[\(（]税前[\)）])?)[:：]?\**'
__PODESCRIPTION__ = u'\**(?:'+ITEM_PREFIX+u')?(?:工作(?:描述|简介|内容)|Job Description)[:：]?\**'
__PORESPONSIBILITY__ = u'\**(?:(?:目前)?(?:主要|工作)*职'+POASP+u'*责(?:(?:[及和与](?:业绩|技能)|及其成果)|业绩|描述)?|Responsibilities)[:：]?\**'

# Don't use (?(label) ...|...) as they are defined through all repetitions
company_items = {
    'place': ((u'(?:所在地区|工作地点)[:：]?', u'\S*?(?=[__SEP__])'), ),
    'position': ((u'职位(?:名称)?[:：]', POSITION),),
    'company_type': ((u'(?P<typelabel>(单位|企业|公司)性质[:：]?)', u'('+COMPANY_TYPE+u'|[^__SEP__]*?(?=[__SEP__]))'),
        COMPANY_TYPE),
    'company_business': ((u'(?P<businesslabel>(?:单位|所属|公司)行业[:：]?)', u'(?P<nl>['+ANL+u']+'+POASP+u'*)?('+ACOMPANY_BUSINESS+u'|\S*?(?='+POASP+u'*[__SEP__]))', POASP+u'*'),
        u'(?:'+COMPANY_BUSINESS+u'|(?<=[^__SEP__])'+POASP+u'*(?=(?!'+COMPANY_TYPE+u'))'+BUSINESSTRAIL+u'(?='+POASP+u'*[__SEP__]))'),
    'company_department': ((__CODEPARTMENT__, u'(?(codptlbl)\S*|\S+?[部处室册科](?='+POASP+u'*$))'), ),
    'branch': ((u'行业类别[:：]?', u'.*?(?=[__SEP__])'), ),
    'company_employees': ((__COEMPLOYEES__, AEMPLOYEES), ),
    'recommendations': ((u'同事认证[:：]?', u'\d+'), ),
    'company_description': ((__CODESCRIPTION__,
                     u'[^:：__SEP__(?:\\\\\n)]*(?:(?:\\\\\n>?)+[^:：__SEP__(?:\\\\\n)]+)*(?=[__SEP__^])'), )
    }
key_company_items = company_items.copy()

# Special handling for 部门 and 职位 with no [:：]: following space and value are enforced
position_items = {
    'description': ((__PODESCRIPTION__, DEFAULT_ITEM), ),
    'resp_or_desc': ((__PORESPONSIBILITY__, DEFAULT_ITEM), ),
    'place': ((u'\**(?:所在地区|工作地点|Area)[:：]?\**', DEFAULT_ITEM), ),
    'department': ((__DEPARTMENT__, DEFAULT_ITEM), ),
    'department_short': ((u'\**部'+POASP+u'*门[:： \xa0]\**', DEFAULT_ITEM), ),
    'report_to': ((u'\**(?:汇报(?:对象|人职位)|直接上司职位|Report(?:ing)? To)[:：]?\**', DEFAULT_ITEM), ),
    'people_under': ((u'\**(?:下属(?:人数|员工)|Subordinates Num)[:：]?\**', u'(?:(?:\d+)?(?:'+POASP+u'*人)?|'+ANONYMOUS(EMPLOYEES)+u')'), ),
    'reason_leave': ((u'\**(?:本人)?离职(?:转岗)?原因[:：]?\**', DEFAULT_ITEM), ),
    'contact': ((u'\**(?:工作)?证 ?明 ?人[:：]?\**', DEFAULT_ITEM), ),
    'name': ((u'\**(?:[所担]任职[位务][:：]?|职'+POASP+u'*[位务][:： \xa0]|Job Title[:：])\**', u'(?P<aposition>'+POSITION+u'?)'+POASP+u'*(?:(?=[\n\|])|$)'), ),
    'type': ((u'\**(?:职[位务]类别|工作性质)[:：]?\**', DEFAULT_ITEM), ),
    'achievement': ((__ACHIEVEMENT__, DEFAULT_ITEM), ),
    'posalary': ((__POSALARY__, u'(?:'+ASALARY+u'|保密)'), ),
    'project': ((__PROJECT__, DEFAULT_ITEM), ),
    }
key_position_items = position_items.copy()

key_items = key_company_items.copy()
key_items.update(key_position_items)

# Company default lambdas
company_items['company_department'] =  ((__CODEPARTMENT__+'?', u'(?(codptlbl)\S*|\S+?[部处室册科](?='+POASP+u'*$))'), )
company_items['company_employees'] = ((__COEMPLOYEES__+'?', AEMPLOYEES), )
company_items['company_description'] = ((__CODESCRIPTION__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )

SET_COMPANY_DEFAULT = lambda STR: STR.replace(DEFAULT_ITEM, u'[^:：__SEP__(?:\\\\\n)]*(?:(?:\\\\\n>?)*.+)*(?=(?:\\\\)?[__SEP__^]|$)')

# If pipe separated, the position is inside the table
# but sometimes it is inside the company business table
# (position details are then outside all tables.
COMPANY_DETAILS = lambda DETAILS: lambda RE:RE.pattern+u'\n*'+CHECKCOLTOP('codetborder')+u'?'+ASP+u'*\**'+NO_RECURSIVE(RE)(DETAILS)+u'\**\n+(?(codetborder)(?(checknextcol)|(?P<company_description>(?=(?!'+BORDER+u')).*\n)?))\n*'+CHECKCOLBOTTOM('codetborder')

company_details = COMPANY_DETAILS(SET_ALL_ITEMS(SET_COMPANY_DEFAULT)(company_items)(newline_separated)+'{1,13}')
empty_company_details = COMPANY_DETAILS(SET_ALL_ITEMS(SET_COMPANY_DEFAULT)(company_items)(newline_separated)+'{,13}')

company_details_pipeonly = COMPANY_DETAILS(SET_ALL_ITEMS_PIPEONLY(SET_COMPANY_DEFAULT)(company_items)(space_separated)+'{1,13}')
empty_company_details_pipeonly = COMPANY_DETAILS(SET_ALL_ITEMS_PIPEONLY(SET_COMPANY_DEFAULT)(company_items)(space_separated)+'{,13}')

# Position default lambdas
position_items['project'] = ((__PROJECT__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )
position_items['achievement'] = ((__ACHIEVEMENT__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )
position_items['description'] = ((__PODESCRIPTION__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )
position_items['resp_or_desc'] = ((__PORESPONSIBILITY__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )
position_items['department'] = (((u'(?P<dptlbl>'+__DEPARTMENT__+u')', u'(?(dptlbl)'+DEFAULT_ITEM+u'?(?=(?:[\s\|$]|\\\\\n))|\S+?[部处室册科](?='+POASP+u'*$))')), )
position_items['posalary'] = ((u'\**(?P<salbl>'+__POSALARY__+u')?', u'(?(salbl)(?:'+ASALARY+u'|保密)?(?=(?:[\s\|$]|\\\\\n))|'+AASALARY+u')'), )

SET_DEFAULT_YC = SET_ALL_DEFAULT(u'(?:。?\n+)?(?:'+ITEM_PREFIX+u'(?:'+POASP+u'*'+ASP+u'+)?)|(?:[;；]|\\\\)\n+')(u'')(u'(?=$|\|[^\\\\])')(key_items)
SET_DEFAULT = SET_ALL_DEFAULT(u'(?:[;；]|\\\\)\n')(u'')(u'(?=(?:\\\\)?$|\|)')(key_items)
SET_DEFAULT_LP = SET_ALL_DEFAULT(u'\n')(u'?')(u'(?=$|\|[^\\\\])')(key_items)

# If pipe separated, the position is inside the table
# but sometimes it is inside the company business table
# (position details are then outside all tables.
POSITION_DETAILS = lambda DETAILS: lambda RE:BORDERTOP('posdettab')+u'?\n*'+POASP+u'*\**'+RE.pattern+u'\n*(?:'+BORDERTOP('cobutab')+u'?\n*(?=(?!'+ANONPERIOD+u')))?'+DETAILS.replace('__NORECURSIVE__', RE.pattern)+u'\n*'+BORDERBOTTOM('posdettab').replace('__NORECURSIVE__', RE.pattern)

position_details = lambda RE:BORDERTOP('posdettab')+u'?\n*'+POASP+u'*\**'+RE.pattern+u'\n*(?P<cobutab>\-{3,}(?: \-+)* *\n+)?'+SET_DEFAULT(PIPESEPRTED(map(label_separated(newline_separated), position_items.items())))+u'{3,17}\n*'+BORDERBOTTOM('posdettab').replace('__NORECURSIVE__', RE.pattern)
empty_position_details = lambda RE:RE.pattern+position_details(re.compile('')).replace('{3,17}', '{,17}')

# Zhilian specific
zl_items = key_items.copy()
zl_items.update(company_items)
zl_items['company_department'] = ((u'(?P<codptlbl>'+__DEPARTMENT__+u')', u'(?(codptlbl)\S*|\S+?[部处室册科](?='+POASP+u'*$))'), )
zl_items['company_employees'] = ((u'(?P<employlabel>(公司)?规模[:：]?)', AEMPLOYEES), )
zl_details = zl_items.copy()
zl_details.update(position_items)
zl_details['website'] = ((u'网址[:：]', DEFAULT_ITEM), )
zl_details['company_description'] = ((u'(?P<desclabel>(?:公司|企业)(?:描述|介绍|简介|背景)[:：]?)', DEFAULT_ITEM), )
zl_details['project'] = ((__PROJECT__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(zl_items)+DEFAULT_ITEM)), )
zl_details['achievement'] = ((__ACHIEVEMENT__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(zl_items)+DEFAULT_ITEM)), )
zl_details['description'] = ((__PODESCRIPTION__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(zl_items)+DEFAULT_ITEM)), )
zl_details['resp_or_desc'] = ((__PORESPONSIBILITY__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(zl_items)+DEFAULT_ITEM)), )

SET_DEFAULT_ZL = SET_ALL_DEFAULT(u'(?:[;；。]?)\n+')(u'')(u'(?=$|\|[^\\\\])')(zl_items)

zl_position_details = POSITION_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_ZL)(zl_details)(newline_separated)+u'{1,17}')
empty_zl_position_details = POSITION_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_ZL)(zl_details)(newline_separated)+u'{,17}')

# Yingcai specific
position_items_yingcai = position_items.copy()
position_items_yingcai['posalary'] = ((__POSALARY__, u'(?:'+ASALARY+u'|保密)'), )
position_items_yingcai['department'] = (((u'(?P<dptlbl>'+__DEPARTMENT__+u')?', u'(?:(?(dptlbl)|^)\S+?[部处室册科](?='+POASP+u'*(?:$|\|[^\\\\])))')), )
position_items_yingcai['description'] = ((u'(?:'+__PODESCRIPTION__+u')?', MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )

yc_position_details = POSITION_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_YC)(position_items_yingcai)(newline_separated)+u'{1,17}')
empty_yc_position_details = POSITION_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_YC)(position_items_yingcai)(newline_separated)+u'{,17}')

# Space only
position_items_nospace = position_items.copy()
position_items_nospace.update({
    'department_short': ((u'\**部'+POASP+u'*门[:： \xa0]\**', MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), ),
    'name': ((u'\**(?:[所担]任职[位务][:：]?|职'+POASP+u'*[位务][:： \xa0]|Job Title[:：])\**', u'(?P<aposition>'+MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)+u')'), ),
    })


# Implicit line continuation (liepin)
SET_DEFAULT_LC = lambda x: x.replace(DEFAULT_ITEM, u'(?:(?:\n(?!(?:\n|'+POASP+u'*'+ANONPERIOD+u'|'+POASP+u'*(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|'+PREFIX+u'*\-{3,}))|(?<=[:：])\n{2}|.)*?)(?=$|\|[^\\\\])')
lp_position_items = position_items.copy()
lp_position_items.pop('name')

lp_position_items_nospace = position_items_nospace.copy()
lp_position_items_nospace.pop('resp_or_desc')
responsibility_item = {
    'resp_or_desc': ((__PORESPONSIBILITY__, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), ),
    }

DEFAULT_ITEM_SP = u'(?:(?:(?:[;；]|\\\\)\n+(?!(?:'+POASP+u'*'+ANONPERIOD+u'|'+POASP+u'*(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\s+(?=(?!(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\S)*?)(?=$|\s+(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\|[^\\\\])'
SET_DEFAULT_SP = lambda x: x.replace(DEFAULT_ITEM, DEFAULT_ITEM_SP)
DEFAULT_ITEM_NS = u'(?:(?:(?:[;；]|\\\\)\n+(?!(?:'+POASP+u'*'+ANONPERIOD+u'|'+POASP+u'*(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\s+(?=(?!(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\S)+?)(?=$|\s*(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\|[^\\\\])'
SET_DEFAULT_NS = lambda x: x.replace(DEFAULT_ITEM, DEFAULT_ITEM_NS)

company_details_spaceonly = COMPANY_DETAILS(SET_ALL_ITEMS_SPACE(SET_DEFAULT_SP)(company_items)(space_separated)+'{1,13}')
empty_company_details_spaceonly = COMPANY_DETAILS(SET_ALL_ITEMS_SPACE(SET_DEFAULT_SP)(company_items)(space_separated)+'{,13}')

lp_position_details = POSITION_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_LP)(lp_position_items)(newline_separated)+u'{1,17}')
lp_empty_position_details = POSITION_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_LP)(lp_position_items)(newline_separated)+u'*')
lp_position_details_spaceonly = lambda RE:RE.pattern+BORDERTOP('posdettab')+u'?\n*'+POASP+u'*\**'+NO_RECURSIVE(RE)(SET_ALL_ITEMS_SPACE(SET_DEFAULT_SP)(lp_position_items_nospace)(space_separated))+u'{1,17}\n*'+NO_RECURSIVE(RE)(SET_ALL_ITEMS(SET_DEFAULT)(responsibility_item)(space_separated))+u'?\n*'+BORDERBOTTOM('posdettab')

# Do not allow | after space
YIDPT = u'(?:[^-\n:：'+SP+u']|-(?=['+SP+u']{3,}))(?:(?:[^\n:：'+SP+u']|(?:'+POASP+u'\|'+POASP+u')|('+POASP+u'[^\|\n'+SP+u']))+|(?=['+SP+u']{3,}))'
PODEPARTMENT = u'(?:\**'+u'(?P<dpt>'+YIDPT+u')(?:（离职原因：.*?）|[:：])?'+u'\**)'
POFIELDLBL = u'(?:所属行业|Industry)[:：'+SP+u'](?P<ponl>'+POASP+u'*\n+)?'
POFIELD = u'(?P<field>'+u'(?(ponl)([^\n\*:：'+SP+u'](\n+/)?)+|((?:'+POASP+u'\|'+POASP+u')|[^\n\*'+SP+u']|(?:'+POASP+u'[^\n\*'+SP+u']))+)'+u')'
POPOSITION = u'(?='+ANONYMOUS(EXCLUDE_ITEM_KEYS(key_items).replace(u'[:：]?', u'[:：]'))+u')(?P<position>(?:(?(field)[^=\n\*]|[^=\|\n\*])|(?(ponl)|\\\\\*))+?)'
POFINISH = POASP+u'*(?:'+PODEPARTMENT+u'(?(ponl)\n+|'+POASP+u'+)'+u'(?: ?\*+)?(?:主管：)?)?(?:\**'+POPOSITION+POASP+u'*\**'+POASP+u'*(?:（?汇报对象：.*?)?'+POASP+u'*$)'

position_decription_items = {}
# Only used in JY: anything not preceded by item label until the next blank line (accept escaped newlines)
position_decription_items['description'] = ((u'(?:'+__PODESCRIPTION__+u')?', MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_company_items))+u'(?=(?!__NORECURSIVE__))(?:(?:\\\\\n)(?P<followindent> {10,})\n(?(followindent))(?=(?!__NORECURSIVE__))|'+POASP+u'+(?=(?!__NORECURSIVE__))|\S)+'), )

# If space only, the position is outside the table
position_details_spaceonly = lambda RE:RE.pattern+u'\n*'+BORDERTOP('posdettab')+u'?\n*'+POASP+u'*\**'+NO_RECURSIVE(RE)(SET_DEFAULT_SP(SPACESEPRTED(map(label_separated(space_separated), position_items_nospace.items()))))+u'{1,17}\n*'+BORDERBOTTOM('posdettab')
empty_position_details_spaceonly = lambda RE: u'\n*'+BORDERTOP('posdettab')+u'?\n*(?:'+POASP+u'*\**'+NO_RECURSIVE(RE)(SET_ALL_ITEMS_SPACE(SET_DEFAULT_SP)(position_items_nospace)(newline_separated))+u'\n*)*'+BORDERBOTTOM('posdettab')
empty_position_description_details_spaceonly = lambda RE:ASP+u'*(?:'+NO_RECURSIVE(RE)(SET_ALL_ITEMS(SET_DEFAULT)(position_decription_items)(space_separated))+u'\n*)?'+empty_position_details_spaceonly(RE)

# Cannot use append_po as the first part is optional (\n might be missing)
PO = re.compile(u'(?:'+POASP+u'*\**'+POFIELDLBL+u'(?:'+POASP+u'*'+POFIELD+POASP+u'*\**)?(?: ?\*+)?'+POASP+u'*$\n*)?'+u'(?:'+POASP+u'*' + POFINISH +u')?', re.M)

# TACO related grammar
TACOMODEL = u'(?P<companylabel>公司：)?\**(\\\\\*)*(?P<company>__COMPANY__)\**__SEP__'+ASP+u'*(__ITEM____SEP__'+ASP+u'*){0,2}'
PATTERN = u'(?<!(?:职责|工作)描述：\n{2})\**'+PERIOD+ur'\**[:：]?(?!\n{2}项目名称: )'+ASP+u'*'+TACOMODEL+u'\**(?P<position>[^：\|]+?)\**'+ASP+u'*\**'+BDURATION+u'?\**'+ASP+u'*$'
TACO = re.compile(PATTERN.replace('__COMPANY__', u'('+COMPANY+u'\n)?'+COMPANY.replace(u'、', '')+u'?'+ASP+u'*').replace('__SEP__', '\|').replace('__ITEM__', u'[^\|（\(\[【]+('+COMPANYTAIL+u'[^\|（\(\[【]*)?'), re.DOTALL+re.M)

TACOMODELCOPY = TACOMODEL.replace('company', 'ccompany')
# Add line begin for safer searching
PATTERN = u'(?<!(?:职责|工作)描述：\n{2})^\**'+APERIOD+ur'\**[:： \xa0](?!\n{2}项目名称: )'+ASP+u'*'+TACOMODELCOPY+u'(?(ccompanylabel)职位：'+POASP+u'*)\**(?P<cposition>[^：\|\n \xa0]+?)\**'+ASP+u'*\**'+ABDURATION+u'?\**'+ASP+u'*$'
NOPIPETACO = re.compile(PATTERN.replace('__COMPANY__', u'[^\|'+SP+u']+'+POASP+u'*(?:'+BEMPLOYEES+u')?'+POASP+u'*('+exclude_with_parenthesis('')+u')?').replace('__SEP__', u'[\n \xa0]').replace('__ITEM__', u'(?(ccompanylabel)部门：[^'+SP+u']+)'), re.M)
ALLTACO = re.compile(u'((?P<pip>'+TACO.pattern+u')|(?P<nop>'+NOPIPETACO.pattern+u'))', re.M)

# Duration required
DRPOSITION = POSITION+u'('+POSITION.replace('\\n', '').replace('\\*', '').replace('+', '*')+u')?'
DRPATTERN = u'(?<!(?:职责|工作)描述：\n{2})^'+PERIOD+ur'[:：]?(?!\n{2}项目名称: )'+ASP+u'*'+TACOMODEL+u'\**(?P<position>'+DRPOSITION+u'?(（.*?） 兼'+ASP+u'*'+DRPOSITION+u'?)*)。?\**'+ASP+u'*(\|'+ASP+u'*)?'+BDURATION+POASP+u'*$'
# Not use for searching but only for matching (see the code)
DRTACO = re.compile(DRPATTERN.replace('__COMPANY__', u'('+COMPANY+u'\n)?'+COMPANY.replace(u'、', '')+u'?'+ASP+u'*').replace('__SEP__', '\|').replace('__ITEM__', u'([^\|（\(\[【]+'+COMPANYTAIL+u')*([^\|（\(\[【]*)'), re.DOTALL+re.M)

# Exclude more invalid position as WYJCO at entrance of jingying
WYJCO_POS = ur'(?:[^=\w\n\*：:\|\u2013\u2015\u3002（\(\[【]+('+exclude_with_parenthesis(u'人年月')+u')?|\w+(?:'+POASP+u'\w+)*|（兼\S）)+'
WYJCO_DPT = u'(\S+?[部处室册科]|研发|QA|R&D|XP|\S*[&\w\s]+\S*)'
# Company using (?P<company>[^\|\n]+?) is too slow to fail on long empty lines
WYJCOBASE = u'(?P<position>'+WYJCO_POS+u')'+POASP+u'*(\|'+POASP+u'*(?P<dpt>'+WYJCO_DPT+u')'+POASP+u'*(\|'+POASP+u'*(?:[^\n]+))?)?\n+'+POASP+u'*\**(?P<company>[^\|'+SP+u']+(?: [^\|'+SP+u']+)*)'
WYJCO = regex.compile(u'^'+PREFIX+u'*'+PERIOD+POASP+u'{3,}'+WYJCOBASE+POASP+u'*'+BDURATION+'\**$', re.M+regex.ASCII)
DUFRTWYJCO = regex.compile(u'^'+PREFIX+u'*'+PERIOD+BDURATION+POASP+u'{2,}'+WYJCOBASE+'\**'+POASP+u'*'+position_details(re.compile('')).replace('{1,17}', '{2,17}')+u'$', re.M+regex.ASCII)
DUFRTDPTWYJCO = regex.compile(u'^'+PREFIX+u'*'+PERIOD+BDURATION+POASP+u'+'+WYJCOBASE.replace(u'(\|'+POASP+u'*(?P<dpt>'+WYJCO_DPT+u'))?\n+', u'(\|'+POASP+u'*(?P<dpt>'+WYJCO_DPT+u'))')+'\**'+POASP+u'*'+position_details(re.compile('')).replace('{1,17}', '{2,17}')+u'$', re.M+regex.ASCII)
BTCO = re.compile(u'^'+PREFIX+u'*'+PERIOD+ASP+u'+(?P<company>[^'+SP+u']+)'+ASP+u'+'+u'(?P<position>'+POSITION+u'?)'+ASP+u'+(?P<dpt>'+WYJCO_DPT+u')$', re.M)

# Combine presence of duration and bracket around period for safer searching
RCO = re.compile(u'^'+PREFIX+u'*'+CONTEXT+u'?'+ASP+u'*(?P<company>'+COMPANY+u')'+ASP+u'+(?P<position>[^\n:：'+SP+u'\u2013\-]+)'+ASP+u'+('+UNIBRALEFT+u'?'+PERIOD+UNIBRARIGHT+u'?)'+ASP+u'*'+BDURATION+u'?', re.M)
RTACPO = re.compile(u'^'+PREFIX+u'*'+CONTEXT+u'?'+ASP+u'*(?P<company>'+COMPANY+u')'+ASP+u'+(('+UNIBRALEFT+u'?'+ASP+u'*'+PERIOD+ASP+u'*'+UNIBRARIGHT+u'?)|('+BDURATION+u'))', re.M)
HCO = re.compile(u'^'+PREFIX+u'*(?:(?:(?:(?:公司|企业)名称|任职公司)[:：]?'+ASP+u'*\**(?P<company>'+COMPANY+u')\**'+ASP+u'*)|(?:(?:起止|任职)?时间[:：]?'+ASP+u'*\**'+PERIOD+'\**'+ASP+u'*)){2}$', re.M)

PUNCTCO = re.compile(u'^'+PREFIX+u'*'+PERIOD+POASP+u'*(?P<company>'+COMPANY+u')，(?P<position>'+POSITION+u')。$', re.M)

TABLECO = re.compile(u'^工作时间'+ASP+u'+岗位职能'+ASP+u'+公司名称'+ASP+u'*$', re.M)
TABLEPO = re.compile(u'^'+PERIOD+ASP+u'+(?P<position>'+POSITION+u'?)'+ASP+u'+(?P<company>'+COMPANY+u')'+ASP+u'*$', re.M)

SPO = re.compile(u'(项目)?职务[:：]'+ASP+u'*(?P<position>[^= \n:：\*]+)$', re.M)
RESPPO = regex.compile(company_details_pipeonly(re.compile(u'^职责：(?P<position>'+POSITION+u')')), re.M)

def append_po(header, footer):
    return header+POASP+u'*(?:(?:\\\\)?\n)+'+BORDERTOP('appendpo')+u'?'+POASP+u'*'+footer+BORDERBOTTOM('appendpo')

NOBRPOS = POSITION.replace(u'：', u'（）：；;'+ENDLINESEP)
YIPOSITION = NOBRPOS+u'(?P<lbr>[\(（])?(?(lbr)'+NOBRPOS+u'[\)）]('+NOBRPOS+u')?)'
YICO = re.compile(u'^(?:(?P<position>'+YIPOSITION+u')'+POASP+u'*\n+)?'+PERIOD+ASP+u'*?\n'+ASP+u'*(?P<company>'+COMPANY+u'(\n(?=(?!(?:'+COMPANY_TYPE+u'|'+ANONYMOUS(EMPLOYEES)+u'|^\S+?[部处室册科](?='+POASP+u'*$))))'+COMPANY+u')?)'+POASP+u'*$', re.M)

APO = re.compile(u'^(其中)?'+APERIOD+ASP+u'*\**(?P<position>'+POSITION+u'?)('+SALARY+u')\**$', re.M)
TPO = re.compile(u'^'+PREFIX+u'*(?P<aposition>'+POSITION+u'?)('+SALARY+u')?'+ASP+u'*'+APERIOD+''+ASP+u'*$', re.M)
TAPO = re.compile(u'^([所担]任)?职'+ASP+u'*[位务](类别)?[:：]?'+ASP+u'*\**(?P<aposition>'+POSITION+u'?)((('+SALARY+u')?\**'+ASP+u'*)|([\uff1b,].*))$', re.M)
BPO = re.compile(u'^'+PREFIX+u'*\**(?P<position>(?!所属行业)'+POSITION+ASP+u'*)(\|'+ASP+u'*(?P<second>[^元/月'+SP+u']+)'+ASP+u'*)?(\|'+ASP+u'*'+SALARY+u''+ASP+u'*)\**'+ASP+u'*$', re.M)
BPONOSAL = re.compile(BPO.pattern.replace(u'*)\**'+ASP+u'*$', u'*)?\**'+ASP+u'*$'), re.M)

LIEPPO = re.compile(u'(?<!(?:(?:职责|工作)描述|项目成就)：\n{2})^'+PREFIX+u'*(?: ?\*{1,2})?'+APERIOD+POASP+ur'*(?: ?\*{1,2})?(?P<position>'+POSITION+u'?)(?: ?\*{1,2})?'+SALARY+u'?'+POASP+u'*$', re.M)
NLIEPOBASE = u'(?<!(?:(?:职责|工作)描述|项目成就)：\n{2})^(?=(?!\n*'+BORDER+u'))'+PREFIX+u'*(?:工作岗位：'+ASP+u'*)?(?: ?\*{1,2})?(?P<position>'+POSITION+u'?)(?: ?\*{1,2})?'+POASP+u'*('+SALARY+POASP+u'*)?'
NLIEPO = re.compile(NLIEPOBASE+APERIOD, re.M)
NLIEPONOPER = re.compile(NLIEPOBASE+u'(?:'+APERIOD+u'|'+POASP+u'*$)', re.M)

# Could be NLIEPO or LIEPPO without position period or NOPIPETACO with company period
COULDDEPO = re.compile(u'\**(?P<position>'+POSITION+u')\**\n+.*?\n+工作(?:描述|职责)：', re.M)

EMP = re.compile(BEMPLOYEES)

CLASSIFY = {}
for (k,v) in sources.industry_id.sources.items():
    CLASSIFY[k] = re.compile('^(('+')|('.join([m.replace('(', '\(').replace(')', '\)') for m in v])+'))$')


def output_cleanup(groupdict):
    for item in ['company', 'position']:
        try:
            if u'[' in groupdict[item] and groupdict[item][0] == u'[':
                end = groupdict[item].index(u']')
                groupdict[item] = groupdict[item][1:end]
        except KeyError:
            continue
        except TypeError:
            continue

company_summary = lambda x: '|'.join((x['date_from'], x['date_to'], x['name']))
VALID_COMPANY_BUSINESS = re.compile('^'+COMPANY_BUSINESS_KEYWORD+'$')

def business_output(result, groupdict):
    if 'cbusiness' in groupdict and groupdict['cbusiness']:
        result['name'] = fix_name(groupdict['cbusiness'])
    else:
        if 'business' in groupdict and groupdict['business']:
            result['business'] = fix_name(groupdict['business'])
        elif 'abusiness' in groupdict and groupdict['abusiness']:
            result['business'] = fix_name(groupdict['abusiness'])
        elif 'field' in groupdict and groupdict['field']:
            result['business'] = fix_name(groupdict['field'])
        try:
            if not re.compile(COMPANY_BUSINESS_KEYWORD).match(result['business']):
                del result['business']
        except KeyError:
            pass
    return result

def employee_output(result, groupdict):
    if 'employees' in groupdict and groupdict['employees']:
        result['total_employees'] = fix_employees(groupdict['employees'])
    elif 'aemployees' in groupdict and groupdict['aemployees']:
        result['total_employees'] = fix_employees(groupdict['aemployees'])
    elif 'aaemployees' in groupdict and groupdict['aaemployees']:
        result['total_employees'] = fix_employees(groupdict['aaemployees'])
    return result

def company_output(output, groupdict, begin='', end='', company=''):
    if 'company' in groupdict or 'ccompany' in groupdict:
        result = {}
        result['id'] = len(output['company'])
        output_cleanup(groupdict)
        if 'from' in groupdict and groupdict['from']:
            result['date_from'] = fix_date(groupdict['from'])
            result['date_to'] = fix_date(groupdict['to'])
        else:
            result['date_from'] = fix_date(groupdict['afrom'])
            result['date_to'] = fix_date(groupdict['ato'])
        if 'ccompany' in groupdict and groupdict['ccompany']:
            result['name'] = fix_name(EMP.sub('', groupdict['ccompany']))
        else:
            result['name'] = fix_name(EMP.sub('', groupdict['company']))
        if 'duration' in groupdict and groupdict['duration']:
            result['duration'] = fix_duration(groupdict['duration'])
        else:
            result['duration'] = ''
        if 'company_type' in groupdict and groupdict['company_type']:
            result['type'] = fix_name(groupdict['company_type'])
        if 'company_description' in groupdict and groupdict['company_description']:
            result['description'] = fix_name(groupdict['company_description'])
        employee_output(result, groupdict)
        if 'company_business' in groupdict and groupdict['company_business']:
            result['business'] = fix_name(groupdict['company_business'])
        else:
            business_output(result, groupdict)
        output['company'].append(result)

def format_salary(result, groupdict):
    if 'salary_months' in groupdict and groupdict['salary_months']:
        result['salary'] = fix_salary(groupdict['salary'])
        result['salary_months'] = groupdict['salary_months']
    elif 'asalary_months' in groupdict and groupdict['asalary_months']:
        result['salary'] = fix_salary(groupdict['asalary'])
        result['salary_months'] = groupdict['asalary_months']
    elif 'salary' in groupdict and groupdict['salary']:
        result['salary'] = fix_salary(groupdict['salary'])
    elif 'asalary' in groupdict and groupdict['asalary']:
        result['salary'] = fix_salary(groupdict['asalary'])
    elif 'aasalary' in groupdict and groupdict['aasalary']:
        result['salary'] = fix_salary(groupdict['aasalary'])
    elif 'salary_yearly' in groupdict and groupdict['salary_yearly']:
        result['yearly'] = fix_salary(groupdict['salary_yearly']+u'/年')
    elif 'asalary_yearly' in groupdict and groupdict['asalary_yearly']:
        result['yearly'] = fix_salary(groupdict['asalary_yearly']+u'/年')
    return result

def position_output(output, groupdict, begin='', end=''):
    if 'position' in groupdict or 'aposition' in groupdict or 'name' in groupdict:
        result = {}
        output_cleanup(groupdict)
        if 'from' in groupdict and groupdict['from']:
            result['date_from'] = fix_date(groupdict['from'])
            result['date_to'] = fix_date(groupdict['to'])
        else:
            if 'afrom' in groupdict and groupdict['afrom']:
                result['date_from'] = fix_date(groupdict['afrom'])
                result['date_to'] = fix_date(groupdict['ato'])
            else:
                result['date_from'] = fix_date(begin)
                result['date_to'] = fix_date(end)
        if 'cposition' in groupdict and groupdict['cposition']:
            result['name'] = fix_position(groupdict['cposition'])
        else:
            if 'aposition' in groupdict and groupdict['aposition']:
                result['name'] = fix_position(groupdict['aposition'])
            elif 'second' in groupdict and groupdict['second']:
                result['name'] = fix_position(groupdict['second'])
            elif 'name' in groupdict and groupdict['name']:
                result['name'] = fix_position(groupdict['name'])
            elif groupdict['position']:
                result['name'] = fix_position(groupdict['position'])
            else:
                result['name'] = None
        if 'aduration' in groupdict and groupdict['aduration']:
            result['duration'] = fix_duration(groupdict['aduration'])
        else:
            if 'duration' in groupdict and groupdict['duration']:
                result['duration'] = fix_duration(groupdict['duration'])
            else:
                result['duration'] = ''
        try:
            company = output['company'][-1]
            result['at_company'] = company['id']
            #if 'business' not in company:
            #    business_output(company, groupdict)
            if 'total_employees' not in company:
                employee_output(company, groupdict)

        except IndexError:
            result['at_company'] = 0
        if 'field' in groupdict and groupdict['field']:
            for c in output['company']:
                if c['id'] == result['at_company'] and 'business' not in c:
                    c['business'] = groupdict['field']
        # Hack: limit is a guess (sure thing: 50 not enough)
        if (not result['name'] or len(result['name']) > 100):
            return
        for key in position_items:
            if key in groupdict and groupdict[key]:
                if key == 'posalary' or key == 'project':
                    continue
                if key == 'people_under':
                    result[key] = fix_people(groupdict[key])
                elif key == 'department_short':
                        result['department'] = fix_name(groupdict[key])
                elif key == 'resp_or_desc':
                    if 'description' in result:
                        result['responsibility'] = fix_name(groupdict[key])
                    else:
                        result['description'] = fix_name(groupdict[key])
                else:
                    result[key] = fix_name(groupdict[key])
        format_salary(result, groupdict)
        output['position'].append(result)

name = lambda company: company['name']
duration = lambda company: company['duration']
business = lambda company: company['business']
employees = lambda company: company['total_employees']
salary = lambda position: position['salary']
companies = lambda output: len(output[1]['company'])
positions = lambda output: len(output[1]['position'])
company_1 = lambda x: x[1]['company'][0]
company_2 = lambda x: x[1]['company'][1]
position_1 = lambda x: x[1]['position'][0]
position_2 = lambda x: x[1]['position'][1]


def find_xp(RE, text):
    u"""
        >>> assert companies(find_xp(CO, u'2014 年 8 月 – 至今 company (1 年 6 个月)'))
        >>> assert companies(find_xp(CO, u'2010.03 - 至今*深圳市蓝韵实业有限公司* *(5年9个月)*'))
        >>> assert companies(find_xp(CO, u'2013-8 至 今  工作经历（IT服务行业）*---* 1年5个月'))
        >>> assert companies(find_xp(TCO, u'2011.07 - 至今 *四川昱峰医疗器械有限公司陕西分公司* *(3年5个月)*'))
        >>> assert companies(find_xp(TCO, u'2013年04月——至今（含三个月实习期）   器械质量监督检验所（湛江检验室）'))
        >>> assert companies(find_xp(TCO, u'2011年7月—2014年5月 ：广州仁爱医院 [2年10月 ]'))
        >>> assert positions(find_xp(TCO, u'2011/5\~2015/2\\n欧文斯科宁复合材料（中国）有限公司\\n职位：质量经理\\n\\n工作描述：'))
        >>> assert positions(find_xp(TCO, u'2015/03\~    \\n微泰医疗器械（杭州）有限公司\\n职位：质量经理\\n\\n工作描述：')) == 0
        >>> assert positions(find_xp(TCO, u'2000-11 ～ 2010-04  深圳安科高技术股份有限公司\\n担任职位：\\n 研发项目经理；从事大\\n工作描述：'))
        >>> assert positions(find_xp(TCO, u'2012/03-2014/03     武汉维斯第医用科技有限公司\\n部门：南区办事处       职位：分销专员'))
        >>> assert positions(find_xp(regex.compile(company_details(TCO), re.M), u'2005/04-2008/12       浙江省衢州市衢江区人民医院(二甲)\\n科室：手外科    职位：手外科医师'))
        >>> assert 1 == companies(find_xp(TCO, u'2005/11 - 2010/3：DELL（500-1000人）\\n所属行业：计算机硬件\\n职位：系统测试\\n'
        ...     u'  2005/11—2010/3 ｜ DELL ｜系统测试工程师'))
        >>> assert positions(find_xp(TCO, u'2006.01-至今  有限公司\\n职位：财务经理\\n所在地区： 广州\\n所在部门：集团财务部')) # data: bdgywzkv
        >>> assert positions(find_xp(regex.compile(company_details(TCO), re.M), u'2009 /11--至今： 奥泰医疗系统有限责任公司 （150-500人）\\n'
        ...     u'所属行业：   医疗设备/器械\\n部   门：   硬件工程部\\n职   位：   系统工程师\\n职   责：\\n磁共振硬件的调试与测试；'))
        >>> assert 2 == positions(find_xp(TCO, u'2006.01-2014.08         南方石化集团有限公司\\n\\n---------------- -\\n'
        ...     u'职位：财务经理\\n\\n所在地区：       广州\\n\\n工作职责：       1、制定集团、各分公司、子公司、联营公司的预算方案及执行情况；\\n\\n'
        ...     u'6、配合资金部提供各项融资需要的资料。\\n---------------- -\\n\\n'
        ...     u'1996.07-2005.12    佛山禅城酒店有限公司\\n\\n职位：财务主管\\n\\n------------ -\\n所在地区：   佛山\\n\\n'
        ...     u'工作职责：   1、编制收入、费用等各项凭证；\\n\\n4、负责年度审计及税审工作；\\n------------ -'))
    """
    out = {'company': [], 'position': []}
    # Check for chances to get position from details
    if re.compile(u'职'+POASP+u'*[位务]').search(text):
        out = {'company': [], 'position': []}
        pattern = RE.pattern + position_details(re.compile(''))
        MA = regex.compile(pattern,re.M)
        for r in MA.finditer(text):
            company_output(out, r.groupdict())
            if r.group('aposition'):
                position_output(out, r.groupdict())
        if not len(out['position']):
            out = {'company': [], 'position': []}
            pattern = RE.pattern + position_details_spaceonly(re.compile(''))
            MA = regex.compile(pattern,re.M)
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                if r.group('aposition'):
                    position_output(out, r.groupdict())
    if not len(out['position']):
        out = {'company': [], 'position': []}
        MA = regex.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+APO.pattern+u'))', re.M)
        for r in MA.finditer(text):
            if r.group('co'):
                company_output(out, r.groupdict())
            else:
                position_output(out, r.groupdict())
    return len(out['position']), out


def work_xp_new_liepin(text):
    u"""
    Test for NLIEPO (period mandatory)
        >>> assert '1000' in employees(company_1(work_xp_new_liepin(u'2009/07-至今   强生上海医疗器材有限公司\\n'
        ...     u'    公司性质： 外商独资·外企办事处 | 公司规模： 1000-2000人 | 公司行业： 医疗设备/器械\\n   产品经理   2014/09 - 至今  \\n'
        ...     u'    所在地区：北京    所在部门：杨森诊断中国事业部   汇报对象：事业部经理\\n下属人数： 0   薪酬情况： 22000')))
        >>> assert positions(work_xp_new_liepin(u'2010/04-2016/07   华为技术有限公司\\n        公司行业： 通信(设备/运营/增值)\\n'
        ...     u'    软件工程师      2010/04 - 2011/08\\n        所在地区：深圳      所在部门：\\n下属人数： 0      薪酬情况： 保密'))
        >>> assert positions(work_xp_new_liepin(u'**2005.05-2012.08 华为技术有限公司 **\\n\\n'
        ...     u'工作岗位：流程质量经理 2011.05-2012.08\\n\\n下属人数： 10'))
        >>> assert u'总经理' in name(position_1(work_xp_new_liepin(u'2015.12-至今      郑州纽克莱生物技术有限公司\\n'
        ...     u'   公司行业：  制药/生物工程\\n  总经理   2015.12-至今\\n   工作地点：  郑州\\n   下属人数： 15')))
        >>> assert u'运营中心' in name(position_1(work_xp_new_liepin(u'2013.03-至今      北京智博高科生物技术有限公司\\n'
        ...     u'  公司描述： 北京智博北京2000家高新技术企业之一。...\\n  公司性质：  私营·民营企业\\n  公司规模： 50-99人\\n'
        ...     u'  公司行业： 制药/生物工程\\n   运营中心总监   2014.01-至今\\n   薪酬状况：  25000 元 / 月\\n 工作地点： 北京\\n 下属人数： 30')))
        >>> assert u'软件开发' in name(position_1(work_xp_new_liepin(u'2002.09-2005.04         东洋网蓝软件服务有限公司\\n'
        ...     u'工作岗位：软件开发工程师    2002.09-2005.04\\n下属人数：   0\\n工作职责：         负责MRP软件的开发和维护')))

    Test for NLIEPONOPER (no period)
        >>> assert u'工程师' in name(position_1(work_xp_new_liepin(u'2012/10-至今    泰康资产管理有限责任公司\\n'
        ...     u'    公司性质： 私营·民营企业 | 公司规模： 500-999人 | 公司行业： 基金/证券/期货/投资\\n    运维工程师\\n'
        ...     u'    所在地区：北京          所在部门：信息科技部          汇报对象：部门经理\\n下属人数： 10   薪酬情况： 保密')))

    Test for PIPEPO
        >>> assert u'专员' in position_1(work_xp_new_liepin(u'2013.02-至今       迈瑞生物医疗电子股份有限公司\\n\\n'
        ...     u'    公司性质：未填写 | 公司规模： 未填写 | 公司行业：医疗设备/器械\\n\\n公司描述：未填写\\n\\n'
        ...     u'国际市场专员                          2013.02 - 至今\\n\\n所在地区：广东省 | 所在部门：未填写'))['name']
        >>> assert '3500' in salary(position_1(work_xp_new_liepin(u'2006.04-2008.03  大族激光股份有限公司 \\n\\n'
        ...     u'   公司性质：国内上市公司 | 公司规模： 2000-5000人 \\n\\n电气调试工 3500元/月 2006.04 - 2008.03 \\n\\n'
        ...     u'所在地区：深圳 | 所在部门：未填写')))
    """
    out = {'company': [], 'position': []}
    text = re.compile(POASP+'{10,}').sub('   ', text)
    for RE in [CCO, CO, TCO]:
        if (RE == TCO or re.compile(BDURATION).search(text)) and RE.search(text):
            out = {'company': [], 'position': []}
            pattern = company_details(RE)
            if re.compile(SALARY).search(text):
                popattern = lp_position_details_spaceonly(NLIEPONOPER)
            else:
                # Speed up non-matching
                popattern = lp_position_details_spaceonly(NLIEPONOPER).replace(u'('+SALARY+POASP+u'*)?', '')
            MA = regex.compile(append_po(pattern, popattern), re.M)
            res = MA.search(text)
            if res:
                if (res.group('typelabel') or res.group('businesslabel') or
                        res.group('employlabel') or res.group('desclabel')):
                    pattern = empty_company_details(RE)
                else:
                    pattern = empty_company_details_pipeonly(RE)
                MA = regex.compile(append_po(pattern, popattern), re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
                    position_output(out, r.groupdict())
            if not len(out['position']):
                out = {'company': [], 'position': []}
                pattern = company_details(RE)
                if re.compile(SALARY).search(text):
                    popattern = position_details(NLIEPONOPER)
                else:
                    # Speed up non-matching
                    popattern = empty_position_details(NLIEPONOPER).replace(u'('+SALARY+POASP+u'*)?', '')
                MA = regex.compile(append_po(pattern, empty_position_details(NLIEPONOPER)), re.M)
                res = MA.search(text)
                if res:
                    if (res.group('typelabel') or res.group('businesslabel') or
                            res.group('employlabel') or res.group('desclabel')):
                        pattern = empty_company_details(RE)
                    else:
                        pattern = empty_company_details_pipeonly(RE)
                    MA = regex.compile(append_po(pattern, popattern), re.M)
                    for r in MA.finditer(text):
                        company_output(out, r.groupdict())
                        position_output(out, r.groupdict())
        if len(out['position']):
            break
    return len(out['position']), out


def work_xp_liepin(text):
    u"""
    Test for NLIEPO
        >>> assert positions(work_xp_liepin(u'2010.04 - 2016.07     华为技术有限公司\\n\\n采购经理 2010.04 - 2016.07\\n\\n'
        ...     u'- 所在地区：非洲\\n\\n- 汇报对象：采购部长&交付副代表\\n\\n- 下属人数：5人'))

    Test for LIEPPO
        >>> assert companies(work_xp_liepin(u'2012.03 -\\n至今*\** *(2年9个月)*\\n专业服务(咨询/财会/法律/翻译等)\\n'
        ...     u'2012.03 - 至今咨询顾问\\n下属人数：0 | 所在地区：深圳'))
        >>> assert u'江' in company_1(work_xp_liepin(u'2013.09 - 至今\\n江苏\\*\\*医疗器械有限公司\\n(2年9个月)\\n2013.09 - 至今 质量负责人月\\n'
        ...     u'下属人数：0 | 所在地区：北京'))['name']
        >>> assert positions(work_xp_liepin(u'2006.07 - 至今\\n\*\*\*\\n(9年11个月)\\n2006.07 - 至今 质量管理\\n下属人数：0 | 所在地区：北京'))
        >>> assert positions(work_xp_liepin(u'2016.06 - 2016.06\\n系统有限公司\\n 2016.06 - 2016.06 应届生\\n下属人数：0 | 所在地区：北京'))
        >>> assert positions(work_xp_liepin(u'2016.06 - 至今\\n西门子(无锡)有限公司\\n2016.06 - 至今 项目经理\\n下属人数：0 | 所在地区：北京'))
        >>> assert positions(work_xp_liepin(u'2013.07 - 至今 *某高科技*制造行业上市公司 (1年5个月)\\n'
        ...     u'国有企业  |  机械制造/机电/重工  |  10000人以上\\n2013.07 - 至今财务部长\\n'
        ...     u'汇报对象：财务总监、公司高管 | 下属人数：10 | 所在地区：沈阳 | 所在部门：财务控制部'))
        >>> assert positions(work_xp_liepin(u'2004/07-至今    飞利浦超声（上海）有限公司\\n'
        ...     u'    公司性质： 外商独资ﾷ外企办事处 | 公司规模： 100-499人 | 公司行业： 医疗设备/器械 \\n公司描述：飞利浦超声公司是隶属于飞利浦医\\n'
        ...     u'    OEM市场经理     2011/07 - 至今 \\n       所在地区：上海      所在部门：市场销售部    汇报对象：市场销售高级经理 \\n'
        ...     u'下属人数： 2    薪酬情况： 保密    \\n      工作职责：    M市场信息搜集和分析，制定市场营销和产品发展方案。')) # data: t37poj9k
        >>> assert positions(work_xp_liepin(u'2013.06 - 至今 *西门子(深圳)磁共振有限公司 (2年9个月) *\\n\\n医疗设备/器械\\n\\n'
        ...     u'2013.06 - 至今**机械设计工程师**\\n**下属人数：0 | 所在地区：深圳 **'))
        >>> assert positions(work_xp_liepin(u'2010.10 - 至今 *通用电气 (3年4个月) *\\n\\n外商独资·外企办事处  | 10000人以上\\n\\n'
        ...     u'2010.10 - 2014.02**销售主任**9000元/月\\n**下属人数：0 | 所在地区：济南 | 所在部门：LCS **'))
        >>> assert position_1(work_xp_liepin(u'2014.06 - 至今\\n上海分公司\\n(7个月)\\n  2014.06 - 至今 研发工程师\\n下属人数：0 | 所在地区：北京'))
        >>> # Doesn't match lpcv nor nlpcv (#FIXME should it?)
        >>> assert 7 == len(name(position_1(work_xp_liepin(u'2013/04 - 至今 南风风机股份有限公司 （3年6个月）\\n\\n----\\n'
        ...     u'公司性质：私营·民营企业 | 公司规模：1000-2000人 | 公司行业：机械制造/机电/重工\\n----\\n\\n2013/04 - 至今 项目执行部经理\\n\\n'
        ...     u'----\\n**所在地区：**   佛山   **汇报对象：**   总经理   **薪酬情况：**   15000 元/月\\n----')))) #data: cvg3aoi5
        >>> assert 4 == len(name(position_1(work_xp_liepin(u'2015.09 - 至今 *费森尤斯卡比 (6个月) *\\n\\n'
        ...     u'外商独资·外企办事处  |  医疗设备/器械  |  10000人以上\\n--------------------\\n\\n'
        ...     u'2015.09 - 至今**研发总监**\\n----------------------\\n**下属人数：30 | 所在地区：长沙 | 所在部门：研发部 **'))))
        >>> assert 8 == len(name(position_1(work_xp_liepin(u'**2015.09 - 至今** **东芝医疗** (5个月)\\n\\n'
        ...     u'外商独资·外企办事处  |  医疗设备/器械  |  10000人以上\\n-------------------\\n世界五百强医疗器械日本企业\\n\\n'
        ...     u'**2015.09 - 至今高级临床应用专家**17000元/月\\n------------------\\n汇报对象：部门经理 | 下属人数：4 | 所在部门：市场部'))))
    """
    out = {'company': [], 'position': []}
    text = SHORTEN_BLANK(text)
    for RE in [CCO, CO, TCO]:
        if (RE == TCO or re.compile(BDURATION).search(text)) and RE.search(text):
            out = {'company': [], 'position': []}
            pattern = company_details(RE)
            if re.compile(SALARY).search(text):
                popattern = position_details(NLIEPO)
            else:
                # Speed up non-matching
                popattern = position_details(NLIEPO).replace(u'('+SALARY+POASP+u'*)?', '')
            MA = regex.compile(u'((?P<co>'+pattern+u')|(?P<po>'+popattern+u'))', re.M)
            res = MA.search(text)
            if res:
                if res.group('co'):
                    if (res.group('typelabel') or res.group('businesslabel') or
                            res.group('employlabel') or res.group('desclabel')):
                        pattern = empty_company_details(RE)
                        MA = regex.compile(u'((?P<po>'+popattern+u')|(?P<co>'+pattern+u'))', re.M)
                    else:
                        pattern = empty_company_details_pipeonly(RE)
                        MA = regex.compile(u'((?P<po>'+popattern+u')|(?P<co>'+pattern+u'))', re.M)
                for r in MA.finditer(text):
                    if r.group('co'):
                        company_output(out, r.groupdict())
                    else:
                        if not out['company']:
                            continue
                        position_output(out, r.groupdict())
            if not len(out['position']):
                out = {'company': [], 'position': []}
                pattern = company_details(RE)
                if re.compile(SALARY).search(text):
                    popattern = lp_position_details(LIEPPO)
                else:
                    # Speed up non-matching
                    popattern = lp_position_details(LIEPPO).replace(SALARY+u'?', '')
                MA = regex.compile(u'((?P<po>'+popattern+u')|(?P<co>'+pattern+u'))', re.M)
                res = MA.search(text)
                if res:
                    if res.group('co'):
                        if (res.group('typelabel') or res.group('businesslabel') or
                                res.group('employlabel') or res.group('desclabel')):
                            pattern = empty_company_details(RE)
                            MA = regex.compile(u'((?P<po>'+popattern+u')|(?P<co>'+pattern+u'))', re.M)
                        else:
                            pattern = empty_company_details_pipeonly(RE)
                            MA = regex.compile(u'((?P<po>'+popattern+u')|(?P<co>'+pattern+u'))', re.M)
                    for r in MA.finditer(text):
                        if r.group('co'):
                            company_output(out, r.groupdict())
                        else:
                            if not out['company']:
                                continue
                            position_output(out, r.groupdict())
            if len(out['position']):
                break
            out = {'company': [], 'position': []}
            pattern = company_details(RE)
            if re.compile(SALARY).search(text):
                popattern = lp_position_details(NLIEPONOPER)
            else:
                # Speed up non-matching
                popattern = lp_position_details(NLIEPONOPER).replace(u'('+SALARY+POASP+u'*)?', '')
            MA = regex.compile(append_po(pattern, lp_empty_position_details(NLIEPONOPER)), re.M)
            res = MA.search(text)
            if res:
                if (res.group('typelabel') or res.group('businesslabel') or
                        res.group('employlabel') or res.group('desclabel')):
                    pattern = empty_company_details(RE)
                else:
                    pattern = empty_company_details_pipeonly(RE)
                MA = regex.compile(append_po(pattern, popattern), re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
                    position_output(out, r.groupdict())
            if not len(out['position']):
                out = {'company': [], 'position': []}
                pattern = company_details(RE)
                if re.compile(SALARY).search(text):
                    popattern = position_details_spaceonly(LIEPPO)
                else:
                    # Speed up non-matching
                    popattern = position_details_spaceonly(LIEPPO).replace(SALARY+u'?', '')
                MA = regex.compile(u'((?P<co>'+pattern+u')|(?P<po>'+popattern+u'))', re.M)
                for r in MA.finditer(text):
                    if r.group('co'):
                        company_output(out, r.groupdict())
                    else:
                        if not out['company']:
                            continue
                        position_output(out, r.groupdict())
        if len(out['position']):
            break
    return len(out['position']), out

def work_xp_yingcai(text):
    u"""
        >>> assert u'监' in name(position_1(work_xp_yingcai(u'IT项目总监\\n2015.11 - 至今\\n有限责任公司\\n所属行业：贸易/进出口\\n信息建设\\n月薪：保密')))
        >>> assert positions(work_xp_yingcai(u'电子工程师\\n2015.12 - 2016.01\\n有限公司 \\n月薪：2000以下'))
        >>> assert companies(work_xp_yingcai(u'2013.01 - 2014.03\\n技术有限公司\\n其他\\n月薪：保密'))
        >>> assert positions(work_xp_yingcai(u'客户需求。\\n2015.07 - 2015.09\\n长虹集团')) == 0
        >>> assert u'设' in name(position_1(work_xp_yingcai(u'''用户界面（UI）设计\\n2014.03 - 2016.06\\n济南豪斯设计有限公司\\n月薪：保密''')))
        >>> assert companies(work_xp_yingcai(u'1） 2016年5月至今\\n公司首个MTK')) == 0
        >>> assert u'主管' in name(position_1(work_xp_yingcai(u'项目主管\\n2007.11 - 2015.06\\n有限公司\\n国企\\n所属行业：机械制造/机电/重工\\n')))
        >>> assert 1 == companies(work_xp_yingcai(u'项目主管\\n2007.11 - 2015.06\\n有限公司\\n国企\\n所属行业：机械制造/机电/重工\\n月薪：6000\\n'
        ...     u'2007.11 – 2015.06 有限公司\\n所属行业：机械/机电 公司性质：上市公司\\n'))
        >>> assert business(company_1(work_xp_yingcai(u'项目主管\\n2007.11 - 2015.06\\n有限公司\\n国企\\n所属行业：机械制造/机电/重工\\n月薪：6000\\n'
        ...     u'2007.11 – 2015.06 有限公司\\n所属行业：机械制造/机电/重工 公司性质：上市公司\\n'))).endswith(u'重工')
        >>> assert 2 == companies(work_xp_yingcai(u'设备工程师\\n2010.10 - 2016.03 \\n东莞新科磁电厂\\n外商独资\\n500人以上 \\n'
        ...     u'所属行业：电子技术/半导体/集成电路 | 计算机硬件\\n电气工程师/技术员 \\n月薪：6000到8000\\n'
        ...     u'2007.05 - 2009.12 \\n上海润彤机电有限公司\\n民营/私企 \\n技术部'))
        >>> assert position_2(work_xp_yingcai(u'项目主管\\n2014.11 - 2016.01\\n有限公司\\n所属行业：贸易/进出口\\n月薪：6000到8000\\n'
        ...     u'工作描述：\\n有限公司O,TCL等手机项目.\\n'
        ...     u'质量管理/测试工程师\\n2013.11 - 2014.10\\n金凯新瑞光电有限公司\\n所属行业：石油/化工/矿产/地质\\n月薪：4000到6000'))['salary']
        >>> assert companies(work_xp_yingcai(u'WO 专家 \\n2015.07 - 至今\\n有限公司\\n月薪：保密')) # TODO (company detail empty)
        >>> assert business(company_1(work_xp_yingcai(u'销售运营专员/销售数据分析\\n2006.05 - 2008.12\\n欧时电子元件（上海）有限公司\\n代表处\\n'
        ...     u'所属行业：电子技术/半导体/集成电路\\n月薪：3000到4000')))
        >>> assert business(company_1(work_xp_yingcai(u'质量检验员\\n2014.08 - 至今\\n有限公司\\n民营/私企\\n101－300人\\n'
        ...     u'所属行业：计算机软件\\n安全质量部')))
        >>> assert 'Ltd.' in name(company_1(work_xp_yingcai(u'IT项目总监\\n2012.11 - 2015.08\\neCargo enterprise Ltd.\\n'
        ...     u'所属行业：互联网/电子商务\\n月薪：20000到30000')))
        >>> assert companies(work_xp_yingcai(u'2005.09 - 2006.01 \\n江西麦克森国际服饰有限公司\\n全部\\n职位：秘书/行政/文员/助理'))
        >>> assert 0 == companies(work_xp_yingcai(u'2009年02月-2009年9月调入北京森华通达汽车销售服务有限公司\\n财务部\\n职位：会计'))
        >>> assert companies(work_xp_yingcai(u'1995.06 - 2001.04\\n四川南山机器厂\\n国企\\n500人以上 \\n工具处'))
        >>> assert u'其他' in business(company_1(work_xp_yingcai(u'人事行政经理\\n2002.11 - 2007.02\\n创维电子有限公司\\n民营/私企\\n'
        ...     u'所属行业：其他行业\\n月薪：保密\\n所属行业：制造业（彩电、VCD、DVD，家庭影院和卫星接收机）')))
        >>> assert companies(work_xp_yingcai(u'Senior Manager\\n2014.03 - 至今\\nUTC Building and Industrial Syste Asia\\n'
        ...     u'Headquarter美国联合技术公司建筑与工业系统亚洲总部,\\n外商独资\\n所属行业：其他行业\\n月薪：保密\\n'))
        >>> assert companies(work_xp_yingcai(u'财务负责人\\n2014.07 - 至今\\nGT Sapphire technology CO., LTD\\n'
        ...     u'极特蓝宝石科技（贵阳）有限公司\\n外商独资\\n所属行业：电子技术/半导体/集成电路\\n月薪：20000到30000'))
        >>> assert positions(work_xp_yingcai(u'项目经理\\n2005.06 - 2008.07\\n加拿大ATS自动化（天津）有限公司\\n外商独资\\n'
        ...     u'所属行业：机械/设备/重工\\n项目管理部\\n月薪：4000到6000'))   # TODO (unrefenced department)
        >>> assert u'部' not in name(company_1(work_xp_yingcai(u'见习\\n2010.08 - 2010.09\\n中国一汽\\n全部\\n月薪：保密\\n下属人数：0')))
        >>> assert not positions(work_xp_yingcai(u'瑞华会计师事务所总部 审计助理 2012.12-2013.2\\n?执行具体的实质性测试'))
    """
    co_items = company_items.copy()
    co_items.pop('company_department')
    empty_yc_company_details = COMPANY_DETAILS(SET_ALL_ITEMS(SET_COMPANY_DEFAULT)(co_items)(newline_separated)+'{,13}')

    popattern = u'(?:^(?='+EXCLUDE_ITEM_KEYS(key_items)+u')'+YIPOSITION.replace('lbr', 'albr')+u'(?<=(?!部处室册科))$)'
    MAPO = regex.compile(append_po(empty_yc_company_details(YICO), u'(?(position)'+popattern+u'|(?P<aposition>'+popattern+u'))?'), re.M)
    text = re.compile(BORDER, re.M).sub('', text)
    if MAPO.search(text):
        MA = regex.compile(empty_yc_position_details(MAPO), re.M)
    else:
        MA = regex.compile(empty_yc_position_details(regex.compile(empty_company_details(YICO))), re.M)

    out = {'company': [], 'position': []}
    for r in MA.finditer(text):
        company_output(out, r.groupdict())
        if r.group('position') or r.group('aposition'):
            position_output(out, r.groupdict())
    return len(out['position']), out

def work_xp_zhilian(text):
    u"""
        >>> assert companies(work_xp_zhilian(u'2010年6月  --  2013年11月\\n\*\*电子材料有限公司\\n|  IT工程师\\n（3年5个月）\\n'
        ...     u'所属行业：\\n加工制造\\n公司性质：\\n合资\\n公司规模：\\n100-499人\\n职位类别：\\n计算机/网络技术-网络工程师'))
        >>> assert positions(work_xp_zhilian(u'##### **2007年9月  --  2007年12月 西工大多媒体与通信研究所、西安利安集团  |  技术开发部'
        ...     u'  |  软件工程师      （3个月）**\\n> 所属行业：\\n>\\n> 计算机软件\\n>\\n> 公司规模：\\n>\\n> 100-499人'))
        >>> assert 4 == len(name(position_1(work_xp_zhilian(u'##### **2004年9月  --  2006年2月 天士力集团研究院  |  药品研发      （1年5个月）**\\n'
        ...     u'\\n> 所属行业：\\n>\\n> 医药/生物工程\\n>\\n> 公司性质：\\n>\\n> 上市公司'))))
        >>> assert 8 == len(name(company_1(work_xp_zhilian(u'2011年3月  --  2014年10月 中兴通讯\\n有限公司  |  客户服务  | 工程师 （3年7个月）'))))
        >>> assert u'网' in name(position_1(work_xp_zhilian(u'2015年6月  --  至今\\n联想集团\\n|  服务器（EBG）部门\\n|  网络工程师\\n（1年）')))
        >>> assert u'副' in name(position_1(work_xp_zhilian(u'2012年6月  --  2013年6月\\n有限公司\\n|  技术部、PMO（项目管理办公室）\\n'
        ...     u'|  副总经理、PMO副主任\\n（1年）')))
        >>> assert u'生产' in name(position_1(work_xp_zhilian(u'2002年10月  --  2007年2月\\n电脑接插件公司\\n|  设备部。品管部\\n|  生产主管\\n（4年4个月）')))
        >>> assert u'工程师' in name(position_1(work_xp_zhilian(u'2012年10月  --  2013年6月\\n科技有限公司\\n|  研发部\\n'
        ...     u'|  手机PCB Layout工程师 |\\n（8个月）')))
        >>> assert u'QHSE' in name(position_1(work_xp_zhilian(u'2011年11月  --  至今\\n有限公司\\n|  总经理办公室（原）-行政部（现）\\n'
        ...     u'|  QHSE主管\\n（4年7个月）')))
        >>> assert u'应用' in name(position_1(work_xp_zhilian(u'2009年1月  --  至今\\n有限公司\\n|  软件工程师（公司产品） 兼\\n'
        ...     u'视觉应用工程师\\n（7年5个月）')))
        >>> assert u'软件' in name(position_1(work_xp_zhilian(u'2013年8月  --  2014年11月 有限公司  |  linux c++\\n中级软件工程师  （1年3个月）')))
        >>> assert '2006.07' == position_1(work_xp_zhilian(u'91261-11\\n2006年7月-至今\\n中国银行\\n| 人力资源部\\n|  其他\\n（3个月）'))['date_from']
        >>> assert 'Master' in name(position_1(work_xp_zhilian(u'2010年7月 -- 至今 医科达 | 软件质量*工程师*/Scrum\\nMaster   （6年3个月）\\n\\n'
        ...         u'所属行业：\\n\\n医疗设备/器械')))
        >>> assert u'。' not in name(position_1(work_xp_zhilian(u'2008年5月  --  2011年10月\\n伟创力电源系统（北京）有限公司\\n|  行政人事部\\n'
        ...         u'|  目前主要从事薪资、保险、职员入职、离职、劳动合同管理。\\n（3年5个月）\\n所属行业：\\ 电子技术/半导体/集成电路')))
        >>> assert not u'工程师' in name(position_1(work_xp_zhilian(u'1.  2013.7-现在：西门子（深圳）磁共振有限公司|工艺工程师|负责生产工艺改进')))
        >>> assert not companies(work_xp_zhilian(u'2000年6月  --  2006年6月 Praxair Inc。  |  软件工程师（6年）\\n'
        ...     u'所属行业：石油/石化/化工\\n公司性质：外商独资\\n公司规模：10000人以上'))  # FIXME
        >>> assert not u'新加坡' in name(company_1(work_xp_zhilian(u'2007/7 - 2013/2 项目总监|国际投资部\\n新加坡医疗投资有限公司  ( 5年7个月 ) \\n'
        ...     u'医疗设备/器械|少于50人|外资(非欧美)\\n工作描述：')))   # FIXME
        >>> assert u'医疗' in business(company_1(work_xp_zhilian(u' 1. ### 2011年4月 -- 2016年8月 有限公司  |  研发部  |  产品研发  （5年4个月）\\n'
        ...     u'> 所属行业：\\n>\\n> 医疗设备/器械\\n>\\n> 公司性质：\\n>\\n> 民营')))
        >>> assert 10 == len(business(company_1(work_xp_zhilian(u'**2008年12月 -- 2010年6月 广州分公司 | 技术部 | 电气工程师 （1年6个月）**\\n\\n'
        ...     u'> 公司介绍：\\n>\\n> 公司为施耐德电气国内最大的代理商\\\\\\n> 同时为西门子产品\\n>\\n> 所属行业：\\n>\\n> 仪器仪表及工业自动化'))))
        >>> assert 7 == len(business(company_1(work_xp_zhilian(u'2012年9月  --  至今 有限公司  |  售后部门  |  售后工程师  （3年9个月）\\n\\n'
        ...     u'公司介绍：\\n\\n深圳安科高是大型影像设备研发,生产,销售,售后为一体的多元化发展的医疗器械上市公司\\\\n'
        ...     u'全国设有八个分公司。\\n\\n所属行业：医疗设备/器械\\n\\n公司性质：民营\\n\\n公司规模：500-999人'))))
        >>> assert 7 == len(business(company_1(work_xp_zhilian(u'2011年3月  --  2014年5月 深圳市蓝韵实业有限公司  |  '
        ...     u'高级软件测试工程师  （3年2个月）\\n\\n**所属行业：医疗设备/器械 下属人数：5 人**'))))
        >>> assert not '*' in name(position_1(work_xp_zhilian(u'2012年2月  --  2015年3月 佛山市南华仪器股份  |  *电子*工程师      （3年1个月）')))
        >>> assert 4 == len(name(position_1(work_xp_zhilian(u'##### 2012年3月  --  至今 某知名合资医疗器械有限公司  |  质量管理中心  |'
        ...     u'  质量经理      （3年10个月） \\n'))))
        >>> assert 5 == len(name(position_1(work_xp_zhilian(u'##### 2014年7月  --  至今 上海逸思医疗科技有限公司  |  技术部 供应链管理部  |'
        ...     u'  *工艺工程师*      （2年2个月）'))))
        >>> assert 8 == len(name(position_2(work_xp_zhilian(u'2014年2月  --  2015年3月 有限公司  |  嵌入式软件工程师 \\n （1年1个月）\\n'
        ...     u'2012年7月  --  2013年2月 衡阳北方光电信息技术有限公司  |\\n 嵌入式软件工程师      （7个月）'))))

    NOPIPETACO related
        >>> assert not '.' in name(company_1(work_xp_zhilian(u'2013.7-2014.1      COMSIS Ltd.              \\n  总经理助理/ 翻译')))    #FIXME
        >>> assert '500' in employees(company_1(work_xp_zhilian(u'2007 /7--2010 /6： 工程有限公司 （500人以上）\\n通信工程师-项目经理  ')))
        >>> assert position_1(work_xp_zhilian(u'2009.12-2010.01   深圳市理邦精密仪器有限公司 (实习）    \\n     海外客服工程师'))
        >>> assert not positions(work_xp_zhilian(u'2013.05-至今�             苏州微清医疗器械有限公司�\\n                 机械工程师  \\n'
        ...     u'汇报对象：技术总监 \\n工作职责：�               1、'))    # FIXME
        >>> assert not not positions(work_xp_zhilian(u'2014/5--至今                      上海依视路光学有限公司\\n'
        ...     u'负责车间镀膜自动生产线的生产和人员管理考核，工艺控制标准制定，EER，主持QRQC会议，后道的热处理和包装，质量问题'))  # FIXME
        >>> assert not 2 == companies(work_xp_zhilian(u'016.5\~2016.8    湖北省肿瘤医院  \\n'
        ...     u'操作IBA MatriXX调强验证系统，完成科室放疗计划验证和数据的分析与记录\\n2015.9\~2016.3   四川大学华西医院   \\n参与调试Varian'))
        >>> assert u'研发' in name(position_1(work_xp_zhilian(u'2013.8- 至今       公司：广州男科医院有限公司       部门：网络部    \\n'
        ...     u' 职位： 研发工程师')))
        >>> assert '*' not in name(position_1(work_xp_zhilian(u'**2015.06 - 至今 卡尔蔡司光学(中国)有限公司(1年4个月) **\\n\\n'
        ...     u'**自动化软件工程师**\\n\\n职业优势：本人具有15年专业质量管理经历')))
    """
    out = {'company': [], 'position': []}
    text = re.compile(BORDER, re.M).sub('', text)
    if DRTACO.search(text):
        MA = regex.compile(empty_zl_position_details(regex.compile(u'(?P<pip>'+DRTACO.pattern+u')')), re.M)
        for r in MA.finditer(text):
            company_output(out, r.groupdict())
            d = r.groupdict()
            if d['position']:
                d['position'] = re.compile(u'（.*?） 兼'+ASP+u'*').sub('/', d['position'])
            position_output(out, d)
    elif NOPIPETACO.search(text):
        MA = regex.compile(empty_zl_position_details(regex.compile(u'(?P<nop>'+NOPIPETACO.pattern+u')')), re.M)
        for r in MA.finditer(text):
            company_output(out, r.groupdict())
            d = r.groupdict()
            if d['position']:
                d['position'] = re.compile(u'（.*?） 兼'+ASP+u'*').sub('/', d['position'])
            position_output(out, d)
    elif ALLTACO.search(text):
        if not len(out['position']):
            # Support missing pipe in company definition by using NOPIPETACO
            MA = regex.compile(empty_zl_position_details(ALLTACO), re.M)
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                d = r.groupdict()
                if d['position'] or d['cposition']:
                    position_output(out, d)
    return len(out['position']), out

def work_xp_modified_wyjco(text):
    u"""
        >>> business = lambda x: x['business']
        >>> assert u'研究员' in name(position_1(work_xp_modified_wyjco(u'2007/7 - 至今 副研究员|放料设备质量控制实验室\\n'
        ...     u'中国疾控中心辐射安全所 ( 9年3个月 )\\n检测，认证|150-500人|事业单位'))) #data: 01e417128f303...
        >>> assert 0 == positions(work_xp_modified_wyjco(u'2009.03 - 2010.12\\n东软医疗系统NMS (1年9个月)\\n'
        ...     u'中外合营(合资·合作)  |  医疗设备/器械  |  500-999人')) # data: mlh7fqak
        >>> assert 0 == positions(work_xp_modified_wyjco(u'2007.12 - 2010.11 *天健正信会计师事务所黑龙江分所 (2年11个月)*\\n'
        ...     u'2007.12 - 2010.11天健正信会计师事务所黑龙江分所合伙人\\n汇报对象：总经理 | 下属人数：12 | 所在地区：哈尔滨 | 所在部门：审计部\\n'
        ...     u'工作职责：  项目质量控制复核人\\n2005.04 - 2007.12 *黑龙江正达会计师事务所有限公司 (2年8个月)*\\n会计/审计')) # data: 35h876y3
        >>> assert 0 == positions(work_xp_modified_wyjco(u'2008.12  就职于中兴通讯股份有限公司   任职结构设计高级工程师 2008.12\\n'
        ...     u'2014.4 负责产品热设计\\n2004 /1--2004 /9：上海市迪比特实业有限公司(1000-5000人) [ 8个月]\\n所属行业：\\n通信')) # data: z1qrkd48
        >>> assert 0 == positions(work_xp_modified_wyjco(u'2012.10 - 2016.03  法国国家科学研究院下属UMR 8081\\nIR4M实验室  （3年5个月）\\n'
        ...     u'博士研究生／器件研发工程师 | 15000-25000元/月\\n医疗设备/器械 | 企业性质：其它 | 规模：20-99人')) # data: jznu7i80
        >>> assert 0 == positions(work_xp_modified_wyjco(u'2013年6月  --  2013年12月 GE  |  software simplification\\n'
        ...     u'leader      （6个月）\\n所属行业：医疗设备/器械')) # data: yg6g7ujs

    DUFRTWYJCO related
        >>> assert '11' in duration(company_1(work_xp_modified_wyjco(u'2012/1―至今\[4年11个月\]  高级软件工程师 | 研发\\n'
        ...     u'北京大基康明医疗设备有限公司\\n\\n工作描述：')))

    DUFRTDPTWYJCO related
        >>> assert 7 == len(name(position_1(work_xp_modified_wyjco(u'2012/1―至今\[4年11个月\] 高级软件工程师 | 研发 北京大基康明医疗设备有限公司\\n'
        ...     u'工作描述：'))))
    """
    res = None
    out = {'company': [], 'position': []}
    # Speed up non-matching
    if re.compile(BDURATION, re.M).search(text):
        RE = regex.compile(WYJCO.pattern.replace(u'{3,}', '+'), re.M+regex.ASCII)
        res = RE.search(text)
        if res:
            # regex's \w matches re's \w only is regex.ASCII is set
            MA = regex.compile(company_details_pipeonly(RE).replace(u'{1,13}', '{3,13}'), re.M+regex.ASCII)
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        if not len(out['position']):
            out = {'company': [], 'position': []}
            MA = DUFRTWYJCO
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        if not len(out['position']):
            out = {'company': [], 'position': []}
            MA = DUFRTDPTWYJCO
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
    return len(out['position']), out

def position_description_output(out, groupdict):
    d = groupdict.copy()
    if d['description']:
        description = d.pop('description')

        co_items = {}
        co_items['company_description'] = company_items['company_description']
        po_items = position_items_nospace.copy()
        po_items.pop('name')
        po_items.pop('description')
        po_items.pop('resp_or_desc')
        for key in po_items.copy():
            resp_items = {}
            resp_items[key] = po_items[key]
            MARESP = regex.compile(SET_ALL_ITEMS_NOSPACE(SET_DEFAULT_NS)(resp_items)(space_separated).replace(u'[:：]?', u'[:：]'), re.M)
            if len(MARESP.findall(description)) > 1:
                po_items.pop(key)

        MACO = regex.compile(SET_ALL_ITEMS(SET_DEFAULT)(co_items)(newline_separated).replace(u'[:：]?', u'[:：]'), re.M)
        MAPO = regex.compile(SET_ALL_ITEMS_NOSPACE(SET_DEFAULT_NS)(po_items)(space_separated).replace(u'[:：]?', u'[:：]'), re.M)

        res = MACO.search(description)
        if res:
            r = res.groupdict()
            if r['company_description']:
                d['company_description'] = r['company_description']
            description = description.replace(res.group(), '')
        desc = description
        for res in MAPO.finditer(description):
            r = {}
            for key in res.groupdict():
                if res.groupdict()[key]:
                    r[key] = res.groupdict()[key]
            d.update(r)
            # Must avoid replacing all ASP/POASP is spurious match
            if set(r).intersection(position_items):
                desc = desc.replace(res.group(), '')
        d['description'] = desc
    company_output(out, d)
    if d['position']:
        position_output(out, d)

def work_xp_jingying(text):
    u"""
        >>> assert u'鸡' in name(company_1(work_xp_jingying(u'2016/6 -- 至今： 随鸡 [一个月内]\\n 所属行业：计算机服务\\n 傻子 销售经理')))
        >>> assert companies(work_xp_jingying(u'2016/7 -- 至今： 信息产品集团 [ -1年11个月 ]\\n所属行业：计算机硬件\\n销售  区域销售经理'))
        >>> assert companies(work_xp_jingying(u'2013/3 -- 2015/7： 江苏有限公司\\n所属行业：交通/运输/物流\\n'
        ...     u'2005/5 -- 2011/6： 南京分公司\\n所属行业：交通/运输/物流\\n市场部 市场')) == 2
        >>> assert 5 == len(duration(company_1(work_xp_jingying(u'2012 /8--至今：安士制药（中山）有限公司(150-500人) \\[ 3 年9个月\\]\\n'
        ...     u'所属行业：    制药/生物工程\\n研发综合部      项目申报专员，药品注册'))))
        >>> assert positions(work_xp_jingying(u'2013 /7--2014 /12：深圳市宝润科技有限公司(少于50人) [ 1 年5个月]\\n'
        ...     u'所属行业：        医疗设备/器械\\n研发部  医疗器械注册 \\n'
        ...     u'2013 /7--2014 /12：有限公司（50人以下） [ 1年5个月] 所属行业：医疗设备/器械1、负责公司产品\\n'
        ...     u'---------------------------- ---------------')) == 1 # data: rm7em2f2
        >>> assert 0 == positions(work_xp_jingying(u'2003/1 -- 2005/5： （ 50-150人） [ 2年4个月 ]\\n所属行业：餐饮业\\n-----'))
        >>> assert positions(work_xp_jingying(u'2006/9 -- 2009/12： 开发公司 [3年3个月]\\n所属行业：电子技术\\n财务部（离职原因：调动） 会计'))
        >>> assert positions(work_xp_jingying(u'2001/1 -- 2004/3： 有限公司\\n所属行业：电子技术\\n生产部|工程部  组长|工程师'))
        >>> assert u'主' not in name(position_1(work_xp_jingying(u'2008/3 -- 2013/12： 上海分公司\\n所属行业：保险\\n收展一部  主管：人事，招聘')))
        >>> assert positions(work_xp_jingying(u'2012年12月—至今：有限公司\\n所属行业： 电子技术\\n职责:\\n编写程序功能块实现方案')) == 0
        >>> assert u'：' not in name(position_1(work_xp_jingying(u'2010 /4—2014/4：有限公司（300-500人） [ 3年]\\n所属行业：石油/化工/能源\\n'
        ...         u'人力资源部   人事经理  （汇报对象：公司总经理）')))
        >>> assert 1 == positions(work_xp_jingying(u'2007/7 -- 至今： 科技有限公司（ 500-1000人） [ 9年1个月 ]\\n'
        ...         u'所属行业：  医疗设备/器械\\n车间\\*采购部\\*品质部    操作工\\*库房管理员\\*检验员\\*包装员'))
        >>> assert u'****' in name(company_1(work_xp_jingying(u'    2013/3 -- 2016/8： \*\*\*\*集团公司（ 1000-5000人） [ 3年5个月 ]\\n'
        ...         u'所属行业：   法律\\n          法务   法务部诉讼经理\\n    主要负责集团诉讼')))
        >>> assert 5 == len(business(company_1(work_xp_jingying(u'2005/7 -- 2008/6： 研究所（ 50-150人） [ 2年11个月 ]\\n\\n'
        ...         u' 所属行业： 学术/科研\\n  综合部  出纳员\\n\\n2005/07--2008年6月：研究所\\\\\\n所属行业：学术/科研\\\\\\n部出纳员\\\\\\n '))))
        >>> assert employees(company_1(work_xp_jingying(u'2014 /4--至今：有限公司(5000-10000人) [ 2 年]\\n所属行业：计算机软件\\n'
        ...     u'开发部 软件工程师\\n下属人数：0 | 所在地区：北京')))
        >>> assert positions(work_xp_jingying(u'（德国工作经历） 2014 /12 -- 2015 /10 ： 三木控股集团 （ 1000- -0 5000\\n 人）\\n '
        ...     u'所属行业： 办公用品及设备\\n人力资源部 人力资源总监兼经营规划部总监'))
        >>> assert positions(work_xp_jingying(u'2002/7 -- 2006/6： 艾默生过程管理(天津)有限公司 [ 3年11个月 ]\\n\\n'
        ...     u'       所属行业：      机械/设备/重工\\n\\n     .        .\\n\\n 1. 设计磨削抛光机器人系统')) # data: 1557922426
        >>> assert positions(work_xp_jingying(u'1993/3 -- 至今： 安徽中天人律师事务所 [ 23年5个月 ]\\n'
        ...     u'       所属行业：      法律\\n       -               合伙人\\n接受当事人委托参加诉讼')) # data: 1517298785
        >>> assert not u'经理' in name(position_1(work_xp_jingying(u'（韩国工作经历） 2012 /4 -- 2014 /12 ： 真彩文具集团 （ 1000- -0 5000\\n'
        ...     u' 人）\\n所属行业： 办公用品及设备\\n人力资源中心 高级人力资源经理（ COE ）')))    # FIXME
        >>> assert positions(work_xp_jingying(u'2011 /7--至今：光宝网络通讯有限公司   \\n所属行业  电子技术/半导体/集成电路   \\n'
        ...     u'研发部   高级软件工程师     '))
        >>> assert positions(work_xp_jingying(u'2015 /10--2016 /7：中创英泰国际贸易设备有限公司(50-150人) [ 9个月]\\n'
        ...     u'所属行业：\\t机械/设备/重工 \\n海工部  船舶工程师')) # data: wbrnwrob
        >>> assert positions(work_xp_jingying(u'**2014/6-至今 Averydennison Panyu Plant (4000人) 【3年】**\\n\\n'
        ...     u'**所属行业: 印刷/包装/造纸 **\\n\\n**人事行政部 高级行政主管 **'))    # TODO
        >>> assert 'CEO' in name(position_1(work_xp_jingying(u'2013 /10--2014 /10： **上海云树信息技术有限公司** （少于50人）\\n\\n'
        ...     u'所属行业：\\n\\n**总经办**      **CEO & Co-founder**     ')))
        >>> assert not 9 == len(name(position_1(work_xp_jingying(u'2005/8-2006/10 河南汉威电子 (1年 2个月 )\\n\\n'
        ...     u'仪器仪表/工业自动化|150-500人|民营公司\\n\\n开发部 电气工程师/技术员 (兼职)'))))  # FIXME
        >>> assert not 11 == len(name(position_1(work_xp_jingying(u'2010/10 -- 2011/12： 上海运佳黄浦制药有限公司（ 500-1000人） \[ 1年2个月\\n'
        ...     u'\]\\n所属行业： 制药/生物工程\\n\\n质量保证部门 微生物工程师 验证助理'))))    # FIXME (space in PO position)
        >>> assert 2 == positions(work_xp_jingying(u'2005/9 -- 2006/3： 武汉2046音乐会所 [ 6个月 ]\\n管理委员会       副总经理/副总裁\\n'
        ...     u'2001/1 -- 2004/7： 武汉市食品药品监督管理局 [ 3年6个月 ]\\n所属行业：       政府/公共事业\\n稽查分局\\n'
        ...     u'2000/1 -- 2000/12： 湖北捷龙汽车租赁公司 [ 11个月 ]\\n安全技术部         安全员'))

    WYJCO related tests:
        >>> assert u'台湾' in name(company_1(work_xp_jingying(u'2008/3-2010/11         业务推广 | 光电事业处\\n\\n'
        ...         u'台湾汉唐集成股份有限公司 [2年 8个月 ]\\n\\n多元化业务集团公司|150-500人|外资(非欧美)\\n')))
        >>> assert u'医疗' in business(company_1(work_xp_jingying(u'2011/6-2015/6          项目经理|投资部\\n\\n'
        ...         u'有限公司 [4年 ]\\n\\n医疗/护理/卫生|150-500人|民营公司\\n')))
        >>> assert companies(work_xp_jingying(u'   2011/5 -- 2012/10： 有限公司 [ 1000-5000人、合资]（ 1000-5000人） [ 1年5个月 ]\\n\\n'
        ...         u'   所属行业：    检测，认证\\n\\n      食品部       微生物测试工程师'))
        >>> assert u'质量管理' in name(position_1(work_xp_jingying(u'2011/11-2013/11        医疗器械生产/质量管理 | 质量及法规部\\n'
        ...         u'Ambu Ltd [2年 ]\\n医疗设备/器械|500-1000人|外资(欧美)')))
        >>> assert u'店长' in name(position_1(work_xp_jingying(u'   2006/5-2011/7     店长\\n佛山市天地星通讯服务有限公司 ( 5年2个月 )\\n'
        ...         u'        通信/电信运营、增值服务 | 50-150人 | 民营公司')))
        >>> assert u'维护' in name(position_1(work_xp_jingying(u'        2009/3-2010/5      技术支持/维护工程师 | Array Test\\n'
        ...         u'        成都京东方光电科技有限公司 ( 1年2个月 )\\n仪器仪表/工业自动化 | 500-1000人 | 上市公司')))
        >>> assert u'Manager' in name(position_1(work_xp_jingying(u'        2014/12-至今    Project Manager | 液晶面板 LCD\\n'
        ...         u'        Orbotech ( 1年10个月 )\\n电子技术/半导体/集成电路 | 1000-5000人 | 外资(欧美)')))
        >>> assert 0 == positions(work_xp_jingying(u'2009.03 - 2011.03 Longtop Financial Technologies\\n'
        ...     u'Group东南融通集团（纽交所代码NYSE：LFT） (2年)\\n中外合营(合资·合作)  |  IT服务/系统集成  |  10000人以上')) # data: y91n6bgp
        >>> assert positions(work_xp_jingying(u'2015/12-至今     产品专员 | 雅培诊断\\n\\n雅培 \\[10个月 \\]\\n\\n'
        ...     u'医疗设备/器械|1000-5000人|外资(欧美)\\n\\n------------\\n工作描述：   1.区域内\\n------------'))
        >>> assert positions(work_xp_jingying(u'2003/8-2005/3       质量管理/测试工程师(QA/QC工程师)|生产部\\n\\n'
        ...     u'无锡夏普电子元器件有限公司  ( 1年7个月 )\\n\\n电子技术/半导体/集成电路|合资')) # data: fn0ci941
        >>> assert positions(work_xp_jingying(u'2011/10-2012/6        机械工程师 (兼职) |技术研发部\\n\\n'
        ...     u'武汉格瑞拓机械有限公司--研究生期间科研项目合作 \[8个月 \]\\n\\n机械/设备/重工|150-500人|外资(非欧美)')) # data: nhodm7tm
    """
    out = {'company': [], 'position': []}

    # Speed up non-matching
    if re.compile(BDURATION, re.M).search(text) and WYJCO.search(text):
        fst_items = {}
        fst_items['description'] = position_items['description']
        fst_items['company_description'] = company_items['company_description']
        SET_DEFAULT_WYJCO = lambda X: X.replace(DEFAULT_ITEM, MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_company_items))+u'(?:'+POASP+u'+|\n(?!\n)|\S)+')
        wyjco_position_details = BORDERTOP('posdettab')+u'?\n*'+SET_ALL_ITEMS(SET_DEFAULT_WYJCO)(fst_items)(newline_separated)+u'*\n*'+BORDERBOTTOM('posdettab')
        # regex's \w matches re's \w only is regex.ASCII is set
        MA = regex.compile(append_po(empty_company_details_pipeonly(WYJCO), wyjco_position_details), re.M+regex.ASCII)
        for r in MA.finditer(text):
            position_description_output(out, r.groupdict())
        if len(out['position']):
            return len(out['position']), out

    t = text
    MAPROJ = regex.compile(RE_ANY(PRJ_ITEM_KEYS(extractor.project.key_items)).replace(u'[:：]?', u'[:：]'), re.M)
    for r in extractor.project.YPJ.finditer(text):
        if MAPROJ.search(r.group('proj')):
            t = t.replace(r.group(), '')
    text = t

    for RE in [CCO, CO, TCO]:
        if (RE == TCO or re.compile(BDURATION).search(text)) and RE.search(text):
            MA = regex.compile(append_po(RE.pattern, PO.pattern), re.M)
            if MA.search(text):
                MA = regex.compile(append_po(RE.pattern, PO.pattern+empty_position_description_details_spaceonly(RE)), re.M)
                for r in MA.finditer(text):
                    d = r.groupdict()
                    if (d['position'] and not d['position'].strip()) and d['dpt']:
                        d['position'] = d['dpt']
                    position_description_output(out, d)
                if len(out['position']):
                    break
                out = {'company': [], 'position': []}
                # Need to count POASP* in group po
                MA = regex.compile(u'(?P<co>'+empty_company_details_pipeonly(RE)+u')'+u'\n+'
                        u'(?P<po>'+POASP+u'*'+u'(?:'+PO.pattern+u')?'+empty_position_description_details_spaceonly(RE)+u')', re.M)
                indent = None
                for r in MA.finditer(text):
                    if r.group('po'):
                        if r.group('position'):
                            position_description_output(out, r.groupdict())
                        elif r.group('description'):
                            company_output(out, r.groupdict())
                            # If description is indented as field, that is a position
                            if not indent:
                                indent = re.compile('^( *(?P<label>[^\w ]*)\w* +)(?=('+
                                    unicode(r.group('abusiness'))+u'|'+unicode(r.group('field'))+u'))', re.M).search(r.group('co'))
                            descindent = re.compile('^( +)(?=\w)', re.M+re.UNICODE).search(r.group('po'))
                            if ((descindent and indent) and
                                    len(unicode(descindent.group())) == len(unicode(indent.group())) + len(unicode(indent.group('label')))):
                                d = r.groupdict().copy()
                                d['position'] = d.pop('description')
                                position_output(out, d)
                if len(out['position']):
                    break
                MA = regex.compile(company_details(regex.compile(append_po(RE.pattern, PO.pattern))), re.M)
                if MA.search(text):
                    out = {'company': [], 'position': []}
                    MA = regex.compile(position_details(regex.compile(empty_company_details(regex.compile(append_po(RE.pattern, PO.pattern))))), re.M)
                    for r in MA.finditer(text):
                        company_output(out, r.groupdict())
                        position_output(out, r.groupdict())
                    if len(out['position']):
                        break
    return len(out['position']), out

def work_xp(text):
    u"""
    General company matching
        >>> assert work_xp(u'\\n    2014/02-2015/05 有限公司')
        >>> assert not TCO.search(u'  项目成就：\\n\\n  2014.3-2014.11 宝钢湛江钢铁有限公司变电站母差保护项目')
        >>> assert not TCO.search(u'  工作内容：\\n\\n  1、2011.4-2014.1 设备采购与成套中心 仪控设备采购工程师')
        >>> assert not regex.compile(company_details(TCO).replace('{1,13}', '{3,13}'), re.M).search(
        ...     u'  2、2014.2-2016.3 设备采购与成套中心 红沿河项目设备服务办公室\\n仪控设备组组长\\n\\n'
        ...     u'  3. 2016.3-至今 设备采购与成套中心 仪控设备主管工程师\\n\\n  主管组内仪控设备合同执行工作。\\n\\n')
        >>> assert 0 == companies(work_xp(u'  2014.10-2015.2 越南莱州水电站变电站项目\\n\\n  主要成就：'))
        >>> assert work_xp(u'''CT Engineer\\n\\nHealthcare\\n\\n2013年7月 – 至今 (2年7个月)''')
        >>>     # TODO re.compile(u'^(?P<company>\S+)'+ASP+u'+(?P<position>\S+)'+ASP+u'*'+PERIOD+ASP+u'+(\S*)?$', re.M)
        >>> assert companies(work_xp(u'2011年8月—2014年12月 中国海运集团\\n职位：航运部  轮机工程师'))
        >>> assert 2 == companies(work_xp(u'2012.02 - 2012.07 *中科院深圳先进技术研究院 (5个月)*\\n'
        ...     u'事业单位  |  政府/公共事业/非营利机构  |  1000-2000人\\n2012.02 - 2012.07助理工程师（医疗电子/算法）\\n'
        ...     u'所在地区：深圳 | 所在部门：生物医学与健康工程研究所\\n2011.09 - 2011.12 *Medical Physics, Ninewells hospital, the university\\n'
        ...     u'of dundee,UK (3个月)*\\n政府/公共事业/非营利机构\\n2011.09 - 2011.12电子工程师（实习）\\n所在地区：英国\\n'
        ...     u'工作职责：  量子隧道压力材料的测试设计'))
        >>> assert 13 == len(name(company_1(work_xp(u'2015.01 -\\n至今*高新兴科技集团股份有限公司[1000-5000人、上市公司]* *(1年2个月)*\\n\\n'
        ...     u'2015.01 - 至今财务管理中心经理(财务管理中心负责人)'))))
        >>> assert name(company_1(work_xp(u'2011.05 - 2016.03 []{#OLE_LINK1\\n.anchor}*爱克发感光器材(深圳)有限公司 (4年10个月) *\\n\\n'
        ...     u'IT服务/系统集成\\n\\n2011.05 - 2016.03**Collaboration Application analyst**\\n**下属人数：3 | 所在地区：深圳 **')))

    General company detail matching
    -   duration
        >>> assert company_1(work_xp(u'2013.01 -\\n2016.04深圳山龙科技 (3年3个月)\\n2013.01 - 2016.04软件工程师'))['duration']
        >>> assert not u'年' in name(company_1(work_xp(u'2011.01-至今 集团 （4年）\\n2009.04-2011.01 集团 （1年9个月）')))
        >>> assert u'6个月' in company_1(work_xp(u'2007/7-2008/12   广西梧州神农药业有限公司 (50-150人) 【1.5年】\\n'
        ...     u'所属行业:               制药/生物工程\\n\\n人事行政部             董事长秘书'))['duration']

    -   business
        >>> assert u'机械' in business(company_1(work_xp(u'2010.08 - 至今有限公司 (5年10个月)\\n----\\n中外合营 | 机械制造/机电/重工 | 500-999人\\n'
        ...     u'2010.08 - 至今财务负责人\\n汇报对象：总经理 | 下属人数：10 | 所在地区：长沙 | 所在部门：财务部''')))
        >>> assert u'政府' in business(company_1(work_xp(u'2012.04 - 至今\\n环保部核安全中心 (4年4个月)\\n'
        ...     u'事业单位  |  政府/公共事业/非营利机构  |  500-999人 \\n环保部唯一核与辐射技术支持单位\\n2012.04 - 至今高工\\n'
        ...     u'汇报对象：环保部核安全监管司核技术处 | 下属人数：0 | 所在地区：北京')))
        >>> assert u'电子' in business(company_1(work_xp(u'2016.02-至今    深圳大芝麻国际控股有限公司\\n\\n'
        ...     u'     公司性质：未填写 | 公司规模： 未填写 | 公司行业：互联网/移动互联网/电子商务\\n\\n首席运营官  2016.02-至今\\n所在地区：深圳')))
        >>> assert u'医疗设备' in business(company_1(work_xp(u'2005.04-2011.01   沈阳东软医疗系统有限公司\\n\\n'
        ...     u'   公司描述：  双层螺旋CT（NeuViz Twin）、数字化乳腺X射线摄影系统（NeuCare Mammo DR）、从影...\\n\\n'
        ...     u'   公司性质：  私营·民营企业\\n\\n    公司规模：   1000-2000人\\n\\n    公司行业：  医疗设备/器械\\n\\n'
        ...     u'   硬件工程师、风险经理       2005.04-2011.01\\n\\n     工作地点：  沈阳')))
        >>> assert u'电气' in business(company_1(work_xp(u'2010.02-2015.07   浙江正泰仪器仪表有限责任公司\\n公司性质：   国内上市公司\\n'
        ...     u'公司规模：   2000-5000人\\n公司行业：  仪器/仪表/工业自动化/电气\\n担任职务：副总经理  \\n工作地点： 温州')))
        >>> assert 25 == len(business(company_1(work_xp(u'2010年8月  --  2010年9月 奇瑞汽车  |  车床/磨床/铣床/冲床工      （1个月）\\n\\n'
        ...     u'> 所属行业：\\n>\\n> 汽车/摩托车（制造/维护/配件/销售/服务/租赁）\\n>\\n> 公司规模：\\n>\\n> 10000人以上')))) # asprstrip on BPO

    -   employees
        >>> assert '1000' in employees(company_1(work_xp(u'2010年8月  --  2010年9月 奇瑞汽车  |  车床/磨床/铣床/冲床工      （1个月）\\n\\n'
        ...     u'> 所属行业：\\n>\\n> 汽车/摩托车（制造/维护/配件/销售/服务/租赁）\\n>\\n> 公司规模：\\n>\\n> 10000人以上'))) # ANL in business
        >>> assert '1000' in employees(company_1(work_xp(u'2014/4-2015/8    SV HOLDINGS (1年 4个月 )\\n\\n'
        ...     u'家具/家电/玩具/礼品|500-1000人|外资(非欧美)\\n\\n总经办   董事长助理'))) # data: 6abh31qv (business is not COMPANY_BUSINESS)


    General position matching
        >>> assert positions(work_xp(u'2005 /1--2009 /11： 有限公司 （500-1000人）\\n\\n所属行业： 医疗/护理/卫生\\n\\n职位：工程师\\n\\n部 门：系统部'))
        >>> assert positions(work_xp(u'2012.09-至今 有限公司 （3年6个月）\\n\\n研发部主管\\n\\n医疗设备\\n\\n工作描述：'))
        >>> assert u'3G' not in name(position_1(work_xp(u'3G\\n\\nEngineer\\n\\nTelecom\\n\\n2012年4月–至今 (9 个月)中国')))
        >>> assert u'研发项目经理' in name(position_1(work_xp(u'▌2000-11 ～ 2010-04  有限公司\\n\\n担任职位：\\n'
        ...     u'研发项目经理；从事大\\n工作描述：')))

    General position detail matching
    -   salary:
        >>> assert 1 == salary(position_1(work_xp(u'2003.07 - 2006.07 *东芝大连有限公司 医疗器械工厂 (3年) *\\n\\n2000-5000人\\n\\n'
        ...     u'2003.07 - 2006.07**Project Leader**4000月/月元/月\\n**汇报对象：课长 | 下属人数：6 | 所在地区：大连 **'))).count(u'月')


    General matching issues
        >>> assert not positions(work_xp(u'\\n03/2013 – 现在 Consulting\\n\\n高级咨询师')) #FIXME
        >>> assert not positions(work_xp(u'2015/04-至今 Limi（8个月）\\n 开发|60元/月\\n2015/06-至今 有限公司 | php（3个月）\\n工程师|60元/月')) == 2 #FIXME
        >>> assert not positions(work_xp(u'''2014/4-至今：有限公司  产品研发部：工程师''')) #FIXME
        >>> # TODO Next: modified TACO for the trailing line
        >>> assert not positions(work_xp(u'2012-07 至 今\\n\\n有限公司 |\\n职  位： 软件开发(Linux/单片机/DLC/DSP…)')) # FIXME
        >>> assert not positions(work_xp(u'Jun 2012-至今 有限公司---质量经理（管理者代表）'))   #FIXME
        >>> assert not positions(work_xp(u'2014.4--复旦肿瘤医 （Shanghai \\n Center）     医学物理师'))  #FIXME
        >>> assert not positions(work_xp(u'财务总监，连锁集团 （2014年11月2015年5月）'))  #FIXME
        >>> assert not positions(work_xp(u'高级销售经理\\n\\n飞利浦医疗\\n\\n 2014 – 至今 (2 年)福建')) #FIXME #TODO use ECO with AXP
        >>> # Next: detailed date inside full markdown table
        >>> assert not positions(work_xp(u'21/07/2012 — 27/07/2014       项目经理\\n有限公司     四川，中国'))   #FIXME
        >>> assert not positions(work_xp(u'1.  2001.9 – 2004.07  营管理学院   辅导员   工程系'))   #FIXME #TODO use NOPIPETACO
        >>> assert not positions(work_xp(u'就职时间 : 2012-06 ～至今\\n\\n受聘公司 : 有限公司\\n\\n职位名称 : 质量工程师'))   #FIXME
        >>> assert not positions(work_xp(u'2015/03\\~\\n\\n有限公司\\n\\n职位：质量经理'))    #FIXME
        >>> #assert not u'股' in name(company_1(work_xp(u'2014/01 – 2014/11\\n\\n股有限公司 | | 法务主管  ')))   #FIXME


    ECO related
        >>> model = u'Position\\n\\nCompany。\\n\\n2012-07 – Now (2年)'; assert ECO.search(model).group('position')
        >>> assert positions(work_xp(u'Designer\\n\\nHealthcare\\n\\n2011 年 10 月 – 至今 (4 年 4 个月)Wuxi'))
        >>> assert u'工' in name(position_1(work_xp(u'[助理 / \\n工程师](http://www.)\\n\\n[Care]\\n(http://www.)\\n\\n2014年12月–至今(1 年2个月)')))
        >>> assert positions(work_xp(u'项目\\n\\n课程\\n\\nIntern\\n\\nCorporation\\n\\n2011年9月–2013年2月(1年6个月)'))
        >>> assert u'Head' in name(position_1(work_xp(u'Head (FGs\\nmanufacturer)\\n\\nLimited Group\\n\\n2012年6月–至今(2年9个月)')))

    SPO related tests:
        >>> model = u'2012-07 – Now Company。\\n职务：Position'; assert SPO.search(model).group('position')
        >>> assert positions(work_xp(u'2015.07-至今  设备有限公司\\n项目职务： 技术主管\\n所在部门： 研究院'))
        >>> assert positions(work_xp(u'2008.07-2011.03 电力有限公司   职务：工艺技术员/工艺倒班主管\\n工作职责：\\n技术员'))

    jingying related
        >>> model = u'2012-07 – Now   Position | fixed处\\nCompany。 (2年)\\n\\n150-500人|民营'; assert WYJCO.search(model).group('position')
        >>> model = u'2012-07 – Now   Company。\\n所属行业  Business\\nDepartment   Position'; assert PO.search(model).group('position')
        >>> model = u'2012-07 – Now   Company。\\n150-500人|民营\\nDepartment   Position'; assert PO.search(model).group('position')
        >>> model = u'2012-07 – Now Company。 (2年)\\n2012-07 – Now Position'; assert PO.search(model).group('position')
        >>> assert u'自动化' in business(company_1(work_xp(u'搜索同事2015.01 - 至今有限公司(SFAE) (1年7个月)\\n\\n'
        ...     u'外商独资·外企办事处  |  仪器/仪表/工业自动化/电气  |  10000人以上\\n\\n2015.01 - 至今IPM Project Manager & BD22000元/月')))
        >>>     # Different combinations of spaces and unicode spaces
        >>> assert positions(work_xp(u'2010/7--2014/5：有限公司（150-500人）\\n所属行业： 计算机软件\\n研发中心    软件工程师'))
        >>> assert positions(work_xp(u'2014 /10--至今： 有限公司\\n所属行业：\\n 互联网/电子商务\\n\\n管理顾问      高级咨询顾问'))
        >>> assert positions(work_xp(u'2010 /3--至今：医疗设备(150-500人) [ 5 年9个月]\\n所属行业：  医疗/护理/卫生\\nX射线产品事业部   医疗器械研发'))
        >>> assert positions(work_xp(u'2008/3 -- 2014/10： 有限公司（ 1000-5000人） [ 6年7个月 ]\\n所属行业： 电子技术\\n电能表事业部  项目经理'))
        >>> assert positions(work_xp(u'2007 /3--2010 /12：有限公司 [ 3 年9个月]\\n所属行业： 服务(咨询、财会) 越秀集， 5:5 股份。\\n人事部    书/翻译'))    # TODO
        >>> assert positions(work_xp(u'2014 /4--至今：有限公司(150-500人) [ 1 年8个月]\\n所属行业：\\n医疗设备/器械\\nR&D\\n医疗器械研发'))
        >>> assert u'部' not in name(position_1(work_xp(u'''2014/5-至今： 科技集团 [ 2年1个月 ]\\n所属行业： 机械/设备\\n  生产部  生产领班/组长''')))
        >>> assert 'w' not in name(position_1(work_xp(u'2007 /9--2009 /8：INC PROJECT [11个月]\\n 所属行业：   其他\\npro worker  志愿者')))
        >>> assert u'发' in name(position_1(work_xp(u'2014 /4--至今：有限公司[1年8个月]\\n\\n所属行业：\\n\\n医疗设备\\n\\nR&D\\n\\n器械研发')))
        >>> assert u'师' in name(position_1(work_xp(u'2011 /7--至今：有限公司 [ 4 年5个月]\\n\\n所属行业：\\n医疗设\\n\\n/器械\\n技术部\\n工程师')))
        >>> assert u'为' not in name(position_1(work_xp(u'2014/10-至今：有限公司\\n所属行业： 互联网\\n管理顾问      高级咨询顾问\\n为CEO')))
        >>> assert u'户' not in name(position_1(work_xp(u'2010 /3--至今：医疗设备 [5 年]\\n所属行业： 医疗设备/器械\\nX射线产品  器械研发\\n客户')))
        >>> assert u'要' not in name(position_1(work_xp(u'2012 /3--至今：服务中心(150-500人) [ 3年9个月]\\n所属行业： 非盈利机构\\n督导助理\\n主要')))  # TODO
        >>> assert not u'高' in name(position_1(work_xp(u'''2012/4-至今：集团\\n所属行业： 办公用品\\n人力资源 高级经理（ COE ）'''))) #FIXME
        >>> assert u'商务助理' in name(position_1(work_xp(u'2011/7-2013/4     史密斯医疗器械有限公司 (1年 9个月 )\\n'
        ...     u'医疗设备/器械|5000-10000人|外资(欧美)\\n研发部门          商务助理')))

    liepin related
        >>> # Add 。 to make sure company doesn't match position
        >>> model = u'2012-07 – Now Company。\\n2012-07 – Now Position\\n1000元 | 所在部门：Department'; assert LIEPPO.search(model).group('position')
        >>> model = u'2012-07 – Now Company。\\nPosition  2012-07–Now\\n1000元 | 所在部门：Department'; assert NLIEPO.search(model).group('position')
        >>> assert u'品质' in name(position_1(work_xp(u'2007.06-2011.02   爱普生技术(深圳)有限公司 \\n\\n'
        ...     u'   公司性质：外商独资 | 公司规模： 5000人 | 公司行业：机械制造/机电/重工 \\n 公司描述：未填写 \\n\\n'
        ...     u'品质主任      2007.06 - 2011.02 \\n\\n 下属人数：20 | 所在地区：深圳')))

    MOD WYJCO related
        >>> model = u'2012-07 – Now(2年)  Position\\nCompany。\\n\\n工作描述：'; assert DUFRTWYJCO.search(model).group('position')
        >>> model = u'2012-07 – Now(2年)  Position | fixed处\\nCompany。\\n\\n工作描述：'; assert DUFRTWYJCO.search(model).group('position')
        >>> model = u'2012-07 – Now\\[2年\\] Position | fixed处 Company。\\n\\n工作描述：'; assert DUFRTDPTWYJCO.search(model).group('position')

    find_xp related
        >>> model = u'2012-07 – Now Company\\n职位：Position'; assert find_xp(TCO, model)[0]
        >>> model = u'2012-07 – Now Company\\n2012-07 – Now Position  1000元'; assert APO.search(model).group('position')
        >>> assert 2 == companies(work_xp(u'2006.01-2014.08     南方石化集团有限公司\\n\\n----------------n\\n职位：财务经理\\n\\n'
        ...     u'1996.07-2005.12       佛山禅城酒店有限公司\\n\\n职位：财务主管'))
        >>> assert positions(work_xp(u'2014.02 - 至今 有限公司\\n\\n职位： 电气工程师  '))
        >>> assert position_1(work_xp(u'2011.05 - 至今 GE医疗 (4年8个月)\\n2011.05 - 至今研发主管、电气工程师15000元/月'))['salary']
        >>> assert u'发' in name(position_1(work_xp(u'2005/07—2007/05：科技集团\\n\\n所属行业:计算机软件 \\n\\n'
        ...     u'所属部门: 事业群 \\n\\n职位: 开发')))
        >>> assert 4 == len(name(position_1(work_xp(u'▌2012-06～now Shenzhen Shanshi Healthcare Co.,Ltd\\n\\n担任职位：   研发总监'))))

    RESPPO related
        >>> model = u'2012-07 – Now Company。\\n职责：Position\\n150-500人|民营'; assert RESPPO.search(model).group('position')
        >>> assert u'建筑' in business(company_1(work_xp(u'2015/08 - 2016/03   有限公司\\n职责：工程管理\\n'
        ...     u'房地产/建筑/建材/工程| 企业性质：民营| 规模：1000-9999人')))

    BPO related
        >>> model = u'2012-07 – Now Company。 (2年)\\nPosition | 1000元'; assert BPO.search(model).group('position')
        >>> model = u'2012-07 – Now Company。 (2年)\\nDepartment | Position | 1000元'; assert BPO.search(model).group('position')
        >>> model = u'2012-07 – Now Company。 (2年)\\n1000元'; assert not BPO.search(model) # FIXME
        >>> assert not not companies(work_xp(u'**1997.02 - 2000.12  盈生信息中心  （3年10个月） **\\n'
        ...     u'**2001-4000元/月 **\\n贸易/进出口 | 企业性质：民营 | 规模：20人以下'))   #FIXME data: tf84o714
        >>> assert positions(work_xp(u'2008.12-2010.05 公司 （1年5个月）\\n开发部 | 工程师 | 6000元/月'))
        >>> assert positions(work_xp(u'2014/01 - 2015/04 有限公司（1年3个月）\\nWEB、IOS开发工程师|1000元/月以下'))
        >>> assert positions(work_xp(u'**2012.08 - 至今  深圳合信自动化技术有限公司  （2年） **\\n**部门/事业部管理 | 10001-15000元/月 **'))
        >>> assert u'管理' in name(position_1(work_xp(u'2011.12 - 至今  广州市金鑫宝电子有限公司  （4年3个月）\\n'
        ...     u'项目管理/电子工程师\\n医疗设备/器械 | 企业性质：民营')))
        >>> assert u'财务经理' == name(position_1(work_xp(u'2006.02 - 2009.12  沃茨水工业集团  （3年10个月）\\n财务部 | 财务经理 | 15000元/月\\n'
        ...     u'加工制造（原料加工/模具） | 企业性质：外商独资\\n工作描述：    1.职位： （1）刚加入集团时')))
        >>> assert 6 == len(name(position_1(work_xp(u'2013.03 - 至今  企业财务管理顾问  （3年2个月）\\n----\\n\\n##### 财务管理顾问\\n\\n其他'))))
        >>> assert not not positions(work_xp(u'2001.01-2004.12 家具公司 （3年11个月）\\n4001-6000元/月'))   #FIXME (spurious match by BPO?)
        >>> assert u'互联网' in business(company_1(work_xp(u'2012.03-至今 有限公司 （1年1个月）\\n软件工程师\\n互联网/电子商务 | 企业性质：民营\\n')))
        >>> assert u'重工业' in business(company_1(work_xp(u'2013.08 - 2016.06 有限公司  （2年10个月）\\n 工程师 | 10001-15000元/月\\n\\n'
        ...     u'大型设备/机电设备/重工业 | 企业性质：外商独资 | 规模：20-99人\\n\\n')))
        >>> assert u'器械' in business(company_1(work_xp(u'2008.04 - 至今  北研（北京）医疗器械有限公司  （6年9个月） \\n产品开发部 | 软件工程师 \\n'
        ...     u'医疗设备/器械 | 企业性质：合资 | 规模：100-499人 ')))
        >>> assert '10000' in employees(company_1(work_xp(u'2011/11 - 至今   东软集团（沈阳东软医疗系统有限公司）\\n（4年5个月）\\n'
        ...     u'RT产品经理兼西南大区渠道分销经理\\n|8001-10000元/月\\n医疗设备/器械\\n| 企业性质：合资| 规模：10000人以上'))) # data: 550y7tg5
        >>> assert positions(work_xp(u'**2012.08 - 至今  深圳合信自动化技术有限公司  （2年） **\\n-----------------------------\\n'
        ...     u'**部门/事业部管理 | 10001-15000元/月 **\\n仪器仪表及工业自动化 | 企业性质：民营 | 规模：100-499人'))

    New liepin related
        >>> assert positions(work_xp(u'2015.06\\n- 至今*广州昱为网络科技有限公司* *(1年6个月)*\\n\\n---------------\\n'
        ...     u'私营·民营企业  |  互联网/移动互联网/电子商务  |  100-499人\\n广州昱为网络科技有限公司。...\\n---------------\\n\\n'
        ...     u'市场经理\\n汇报对象：市场总监 | 下属人数：5 | 所在地区：广州 | 所在部门：市场部')) # data: sqmlpe5u
        >>> assert 5 == len(name(position_1(work_xp(u'2011.11 - 2016.06Prismatic Sensor AB (Sweden)** (4年7个月)\\n\\n'
        ...     u'-----------\\n外商独资·外企办事处  |  医疗设备/器械  |  1-49人\\nsubsequent system integration.\\n-----------\\n\\n'
        ...     u'-----------\\n**研发工程师**\\n下属人数：1 | 所在地区：瑞典\\n-----------'))))

    BPONOSAL related
        >>> model = u'2012-07 – Now Company。 (2年)\\nPosition'; assert BPONOSAL.search(model).group('position')
        >>> assert 2 == companies(work_xp(u'**2010.07 - 2012.02  中国船舶集团安庆中船柴油机有限公司  （1年7个月）**\\n\\n'
        ...     u'##### **产品开发/技术/工艺 | 2001-4000元/月**\\n\\n大型设备/机电设备/重工业 | 企业性质：国企\\n\\n'
        ...     u'工作描述：   从事大型分离机械研发、样机的生产跟踪。\\n\\n**2009.03 - 2009.07  安徽冶金职业技术学院  （4个月）**\\n\\n'
        ...     u'##### **科研人员**\\n\\n学术/科研 | 企业性质：事业单位 | 规模：100-499人'))
        >>> assert 7 == len(name(position_1(work_xp(u'**2015.02 - 至今  广州未莱信息科技有限公司  （1年1个月）**\\n\\n'
        ...     u'##### **WEB前端开发**\\n\\n计算机软件   \\n\\n------------\\n工作描述：  等等；\\n------------'))))

    COULDDEPO related
        >>> model = u'2012-07 – Now Company。 (2年)\\nPosition\\n工作职责：anything'; assert COULDDEPO.search(model).group('position')
        >>> assert positions(work_xp(u'**2015.06 - 至今 卡尔蔡司光学(中国)有限公司(1年4个月) **\\n\\n'
        ...     u'**自动化软件工程师**\\n\\n工作职责：负责公司非标自动化设备开发的电气和软件部分'))

    All TACO related
        >>> model = u'2012-07 – Now Company\\nPosition'; assert NOPIPETACO.search(model).group('cposition')
        >>> model = u'2012-07 – Now Company\\nPosition (2年)'; assert NOPIPETACO.search(model).group('cposition')
        >>> model = u'2012-07 – Now Company | Position (2年)'; assert DRTACO.search(model).group('position')
        >>> model = u'2012-07 – Now Company | Department | Position (2年)'; assert DRTACO.search(model).group('position')
        >>> assert companies(work_xp(u'2014年10月——2014年11月   技工学校    实习班主任、老师'))
        >>> assert companies(work_xp(u'2000年6月-2007年6月 公司 | 管理部\\n | 副课长\\n(一) 2000.06-2004.06：管理 人事副课长')) == 1
        >>> assert u'离子' in name(company_2(work_xp(u'2008年11月  --  2010年12月\\n公司、集团有限公司（中国建材）  |  EHS部  |\\n'
        ...     u' 安全业务经理  （2年1个月）\\n2006年9月  --  2008年11月 \\n'
        ...     u'加拿大HDI矿业集团西藏天圆矿业资源开发有限公司、比利时亿比亚离子\\n |  安全部  |  安全监理、主管  （2年2个月） ')))
        >>> assert positions(work_xp(u'2015年5月～至今  有限公司\\n  人力资源总监'))
        >>> assert positions(work_xp(u'2014/06 -- 2014/12\\n\\n有限公司 | 项目经理'))
        >>> assert positions(work_xp(u'2009/09 -- 2010/09\\n\\nAlcatel | CIO | Engineer'))
        >>> assert positions(work_xp(u'2014年4月 -- 至今 公司 | 客户服务经理、CT临床支持经理 （2年1个月）'))
        >>> assert positions(work_xp(u'2014年2月 -- 至今 管理（中国）有限公司\\n | 人力资源总监 （2年3个月）'))
        >>> assert positions(work_xp(u'。2010/07 -- 2012/06\\n\\n政邦律师事务所 | | 律师助理'))
        >>> assert positions(work_xp(u'\\n2007年3月～2009年2月  有限公司\\n\\n其中2009/3—2010/9培训主管'))
        >>> assert positions(work_xp(u'2001年6月 -- 至今 第一附属医院 | 影像中心 |\\n放射科医师  （14年11个月）'))
        >>> assert positions(work_xp(u'2008年3月-2011年5月 Care Ltd. | 工程师\\n2011年5月-2013年6月 医疗  工程师')) == 2
        >>> assert u'工程师' in name(position_1(work_xp(u'2010.03 - 2011.08  广州丰得利实业公司  （1年5个月）'
        ...     u'技术部 | 电子工程师\\n医疗设备/器械 | 企业性质：民营')))
        >>> assert u'工程师' in name(position_1(work_xp(u'2014年6月  --  至今 西藏华东水电成套设备有限公司  |  电气工程师'
        ...     u'     （2年）\\n\\n所属行业：\\n\\n电气/电力/水利'))) # to pass WYCO must not match
        >>> assert 4 == len(name(position_1(work_xp(u'2011年2月 -- 至今 中国医药工业有限公司 | 安全环保部 | 部门经理\\n（5年5个月）\\n\\n'
        ...     u'所属行业：\\n\\n医药/生物工程\\n\\n公司性质：\\n\\n国企\\n\\n公司规模：\\n\\n1000-9999人'))))
        >>>     # TODO empty middle field between pipes (spurious match to TACO?, pass otherwise)
        >>> assert not u'Leader' in name(position_1(work_xp(u'2010/10 -- Now\\n\\nHealthcare | CT | R&D | Engineer / Project\\nLeader')))  #FIXME
        >>> assert not u'硬件' in name(position_1(work_xp(u'2016.06 - 至今  上海光电医用电子仪器有限公司\\n基础部硬件工程师 | 10001-15000元/月\\n'
        ...     u'医疗设备/器械 | 企业性质：外商独资 | 规模：100-499人')))   #FIXME (spurious match by TACO?)
        >>> assert duration(company_1(work_xp(u'2001年6月 -- 至今 第一附属医院 | 影像中心 |\\n放射科医师  （14年11个月）')))
        >>> assert duration(company_1(work_xp(u'2014年4月 -- 至今 公司 | 客户服务经理、CT临床支持经理\\n （2年1个月）')))
        >>> assert duration(company_1(work_xp(u'2012年1月 -- 2012年10月 有限公司 | 支持部\\n | 部经理 （9个月）')))
        >>> assert u'政府' in business(company_1(work_xp(u'2014年7月  --  至今 研究院珠海检测院  |\\n 公务员/事业单位人员  （1年11个月）\\n\\n'
        ...     u'所属行业：\\n\\n政府/公共事业/非盈利机构')))
        >>> assert u'器械' in business(company_1(work_xp(u'2014年4月  --  至今 深圳公司  |  客户服务经理\\n      （2年1个月）\\n\\n'
        ...     u'所属行业：医疗设备/器械')))
        >>> assert u'器械' in business(company_1(work_xp(u'2006年1月  --  2011年6月 有限公司 | 售后服务部 | 现场服务工程师  （6年5个月）\\n\\n'
        ...     u'公司介绍：加速器医疗设备\\n\\n所属行业：医疗设备/器械')))
        >>> assert '100' in employees(company_1(work_xp(u'##### 2012年3月 -- 至今 有限公司 | 质量管理中心 | 质量经理 （3年10个月）\\n'
        ...     u'所属行业：\\n\\n医疗设备/器械\\n\\n公司性质：\\n\\n合资\\n\\n公司规模：\\n\\n100-499人')))

    PCO related
        >>> model = u'2012-07 – Now Company | Position (2年)'; assert PCO.search(model).group('position')  # First covered by DRTACO
        >>> model = u'2012-07 – Now Co\\nmpany | Position (2年)'; assert PCO.search(model).group('position') # Not covered by DRTACO
        >>> # TODO Add some

    PUNCTCO related
        >>> model = u'2012-07 – Now Company，Position。'; assert PUNCTCO.search(model).group()
        >>> assert positions(work_xp(u'2013.9- 至今 苏州微清医疗器械有限公司，高级算法工程师。'))

    TCO related
        >>> model = u'2012-07 – Now Company'; assert TCO.search(model).group()
        >>> assert companies(work_xp(u'1.  2013.8——至今 有限公司'))
        >>> assert companies(work_xp(u'（海外）2011/3 -\\n2014/7：有限公司（5000-10000人）'))
        >>> assert companies(work_xp(u'??2015.10– 2016.01 赛诺微医疗科技（北京）有限公司')) # Is matched by other if TCO fully removed

    RCO related
        >>> model = u'Company Position 2012-07 – Now (2年)'; assert RCO.search(model).group('position')
        >>> assert positions(work_xp(u'有限公司 工程师 2013/07\~2014/08  广州'))
        >>> assert positions(work_xp(u'有限公司 招聘主管 2015/03 至今（ 1 年 1 个月） 保密'))
        >>> assert positions(work_xp(u'有限公司 招聘主管 2009/03 至 2013/03 （ 4\\n年） 保密'))
        >>> assert positions(work_xp(u'有限公司  加速器工程师  2013/07\~2014/08  广州\\n\\n公司  技术研发工程师  2014/08至今  上海')) == 2

    RTACPO related
        >>> model = u'Company (2年) \\n2012-07 – Now Position  1000元'; assert RTACPO.search(model).group()
        >>> model = u'Company (2年) \\n2012-07 – Now Position  1000元'; assert APO.search(model).group('position')
        >>> model = u'Company 2012-07 – Now \\n2012-07 – Now Position  1000元'; assert RTACPO.search(model).group()
        >>> assert companies(work_xp(u'■医院 （2012-04 \~ 至今）\\n公司性质：\\n担任职位：英语翻译'))
    """
    RE = None
    out = {'company': [], 'position': []}
    if ECO.search(text):
        out = {'company': [], 'position': []}
        for r in ECO.finditer(text):
            company_output(out, r.groupdict())
            position_output(out, r.groupdict())
    if not len(out['position']):
        out = {'company': [], 'position': []}
        RE = regex.compile(company_details(re.compile(BDURATION, re.M)), re.M)
        res = RE.search(text)
        # Only run SPO if WYJCO does not match (for speed up)
        if not res:
            # Can't use CO/TCO as they expect EOL
            MA = regex.compile(u'^'+ASP+u'*'+PERIOD+ASP+u'*(?P<company>[^' + SENTENCESEP + '=\n\*]+?)'+ASP+u'*'+SPO.pattern, re.M)
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
    if not len(out['position']):
        if not len(out['position']):
            pos, out = work_xp_liepin(text)
            if pos:
                return pos, out
            if not pos:
                pos, out = work_xp_modified_wyjco(text)
                if pos:
                    return pos, out
            if not pos:
                pos, out = work_xp_jingying(text)
                if pos:
                    return pos, out
            for RE in [CCO, CO, TCO]:
                if (RE == TCO or re.compile(BDURATION).search(text)) and RE.search(text):
                    out = {'company': [], 'position': []}
                    if not len(out['position']):
                        MA = regex.compile(company_details(RE).replace('{1,13}', '{3,13}'), re.M)
                        if not MA.search(text):
                            # company_business always matches what RE matches
                            MA = regex.compile(empty_company_details(RE), re.M)
                        pos, out = find_xp(MA, text)
                        if pos:
                            return pos, out
                    if not len(out['position']):
                        out = {'company': [], 'position': []}
                        MA = regex.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+RESPPO.pattern+u'))', re.M)
                        for r in MA.finditer(text):
                            if r.group('co'):
                                dfrom, dto = r.group('from'), r.group('to')
                                company_output(out, r.groupdict())
                            else:
                                position_output(out, r.groupdict(), begin=dfrom, end=dto)
                        if len(out['position']):
                            return len(out['position']), out
                    #break
        if re.compile(BDURATION).search(text) and CO.search(text):
            # Can try more things with CO as both PERIOD and DURATION safeguards
            if BPO.search(text):
                out = {'company': [], 'position': []}
                # While we have a BPO-like document, also match BPONOSAL inside
                MA = regex.compile(u'((?P<co>'+CO.pattern+u')'+ASP+u'*(\-{3,}(?: \-+)* *\n+)?'+ASP+u'*(?P<po>'+empty_company_details_pipeonly(BPONOSAL)+u'))', re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
                    position_output(out, r.groupdict())
            if not len(out['position']):
                pos, out = work_xp_new_liepin(text)
                if pos:
                    return pos, out
            if not len(out['position']):
                out = {'company': [], 'position': []}
                MA = regex.compile(u'((?P<co>'+CO.pattern+u')'+ASP+u'*(\-{3,}(?: \-+)* *\n+)?'+ASP+u'*(?P<po>'+empty_company_details_pipeonly(BPONOSAL)+u'))', re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
                    position_output(out, r.groupdict())
            if not len(out['position']):
                out = {'company': [], 'position': []}
                MA = regex.compile(u'(?P<co>'+CO.pattern+u')(\n+'+COULDDEPO.pattern+u')?', re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
                    if r.group('position'):
                        position_output(out, r.groupdict())
        elif DRTACO.search(text) or ALLTACO.search(text):
            pos, out = work_xp_zhilian(text)
        elif PCO.search(text):
            out = {'company': [], 'position': []}
            MA = regex.compile(empty_company_details(PCO), re.M)
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        elif PUNCTCO.search(text):
            out = {'company': [], 'position': []}
            MA = PUNCTCO
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        elif TCO.search(text):
            if not len(out['position']):
                out = {'company': [], 'position': []}
                pattern = empty_company_details(TCO)
                # If position was present, it would have been catched in find_xp
                MA = regex.compile(empty_position_details(regex.compile(pattern)), re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
        elif RCO.search(SHORTEN_BLANK(text)):
            out = {'company': [], 'position': []}
            for r in RCO.finditer(SHORTEN_BLANK(text)):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        elif RTACPO.search(SHORTEN_BLANK(text)):
            out = {'company': [], 'position': []}
            pattern = empty_company_details(RTACPO)
            MA = regex.compile(pattern+ASP+u'+'+TAPO.pattern[1:], re.M)
            for r in MA.finditer(SHORTEN_BLANK(text)):
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
    return len(out['position']), out

def table_based_xp(text):
    u"""
        >>> assert table_based_xp(u'公司名称 有限公司\\n时间  2013.06 ——2014.04\\n\\n职务 助理硬件工程师')[0]
        >>> assert table_based_xp(u'任职时间 2013 年9月至2014年9月\\n企业名称 投资有限公司\\n职位  财务总监')[0]
        >>> assert table_based_xp(u'1、任职公司： （日资） 尼利可自动控制机器（上海）有限公司\\n任职时间：2013.05-至今\\n'
        ...     u'公司背景：\\n职　　位：现场应用工程师，研发工程师')[0]
        >>> assert positions(table_based_xp(u'1.  公司名称: 广州市动景计算机科技有限公司（手机UC浏览器）\\n起止时间: 2011年9月-2013年5月\\n'
        ...     u'行业类别: 互联网/IT\\n担任职位：财务经理\\n汇报对象：财务总监\\n下属人数：8人\\n工作职责：准备集团每月')) # data: 5cyp5myj
        >>> assert positions(table_based_xp(u'任职时间      2005年4月至2013年3月\\n企业名称  投资有限公司   所在地区   广州\\n'
        ...     u'企业简介  （嘉汉林业投资有限公司）\\n部门   财务部   直接上司职位  副总裁\\n职位   财务经理（财务负责人） ')) # data: 616r6zx3
        >>> assert u'硬件' in name(position_1(table_based_xp(u'公司名称  有限公司\\n时间  2013.06 ——2014.04\\n职务  硬件工程师'))) # data: jvcdkbhx
    """
    out = {'company': [], 'position': []}
    if HCO.search(text):
        pattern = empty_company_details(HCO)
        MA = regex.compile(empty_position_details(regex.compile(pattern)), re.M)
        for r in MA.finditer(text):
            company_output(out, r.groupdict())
            if r.group('aposition'):
                position_output(out, r.groupdict())
    return len(out['position']), out


def match_classify(experience, company_service=None):
    u"""
        >>> import yaml
        >>> experience = yaml.load(u'company:\\n'
        ... u'    - {business: 房地产, date_from: \\'2012.06\\', date_to: 至今, duration: 4年2个月, id: 0, name: 有限公司,\\n'
        ... u'        total_employees: 150-500人}')
        >>> assert len(match_classify(experience)) == 1
        >>> assert u'房地产' == match_classify(experience)[0]
        >>> experience = yaml.load(u'company:\\n'
        ... u'    - {business: 医疗设备/器械, date_from: \\'2010.03\\', date_to: 至今, duration: 6年5个月, id: 0,\\n'
        ... u'      name: 医疗设备, total_employees: 150-500人}')
        >>> assert len(match_classify(experience)) == 1
        >>> assert u'生物' in match_classify(experience)[0]
        >>> experience = yaml.load(u'company:\\n'
        ... u'    - {business: 医疗设备/器械, date_from: \\'2012.09\\', date_to: 至今, duration: 3年11个月, id: 0,\\n'
        ... u'      name: 有限公司, total_employees: 500-1000人}\\n'
        ... u'    - {business: 计算机软件, date_from: \\'2003.07\\', date_to: \\'2010.11\\', duration: 7年4个月, id: 2,\\n'
        ... u'      name: 有限公司, total_employees: 150-500人}')
        >>> assert u'计算机软件' in match_classify(experience)
        >>> assert u'生物/制药/医疗器械' in match_classify(experience)
        >>> experience = yaml.load(u'company:\\n'
        ... u'    - {business: 电子技术 | 计算机硬件, date_from: \\'2010.10\\', date_to: 至今, duration: 5年,\\n'
        ... u'      id: 0, name: 东莞电厂}')
        >>> assert len(match_classify(experience)) == 2
    """
    output = set()
    try:
        company = experience['company']
        for c in company:
            try:
                business = [b.strip() for b in c['business'].split('|')]
                for (k, v) in CLASSIFY.items():
                    for b in business:
                        m = v.match(b)
                        if m:
                            output.add(k)
            except KeyError:
                if company_service and company_service.exists(extractor.unique_id.company_id(c['name'])):
                    try:
                        for b in company_service.getyaml(extractor.unique_id.company_id(c['name']))['business']:
                            for (k, v) in CLASSIFY.items():
                                m = v.match(b)
                                if m:
                                    output.add(k)
                    except KeyError:
                        pass
            finally:
                pass
    except KeyError:
        pass
    finally:
        return sorted(list(output))


def fix_output(processed, as_date=None):
    result = {}
    for company in processed['company']:
        positions = [p for p in processed['position'] if p['at_company'] == company['id']]
        if len(positions) <= 1:
            if not company['duration']:
                company['duration'] = compute_duration(company['date_from'], company['date_to'], as_date)
            try:
                positions[0]['duration'] = company['duration']
                del company['duration']
            except IndexError:
                continue
            except KeyError:
                continue
    if processed['company']:
        classify = match_classify(processed)
        if classify:
            result['classify'] = classify
        processed['company'] = sorted(processed['company'], key=lambda x: x['date_to'], reverse=True)
        result['experience'] = processed
    return result

def fix_new_liepin(d, as_date=None):
    u"""
    """
    processed = {'company': [], 'position': []}
    res = XP.search(d)
    if res:
        pos, out = work_xp_new_liepin(res.group('expe'))
        if not pos and len(out['company']) == 0:
            pass
        else:
            processed = out
    else:
        res = AXP.search(d)
        if res:
            pos, out = work_xp_new_liepin(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
    return fix_output(processed, as_date)

def fix_new_liepin(d, as_date=None):
    u"""
    """
    processed = {'company': [], 'position': []}
    res = XP.search(d)
    if res:
        pos, out = work_xp_new_liepin(res.group('expe'))
        if not pos and len(out['company']) == 0:
            pass
        else:
            processed = out
    else:
        res = AXP.search(d)
        if res:
            pos, out = work_xp_new_liepin(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
    return fix_output(processed, as_date)

def fix_liepin(d, as_date=None):
    u"""
    PJCO related tests
        >>> assert u'美' in fix_liepin(
        ...     u'项目经历\\n 2013.09-至今 手术器械\\n项目职务： 经理\\n\\n所在公司： 美国\\n教育经历')['experience']['company'][0]['name']
        >>> assert u'设' in fix_liepin(
        ...     u'项目经历\\n 2009.04 - 2010.03 飞机除冰车技术改进\\n所在公司： 设备有限公司\\n教育经历')['experience']['company'][0]['name']
        >>> assert u'医' in fix_liepin(u'项目经历\\n 2012.12 - 至今 系统Coreload 3.x\\n项目职务： 高级工程师\\n所在公司： 医疗(中国)\\n教育经历'
        ...     )['experience']['company'][0]['name']
        >>> assert u'苏' in fix_liepin(u'项目经历\\n   2011.01 - 2016.02 自研开发\\n项目职务：设备部经理\\n所在公司：苏州\*\*\*有限公司\\n教育经历'
        ...     )['experience']['company'][0]['name']
    """
    if is_nlpcv(d):
        return fix_new_liepin(d, as_date)

    processed = {'company': [], 'position': []}
    res = XP.search(d)
    if res:
        pos, out = work_xp_liepin(res.group('expe'))
        if not pos and len(out['company']) == 0:
            pass
        else:
            processed = out
    else:
        res = AXP.search(d)
        if res:
            pos, out = work_xp_liepin(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
        elif PXP.search(d):
            out = {'company': [], 'position': []}
            res = PXP.search(d)
            if PJCO.search(res.group('expe')):
                for r in PJCO.finditer(res.group('expe')):
                    company_output(out, r.groupdict())
                    if r.group('position'):
                        position_output(out, r.groupdict())
            if not len(out['position']) and len(out['company']) == 0:
                pass
            else:
                processed = out
    return fix_output(processed, as_date)

def fix_yingcai(d, as_date=None):
    u"""
        >>> assert u'4年' in fix_yingcai(u'工作经历\\n2010.04 - 2014.11\\n商业银行\\n所属行业：计算机硬件\\n月薪：保密\\n'
        ...     u'销售部内勤')['experience']['company'][0]['duration']
    """
    processed = {'company': [], 'position': []}
    for RE in [PRXP, AXP]:
        res = RE.search(d)
        if res:
            pos, out = work_xp_yingcai(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed, as_date)

def fix_zhilian(d, as_date=None):
    u"""
    """
    processed = {'company': [], 'position': []}
    for RE in [PRXP, AXP]:
        res = RE.search(d)
        if res:
            pos, out = work_xp_zhilian(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed, as_date)

def fix_jingying(d, as_date=None):
    u"""
    """
    processed = {'company': [], 'position': []}
    for RE in [XP, AXP]:
        res = RE.search(d)
        if res:
            pos, out = work_xp_jingying(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed, as_date)
    
    
def fix(d, as_dict=False, as_date=None):
    u"""
        >>> assert XP.search(u'**工作经历 **\\n\\n**2012.10 - 2013.01  生产测试平台开发 **\\n\\n**教育经历 **')
        >>> assert not fix(u'2014年7月\~  苹果采购运营管理（上海）有限公司')[0][0] #FIXME
        >>> assert fix(u'工作经历：\\n\\n 教育背景：\\n\\n 2009年')[1]
        >>> assert fix(u'工作经历\\n公司名称：美赞臣营养品有限公司\\n 起止时间：2013年5月-至今')[0][0]
        >>> assert fix(u'工作经历\\n音视频可靠光传输系统项目背景')[1] == 3   #项目背景 stop inside text
        >>> assert fix(u'工作经验：1年\\n公司名称 深圳x有限公司\\n 时间 2013.06 ——2014.04\\n职务 硬件工程师')[0][1]
        >>> assert fix(u'工作经历\\n1.  公司名称：有限公司\\n起止时间：2013年5月-至今\\n\\n担任职位：总账高级会计师')[0][1]
        >>> assert fix(u'工作经验\\n工作时间 岗位职能 公司名称\\n2013年11月至2015年1月 设计师 旗舰店', True)['experience']['position']
        >>> assert not fix(u'''工作经历\\n销售经理\\n飞利浦\\n 2014 – 至今 (2 年)福建\\n销售与渠道\\n教育背景''', True) #FIXME
        >>> assert not fix(u'工作经验\\n器械股份有限公司\\n技术质量部 | 项目主管\\n汇报上级：研发经理\\n工作地点：北京\\n'
        ...     u'工作时间：2009/06-2011/08\\n 工作内容（医疗器械经验）', True) #FIXME
        >>> assert u'深圳' in fix(u'简历ID：RCC0024498841\\n工作经验\\n\\n'
        ...     u'2013年3月  --  至今 深圳市有限公司  |  软件研发工程师\\n      （3年4个月）\\n\\n'
        ...     u'2013 年 3 月 -至今\\n就职于深圳市博英医疗仪器科技有限公司技术部，担任应用软件工程师。 负责\\n\\n'
        ...     u'2012年2月  --  2013年3月 有限公司  |  软件工程师\\n      （1年1个月）\\n\\n'
        ...     u'2012 年 2 月至 2013 年 3 月\\n\\n就职于公司研发中心软件部。主要服务于大型 LED\\n', True)['experience']['company'][0]['name']
        >>> assert 2 == len(fix(u'工作经历\\n----------\\n2015/04 - 2015/12   Pluscale Limited（8个月）\\nWEB前端开发|4001-6000元/月\\n'
        ...     u'互联网/电子商务|企业性质：外商独资|规模：20人以下\\n\\n2014/01 - 2015/04   江门市天诺信息科技有限公司（1年3个月）\\n'
        ...     u'WEB安全维护、IOS开发工程师|1000元/月以下\\n互联网/电子商务|企业性质：民营|规模：20人以下', True)['experience']['company'])
        >>> assert not 2 == len(fix(u'工作经历\\n----------\\n2015/06 - 2015/09   广州咪哑科技有限公司 | php工程师（3个月）\\n'
        ...     u'web前端开发工程师、php工程师|4001-6000元/月\\n互联网/电子商务|企业性质：民营|规模：20人以下\\n\\n'
        ...     u'2014/01 - 2015/04   江门市天诺信息科技有限公司（1年3个月）\\n'
        ...     u'WEB安全维护、IOS开发工程师|1000元/月以下\\n互联网/电子商务|企业性质：民营|规模：20人以下', True)['experience']['company'])    #FIXME

    All TACO related
        >>> assert u'基础' in fix(u'简历ID：RCC0012345678\\n\\n姓名：\\n工作经验\\n\\n2007年6月 -- 2014年2月 基础医疗  |  人力资源经理\\n'
        ...     u'   （6年8个月）\\n\\n1.结合公司战略和业务需要\\n\\n2.修订执行人力', True)['experience']['company'][0]['name']

    The next statement is that output (3) from PO in matching
    the next string should not be overwritten by BPO (2),
    regardless PO find no position.
        >>> assert not len(fix(u'工作经历\\n2015-4 至 今       小队*---*2个月\\n带领队员\\n2014-7 至 2014-9  管理有限公司*---* 3个月\\n'
        ...     u'所在部门：开发一部\\n2014-3 至 2014-6 东方学校*---* 4个月\\n----\\n教育经历', True)['experience']['company']) == 3    #FIXME

    Business for TXP/TPO:
        >>> assert fix(u'---------\\n2012.06-至今  器械有限公司\\n\\n    公司性质：中外合营 | 公司规模： 1000人 | 公司行业：医疗设备/器械\\n'
        ...     u'公司描述：国内\\n\\n生产质量管理部经理 7000元/月   2013.10 - 至今\\n---------', True)['experience']['company'][0]['business']
        >>> assert fix(u'---------\\n2006.07-2008.06  电子有限公司\\n\\n  公司性质：未填写 | 公司规模： 未填写 | 公司行业：电子技术/半导体/集成电路'
        ...     u'公司描述：未填写\\n\\n高级采购员    2006.07 - 2008.06\\n---------', True)['experience']['company'][0]['business']
    """
    def fix_output_legacy(processed, reject, as_date):
        if as_dict:
            return fix_output(processed, as_date)
        else:
            for company in processed['company']:
                company['at_company'] = -1
            tuple_format = lambda x: tuple([x[k] for k in ['date_from', 'date_to', 'name', 'duration', 'at_company']])
            return ([tuple_format(p) for p in processed['company']], [tuple_format(p) for p in processed['position']]), reject

    if as_dict:
        if is_jycv(d):
            return fix_jingying(d, as_date)
        elif is_lpcv(d):
            return fix_liepin(d, as_date)
        elif is_zlcv(d):
            return fix_zhilian(d, as_date)
        elif is_yccv(d):
            return fix_yingcai(d, as_date)
        elif is_nlpcv(d):
            return fix_new_liepin(d, as_date)

    reject = 0
    processed = {'company': [], 'position': []}
    res = BTXP.search(d)
    if res:
        for r in BTCO.finditer(res.group('expe')):
            company_output(processed, r.groupdict())
            position_output(processed, r.groupdict())
    if len(processed['position']):
        return fix_output_legacy(processed, reject, as_date)
    res = XP.search(d)
    if res:
        pos, out = table_based_xp(res.group('expe'))
        if not pos and len(out['company']) == 0:
            pos, out = work_xp(res.group('expe'))
            if not pos and len(out['company']) == 0:
                reject = 1
            else:
                processed = out
        else:
            processed = out
    else:
        res = AXP.search(d)
        if res:
            if TABLECO.search(res.group('expe')):
                out = {'company': [], 'position': []}
                for r in TABLEPO.finditer(res.group('expe')):
                    company_output(out, r.groupdict())
                    position_output(out, r.groupdict())
                processed = out
            else:
                pos, out = table_based_xp(res.group('expe'))
                if not pos and len(out['company']) == 0:
                    pos, out = work_xp(res.group('expe'))
                    if not pos and len(out['company']) == 0:
                        reject = 3
                    else:
                        processed = out
                else:
                    processed = out
        elif EXP.search(d):
            out = {'company': [], 'position': []}
            res = EXP.search(d)
            pos, out = work_xp(res.group('expe'))
            if not pos and len(out['company']) == 0:
                reject = 5
            else:
                processed = out
        elif TXP.search(d):
            out = {'company': [], 'position': []}
            res = TXP.search(d)
            pos, out = table_based_xp(res.group('expe'))
            if pos:
                return fix_output_legacy(out, reject, as_date)
            if TCO.search(res.group('expe')):
                complement = u'\n*'+ASP+u'*公司性质：\S+ \| 公司规模： '+AEMPLOYEES+u' \| 公司行业：(?P<business>\S+)$'
                MA = regex.compile(u'((?P<co>'+TCO.pattern+u'('+complement+u')?)|(?P<po>'+TPO.pattern+u'))', re.M)
                for r in MA.finditer(res.group('expe')):
                    if r.group('co'):
                        company_output(out, r.groupdict())
                    else:
                        position_output(out, r.groupdict())
                if not len(out['position']):
                    out = {'company': [], 'position': []}
                    dto = ''
                    dfrom = ''
                    MA = regex.compile(u'((?P<co>'+TCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
                    for r in MA.finditer(res.group('expe')):
                        if r.group('co'):
                            dfrom, dto = r.group('from'), r.group('to')
                            company_output(out, r.groupdict())
                        else:
                            position_output(out, r.groupdict(), begin=dfrom, end=dto)
            if not len(out['position']) and len(out['company']) == 0:
                reject = 2
            else:
                processed = out
        else:
            reject = 4
    return fix_output_legacy(processed, reject, as_date)
