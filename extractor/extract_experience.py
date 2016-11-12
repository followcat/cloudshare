# -*- coding: utf-8 -*-
import re

import sources.industry_id

from extractor.utils_parsing import *
import extractor.unique_id


XP = re.compile(ur'^'+ASP+u'*'+ UNIBRALEFT +u'?((((工'+ASP+u'?作'+ASP+u'?)|(实习)|(工作(与)?实践))经'+ASP+u'?[历验])|(实习与实践))'+ UNIBRARIGHT +u'?(?P<expe>.*?)^'+ASP+u'*(?='+ UNIBRALEFT +u'?((((项'+ASP+u'?目)|(教'+ASP+u'?育))'+ASP+u'?((经'+ASP+u'?[历验])|(背景)|(/?培训)))|(工作内容（医疗器械经验）))'+ UNIBRARIGHT +u'?)', re.DOTALL+re.M)
AXP = re.compile(ur'^'+ASP+u'*'+ UNIBRALEFT +u'?((((工'+ASP+u'?作'+ASP+u'?)|(实习)|(工作(与)?实践))经'+ASP+u'?[历验])|(实习与实践))'+ UNIBRARIGHT +u'?[:：]?'+ASP+u'*'+DURATION+'?'+ASP+u'*?\n(?P<expe>.*)', re.DOTALL+re.M)
TXP = re.compile(ur'-{9}[\-'+SP+u']*(?P<expe>'+PERIOD+ur'.*?)(?=-{9}[\-'+SP+u']*)', re.DOTALL)

PXP = re.compile(ur'^'+ASP+u'*'+ UNIBRALEFT +u'?项目经历'+ UNIBRARIGHT +u'?(?P<expe>.*?)^'+ASP+u'*(?='+ UNIBRALEFT +u'?(((教'+ASP+u'?育))'+ASP+u'?((经'+ASP+u'?[历验])|(背景)|(培训)))'+ UNIBRARIGHT +u'?)', re.DOTALL+re.M)


# Allow multiline once in company name when duration is present
# As company has at least one char, need to handle break just as company tail
# Catching all employees is too expensive on parenthesis repetition, some will be post processed
ECO = re.compile(u'^(?P<position>(\S[\S ]+\n)*)\n+(?P<company>(\S[\S ]+\n)*)\n+' + PERIOD +ASP+u'*' + BDURATION, re.M+re.DOTALL)
CO = re.compile(PERIOD+ur'(('+ASP+u'?[:：'+SP+u']'+ASP+u'*)|([:：]?'+ASP+u'*(?P<cit>\*)?))(?P<company>'+COMPANY+u'(\n'+COMPANYTAIL+u')?)'+BEMPLOYEES+'?(?(cit)\*)?'+ASP+u'*'+BDURATION+'(?(cit)\*)?'+ASP+u'*$', re.DOTALL+re.M)
CCO = re.compile(PERIOD+ur'(('+ASP+u'?[:：'+SP+u']'+ASP+u'*)|([:：]?'+ASP+u'*(?P<cit>\*)?))(?P<company>'+COMPANY+u'(\n'+COMPANY+u')?)'+BEMPLOYEES+'?(?(cit)\*)?'+ASP+u'*'+BDURATION+'(?(cit)\*)?'+ASP+u'*$', re.DOTALL+re.M)
TCO = re.compile(u'^'+PREFIX+u'*'+CONTEXT+u'?'+ASP+u'*'+PERIOD+ur'(('+ASP+u'?[:：'+SP+u']'+ASP+u'*)|([:：]?'+ASP+u'*(?P<cit>\*)?))(?P<company>'+COMPANY+u')'+ASP+u'*'+BDURATION+'?(?(cit)\*)?$', re.DOTALL+re.M)
PCO = re.compile(PERIOD+ur'(('+ASP+u'?[:：'+SP+u']'+ASP+u'*)|([:：]?'+ASP+u'*(?P<cit>\*)?))(?P<company>'+COMPANY+u'(\n(('+COMPANY+u')|('+COMPANYTAIL+u')))?)(?(cit)\*)'+ASP+u'*\|'+ASP+u'*(?P<position>'+POSITION+u'?)'+ASP+u'*'+BDURATION+'$', re.DOTALL+re.M)

PJCO = re.compile(u'^'+PREFIX+u'*'+ASP+u'*'+PERIOD+ASP+u'*(?P<project>.+)\n('+ASP+u'*项目职务[:：]?'+ASP+u'*(?P<position>'+POSITION+u'))?'+ASP+u'*所在公司[:：]?'+ASP+u'*(?P<company>'+COMPANY+u')$', re.M)
WYJCO = re.compile(u'^'+PREFIX+u'*'+ASP+u'*'+PERIOD+ASP+u'*(?P<position>'+POSITION+u')'+ASP+u'*\|'+ASP+u'*(?P<dpt>\S+)\n'+ASP+u'*(?P<cit>\*)?(?P<company>'+COMPANY+u')'+ASP+u'*'+BDURATION+'(?(cit)\*)?$', re.M)

# Avoid conflict in group names when combining *CO and *PO
AEMPLOYEES = EMPLOYEES.replace('employees', 'aemployees')
APERIOD = PERIOD.replace('from', 'afrom').replace('to', 'ato')
ABDURATION = BDURATION.replace('duration', 'aduration').replace('br', 'abr').replace('dit', 'adit')

AAEMPLOYEES = EMPLOYEES.replace('employees', 'aaemployees')

# TACO related grammar
TACOMODEL = u'(\\\\\*)*(?P<company>__COMPANY__)__SEP__'+ASP+u'*(__ITEM____SEP__'+ASP+u'*){0,2}(?P<position>'+POSITION+u'?)'
PATTERN = PREFIX+u'*'+CONTEXT+u'?'+ASP+u'*'+PERIOD+ur'[:：]?'+ASP+u'*'+TACOMODEL+ASP+u'*'+BDURATION+u'?(\n+(公司介绍：\n*.+?\n+)?所属行业：\n*(?P<business>\S+))?$'
TACO = re.compile(PATTERN.replace('__COMPANY__', u'('+COMPANY+u'\n)?'+COMPANY+u'?'+ASP+u'*').replace('__SEP__', '\|').replace('__ITEM__', u'[^\|（\(\[【]+('+COMPANYTAIL+u'[^\|（\(\[【]*)?'), re.DOTALL+re.M)
TACOMODELCOPY = TACOMODEL.replace('company', 'ccompany').replace('position', 'cposition')
# Add line begin for safer searching
PATTERN = u'^'+PREFIX+u'*'+CONTEXT+u'?'+ASP+u'*'+APERIOD+ur'[:：]?'+ASP+u'*'+TACOMODELCOPY+ASP+u'*'+ABDURATION+u'?(\n+(公司介绍：\n*.+?\n+)?所属行业：\n*(?P<cbusiness>\S+))?$'
# Duration required
DRPOSITION = POSITION+u'('+POSITION.replace('\\n', '').replace('\\*', '').replace('+', '*')+u')?'
DRTACOMODEL = u'(\\\\\*)*(?P<company>__COMPANY__)__SEP__'+ASP+u'*(__ITEM____SEP__'+ASP+u'*){0,2}(?P<position>'+DRPOSITION+u'?(（.*?） 兼'+ASP+u'*'+DRPOSITION+u'?)*)'
DRPATTERN = PREFIX+u'*'+CONTEXT+u'?'+ASP+u'*'+PERIOD+ur'[:：]?'+ASP+u'*'+DRTACOMODEL+ASP+u'*(\|'+ASP+u'*)?'+BDURATION+u'(\n+(公司介绍：\n*.+?\n+)?所属行业：\n*(?P<business>\S+))?$'
# Not use for searching but only for matching (see the code)
DRTACO = re.compile(DRPATTERN.replace('__COMPANY__', u'('+COMPANY+u'\n)?'+COMPANY+u'?'+ASP+u'*').replace('__SEP__', '\|').replace('__ITEM__', u'([^\|（\(\[【]+'+COMPANYTAIL+u')*([^\|（\(\[【]*)'), re.DOTALL+re.M)
NOPIPETACO = re.compile(PATTERN.replace('__COMPANY__', '\S+'+ASP+u'*').replace('__SEP__', ' ').replace('__ITEM__', '\S+'), re.M)
ALLTACO = re.compile(u'((?P<pip>'+TACO.pattern+u')|(?P<nop>'+NOPIPETACO.pattern+u'))', re.M)

