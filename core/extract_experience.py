# -*- coding: utf-8 -*-
import re

from interface.utils_parsing import *


SALARY = u'\d[\- \d\|]*(月/月)?元/月(以[上下])?'
EMPLOYEES = u'((?P<employees>(少于)?\d[\d '+SEP+u']*人(以[上下])?)([' + SENTENCESEP + u'].*?)?)'
BEMPLOYEES = u'('+ UNIBRALEFT +ASP+u'*' + EMPLOYEES + UNIBRARIGHT +u')'
BDURATION = u'(((?P<br>(?P<dit>\*)?'+UNIBRALEFT+u')|(\*\-{3}\*))' + ASP+u'*' + DURATION + u'(?(br)' +UNIBRARIGHT + u'(?(dit)\*)))'


XP = re.compile(ur'^'+ UNIBRALEFT +u'?((((工'+ASP+u'?作'+ASP+u'?)|(实习)|(工作(与)?实践))经'+ASP+u'?[历验])|(实习与实践))'+ UNIBRARIGHT +u'?(?P<expe>.*?)^(?='+ UNIBRALEFT +u'?(((项'+ASP+u'?目)|(教'+ASP+u'?育))'+ASP+u'?((经'+ASP+u'?[历验])|(背景)|(培训)))'+ UNIBRARIGHT +u'?)', re.DOTALL+re.M)
AXP = re.compile(ur'^'+ UNIBRALEFT +u'?((((工'+ASP+u'?作'+ASP+u'?)|(实习)|(工作(与)?实践))经'+ASP+u'?[历验])|(实习与实践))'+ UNIBRARIGHT +u'?[:：\ufffd]?'+ASP+u'*'+DURATION+'?'+ASP+u'*?\n(?P<expe>.*)', re.DOTALL+re.M)
TXP = re.compile(ur'-{9}[\-'+SP+u']*(?P<expe>'+PERIOD+ur'.*?)(?=-{9}[\-'+SP+u']*)', re.DOTALL)


PREFIX = u'((\d+['+SENTENCESEP+u'\.]?'+ASP+u'*)|('+UNIBRALEFT+u'[^年月（\(\[【'+CHNUMBERS+u']+?'+UNIBRARIGHT+u')|([◆\?]+))?'

# Allow multiline once in company name when duration is present
# As company has at least one char, need to handle break just as company tail
# Catching all employees is too expensive on parenthesis repetition, some will be post processed
ECO = re.compile(u'^(?P<position>(\S[\S ]+\n)*)\n+(?P<company>(\S[\S ]+\n)*)\n+' + PERIOD +ASP+u'*' + BDURATION, re.M+re.DOTALL)
CO = re.compile(PERIOD+ur'[:：\ufffd]?'+ASP+u'*(?P<cit>\*)?(?P<company>'+COMPANY+u'(\n(('+COMPANY+u')|('+COMPANYTAIL+u')))?)'+BEMPLOYEES+'?(?(cit)\*)?'+ASP+u'*'+BDURATION+'(?(cit)\*)?'+ASP+u'*$', re.DOTALL+re.M)
PCO = re.compile(PERIOD+ur'[:：\ufffd]?'+ASP+u'*(?P<cit>\*)?(?P<company>'+COMPANY+u'(\n(('+COMPANY+u')|('+COMPANYTAIL+u')))?)(?(cit)\*)'+ASP+u'*\|'+ASP+u'*(?P<position>'+POSITION+u'?)'+ASP+u'*'+BDURATION+'$', re.DOTALL+re.M)
TCO = re.compile(u'^'+PREFIX+ASP+u'*'+PERIOD+ur'[:：\ufffd]?'+ASP+u'*(?P<cit>\*)?(?P<company>'+COMPANY+u')(?(cit)\*)?'+ASP+u'*'+BDURATION+'?(?(cit)\*)?$', re.DOTALL+re.M)

# Avoid conflict in group names when combining *CO and *PO
APERIOD = PERIOD.replace('from', 'afrom').replace('to', 'ato')
ABDURATION = BDURATION.replace('duration', 'aduration').replace('br', 'abr').replace('dit', 'adit')

