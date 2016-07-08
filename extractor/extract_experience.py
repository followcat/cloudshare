# -*- coding: utf-8 -*-
import re

from extractor.utils_parsing import *


XP = re.compile(ur'^'+ASP+u'*'+ UNIBRALEFT +u'?((((工'+ASP+u'?作'+ASP+u'?)|(实习)|(工作(与)?实践))经'+ASP+u'?[历验])|(实习与实践))'+ UNIBRARIGHT +u'?(?P<expe>.*?)^'+ASP+u'*(?='+ UNIBRALEFT +u'?(((项'+ASP+u'?目)|(教'+ASP+u'?育))'+ASP+u'?((经'+ASP+u'?[历验])|(背景)|(培训)))'+ UNIBRARIGHT +u'?)', re.DOTALL+re.M)
AXP = re.compile(ur'^'+ASP+u'*'+ UNIBRALEFT +u'?((((工'+ASP+u'?作'+ASP+u'?)|(实习)|(工作(与)?实践))经'+ASP+u'?[历验])|(实习与实践))'+ UNIBRARIGHT +u'?[:：]?'+ASP+u'*'+DURATION+'?'+ASP+u'*?\n(?P<expe>.*)', re.DOTALL+re.M)
TXP = re.compile(ur'-{9}[\-'+SP+u']*(?P<expe>'+PERIOD+ur'.*?)(?=-{9}[\-'+SP+u']*)', re.DOTALL)


# Allow multiline once in company name when duration is present
# As company has at least one char, need to handle break just as company tail
# Catching all employees is too expensive on parenthesis repetition, some will be post processed
ECO = re.compile(u'^(?P<position>(\S[\S ]+\n)*)\n+(?P<company>(\S[\S ]+\n)*)\n+' + PERIOD +ASP+u'*' + BDURATION, re.M+re.DOTALL)
CO = re.compile(PERIOD+ur'[:：]?'+ASP+u'*(?P<cit>\*)?(?P<company>'+COMPANY+u'(\n(('+COMPANY+u')|('+COMPANYTAIL+u')))?)'+BEMPLOYEES+'?(?(cit)\*)?'+ASP+u'*'+BDURATION+'(?(cit)\*)?'+ASP+u'*$', re.DOTALL+re.M)
PCO = re.compile(PERIOD+ur'[:：]?'+ASP+u'*(?P<cit>\*)?(?P<company>'+COMPANY+u'(\n(('+COMPANY+u')|('+COMPANYTAIL+u')))?)(?(cit)\*)'+ASP+u'*\|'+ASP+u'*(?P<position>'+POSITION+u'?)'+ASP+u'*'+BDURATION+'$', re.DOTALL+re.M)
TCO = re.compile(u'^'+PREFIX+u'?'+CONTEXT+u'?'+ASP+u'*'+PERIOD+ur'[:：]?'+ASP+u'*(?P<cit>\*)?(?P<company>'+COMPANY+u')(?(cit)\*)?'+ASP+u'*'+BDURATION+'?(?(cit)\*)?$', re.DOTALL+re.M)

# Avoid conflict in group names when combining *CO and *PO
APERIOD = PERIOD.replace('from', 'afrom').replace('to', 'ato')
ABDURATION = BDURATION.replace('duration', 'aduration').replace('br', 'abr').replace('dit', 'adit')

# TACO related grammar
TACOMODEL = ur'[:：]?'+ASP+u'*(?P<company>__COMPANY__)'+ASP+u'*__SEP__(__ITEM__'+ASP+u'*__SEP__)?'+ASP+u'*(?P<position>'+POSITION+u'?)'+ASP+u'*'
PATTERN = PREFIX+u'?'+CONTEXT+u'?'+ASP+u'*'+PERIOD+TACOMODEL+BDURATION+u'?$'
TACO = re.compile(PATTERN.replace('__COMPANY__', COMPANY+u'?').replace('__SEP__', '\|').replace('__ITEM__', '.+?'), re.M)
TACOMODELCOPY = TACOMODEL.replace('company', 'ccompany').replace('position', 'cposition')
# Add line begin for safer searching
PATTERN = u'^'+PREFIX+u'?'+CONTEXT+u'?'+ASP+u'*'+APERIOD+TACOMODELCOPY+ABDURATION+u'?$'
# Not use for searching but only for matching (see the code)
NOPIPETACO = re.compile(PATTERN.replace('__COMPANY__', '\S+').replace('__SEP__', ' ').replace('__ITEM__', '\S+'), re.M)
ALLTACO = re.compile(u'((?P<pip>'+TACO.pattern+u')|(?P<nop>'+NOPIPETACO.pattern+u'))', re.M)