# Combine presence of duration and bracket around period for safer searching
RCO = re.compile(u'^'+PREFIX+u'*■?'+CONTEXT+u'?'+ASP+u'*(?P<company>[^\n:：'+SP+u'\u2013\-]+)'+ASP+u'+((?P<position>[^\n:：'+SP+u'\u2013\-]+)'+ASP+u'+)?(('+UNIBRALEFT+u'?'+PERIOD+UNIBRARIGHT+u'?)|('+BDURATION+u'))', re.M)
HCO = re.compile(u'((((公司)|(企业))名称[:：]?'+ASP+u'*\*?(?P<company>'+COMPANY+u')\*?'+ASP+u'*(所在地区[:：]?'+ASP+u'*\S+'+ASP+u'*)?)|(((起止)|(任职))?时间[:：]?'+ASP+u'*\*?'+PERIOD+'\*?'+ASP+u'*)){2}$', re.M)

TABLECO = re.compile(u'^工作时间'+ASP+u'+岗位职能'+ASP+u'+公司名称'+ASP+u'*$', re.M)
TABLEPO = re.compile(u'^'+PERIOD+ASP+u'+(?P<position>'+POSITION+u'?)'+ASP+u'+(?P<company>'+COMPANY+u')'+ASP+u'*$', re.M)

SPO = re.compile(u'(项目)?职务[:：]'+ASP+u'*(?P<aposition>[^= \n:：\*]+)$', re.M)

POASP = ASP.replace('\s', ' ')
PODEPARTMENT = u'([^\n:：'+SP+u']|('+POASP+u'[^\n'+SP+u']))+'
POFIELD = u'(?(nl)(([^\n:：'+SP+u'](\n+/)?)+)|([^\n'+SP+u']|('+POASP+u'[^\n'+SP+u']))+)'
PO = re.compile(u'所属行业[:：]'+POASP+u'*?(?P<nl>\n+)?'+POASP+u'*(?P<field>'+POFIELD+u')'+POASP+u'*\n+(?:(?:'+ASP+u'*(?='+APERIOD+u')|(?:\-{3})|(?:下属人数)|(?:所在地区)|(?:汇报对象)|(?:所在部门))|(?:'+POASP+u'*((?P<dpt>'+PODEPARTMENT+u'(（离职原因：.*?）)?)(?(nl)()|(?:'+POASP+u'+)))?(?(nl)(?:'+POASP+u'*(\n+|('+POASP+u'+))))(主管：)?(?P<aposition>(?(dpt)(?:[^=\n:：]+)|(?:[^= \n:：]+)))(（汇报对象：.*?）)?$))', re.M)

IXPO = re.compile(u'所属行业[:：]'+ASP+u'*(?P<field>.+)\n+'+ASP+u'*(所属)?部'+ASP+u'*门[:：].*\n+'+ASP+u'*职'+ASP+u'*位[:：]'+ASP+u'*(?P<aposition>'+POSITION+u'?)'+ASP+u'*$', re.M)
APO = re.compile(u'^(其中)?'+APERIOD+ASP+u'*\*?(?P<aposition>'+POSITION+u'?)('+SALARY+u')?\*?$', re.M)
TPO = re.compile(u'^'+ASP+u'*(?P<aposition>'+POSITION+u'?)('+SALARY+u')?'+ASP+u'*'+APERIOD+''+ASP+u'*$', re.M)
TAPO = re.compile(u'^([所担]任)?职[位务](类别)?[:：]?'+ASP+u'*\*?(?P<aposition>'+POSITION+u'?)((('+SALARY+u')?\*?'+ASP+u'*)|(\uff1b.*))$', re.M)
BPO = re.compile(u'^(?P<aposition>(?!所属行业)'+POSITION+ASP+u'*)(\|'+ASP+u'*(?P<second>[^元/月'+SP+u']+)'+ASP+u'*)?($|(\|'+ASP+u'*('+SALARY+u')$))', re.M)
# Force use of ascii space to avoid matching new line and step over TCO in predator results
LIEPPO = re.compile(u'(?<!\\\\\n)^'+ASP+u'*'+APERIOD+ur' +(?P<aposition>'+POSITION+u'?)('+SALARY+u')?\n'+ASP+u'*((下属人数)|(所在地区)|(汇报对象)|(所在部门))：.*$', re.M)
RESPPO = re.compile(u'^职责：(?P<position>'+POSITION+u')\n(?P<field>\S+?)\| 企业性质：\S+?\| 规模：'+AEMPLOYEES+'$', re.M)

COMPANY_TYPE_KEYWORD = u'外商|企业|外企|合营|事业单位|上市|机关|合资|国企|民营|外资\(非欧美\)|代表处|股份制'
COMPANY_TYPE = u'(([^/\|\n\- ：]*?(('+COMPANY_TYPE_KEYWORD+u')[^\|\n\- ]*)+)|(其他))'
pos_company_business = lambda RE:RE.pattern+u'(\n'+ASP+u'*(?!所属行业：)'+POASP+u'*(((?P<title>企业性质：)?'+COMPANY_TYPE+u')|('+POASP+u'*\|'+POASP+u'*)|(?P<business>[^\|\n\-： ]+?)(?=[\|\n ])){1,3}(?(title)('+POASP+u'*\|'+POASP+u'*(规模：)?'+AEMPLOYEES+u')?|('+POASP+u'*\|'+POASP+u'*(规模：)?'+AAEMPLOYEES+u'))\n)?'

NOBRPOS = POSITION.replace(u'：', u'（）：'+ENDLINESEP)
YIPOSITION = NOBRPOS+u'(?P<lbr>[\(（])?(?(lbr)'+NOBRPOS+u'[\)）]('+NOBRPOS+u')?)'
YICO = re.compile(u'^((?P<position>'+YIPOSITION+u')'+ASP+u'+)?'+PERIOD+ASP+u'*?\n'+ASP+u'*(?P<company>'+COMPANY+u')((('+ASP+u'+'+COMPANY_TYPE+u')|('+ASP+u'+'+EMPLOYEES+u')|('+ASP+u'+所属行业[:：]'+POASP+u'*?(?P<nl>\n+)?'+POASP+u'*(?P<business>.+))){1,3}|(('+ASP+u'+(?P<dpt>'+PODEPARTMENT+u'))?('+ASP+u'+(?P<positiontype>'+POSITION+u'))?'+ASP+u'+(('+SALARY+u')|(职位[:：](?P<aposition>'+POSITION+u'))))){1,2}'+ASP+u'*$', re.M)