# TACO related grammar
TACOMODEL = ur'[:：\ufffd]?'+ASP+u'*(?P<company>__COMPANY__)'+ASP+u'*__SEP__(__ITEM__'+ASP+u'*__SEP__)?'+ASP+u'*(?P<position>'+POSITION+u'?)'+ASP+u'*'
PATTERN = PREFIX+ASP+u'*'+PERIOD+TACOMODEL+BDURATION+u'?$'
TACO = re.compile(PATTERN.replace('__COMPANY__', COMPANY+u'?').replace('__SEP__', '\|').replace('__ITEM__', '.+?'), re.M)
TACOMODELCOPY = TACOMODEL.replace('company', 'ccompany').replace('position', 'cposition')
# Add line begin for safer searching
PATTERN = u'^'+PREFIX+ASP+u'*'+APERIOD+TACOMODELCOPY+ABDURATION+u'?$'
# Not use for searching but only for matching (see the code)
NOPIPETACO = re.compile(PATTERN.replace('__COMPANY__', '\S+').replace('__SEP__', ' ').replace('__ITEM__', '\S+'), re.M)
ALLTACO = re.compile(u'((?P<pip>'+TACO.pattern+u')|(?P<nop>'+NOPIPETACO.pattern+u'))', re.M)

# Combine presence of duration and bracket around period for safer searching
RCO = re.compile(u'^'+PREFIX+u'■?'+ASP+u'*(?P<company>\S+)'+ASP+u'+(?P<position>(\S+)?)(?(position)(('+ASP+u'+)|('+UNIBRALEFT+u')))'+PERIOD+u'(?(position)(('+ASP+u'+'+BDURATION+u')|('+UNIBRARIGHT+u')))', re.M)
HCO = re.compile(u'公司名称[:：]?'+ASP+u'*\*?(?P<company>'+COMPANY+u')\*?'+ASP+u'*(起止)?时间[:：]?'+ASP+u'*\*?'+PERIOD+'\*?$', re.M)


PO = re.compile(u'所属行业[:：\ufffd]'+ASP+u'+.*?'+ASP+u'*?\n(.*?[\t ]+)?(?P<aposition>'+POSITION+u'?)'+ASP+u'*$', re.M)
APO = re.compile(u'^(其中)?'+APERIOD+ur''+ASP+u'*\*?(?P<aposition>'+POSITION+u'?)('+SALARY+u')?\*?$', re.M)
TPO = re.compile(u'^'+ASP+u'*(?P<aposition>'+POSITION+u'?)('+SALARY+u')?'+ASP+u'*'+APERIOD+''+ASP+u'*$', re.M)
TAPO = re.compile(u'^([所担]任)?职[位务](类别)?[:：\ufffd]?'+ASP+u'*\*?(?P<aposition>'+POSITION+u'?)('+SALARY+u')?\*?'+ASP+u'*$', re.M)
BPO = re.compile(u'^((?P<aposition>'+POSITION+u')'+ASP+u'*\|)?((?P<second>.+?)\|)?'+ASP+u'*('+SALARY+u')', re.M)

EMP = re.compile(BEMPLOYEES)


def format_output(output, begin, end, name, duration=None, _id=0):
    name = EMP.sub('', name)
    if not duration:
        duration = ''
    output.append((fix_date(begin), fix_date(end), fix_name(name), fix_duration(duration), _id-1))


def find_xp(RE, text):
    u"""
        >>> assert find_xp(CO, u'2014 年 8 月 – 至今 company (1 年 6 个月)')[1][0]
        >>> assert find_xp(CO, u'2010.03 - 至今*深圳市蓝韵实业有限公司* *(5年9个月)*')[1][0]
        >>> assert find_xp(CO, u'2013-8 至 今  工作经历（IT服务行业）*---* 1年5个月')[1][0]
    """
    pos = 0
    out = ([], [])
    MA = re.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+PO.pattern+u'))', re.M)
    dto = ''
    dfrom = ''
    for r in MA.finditer(text):
        if r.group('co'):
            dfrom, dto = r.group('from'), r.group('to')
            format_output(out[0], dfrom, dto, r.group('company'), r.group('duration'))
        else:
            pos +=1
            format_output(out[1], dfrom, dto, r.group('aposition'), _id=len(out[0]))
    if not pos:
        out = ([], [])
        MA = re.compile(u'((?P<co>'+RE.pattern+u')|(?P<po>'+APO.pattern+u'))', re.M)
        for r in MA.finditer(text):
            if r.group('co'):
                format_output(out[0], r.group('from'), r.group('to'), r.group('company'), r.group('duration'))
            else:
                pos +=1
                format_output(out[1], r.group('afrom'), r.group('ato'), r.group('aposition'), _id=len(out[0]))
    return pos, out