# Combine presence of duration and bracket around period for safer searching
RCO = re.compile(u'^'+PREFIX+u'?■?'+CONTEXT+u'?'+ASP+u'*(?P<company>\S+)'+ASP+u'+(?P<position>(\S+)?)(?(position)(('+ASP+u'+)|('+UNIBRALEFT+u')))'+PERIOD+u'(?(position)(('+ASP+u'+'+BDURATION+u')|('+UNIBRARIGHT+u')))', re.M)
HCO = re.compile(u'公司名称[:：]?'+ASP+u'*\*?(?P<company>'+COMPANY+u')\*?'+ASP+u'*(起止)?时间[:：]?'+ASP+u'*\*?'+PERIOD+'\*?$', re.M)

POASP = ASP.replace('\s', ' ')
PODEPARTMENT = u'([^\n:：'+SP+u']|('+POASP+u'[^\n'+SP+u']))+'
POFIELD = u'(?(nl)(([^\n:：'+SP+u'](\n+/)?)+)|([^\n'+SP+u']|('+POASP+u'[^\n'+SP+u']))+)'
PO = re.compile(u'所属行业[:：]'+POASP+u'*?(?P<nl>\n+)?'+POASP+u'*'+POFIELD+POASP+u'*\n+'+POASP+u'*('+PODEPARTMENT+u'(?(nl)()|('+POASP+u'+)))?(?(nl)('+POASP+u'*\n+'+POASP+u'*))(?P<aposition>'+POSITION+u'?)'+POASP+u'*$', re.M)

IXPO = re.compile(u'所属行业[:：].*\n+'+ASP+u'*(所属)?部'+ASP+u'*门[:：].*\n+'+ASP+u'*职'+ASP+u'*位[:：]'+ASP+u'*(?P<aposition>'+POSITION+u'?)'+ASP+u'*$', re.M)
APO = re.compile(u'^(其中)?'+APERIOD+ASP+u'*\*?(?P<aposition>'+POSITION+u'?)('+SALARY+u')?\*?$', re.M)
TPO = re.compile(u'^'+ASP+u'*(?P<aposition>'+POSITION+u'?)('+SALARY+u')?'+ASP+u'*'+APERIOD+''+ASP+u'*$', re.M)
TAPO = re.compile(u'^([所担]任)?职[位务](类别)?[:：]?'+ASP+u'*\*?(?P<aposition>'+POSITION+u'?)('+SALARY+u')?\*?'+ASP+u'*$', re.M)
BPO = re.compile(u'^(?P<aposition>(?!所属行业)'+POSITION+ASP+u'*)(\|'+ASP+u'*(?P<second>[^元/月'+SP+u']+)'+ASP+u'*)?($|(\|'+ASP+u'*('+SALARY+u')$))', re.M)
# Force use of ascii space to avoid matching new line and step over TCO in predator results
LIEPPO = re.compile(u'(?<!\\\\\n)^'+ASP+u'*'+APERIOD+ur' +(?P<aposition>'+POSITION+u'?)('+SALARY+u')?'+ASP+u'*$', re.M)

EMP = re.compile(BEMPLOYEES)


def output_cleanup(groupdict):
    for item in ['company', 'position']:
        try:
            if u'[' in groupdict[item]:
                begin = groupdict[item].index(u'[')
                end = groupdict[item].index(u']')
                groupdict[item] = groupdict[item][begin+1:end]
        except KeyError:
            continue
        except TypeError:
            continue
                    
def company_output(output, groupdict, begin='', end='', company=''):
    if 'company' in groupdict or 'ccompany' in groupdict:
        result = {}
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
            result['total_employees'] = groupdict['employees']
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

def position_output(output, groupdict, begin='', end='', company=''):
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
            result['at_company'] = len(output['company'])-1
        except:
            result['at_company'] = output['company'].index(company)
        format_salary(result, groupdict)
        output['position'].append(result)