company_business = lambda RE:RE.pattern+u'(\n+'+ASP+u'*\-{3}\-*\n('+POASP+u'*'+COMPANY_TYPE+POASP+u'*\|)?'+POASP+u'*(?P<business>[^\|\n\-： ]+?)('+POASP+u'*\|'+POASP+u'*'+AEMPLOYEES+u')?\n)?'

company_business_noborder_strong = lambda RE:RE.pattern+u'\n+'+u'(?!所属行业：)'+POASP+u'*((((企业性质|公司性质)：)?'+COMPANY_TYPE+u')?('+POASP+u'*\|'+POASP+u'*)?((公司行业：)?(?P<business>(?=(?!'+AAEMPLOYEES+u'))[^\|\n\-：'+SP+u']+?(?!('+COMPANY_TYPE_KEYWORD+u')))(?=[\|\n'+SP+u']))('+POASP+u'*\|'+POASP+u'*)(((公司)?规模：)?'+AEMPLOYEES+u'))\n'

company_business_noborder = lambda RE:RE.pattern+u'\n+'+POASP+u'*((((企业性质|公司性质)：)?'+COMPANY_TYPE+u')|('+POASP+u'*\|'+POASP+u'*)|((公司行业：)?(?P<business>(?=(?!'+AAEMPLOYEES+u'))[^\|\n\-：'+SP+u']+?(?!('+COMPANY_TYPE_KEYWORD+u')))(?=[\|\n'+SP+u']))|(((公司)?规模：)?'+AEMPLOYEES+u')){1,5}\n'

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
        if 'employees' in groupdict and groupdict['employees']:
            result['total_employees'] = fix_employees(groupdict['employees'])
        elif 'aemployees' in groupdict and groupdict['aemployees']:
            result['total_employees'] = fix_employees(groupdict['aemployees'])
        elif 'aaemployees' in groupdict and groupdict['aaemployees']:
            result['total_employees'] = fix_employees(groupdict['aaemployees'])
        if 'cbusiness' in groupdict and groupdict['cbusiness']:
            result['name'] = fix_name(groupdict['cbusiness'])
        else:
            if 'business' in groupdict and groupdict['business']:
                result['business'] = fix_name(groupdict['business'])
        output['company'].append(result)

def format_salary(result, groupdict):
    if 'salary_months' in groupdict and groupdict['salary_months']:
        result['salary'] = fix_salary(groupdict['salary'])
        result['salary_months'] = groupdict['salary_months']
    elif 'salary' in groupdict and groupdict['salary']:
        result['salary'] = fix_salary(groupdict['salary'])
    elif 'yearly' in groupdict and groupdict['yearly']:
        result['yearly'] = fix_salary(groupdict['yearly']+u'/年')
    return result

def position_output(output, groupdict, begin='', end=''):
    if 'position' in groupdict or 'aposition' in groupdict:
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
            result['name'] = fix_name(groupdict['cposition'])
        else:
            if 'aposition' in groupdict and groupdict['aposition']:
                if 'second' in groupdict and groupdict['second']:
                    result['name'] = fix_name(groupdict['second'])
                else:
                    result['name'] = fix_name(groupdict['aposition'])
            else:
                result['name'] = fix_name(groupdict['position'])
        if 'aduration' in groupdict and groupdict['aduration']:
            result['duration'] = fix_duration(groupdict['aduration'])
        else:
            if 'duration' in groupdict and groupdict['duration']:
                result['duration'] = fix_duration(groupdict['duration'])
            else:
                result['duration'] = ''
        try:
            result['at_company'] = output['company'][-1]['id']
        except IndexError:
            result['at_company'] = 0
        if 'field' in groupdict and groupdict['field']:
            for c in output['company']:
                if c['id'] == result['at_company'] and 'business' not in c:
                    c['business'] = groupdict['field']

        format_salary(result, groupdict)
        output['position'].append(result)

name = lambda company: company['name']
duration = lambda company: company['duration']
business = lambda company: company['business']
companies = lambda output: output[1]['company']
positions = lambda output: output[1]['position']
company_1 = lambda x: companies(x)[0]
position_1 = lambda x: positions(x)[0]


def find_xp(RE, text):
    u"""
        >>> assert companies(find_xp(CO, u'2014 年 8 月 – 至今 company (1 年 6 个月)'))
        >>> assert companies(find_xp(CO, u'2010.03 - 至今*深圳市蓝韵实业有限公司* *(5年9个月)*'))
        >>> assert companies(find_xp(CO, u'2013-8 至 今  工作经历（IT服务行业）*---* 1年5个月'))
        >>> assert companies(find_xp(TCO, u'2013年04月——至今（含三个月实习期）   器械质量监督检验所（湛江检验室）'))
        >>> assert companies(find_xp(TCO, u'2011年7月—2014年5月 ：广州仁爱医院 [2年10月 ]'))
    """
    pos = 0
    if not pos:
        dto = ''
        dfrom = ''
        out = {'company': [], 'position': []}
        MA = re.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+IXPO.pattern+u'))', re.M)
        for r in MA.finditer(text):
            if r.group('co'):
                dfrom, dto = r.group('from'), r.group('to')
                company_output(out, r.groupdict())
            else:
                pos +=1
                position_output(out, r.groupdict(), begin=dfrom, end=dto)
    if not pos:
        out = {'company': [], 'position': []}
        MA = re.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+APO.pattern+u'))', re.M)
        for r in MA.finditer(text):
            if r.group('co'):
                company_output(out, r.groupdict())
            else:
                pos +=1
                position_output(out, r.groupdict())
    return pos, out


def work_xp_liepin(text):
    u"""
    Test for LIEPPO
        >>> assert position_1(work_xp_liepin(u'''2014.06 - 2015.01\\n上海分公司\\n(7个月)\\n  2014.06 - 2015.01 研发工程师\\n下属人数：'''))
        >>> assert company_1(work_xp_liepin(
        ...     u'2014 /4--至今：有限公司(5000-10000人) [ 2 年]\\n所属行业：计算机软件\\n开发部 软件工程师\\n下属人数：'))['total_employees']
        >>> assert u'江' in company_1(work_xp_liepin(
        ...     u'2013.09 - 至今\\n江苏\\*\\*医疗器械有限公司\\n(2年9个月)\\n2013.09 - 至今 质量负责人月\\n下属人数：'))['name']
        >>> assert positions(work_xp_liepin(u'''2006.07 - 至今\\n\*\*\*\\n(9年11个月)\\n2006.07 - 至今 质量管理\\n下属人数：'''))
        >>> assert positions(work_xp_liepin(u'2016.06 - 2016.06\\n系统有限公司\\n 2016.06 - 2016.06 应届生\\n下属人数：'))
        >>> assert positions(work_xp_liepin(u'''2016.06 - 至今\\n西门子中压开关技术(无锡)有限公司\\n2016.06 - 至今 项目经理\\n下属人数：'''))
    """
    pos = 0
    out = {'company': [], 'position': []}
    for RE in [CCO, CO, TCO]:
        if (RE == TCO or re.compile(BDURATION).search(text)) and RE.search(text):
            pattern = company_business(RE)
            MA = re.compile(u'((?P<po>'+LIEPPO.pattern+u')|(?P<co>'+pattern+u'))', re.M)
            for r in MA.finditer(text):
                if r.group('co'):
                    company_output(out, r.groupdict())
                else:
                    if not out['company']:
                        continue
                    pos +=1
                    position_output(out, r.groupdict())
        if pos:
            break
    return pos, out