def work_xp(text):
    u"""
        >>> assert work_xp(u'2014年4月 -- 至今 公司 | 客户服务经理、CT临床支持经理 （2年1个月）')[0]
        >>> assert not not u'年' in work_xp(u'2011.01-至今 集团 （4年）\\n2009.04-2011.01 集团 （1年9个月）')[1][0][0][2]    #FIXME
        >>> assert not work_xp(u'\\n03/2013 – 现在 Consulting\\n\\n高级咨询师')[0] #FIXME
        >>> assert work_xp(u'有限公司 招聘主管 2009/03 至 2013/03 （ 4\\n年） 保密')[1][1]
        >>> assert not work_xp(u'有限公司  加速器工程师  2013/07\~2014/08  广州\\n\\n公司  技术研发工程师  2014/08至今  上海')[0] == 2 #FIXME
        >>> assert not work_xp(u'有限公司 招聘主管 2015/03 至今（ 1 年 1 个月） 保密')[0] == 1 #FIXME
        >>> assert not work_xp(u'2015年5月～至今  有限公司\\n  人力资源总监')[0] == 1  #FIXME
        >>> assert work_xp(u'2014年2月 -- 至今 管理（中国）有限公司\\n | 人力资源总监 （2年3个月）')[0]
        >>> assert work_xp(u'（海外）2011/3 -\\n2014/7：有限公司（5000-10000人）')[1][0]
        >>> assert work_xp(u'1.  2013.8——至今 有限公司')[1][0]
        >>> assert work_xp(u'\\n    2014/02-2015/05 有限公司')
        >>> assert work_xp(u'\\n2007年3月～2009年2月  有限公司\\n\\n其中2009/3—2010/9培训主管')[1][1]
        >>> assert work_xp(u'2001年6月 -- 至今 第一附属医院 | 影像中心 |\\n放射科医师  （14年11个月）')[1][1]
        >>> assert work_xp(u'2001年6月 -- 至今 第一附属医院 | 影像中心 |\\n放射科医师  （14年11个月）')[1][0][0][3]
        >>> assert work_xp(u'2014年4月 -- 至今 公司 | 客户服务经理、CT临床支持经理\\n （2年1个月）')[1][0][0][3]
        >>> assert work_xp(u'2012年1月 -- 2012年10月 有限公司 | 支持部\\n | 部经理 （9个月）')[1][0][0][3]
        >>> assert len(work_xp(u'2008年3月-2011年5月 Care Ltd. | 工程师\\n2011年5月-2013年6月 医疗  工程师')[1][1]) == 2
        >>> assert len(work_xp(u'2000年6月-2007年6月 公司 | 管理部\\n | 副课长\\n(一) 2000.06-2004.06：管理 人事副课长')[1][0]) == 1
        >>> assert work_xp(u'2008.12-2010.05 公司 （1年5个月）\\n开发部 | 工程师 | 6000元/月')[1][1]
        >>> assert not work_xp(u'2001.01-2004.12 家具公司 （3年11个月）\\n4001-6000元/月')[1][1]
        >>> assert work_xp(u'2012.09-至今 有限公司 （3年6个月）\\n\\n研发部主管\\n\\n医疗设备\\n\\n工作描述：')[1][1]
        >>> assert work_xp(u'。2010/07 -- 2012/06\\n\\n政邦律师事务所 | | 律师助理')[1][1]
        >>> assert work_xp(u'2014/01 - 2015/04 有限公司（1年3个月）\\nWEB、IOS开发工程师|1000元/月以下')[1][1]
        >>> assert not work_xp(u'2015/04-至今 Limi（8个月）\\n WEB开发|60元/月\\n2015/06-至今 有限公司 | php（3个月）\\n工程师|60元/月')[0] == 2 #FIXME
        >>> assert not work_xp(u'''2014/4-至今：有限公司  产品研发部：工程师''')[0] #FIXME
        >>> assert work_xp(u'??2015.10– 2016.01 赛诺微医疗科技（北京）有限公司')[1][0]
        >>> assert work_xp(u'Designer\\n\\nHealthcare\\n\\n2011 年 10 月 – 至今 (4 年 4 个月)Wuxi')[1][1]
        >>> assert work_xp(u'''CT Engineer\\n\\nHealthcare\\n\\n2013年7月 – 至今 (2年7个月)''')
        >>> assert u'工' in work_xp(u'[助理 / \\n工程师](http://www.)\\n\\n[Care]\\n(http://www.)\\n\\n2014年12月–至今(1 年2个月)')[1][1][0][2]
        >>> assert work_xp(u'项目\\n\\n课程\\n\\nIntern\\n\\nCorporation\\n\\n2011年9月–2013年2月(1年6个月)')[1][1]
        >>> assert u'Head' in work_xp(u'Head (FGs\\nmanufacturer)\\n\\nLimited Group\\n\\n2012年6月–至今(2年9个月)')[1][1][0][2]
        >>> assert u'3G' not in work_xp(u'3G\\n\\nEngineer\\n\\nTelecom\\n\\n2012年4月–至今 (9 个月)中国')[1][1][0][2]
        >>>     # TODO re.compile(u'^(?P<company>\S+)'+ASP+u'+(?P<position>\S+)'+ASP+u'*'+PERIOD+ASP+u'+(\S*)?$', re.M)
        >>> assert not work_xp(u'有限公司 工程师 2013/07\~2014/08  广州')[0] #FIXME
        >>> assert work_xp(u'■医院 （2012-04 \~ 至今）\\n公司性质：\\n担任职位：英语翻译')[1][0]
        >>> assert not work_xp(u'2014年10月——2014年11月   技工学校    实习班主任、老师')[1][0]  #FIXME
        >>>     #TODO use NOPIPETACO
        >>> assert work_xp(u'2009/09 -- 2010/09\\n\\nAlcatel | CIO | Engineer')[0]
        >>>     # TODO empty middle field between pipes
        >>> assert not u'Leader' in work_xp(u'2010/10 -- Now\\n\\nHealthcare | CT | R&D | Engineer / Project\\nLeader')[1][1][0][2]  #FIXME
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
    """
    RE = None
    pos = 0
    out = ([], [])
    if True:
        if ECO.search(text):
            out = ([], [])
            for r in ECO.finditer(text):
                cleanup = {'company': r.group('company'),
                            'position': r.group('position')
                        }
                for item in ['company', 'position']:
                    if u'[' in r.group(item):
                        begin = r.group(item).index(u'[')
                        end = r.group(item).index(u']')
                        cleanup[item] = r.group(item)[begin+1:end]
                    
                format_output(out[0], r.group('from'), r.group('to'),
                                cleanup['company'].replace('\n', ' '), r.group('duration'))
                pos +=1
                format_output(out[1], r.group('from'), r.group('to'),
                                cleanup['position'].replace('\n', ' '), _id=len(out[0]))
        elif CO.search(text):
            # Can try more things with CO as both PERIOD and DURATION safeguards
            pos, out = find_xp(CO, text)
            if not pos:
                out = ([], [])
                MA = re.compile(u'(?P<co>'+CO.pattern+u')'+ASP+u'*('+BPO.pattern+ASP+u'*)?$', re.M)
                for r in MA.finditer(text):
                    format_output(out[0], r.group('from'), r.group('to'), r.group('company'), r.group('duration'))
                    if r.group('aposition'):
                        pos +=1
                        if r.group('second'):
                            format_output(out[1], r.group('from'), r.group('to'), r.group('second'), _id=len(out[0]))
                        else:
                            format_output(out[1], r.group('from'), r.group('to'), r.group('aposition'), _id=len(out[0]))
            if not pos:
                out = ([], [])
                MA = re.compile(u'(?P<co>'+CO.pattern+u')(\n+(?P<position>'+POSITION+u')\n+.*?\n+工作描述：)?', re.M)
                for r in MA.finditer(text):
                    format_output(out[0], r.group('from'), r.group('to'), r.group('company'), r.group('duration'))
                    if r.group('position'):
                        pos +=1
                        format_output(out[1], r.group('from'), r.group('to'), r.group('position'), _id=len(out[0]))
        elif TACO.search(text):
            # Support missing pipe in company definition by using NOPIPETACO
            for r in ALLTACO.finditer(text):
                if r.group('pip'):
                    dfrom, dto = r.group('from'), r.group('to')
                    format_output(out[0], dfrom, dto, r.group('company'), r.group('duration'))
                    pos += 1
                    format_output(out[1], dfrom, dto, r.group('position'), _id=len(out[0]))
                else:
                    dfrom, dto = r.group('afrom'), r.group('ato')
                    format_output(out[0], dfrom, dto, r.group('ccompany'), r.group('aduration'))
                    pos += 1
                    format_output(out[1], dfrom, dto, r.group('cposition'), _id=len(out[0]))
        elif PCO.search(text):
            out = ([], [])
            for r in PCO.finditer(text):
                format_output(out[0], r.group('from'), r.group('to'), r.group('company'), r.group('duration'))
                pos +=1
                format_output(out[1], r.group('from'), r.group('to'), r.group('position'), _id=len(out[0]))
        elif TCO.search(text):
            pos, out = find_xp(TCO, text)
            if not pos:
                out = ([], [])
                MA = re.compile(u'((?P<co>'+TCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
                for r in MA.finditer(text):
                    if r.group('co'):
                        dfrom, dto = r.group('from'), r.group('to')
                        format_output(out[0], dfrom, dto, r.group('company'), r.group('duration'))
                    else:
                        # We need this if broken period '2015/03\~\n' leads to missing company
                        if not out[0]:
                            break
                        pos +=1
                        format_output(out[1], dfrom, dto, r.group('aposition'), _id=len(out[0]))
        elif RCO.search(text):
            out = ([], [])
            MA = re.compile(u'((?P<co>'+RCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
            for r in MA.finditer(text):
                if r.group('co'):
                    dfrom, dto = r.group('from'), r.group('to')
                    format_output(out[0], dfrom, dto, r.group('company'), r.group('duration'))
                    if r.group('position'):
                        pos +=1
                        format_output(out[1], dfrom, dto, r.group('position'), _id=len(out[0]))
                else:
                    pos +=1
                    format_output(out[1], dfrom, dto, r.group('aposition'), _id=len(out[0]))
    return pos, out

def table_based_xp(text):
    u"""
        >>> assert table_based_xp(u'''\\n公司名称 有限公司\\n时间  2013.06 ——2014.04\\n\\n职务 助理硬件工程师''')[0]
    """
    pos = 0
    out = ([], [])
    if HCO.search(text):
        dto = ''
        dfrom = ''
        MA = re.compile(u'((?P<co>'+HCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
        for r in MA.finditer(text):
            if r.group('co'):
                dfrom, dto = r.group('from'), r.group('to')
                format_output(out[0], dfrom, dto, r.group('company'))
            else:
                pos +=1
                format_output(out[1], dfrom, dto, r.group('aposition'), _id=len(out[0]))
    return pos, out


def fix(d):
    u"""
        >>> assert not fix("2014年7月\~  苹果采购运营管理（上海）有限公司")[0] #FIXME
        >>> assert fix(u'工作经历：\\n\\n 教育背景：\\n\\n 2009年')[1] == 3
        >>> assert fix(u'工作经历\\n公司名称：美赞臣营养品有限公司\\n 起止时间：2013年5月-至今')[0]
        >>> assert fix(u'工作经历\\n音视频可靠光传输系统项目背景')[1] == 3   #项目背景 stop inside text
        >>> assert fix(u'工作经验：1年\\n公司名称 深圳x有限公司\\n 时间 2013.06 ——2014.04\\n职务 硬件工程师')[0][1]
        >>> assert fix(u'工作经历\\n1.  公司名称：有限公司\\n起止时间：2013年5月-至今\\n\\n担任职位：总账高级会计师')[0]
    """
    reject = 0
    processed = None
    res = XP.search(d)
    if res:
        pos, out = work_xp(res.group('expe'))
        if not pos and len(out[0]) == 0:
            reject = 1
        else:
            processed = out
    else:
        res = AXP.search(d)
        if res:
            pos, out = work_xp(res.group('expe'))
            if not pos and len(out[0]) == 0:
                pos, out = table_based_xp(res.group('expe'))
                if not pos and len(out[0]) == 0:
                    reject = 3
                else:
                    processed = out
            else:
                processed = out
        elif TXP.search(d):
            pos = 0
            out = ([], [])
            res = TXP.search(d)
            if TCO.search(res.group('expe')):
                MA = re.compile(u'((?P<co>'+TCO.pattern+u')|(?P<po>'+TPO.pattern+u'))', re.M)
                for r in MA.finditer(res.group('expe')):
                    if r.group('co'):
                        format_output(out[0], r.group('from'), r.group('to'), r.group('company'), r.group('duration'))
                    else:
                        pos +=1
                        format_output(out[1], r.group('afrom'), r.group('ato'), r.group('aposition'), _id=len(out[0]))
                if not pos:
                    out = ([], [])
                    dto = ''
                    dfrom = ''
                    MA = re.compile(u'((?P<co>'+TCO.pattern+u')|(?P<po>'+TAPO.pattern+u'))', re.M)
                    for r in MA.finditer(res.group('expe')):
                        if r.group('co'):
                            dfrom, dto = r.group('from'), r.group('to')
                            format_output(out[0], dfrom, dto, r.group('company'), r.group('duration'))
                        else:
                            pos +=1
                            format_output(out[1], dfrom, dto, r.group('aposition'), _id=len(out[0]))
            if not pos and len(out[0]) == 0:
                reject = 2
            else:
                processed = out
        else:
            reject = 4
    return processed, reject