name = lambda company: company['name']
duration = lambda company: company['duration']
companies = lambda output: output[1]['company']
positions = lambda output: output[1]['position']
company_1 = lambda x: companies(x)[0]
position_1 = lambda x: positions(x)[0]

def find_xp(RE, text):
    u"""
        >>> assert companies(find_xp(CO, u'2014 年 8 月 – 至今 company (1 年 6 个月)'))
        >>> assert companies(find_xp(CO, u'2010.03 - 至今*深圳市蓝韵实业有限公司* *(5年9个月)*'))
        >>> assert companies(find_xp(CO, u'2013-8 至 今  工作经历（IT服务行业）*---* 1年5个月'))
    """
    pos = 0
    out = {'company': [], 'position': []}
    MA = re.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+IXPO.pattern+u'))', re.M)
    dto = ''
    dfrom = ''
    for r in MA.finditer(text):
        if r.group('co'):
            dfrom, dto = r.group('from'), r.group('to')
            company_output(out, r.groupdict())
        else:
            pos +=1
            position_output(out, r.groupdict(), begin=dfrom, end=dto)
    if not pos:
        dto = ''
        dfrom = ''
        out = {'company': [], 'position': []}
        MA = re.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+PO.pattern+u'))', re.M)
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
    if not pos:
        MA = re.compile(u'((?P<co>'+RE.pattern+u')'+ASP+u'*(?P<po>'+LIEPPO.pattern+u'))', re.M)
        if MA.search(text):
            out = {'company': [], 'position': []}
        for r in MA.finditer(text):
            company_output(out, r.groupdict())
            pos +=1
            position_output(out, r.groupdict())
    return pos, out


def work_xp(text):
    u"""
        >>> assert work_xp(u'2014年4月 -- 至今 公司 | 客户服务经理、CT临床支持经理 （2年1个月）')[0]
        >>> assert not u'年' in name(company_1(work_xp(u'2011.01-至今 集团 （4年）\\n2009.04-2011.01 集团 （1年9个月）')))
        >>> assert not work_xp(u'\\n03/2013 – 现在 Consulting\\n\\n高级咨询师')[0] #FIXME
        >>> assert positions(work_xp(u'有限公司 招聘主管 2009/03 至 2013/03 （ 4\\n年） 保密'))
        >>> assert not work_xp(u'有限公司  加速器工程师  2013/07\~2014/08  广州\\n\\n公司  技术研发工程师  2014/08至今  上海')[0] == 2 #FIXME
        >>> assert not work_xp(u'有限公司 招聘主管 2015/03 至今（ 1 年 1 个月） 保密')[0] == 1 #FIXME
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
        >>> assert not work_xp(u'2012年12月—至今：有限公司[16个月]\\n所属行业： 医疗电子\\n职责:\\n编写程序功能块实现方案')[0]  # Do not FIXME
        >>>     # Different combinations of spaces and unicode spaces
        >>> assert work_xp(u'2010/7--2014/5：有限公司（150-500人）\\n所属行业： 计算机软件\\n研发中心    软件工程师')[0]
        >>> assert work_xp(u'2014 /10--至今： 有限公司\\n所属行业：\\n 互联网/电子商务\\n\\n管理顾问      高级咨询顾问')[0]
        >>> assert work_xp(u'2010 /3--至今：医疗设备(150-500人) [ 5 年9个月]\\n所属行业：  器械\\nX射线产品事业部   医疗器械研发')[0]
        >>> assert work_xp(u'2008/3 -- 2014/10： 有限公司（ 1000-5000人） [ 6年7个月 ]\\n所属行业： 仪器仪表\\n电能表事业部  项目经理')[0]
        >>> assert work_xp(u'2007 /3--2010 /12：有限公司 [ 3 年9个月]\\n所属行业： 服务(咨询、财会) 越秀集， 5:5 股份。\\n人事部    书/翻译')[0]
        >>> assert u'部' not in name(position_1(work_xp(u'''2014/5-至今： 科技集团 [ 2年1个月 ]\\n所属行业： 机械/设备\\n  生产部  生产领班/组长''')))
        >>> assert 'w' not in name(position_1(work_xp(u'2007 /9--2009 /8：INC PROJECT [11个月]\\n 所属行业：   其他\\npro worker  志愿者')))
        >>> assert work_xp(u'2014 /4--至今：有限公司(150-500人) [ 1 年8个月]\\n所属行业：\\n医疗设备/器械\\nR&D\\n医疗器械研发')[0]
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
        >>> assert not work_xp(u'有限公司 工程师 2013/07\~2014/08  广州')[0] #FIXME
        >>> assert companies(work_xp(u'■医院 （2012-04 \~ 至今）\\n公司性质：\\n担任职位：英语翻译'))
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

    Test for LIEPPO
        >>> assert position_1(work_xp(u'''2014.06 - 2015.01\\n上海分公司\\n(7个月)\\n  2014.06 - 2015.01 研发工程师'''))

        >>> assert company_1(work_xp(u'2014 /4--至今：有限公司(5000-10000人) [ 2 年]\\n所属行业：计算机软件\\n开发部 软件工程师'))['total_employees']
        >>> assert position_1(work_xp(u'2011.05 - 至今 GE医疗 (4年8个月\\n2011.05 - 至今研发主管、电气工程师15000元/月'))['salary']
    """
    RE = None
    pos = 0
    out = {'company': [], 'position': []}
    if True:
        if ECO.search(text):
            out = {'company': [], 'position': []}
            for r in ECO.finditer(text):
                pos +=1
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        elif CO.search(text):
            # Can try more things with CO as both PERIOD and DURATION safeguards
            pos, out = find_xp(CO, text)
            if not pos:
                out = {'company': [], 'position': []}
                MA = re.compile(u'((?P<co>'+CO.pattern+u')'+ASP+u'*(?P<po>'+BPO.pattern+u'))', re.M)
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
        elif TACO.search(text):
            # Support missing pipe in company definition by using NOPIPETACO
            for r in ALLTACO.finditer(text):
                pos += 1
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        elif PCO.search(text):
            out = {'company': [], 'position': []}
            for r in PCO.finditer(text):
                pos +=1
                company_output(out, r.groupdict())
                position_output(out, r.groupdict())
        elif TCO.search(text):
            pos, out = find_xp(TCO, text)
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