def work_xp_yingcai(text):
    u"""
        >>> assert u'监' in name(position_1(work_xp_yingcai(u'IT项目总监\\n2015.11 - 至今\\n有限责任公司\\n所属行业：贸易\\n信息建设\\n月薪：保密')))
        >>> assert positions(work_xp_yingcai(u'电子工程师\\n2015.12 - 2016.01\\n有限公司 \\n月薪：2000以下'))
        >>> assert companies(work_xp_yingcai(u'2013.01 - 2014.03\\n技术有限公司\\n其他\\n月薪：保密'))
        >>> assert len(positions(work_xp_yingcai(u'客户需求。\\n2015.07 - 2015.09\\n长虹集团'))) == 0
        >>> assert u'设' in name(position_1(work_xp_yingcai(u'''用户界面（UI）设计\\n2014.03 - 2016.06\\n济南豪斯设计有限公司\\n月薪：保密''')))
        >>> assert len(companies(work_xp_yingcai(u'1） 2016年5月至今\\n公司首个MTK'))) == 0
        >>> assert u'主管' in name(position_1(work_xp_yingcai(u'项目主管\\n2007.11 - 2015.06\\n有限公司\\n国企\\n所属行业：机械/机电\\n')))
        >>> assert 1 == len(companies(work_xp_yingcai(u'项目主管\\n2007.11 - 2015.06\\n有限公司\\n国企\\n所属行业：机械/机电\\n月薪：6000到8000\\n'
        ...     u'2007.11 – 2015.06 有限公司\\n所属行业：机械/机电 公司性质：上市公司\\n')))
        >>> assert business(company_1(work_xp_yingcai(u'项目主管\\n2007.11 - 2015.06\\n有限公司\\n国企\\n所属行业：机械/机电\\n月薪：6000到8000\\n'
        ...     u'2007.11 – 2015.06 有限公司\\n所属行业：机械/机电 公司性质：上市公司\\n'))).endswith(u'机电')
        >>> assert 2 == len(companies(work_xp_yingcai(u'设备工程师\\n2010.10 - 2016.03 \\n东莞新科磁电厂\\n外商独资\\n500人以上 \\n'
        ...     u'所属行业：电子技术/半导体/集成电路 | 计算机硬件\\n电气工程师/技术员 \\n月薪：6000到8000\\n'
        ...     u'2007.05 - 2009.12 \\n上海润彤机电有限公司\\n民营/私企 \\n技术部')))
        >>> assert positions(work_xp_yingcai(u'项目主管\\n2014.11 - 2016.01\\n有限公司\\n所属行业：贸易/进出口\\n月薪：6000到8000\\n'
        ...     u'2014/11 - 2016/01\\n有限公司O,TCL等手机项目.\\n'
        ...     u'质量管理/测试工程师\\n2013.11 - 2014.10\\n金凯新瑞光电有限公司\\n所属行业：石油/化工/矿产/地质\\n月薪：4000到6000'))[1]['salary']
        >>> assert companies(work_xp_yingcai(u'WO 专家 \\n2015.07 - 至今\\n有限公司\\n月薪：保密'))
        >>> assert business(company_1(work_xp_yingcai(u'销售运营专员/销售数据分析\\n2006.05 - 2008.12\\n欧时电子元件（上海）有限公司\\n代表处\\n'
        ...     u'所属行业：电子技术/半导体/集成电路\\n月薪：3000到4000')))
        >>> assert business(company_1(work_xp_yingcai(u'质量检验员\\n2014.08 - 至今\\n有限公司\\n民营/私企\\n101－300人\\n'
        ...     u'所属行业：计算机软件\\n安全质量部')))
        >>> assert 'Ltd.' in name(company_1(work_xp_yingcai(u'IT项目总监\\n2012.11 - 2015.08\\neCargo enterprise Ltd.\\n'
        ...     u'所属行业：互联网/电子商务\\n月薪：20000到30000')))
        >>> assert companies(work_xp_yingcai(u'2005.09 - 2006.01 \\n江西麦克森国际服饰有限公司\\n全部\\n职位：秘书/行政/文员/助理'))
        >>> assert 0 == len(companies(work_xp_yingcai(u'2009年02月-2009年9月调入北京森华通达汽车销售服务有限公司\\n财务部\\n职位：会计')))
        >>> assert companies(work_xp_yingcai(u'1995.06 - 2001.04\\n四川南山机器厂\\n国企\\n500人以上 \\n工具处'))
        >>> assert u'其他' in business(company_1(work_xp_yingcai(u'人事行政经理\\n2002.11 - 2007.02\\n创维电子有限公司\\n民营/私企\\n'
        ...     u'所属行业：其他行业\\n月薪：保密\\n所属行业：制造业（彩电、VCD、DVD，家庭影院和卫星接收机）')))
        >>> assert not companies(work_xp_yingcai(u'Senior Manager\\n2014.03 - 至今\\nUTC Building and Industrial Syste Asia\\n'
        ...     u'Headquarter美国联合技术公司建筑与工业系统亚洲总部,\\n外商独资\\n所属行业：其他行业\\n月薪：保密\\n')) #FIXME
        >>> assert not companies(work_xp_yingcai(u'财务负责人\\n2014.07 - 至今\\nGT Sapphire technology CO., LTD\\n'
        ...     u'极特蓝宝石科技（贵阳）有限公司\\n外商独资\\n所属行业：电子技术/半导体/集成电路\\n月薪：20000到30000')) #FIXME
    """
    pos = 0
    out = {'company': [], 'position': []}
    for r in YICO.finditer(text):
        company_output(out, r.groupdict())
        if r.group('position') or r.group('aposition'):
            pos +=1
            position_output(out, r.groupdict())
        elif len(out['company']) > 1:
            if company_summary(out['company'][-1]) == company_summary(out['company'][-2]):
                out['company'].pop()
    return pos, out

def work_xp_zhilian(text):
    u"""
        >>> assert companies(work_xp_zhilian(u'2010年6月  --  2013年11月\\n\*\*电子材料有限公司\\n|  IT工程师\\n（3年5个月）\\n'
        ...     u'所属行业：\\n加工制造\\n公司性质：\\n合资\\n公司规模：\\n100-499人\\n职位类别：\\n计算机/网络技术-网络工程师'))
        >>> assert ' ' in name(company_1(work_xp_zhilian(u'2011年3月  --  2014年10月 中兴通讯\\n有限公司  |  客户服务  | 工程师 （3年7个月）')))
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

    """
    pos = 0
    out = {'company': [], 'position': []}
    if DRTACO.search(text):
        for r in DRTACO.finditer(text):
            pos += 1
            company_output(out, r.groupdict())
            d = r.groupdict()
            d['position'] = re.compile(u'（.*?） 兼'+ASP+u'*').sub('/', d['position'])
            position_output(out, d)
    elif TACO.search(text):
        if not pos:
            # Support missing pipe in company definition by using NOPIPETACO
            for r in ALLTACO.finditer(text):
                pos += 1
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
    return pos, out

def work_xp_jingying(text):
    u"""
        >>> assert u'鸡' in name(company_1(work_xp_jingying(u'2016/6 -- 至今： 随鸡 [一个月内]\\n 所属行业：计算机服务\\n 傻子 销售经理')))
        >>> assert companies(work_xp_jingying(u'2016/7 -- 至今： 信息产品集团 [ -1年11个月 ]\\n所属行业：计算机硬件\\n销售  区域销售经理'))
        >>> assert len(companies(work_xp_jingying(u'2013/3 -- 2015/7： 江苏有限公司\\n所属行业：交通/运输/物流\\n'
        ...     u'2005/5 -- 2011/6： 南京分公司\\n所属行业：交通/运输/物流\\n市场部 市场'))) == 2
        >>> assert len(positions(work_xp_jingying(u'2003/1 -- 2005/5： （ 50-150人） [ 2年4个月 ]\\n所属行业：餐饮业\\n-----'))) == 0
        >>> assert positions(work_xp_jingying(u'2006/9 -- 2009/12： 开发公司 [3年3个月]\\n所属行业：电气\\n财务部（离职原因：调动） 会计'))
        >>> assert positions(work_xp_jingying(u'2001/1 -- 2004/3： 有限公司\\n所属行业：电子技术\\n生产部|工程部  组长|工程师'))
        >>> assert u'主' not in name(position_1(work_xp_jingying(u'2008/3 -- 2013/12： 上海分公司\\n所属行业：保险\\n收展一部  主管：人事，招聘')))
        >>> assert len(positions(work_xp_jingying(u'2012年12月—至今：有限公司\\n所属行业： 医疗电子\\n职责:\\n编写程序功能块实现方案'))) == 0
        >>> assert u'：' not in name(position_1(work_xp_jingying(u'2010 /4—2014/4：有限公司（300-500人） [ 3年]\\n所属行业：石油/化工/能源\\n'
        ...         u'人力资源部   人事经理  （汇报对象：公司总经理）')))
        >>> assert 1 == len(positions(work_xp_jingying(u'2007/7 -- 至今： 科技有限公司（ 500-1000人） [ 9年1个月 ]\\n'
        ...         u'所属行业：  医疗设备/器械\\n车间\\*采购部\\*品质部    操作工\\*库房管理员\\*检验员\\*包装员')))
        >>> assert u'****' in name(company_1(work_xp_jingying(u'    2013/3 -- 2016/8： \*\*\*\*集团公司（ 1000-5000人） [ 3年5个月 ]\\n'
        ...         u'所属行业：   法律\\n          法务   法务部诉讼经理\\n    主要负责集团诉讼')))
        >>> assert 5 == len(business(company_1(work_xp_jingying(u'2005/7 -- 2008/6： 研究所（ 50-150人） [ 2年11个月 ]\\n\\n'
        ...         u'  所属行业：  学术/科研\\n\\n  综合部   出纳员\\n\\n2005/07--2008年6月：研究所\\\\\\n所属行业：学术/科研\\\\\\n部出纳员\\\\\\n '))))

    WYJCO related tests:
        >>> business = lambda x: x['business']
        >>> assert u'台湾' in name(company_1(work_xp_jingying(u'2008/3-2010/11         业务推广 | 光电事业处\\n\\n'
        ...         u'台湾汉唐集成股份有限公司 [2年 8个月 ]\\n\\n多元化业务集团公司|150-500人|外资(非欧美)\\n')))
        >>> assert u'医疗' in business(company_1(work_xp_jingying(u'2011/6-2015/6          项目经理|投资部\\n\\n'
        ...         u'有限公司 [4年 ]\\n\\n医疗/护理/卫生|150-500人|民营公司\\n')))

    """
    pos = 0
    out = {'company': [], 'position': []}
    res = WYJCO.search(text)
    if res:
        RE = re.compile(company_business_noborder(WYJCO), re.M)
        for r in RE.finditer(text):
            pos +=1
            company_output(out, r.groupdict())
            position_output(out, r.groupdict())
        if pos:
            return pos, out
    for RE in [CCO, CO, TCO]:
        if (RE == TCO or re.compile(BDURATION).search(text)) and RE.search(text):
            dto = ''
            dfrom = ''
            out = {'company': [], 'position': []}
            MA = re.compile(u'((?P<co>'+RE.pattern+ASP+u'*(?(duration)()|(?=所属行业：)))|(?P<po>'+PO.pattern+u'))', re.M)
            for r in MA.finditer(text):
                if r.group('co'):
                    dfrom, dto = r.group('from'), r.group('to')
                    company_output(out, r.groupdict())
                else:
                    if r.group('aposition'):
                        pos +=1
                        position_output(out, r.groupdict(), begin=dfrom, end=dto)
        if pos:
            break
    return pos, out