def fix(d, as_dict=False):
    u"""
        >>> assert not fix("2014年7月\~  苹果采购运营管理（上海）有限公司")[0][0] #FIXME
        >>> assert fix(u'工作经历：\\n\\n 教育背景：\\n\\n 2009年')[1] == 1
        >>> assert fix(u'工作经历\\n公司名称：美赞臣营养品有限公司\\n 起止时间：2013年5月-至今')[0][0]
        >>> assert fix(u'工作经历\\n音视频可靠光传输系统项目背景')[1] == 3   #项目背景 stop inside text
        >>> assert fix(u'工作经验：1年\\n公司名称 深圳x有限公司\\n 时间 2013.06 ——2014.04\\n职务 硬件工程师')[0][1]
        >>> assert fix(u'工作经历\\n1.  公司名称：有限公司\\n起止时间：2013年5月-至今\\n\\n担任职位：总账高级会计师')[0][1]
    """
    def fix_output(processed, reject):
        if as_dict:
            result = {}
            for (index, company) in enumerate(processed['company']):
                positions = [p for p in processed['position'] if p['at_company'] == index]
                if len(positions) <= 1:
                    try:
                        positions[0]['duration'] = company['duration']
                        del company['duration']
                    except IndexError:
                        continue
                    except KeyError:
                        continue
            if processed['company']:
                result['experience'] = processed
            return result
        else:
            for company in processed['company']:
                company['at_company'] = -1
            tuple_format = lambda x: tuple([x[k] for k in ['date_from', 'date_to', 'name', 'duration', 'at_company']])
            return ([tuple_format(p) for p in processed['company']], [tuple_format(p) for p in processed['position']]), reject

    reject = 0
    processed = {'company': [], 'position': []}
    res = XP.search(d)
    if res:
        pos, out = work_xp(res.group('expe'))
        if not pos and len(out['company']) == 0:
            reject = 1
        else:
            processed = out
    else:
        res = AXP.search(d)
        if res:
            pos, out = work_xp(res.group('expe'))
            if not pos and len(out['company']) == 0:
                pos, out = table_based_xp(res.group('expe'))
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
                MA = re.compile(u'((?P<co>'+TCO.pattern+u')|(?P<po>'+TPO.pattern+u'))', re.M)
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
    return fix_output(processed, reject)