def work_xp(text):
    u"""
        >>> assert work_xp(u'2014年4月 -- 至今 公司 | 客户服务经理、CT临床支持经理 （2年1个月）')[0]
        >>> assert not u'年' in name(company_1(work_xp(u'2011.01-至今 集团 （4年）\\n2009.04-2011.01 集团 （1年9个月）')))
        >>> assert not work_xp(u'\\n03/2013 – 现在 Consulting\\n\\n高级咨询师')[0] #FIXME
        >>> assert positions(work_xp(u'有限公司 招聘主管 2009/03 至 2013/03 （ 4\\n年） 保密'))
        >>> assert work_xp(u'有限公司  加速器工程师  2013/07\~2014/08  广州\\n\\n公司  技术研发工程师  2014/08至今  上海')[0] == 2
        >>> assert work_xp(u'有限公司 招聘主管 2015/03 至今（ 1 年 1 个月） 保密')[0] == 1
        >>> assert not work_xp(u'2015年5月～至今  有限公司\\n  人力资源总监')[0] == 1  #FIXME
        >>> assert work_xp(u'2014年2月 -- 至今 管理（中国）有限公司\\n | 人力资源总监 （2年3个月）')[0]
        >>> assert companies(work_xp(u'（海外）2011/3 -\\n2014/7：有限公司（5000-10000人）'))
        >>> assert companies(work_xp(u'1.  2013.8——至今 有限公司'))
        >>> assert work_xp(u'\\n    2014/02-2015/05 有限公司')
        >>> assert positions(work_xp(u'\\n2007年3月～2009年2月  有限公司\\n\\n其中2009/3—2010/9培训主管'))
        >>> assert positions(work_xp(u'2001年6月 -- 至今 第一附属医院 | 影像中心 |\\n放射科医师  （14年11个月）'))
        >>> assert duration(company_1(work_xp(u'2001年6月 -- 至今 第一附属医院 | 影像中心 |\\n放射科医师  （14年11个月）')))
        >>> assert duration(company_1(work_xp(u'2014年4月 -- 至今 公司 | 客户服务经理、CT临床支持经理\\n （2年1个月）')))
        >>> assert duration(company_1(work_xp(u'2012年1月 -- 2012年10月 有限公司 | 支持部\\n | 部经理 （9个月）')))
        >>> assert len(positions(work_xp(u'2008年3月-2011年5月 Care Ltd. | 工程师\\n2011年5月-2013年6月 医疗  工程师'))) == 2
        >>> assert len(companies(work_xp(u'2000年6月-2007年6月 公司 | 管理部\\n | 副课长\\n(一) 2000.06-2004.06：管理 人事副课长'))) == 1
        >>> assert positions(work_xp(u'2008.12-2010.05 公司 （1年5个月）\\n开发部 | 工程师 | 6000元/月'))
        >>> assert not not positions(work_xp(u'2001.01-2004.12 家具公司 （3年11个月）\\n4001-6000元/月'))   #FIXME
        >>> assert positions(work_xp(u'2012.09-至今 有限公司 （3年6个月）\\n\\n研发部主管\\n\\n医疗设备\\n\\n工作描述：'))
        >>> assert positions(work_xp(u'。2010/07 -- 2012/06\\n\\n政邦律师事务所 | | 律师助理'))
        >>> assert positions(work_xp(u'2014/01 - 2015/04 有限公司（1年3个月）\\nWEB、IOS开发工程师|1000元/月以下'))
        >>> assert work_xp(u'2005 /1--2009 /11： 有限公司 （500-1000人）\\n\\n所属行业： 医疗\\n\\n部 门：系统部\\n\\n职位：工程师')[0]
        >>> assert u'发' in name(position_1(work_xp(u'2005/07—2007/05：科技集团\\n\\n所属行业:计算机软件 \\n\\n所属部门: 事业群 \\n\\n职位: 开发')))
        >>>     # Different combinations of spaces and unicode spaces
        >>> assert work_xp(u'2010/7--2014/5：有限公司（150-500人）\\n所属行业： 计算机软件\\n研发中心    软件工程师')[0]
        >>> assert work_xp(u'2014 /10--至今： 有限公司\\n所属行业：\\n 互联网/电子商务\\n\\n管理顾问      高级咨询顾问')[0]
        >>> assert work_xp(u'2010 /3--至今：医疗设备(150-500人) [ 5 年9个月]\\n所属行业：  器械\\nX射线产品事业部   医疗器械研发')[0]
        >>> assert work_xp(u'2008/3 -- 2014/10： 有限公司（ 1000-5000人） [ 6年7个月 ]\\n所属行业： 仪器仪表\\n电能表事业部  项目经理')[0]
        >>> assert work_xp(u'2007 /3--2010 /12：有限公司 [ 3 年9个月]\\n所属行业： 服务(咨询、财会) 越秀集， 5:5 股份。\\n人事部    书/翻译')[0]
        >>> assert u'部' not in name(position_1(work_xp(u'''2014/5-至今： 科技集团 [ 2年1个月 ]\\n所属行业： 机械/设备\\n  生产部  生产领班/组长''')))
        >>> assert 'w' not in name(position_1(work_xp(u'2007 /9--2009 /8：INC PROJECT [11个月]\\n 所属行业：   其他\\npro worker  志愿者')))
        >>> assert work_xp(u'2014 /4--至今：有限公司(150-500人) [ 1 年8个月]\\n所属行业：\\n医疗设备/器械\\nR&D\\n医疗器械研发')[0]
        >>> assert u'发' in name(position_1(work_xp(u'2014 /4--至今：有限公司[1年8个月]\\n\\n所属行业：\\n\\n医疗设备\\n\\nR&D\\n\\n器械研发')))
        >>> assert u'师' in name(position_1(work_xp(u'2011 /7--至今：有限公司 [ 4 年5个月]\\n\\n所属行业：\\n医疗设\\n\\n/器械\\n技术部\\n工程师')))
        >>> assert u'为' not in name(position_1(work_xp(u'2014/10-至今：有限公司\\n所属行业： 互联网\\n管理顾问      高级咨询顾问\\n为CEO')))
        >>> assert u'户' not in name(position_1(work_xp(u'2010 /3--至今：医疗设备 [5 年]\\n所属行业： 医疗设备/器械\\nX射线产品  器械研发\\n客户')))
        >>> assert u'要' not in name(position_1(work_xp(u'2012 /3--至今：服务中心(150-500人) [ 3 年9个月]\\n所属行业： 非盈利机构\\n督导助理\\n主要')))
        >>> assert not u'高' in name(position_1(work_xp(u'''2012/4-至今：集团\\n所属行业： 办公用品\\n人力资源 高级经理（ COE ）'''))) #FIXME
        >>> assert not work_xp(u'2015/04-至今 Limi（8个月）\\n 开发|60元/月\\n2015/06-至今 有限公司 | php（3个月）\\n工程师|60元/月')[0] == 2 #FIXME
        >>> assert not work_xp(u'''2014/4-至今：有限公司  产品研发部：工程师''')[0] #FIXME
        >>> assert companies(work_xp(u'??2015.10– 2016.01 赛诺微医疗科技（北京）有限公司'))
        >>> assert positions(work_xp(u'Designer\\n\\nHealthcare\\n\\n2011 年 10 月 – 至今 (4 年 4 个月)Wuxi'))
        >>> assert work_xp(u'''CT Engineer\\n\\nHealthcare\\n\\n2013年7月 – 至今 (2年7个月)''')
        >>> assert u'工' in name(position_1(work_xp(u'[助理 / \\n工程师](http://www.)\\n\\n[Care]\\n(http://www.)\\n\\n2014年12月–至今(1 年2个月)')))
        >>> assert positions(work_xp(u'项目\\n\\n课程\\n\\nIntern\\n\\nCorporation\\n\\n2011年9月–2013年2月(1年6个月)'))
        >>> assert u'Head' in name(position_1(work_xp(u'Head (FGs\\nmanufacturer)\\n\\nLimited Group\\n\\n2012年6月–至今(2年9个月)')))
        >>> assert u'3G' not in name(position_1(work_xp(u'3G\\n\\nEngineer\\n\\nTelecom\\n\\n2012年4月–至今 (9 个月)中国')))
        >>>     # TODO re.compile(u'^(?P<company>\S+)'+ASP+u'+(?P<position>\S+)'+ASP+u'*'+PERIOD+ASP+u'+(\S*)?$', re.M)
        >>> assert work_xp(u'有限公司 工程师 2013/07\~2014/08  广州')[0]
        >>> assert companies(work_xp(u'2011年8月—2014年12月 中国海运集团\\n职位：航运部  轮机工程师'))
        >>> assert not companies(work_xp(u'2014年10月——2014年11月   技工学校    实习班主任、老师'))  #FIXME
        >>>     #TODO use NOPIPETACO
        >>> assert work_xp(u'2009/09 -- 2010/09\\n\\nAlcatel | CIO | Engineer')[0]
        >>>     # TODO empty middle field between pipes
        >>> assert not u'Leader' in name(position_1(work_xp(u'2010/10 -- Now\\n\\nHealthcare | CT | R&D | Engineer / Project\\nLeader')))  #FIXME
        >>>     # TODO modified TACO for the trailing line
        >>> assert not work_xp(u'2012-07 至 今\\n\\n有限公司 |\\n职  位： 软件开发(Linux/单片机/DLC/DSP…)')[0] # FIXME
        >>> assert not work_xp(u'Jun 2012-至今 有限公司---质量经理（管理者代表）')[0]   #FIXME
        >>> assert not work_xp(u'2013.9- 至今 苏州微清医疗器械有限公司，高级算法工程师。')[0]   #FIXME
        >>> assert not work_xp(u'2014.4--复旦肿瘤医 （Shanghai \\n Center）     医学物理师')[0]  #FIXME
        >>> assert not work_xp(u'财务总监，连锁集团 （2014年11月2015年5月）')[0]  #FIXME
        >>> assert not work_xp(u'高级销售经理\\n\\n飞利浦医疗\\n\\n 2014 – 至今 (2 年)福建')[0] #FIXME
        >>>     #TODO use ECO with AXP
        >>> assert work_xp(u'2014/06 -- 2014/12\\n\\n有限公司 | 项目经理')[0]
        >>> assert not work_xp(u'21/07/2012 — 27/07/2014       项目经理\\n有限公司     四川，中国')[0]   #FIXME
        >>>     # Detailed date inside full markdown table
        >>> assert not work_xp(u'1.  2001.9 – 2004.07  营管理学院   辅导员   工程系')[0]   #FIXME
        >>>     #TODO use NOPIPETACO
        >>> assert not work_xp(u'就职时间 : 2012-06 ～至今\\n\\n受聘公司 : 有限公司\\n\\n职位名称 : 质量工程师')[0]   #FIXME
        >>> assert work_xp(u'2014.02 - 至今 有限公司\\n\\n职位： 电气工程师  ')[0]
        >>> assert not work_xp(u'2015/03\\~\\n\\n有限公司\\n\\n职位：质量经理')[0]    #FIXME
        >>> assert position_1(work_xp(u'2011.05 - 至今 GE医疗 (4年8个月\\n2011.05 - 至今研发主管、电气工程师15000元/月'))['salary']
        >>> assert len(companies(work_xp(u'2012.02-2012.07 *研究院 (5个月)*\\n2012.02 - 2012.07助理工程师（医疗电子/算法）\\n'
        ...     u'2011.09-2011.12 *University\\nof dundee,UK (3个月)*'))) == 2
        >>> assert company_1(work_xp(u'2013.01 -\\n2016.04深圳山龙科技 (3年3个月)\\n'
        ...     u'2013.01 - 2016.04软件工程师'))['duration']
        >>> assert u'股' in name(company_1(work_xp(u'2014/01 – 2014/11\\n\\n股有限公司 | | 法务主管  ')))

    SPO related tests:
        >>> assert companies(work_xp(u'2015.07-至今  设备有限公司\\n项目职务： 技术主管\\n所在部门： 研究院'))
        >>> assert positions(work_xp(u'2015.07-至今  设备有限公司\\n项目职务： 技术主管\\n所在部门： 研究院'))
        >>> assert positions(work_xp(u'2008.07-2011.03 电力有限公司   职务：工艺技术员/工艺倒班主管\\n工作职责：\\n技术员'))
        >>> assert u'机械' in business(company_1(work_xp(u'2010.08 - 至今有限公司 (5年10个月)\\n----\\n中外合营 | 机械制造/机电/重工 | 500-999人\\n'
        ...     u'2010.08 - 至今财务负责人\\n汇报对象：总经理 | 下属人数：10 | 所在地区：长沙 | 所在部门：财务部''')))
        >>> assert u'政府' in business(company_1(work_xp(u'2012.04 - 至今\\n\\n环保部核安全中心 (4年4个月)\\n\\n'
        ...     u'事业单位  |  政府/公共事业  |  500-999人\\n\\n环保部唯一核与辐射技术支持单位\\n\\n2012.04 - 至今高工')))
        >>> assert u'政府' in business(company_1(work_xp(u'2014年7月  --  至今 研究院珠海检测院  |\\n 公务员/事业单位人员  （1年11个月）\\n\\n'
        ...     u'所属行业：\\n\\n政府/公共事业/非盈利机构')))
        >>> assert u'器械' in business(company_1(work_xp(u'2014年4月  --  至今 深圳公司  |  客户服务经理\\n      （2年1个月）\\n\\n'
        ...     u'所属行业：医疗设备/器械')))
        >>> assert u'器械' in business(company_1(work_xp(u'2006年1月  --  2011年6月 有限公司 | 售后服务部 | 现场服务工程师  （6年5个月）\\n\\n'
        ...     u'公司介绍：加速器医疗设备\\n\\n所属行业：医疗设备/器械')))
        >>> assert u'重工业' in business(company_1(work_xp(u'2013.08 - 2016.06 有限公司  （2年10个月）\\n 工程师 | 10001-15000元/月\\n\\n'
        ...     u'大型设备/机电设备/重工业 | 企业性质：外商独资 | 规模：20-99人\\n\\n')))
        >>> assert u'互联网' in business(company_1(work_xp(u'2012.03 - 至今 有限公司 （1年1个月）\\n软件工程师\\n互联网 | 企业性质：民营\\n')))
        >>> assert u'自动化' in business(company_1(work_xp(u'搜索同事2015.01 - 至今有限公司(SFAE) (1年7个月)\\n\\n'
        ...     u'外商独资·外企办事处  |  仪器/仪表/工业自动化/电气  |  10000人以上\\n\\n2015.01 - 至今IPM Project Manager & BD22000元/月')))

    RESPPO related
        >>> assert u'建筑' in business(company_1(work_xp(u'2015/08 - 2016/03   有限公司\\n职责：工程管理\\n'
        ...     u'房地产/建筑/建材/工程| 企业性质：民营| 规模：1000-9999人')))

    RCO related
        >>> assert companies(work_xp(u'■医院 （2012-04 \~ 至今）\\n公司性质：\\n担任职位：英语翻译'))
        >>> assert u'研发项目经理' == name(position_1(work_xp(u'▌2000-11 ～ 2010-04  有限公司\\n\\n担任职位：\\n研发项目经理；从事大')))
    """
    RE = None
    pos = 0
    out = {'company': [], 'position': []}
    if ECO.search(text):
        out = {'company': [], 'position': []}
        for r in ECO.finditer(text):
            pos +=1
            company_output(out, r.groupdict())
            position_output(out, r.groupdict())
    if not pos:
        out = {'company': [], 'position': []}
        RE = re.compile(company_business_noborder(re.compile(BDURATION, re.M)), re.M)
        res = RE.search(text)
        # Only run SPO if WYJCO does not match (for speed up)
        if not res:
            # Can't use CO/TCO as they expect EOL
            MA = re.compile(u'^'+ASP+u'*'+PERIOD+ASP+u'*(?P<company>[^' + SENTENCESEP + '=\n\*]+?)'+ASP+u'*'+SPO.pattern, re.M)
            for r in MA.finditer(text):
                company_output(out, r.groupdict())
                pos +=1
                position_output(out, r.groupdict())
    if not pos:
        if not pos:
            pos, out = work_xp_jingying(text)
            if pos:
                return pos, out
            for RE in [CCO, CO, TCO]:
                if (RE == TCO or re.compile(BDURATION).search(text)) and RE.search(text):
                    MA = re.compile(company_business_noborder_strong(RE), re.M)
                    if MA.search(text):
                        MA = re.compile(company_business_noborder(RE), re.M)
                    else:
                        # company_business always matches what RE matches
                        MA = re.compile(company_business(RE))
                    pos, out = find_xp(MA, text)
                    if pos:
                        return pos, out
                    else:
                        out = {'company': [], 'position': []}
                        MA = re.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+RESPPO.pattern+u'))', re.M)
                        for r in MA.finditer(text):
                            if r.group('co'):
                                dfrom, dto = r.group('from'), r.group('to')
                                company_output(out, r.groupdict())
                            else:
                                pos +=1
                                position_output(out, r.groupdict(), begin=dfrom, end=dto)
                        if pos:
                            return pos, out
                    break
            if not pos:
                pos, out = work_xp_liepin(text)
                if pos:
                    return pos, out
        if re.compile(BDURATION).search(text) and CO.search(text):
            # Can try more things with CO as both PERIOD and DURATION safeguards
            if not pos:
                out = {'company': [], 'position': []}
                MA = re.compile(u'((?P<co>'+CO.pattern+u')'+ASP+u'*(?P<po>'+pos_company_business(BPO)+u'))', re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
                    pos +=1
                    position_output(out, r.groupdict())
            if not pos:
                out = {'company': [], 'position': []}
                MA = re.compile(u'(?P<co>'+CO.pattern+u')(\n+(?P<position>'+POSITION+u')\n+.*?\n+工作描述：)?', re.M)
                for r in MA.finditer(text):
                    company_output(out, r.groupdict())
                    if r.group('position'):
                        pos +=1
                        position_output(out, r.groupdict())
        elif DRTACO.search(text) or TACO.search(text):
            pos, out = work_xp_zhilian(text)
        elif PCO.search(text):
            out = {'company': [], 'position': []}
            for r in PCO.finditer(text):
                pos +=1
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        elif TCO.search(text):
            if not pos:
                out = {'company': [], 'position': []}
                MA = re.compile(u'((?P<co>'+TCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
                for r in MA.finditer(text):
                    if r.group('co'):
                        dfrom, dto = r.group('from'), r.group('to')
                        company_output(out, r.groupdict())
                    else:
                        # We need this if broken period '2015/03\~\n' leads to missing company
                        if not out['company']:
                            break
                        pos +=1
                        position_output(out, r.groupdict(), begin=dfrom, end=dto)
        elif RCO.search(text):
            out = {'company': [], 'position': []}
            MA = re.compile(u'((?P<co>'+RCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
            for r in MA.finditer(text):
                if r.group('co'):
                    dfrom, dto = r.group('from'), r.group('to')
                    company_output(out, r.groupdict())
                    if r.group('position'):
                        pos +=1
                        position_output(out, r.groupdict(), begin=dfrom, end=dto)
                else:
                    pos +=1
                    position_output(out, r.groupdict(), begin=dfrom, end=dto)
    return pos, out

def table_based_xp(text):
    u"""
        >>> assert table_based_xp(u'''\\n公司名称 有限公司\\n时间  2013.06 ——2014.04\\n\\n职务 助理硬件工程师''')[0]
        >>> assert table_based_xp(u'''\\n任职时间 2013 年9月至2014年9月\\n企业名称 投资有限公司\\n职位  财务总监''')[0]
    """
    pos = 0
    out = {'company': [], 'position': []}
    if HCO.search(text):
        dto = ''
        dfrom = ''
        MA = re.compile(u'((?P<co>'+HCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
        for r in MA.finditer(text):
            if r.group('co'):
                dfrom, dto = r.group('from'), r.group('to')
                company_output(out, r.groupdict())
            else:
                pos +=1
                position_output(out, r.groupdict(), begin=dfrom, end=dto)
    return pos, out


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


def fix_output(processed):
    result = {}
    for company in processed['company']:
        positions = [p for p in processed['position'] if p['at_company'] == company['id']]
        if len(positions) <= 1:
            if not company['duration']:
                company['duration'] = compute_duration(company['date_from'], company['date_to'])
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

def fix_liepin(d):
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
            pos = 0
            out = {'company': [], 'position': []}
            res = PXP.search(d)
            if PJCO.search(res.group('expe')):
                for r in PJCO.finditer(res.group('expe')):
                    company_output(out, r.groupdict())
                    if r.group('position'):
                        pos +=1
                        position_output(out, r.groupdict())
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
    return fix_output(processed)

def fix_yingcai(d):
    u"""
        >>> assert u'4年' in fix_yingcai(u'工作经历\\n2010.04 - 2014.11\\n商业银行\\n所属行业：计算机硬件\\n月薪：保密\\n'
        ...     u'销售部内勤')['experience']['company'][0]['duration']
    """
    pos = 0
    processed = {'company': [], 'position': []}
    res = XP.search(d)
    for RE in [XP, AXP]:
        res = RE.search(d)
        if res:
            pos, out = work_xp_yingcai(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed)

def fix_zhilian(d):
    u"""
    """
    pos = 0
    processed = {'company': [], 'position': []}
    res = XP.search(d)
    for RE in [XP, AXP]:
        res = RE.search(d)
        if res:
            pos, out = work_xp_zhilian(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed)

def fix_jingying(d):
    u"""
    """
    pos = 0
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
    return fix_output(processed)
    
    
def fix(d, as_dict=False):
    u"""
        >>> assert not fix("2014年7月\~  苹果采购运营管理（上海）有限公司")[0][0] #FIXME
        >>> assert fix(u'工作经历：\\n\\n 教育背景：\\n\\n 2009年')[1] == 1
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
        >>> assert not u'基础' in fix(u'简历ID：RCC0012345678\\n\\n姓名：\\n工作经验\\n\\n2007年6月 -- 2014年2月 基础医疗  |  人力资源经理\\n'
        ...     u'   （6年8个月）\\n\\n1.结合公司战略和业务需要\\n\\n2.修订执行人力', True)['experience']['company'][0]['name'] #FIXME

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
    def fix_output_legacy(processed, reject):
        if as_dict:
            return fix_output(processed)
        else:
            for company in processed['company']:
                company['at_company'] = -1
            tuple_format = lambda x: tuple([x[k] for k in ['date_from', 'date_to', 'name', 'duration', 'at_company']])
            return ([tuple_format(p) for p in processed['company']], [tuple_format(p) for p in processed['position']]), reject

    if as_dict:
        if is_jycv(d):
            return fix_jingying(d)
        elif is_lpcv(d):
            return fix_liepin(d)
        elif is_zlcv(d):
            return fix_zhilian(d)
        elif is_yccv(d):
            return fix_yingcai(d)

    reject = 0
    processed = {'company': [], 'position': []}
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
            pos = 0
            if TABLECO.search(res.group('expe')):
                out = {'company': [], 'position': []}
                for r in TABLEPO.finditer(res.group('expe')):
                    company_output(out, r.groupdict())
                    pos +=1
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
        elif TXP.search(d):
            pos = 0
            out = {'company': [], 'position': []}
            res = TXP.search(d)
            if TCO.search(res.group('expe')):
                complement = u'\n*'+ASP+u'*公司性质：\S+ \| 公司规模： '+EMPLOYEES+u' \| 公司行业：(?P<business>\S+)$'
                MA = re.compile(u'((?P<co>'+TCO.pattern+u'('+complement+u')?)|(?P<po>'+TPO.pattern+u'))', re.M)
                for r in MA.finditer(res.group('expe')):
                    if r.group('co'):
                        company_output(out, r.groupdict())
                    else:
                        pos +=1
                        position_output(out, r.groupdict())
                if not pos:
                    out = {'company': [], 'position': []}
                    dto = ''
                    dfrom = ''
                    MA = re.compile(u'((?P<co>'+TCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
                    for r in MA.finditer(res.group('expe')):
                        if r.group('co'):
                            dfrom, dto = r.group('from'), r.group('to')
                            company_output(out, r.groupdict())
                        else:
                            pos +=1
                            position_output(out, r.groupdict(), begin=dfrom, end=dto)
            if not pos and len(out['company']) == 0:
                reject = 2
            else:
                processed = out
        else:
            reject = 4
    return fix_output_legacy(processed, reject)
