# -*- coding: utf-8 -*-
import re

from extractor.utils_parsing import *


ED_PERIOD = u'(('+PERIOD+u')|(?P<ato>'+DATE+u'))'
# We check for braket to avoid catching title 教育/培训/学术/科研/院校
ED = re.compile(ur'^'+PREFIX+u'*(?P<br>'+UNIBRALEFT +u')?\**教'+ASP+u'*育'+ASP+u'*((经'+ASP+u'*[历验])|(背景)|((?(br)/?)[及与]?培训))[:：]?'+ UNIBRARIGHT +u'?(?P<edu>.*?)^'+PREFIX+u'*(?='+ UNIBRALEFT +u'?\**((((项'+ASP+u'*目)|((工'+ASP+u'*作'+ASP+u'*)|(实习)|(工作(与)?实践))){1,}'+ASP+u'*经'+ASP+u'*[历验])|(实习与实践)|(背景)|(培训)|(语言((能力)|(技能)))|(所获奖项)|(校内职务)|(学生实践经验)|(技能证书)|(接受培训)|(社会经验)|素质技能)'+ UNIBRARIGHT +u'?)', re.DOTALL+re.M)
AED = re.compile(ur'^'+PREFIX+u'*(?P<br>'+ UNIBRALEFT +u')?\**教'+ASP+u'*育'+ASP+u'*((经'+ASP+u'*[历验])|(背景)|((?(br)/?)[及与]?培训))[:：]?'+ UNIBRARIGHT +u'?(?P<edu>.*)', re.DOTALL+re.M)
EED = re.compile(ur'^'+PREFIX+'*'+ASP+u'*(?P<br>'+ UNIBRALEFT +u')?\**Education\**'+ UNIBRARIGHT +u'?\n(?P<edu>.*)', re.DOTALL+re.M)


PELASTMA = re.compile(u'^'+POESP+u'*'+CONTEXT+u'?'+POESP+u'*'+SCHOOL+POESP+u'+'+MAJOR+POESP+u'+'+EDUCATION+POESP+u'+'+PERIOD, re.M)
PIPELASTMA = re.compile(u'^'+POESP+u'*'+CONTEXT+u'?'+POESP+u'*'+SCHOOL+POESP+u'+\|'+POESP+u'+'+EDUCATION+POESP+u'+\|'+POESP+u'+'+MAJOR+POESP+u'+'+PERIOD, re.M)
PIPEEDMA = re.compile(u'^'+POESP+u'*'+CONTEXT+u'?'+POESP+u'*'+PERIOD+POESP+u'*'+SCHOOL+u'\n+'+POESP+u'*'+EDUCATION+POESP+u'*\|'+POESP+u'*'+MAJOR+u'$', re.M)
PIPEEDLASTMA = re.compile(u'^'+POESP+u'*'+CONTEXT+u'?'+POESP+u'*'+PERIOD+POESP+u'*'+SCHOOL+u'\n+'+POESP+u'*'+MAJOR+POESP+u'+\|'+POESP+u'+'+EDUCATION, re.M)

SENSEMA = re.compile(CONTEXT+u'?'+PERIOD+u'[\n'+SP+EDUFIELDSEP+u']*'+SCHOOL+ASP+u'*(?P<sep>['+EDUFIELDSEP+u'])'+ASP+u'*'+MAJOR+ASP+u'*(?P=sep)'+ASP+u'*'+EDUCATION+ASP+u'*'+exclude_with_parenthesis('')+u'?'+ASP+u'*$', re.M)
SENSEDROP = u'((\S+)[\n'+SP+EDUFIELDSEP+u']*)?'
RVSENSEMA = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+SCHOOL+ASP+u'*'+PERIOD+u'[\n'+SP+EDUFIELDSEP+u']*'+MAJOR+ASP+u'*(?P<sep>['+EDUFIELDSEP+u'])'+ASP+u'*'+SENSEDROP+u''+EDUCATION+ASP+u'*(?P=sep)'+ASP+u'*'+SENSEDROP+u'$', re.M)
MAJFSTMA = re.compile(PREFIX+u'*'+PERIOD+ur'[:：]?[\n'+SP+u']+'+UNIBRALEFT+u'(?P<major>\S+)'+UNIBRARIGHT+'\([^\(]*\)[\n'+SP+u']+'+SCHOOL+ASP+u'+'+EDUCATION+ASP+u'*$', re.M)
# Major is optional
SPSOLHDR = ASP+u'*(?P<col1>-{5,}) (?:-{5,}) (?:-{5,}) (?:-{5,})\n'
SEPLIST = ur'[:：]?'+ASP+u'*'
CTL = (u'(?P<period>'+PERIOD+u')', SCHOOL)
SPSOLMA = re.compile(CONTEXT+u'?'+PREFIX+u'*'+SEPLIST.join(CTL)+u'[\n'+SP+u']+(([^'+SP+u']+[\n'+SP+u']+)?((?P<major>[^'+SP+u']+(\s'+exclude_with_parenthesis('')+u')?)[\n'+SP+u']+))?'+EDUCATION+ASP+u'*', re.M)
RVSPSOLMA = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+SEPLIST.join(reversed(CTL))+u'[\n'+SP+u']+(([^'+SP+u']+[\n'+SP+u']+)?((?P<major>[^'+SP+u']+(\s'+exclude_with_parenthesis('')+u')?)[\n'+SP+u']+))?'+EDUCATION+ASP+u'*', re.M)
UCSOLMA = re.compile(CONTEXT+u'?'+PREFIX+u'*'+PERIOD+ur'[:：]?'+ASP+u'*'+SCHOOL+u'( ?[\xa0\ufffd])'+ASP+u'*((?P<major>[^\ufffd\xa0'+u'\n]+?)( ?[\xa0\ufffd])'+ASP+u'*)?'+EDUCATION, re.M)
SPSOLMAEDFST = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+PERIOD+ur'[:：]?'+ASP+u'*'+EDUCATION+u'[\n'+SP+u']+'+SCHOOL+u'[\n'+SP+u']+(?P<major>[^'+SP+u']+)[\n'+SP+u']+', re.M)

SEPLIST = u'[\n'+SP+u']*)|(?:(\d\.)?'+ASP+u'*'
VRT = (u'(毕业)?[院学]校(名称)?[:：]'+ASP+u'*'+SCHOOL, u'((就读)|(入学))?时间[:：]'+ASP+u'*'+PERIOD, u'专业(名称)?[:：]'+ASP+u'*(?P<major>.+?)', u'学[位历][:：]'+ASP+u'*'+EDUCATION+ASP)
HDVRTMA = re.compile(u'^'+PREFIX+u'*(?:(?:(\d\.)?'+ASP+u'*'+ SEPLIST.join(VRT) +u')){4}'+ASP+u'*$', re.M)

SEPLIST = u''
CTL = (u'\**(?P<school>.+?)\**', u'(?P<br>'+UNIBRALEFT+')?'+ASP+u'*\**'+PERIOD+u'\**'+ASP+u'*(?(br)'+UNIBRARIGHT+')')
MANDCTLMA = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+ SEPLIST.join(CTL)+ASP+u'+专业(名称)?[:：]'+ASP+u'*(?P<major>.+?)'+ASP+u'*学(历/学)?[历位][:：]'+ASP+u'*'+EDUCATION, re.M)
RVMANDCTLMA = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+ SEPLIST.join(reversed(CTL))+ASP+u'+专业(名称)?[:：]'+ASP+u'*(?P<major>.+?)'+ASP+u'*学(历/学)?[历位][:：]'+ASP+u'*'+EDUCATION, re.M)
HDCTLMA = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+ SEPLIST.join(CTL)+ASP+u'*\n+('+ASP+u'*专业(名称)?[:：])?'+ASP+u'*(?P<major>.+?)'+ASP+u'*(学院名称[:：]'+ASP+u'*\S+'+ASP+u'+'+ASP+u'*)?学(历/学)?[历位][:：]'+ASP+u'*'+EDUCATION+u'('+ASP+u'+((是否)|(全日制))统招[:：]?'+ASP+u'*[是否])?', re.M)
RVHDCTLMA = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+ SEPLIST.join(reversed(CTL))+ASP+u'*\n+('+ASP+u'*专业(名称)?[:：])?'+ASP+u'*(?P<major>.+?)'+ASP+u'*(学院名称[:：]'+ASP+u'*\S+'+ASP+u'+'+ASP+u'*)?学(历/学)?[历位][:：]'+ASP+u'*'+EDUCATION+u'('+ASP+u'+((是否)|(全日制))统招[:：]?'+ASP+u'*[是否])?', re.M)

NLSMLMA = re.compile(u'^'+CONTEXT+u'?'+PREFIX+u'*'+PERIOD+ur'[:：]?'+ASP+u'*'+SCHOOL+u'\n{2}'+ASP+u'*'+EDUCATION+u'\n{2}'+ASP+u'*(?P<major>\S+)'+ASP+u'*$', re.M)

TABHDRMAJ = u'^'+ASP+u'*时'+ASP+u'*间段?'+ASP+u'+[院学]'+ASP+u'*校('+ASP+u'*名'+ASP+u'*称)?'+ASP+u'+专'+ASP+u'*业'+ASP+u'+(获得证书/)?学'+ASP+u'*历(/学位)?('+ASP+u'+证'+ASP+u'*书)?('+ASP+u'+是否统招)?(?P<edu>.+)'

TED = re.compile(u'^'+ASP+u'*-{3}[\- ]*\n'+HDCTLMA.pattern+u'\n-{3}[\- ]*$', re.M)
THED = re.compile(u'^'+ASP+u'*(-{3}[\-'+SP+u']*\n+)?'+TABHDRMAJ+'+-{3}[\-'+SP+u']*$', re.DOTALL+re.M)

YIED = re.compile(u'^'+SCHOOL+ASP+u'+(('+PERIOD+u')|((?P<afrom>)(?P<ato>'+DATE+')))'+ASP+u'+'+EDUCATION+u'('+ASP+u'+(?P<major>[^=\n\*：:\|]+))?$', re.M)
SINGLEYIED = re.compile(u'^教育经[历位]'+ASP+u'+'+SCHOOL+ASP+u'+'+PERIOD+ASP+u'+(?P<major>[^=\n\*：:\|]+)$', re.M)

SUMMARYEDU = re.compile(u'学'+ASP+u'*[历位][:：]'+ASP+u'*(?P<education>\S+)', re.M)
SUMMARYMAJOR = re.compile(u'专'+ASP+u'*业[:：]'+ASP+u'*(?P<major>\S+)', re.M)
SUMMARYSCHOOL = re.compile(u'((毕业院)|(学))'+ASP+u'*校[:：]'+ASP+u'*'+SCHOOL, re.M)

EMA = re.compile('^'+PREFIX+'*'+ASP+'*\**'+SCHOOL+u'\**\n+'+PREFIX+'*'+ASP+'*'+EDUCATION+','+ASP+'*'+MAJOR+u'\n+(?P<from>\d{4}|'+ENPDATE+u')'+DATESEP+'(?P<to>\d{4}|'+ENPDATE+u')', re.M)

def format_output(output, groupdict, summary=None):
    result = {
        'major': '',
        'education': '',
        'school': fix_name(groupdict['school'].replace('\n', ' ')),
        }
    if groupdict['from']:
        result['date_from'] = fix_date(groupdict['from'])
        result['date_to'] = fix_date(groupdict['to'])
    else:
        result['date_from'] = fix_date(groupdict['afrom'])
        result['date_to'] = fix_date(groupdict['ato'])
    try:
        result['education'] = fix_education(groupdict['education'])
        if groupdict['shorted4']:
            result['education'] = fix_education(groupdict['shorted4'])
        elif groupdict['shorted6']:
            result['education'] = fix_education(groupdict['shorted6'])
        elif groupdict['shorted7']:
            result['education'] = fix_education(groupdict['shorted7'])
    except KeyError:
        if summary:
            result['education'] = fix_education(summary['education'])
            
    try:
        result['major'] = fix_name(groupdict['major'].replace('\n', ' '))
    except AttributeError:
        if summary and 'major' in summary:
            result['major'] = fix_name(summary['major'])
        else:
            result['major'] = ''
    output.append(result)

schools = lambda output: output[1]
school_1 = lambda output: output[1][0]
name = lambda school: school['school']
major = lambda school: school['major']
education = lambda school: school['education']

def education_xp(text, summary=None):
    u"""
        >>> assert education_xp(u'1999年9月至2001年7月  北京科技经营管理学院  计算机应用技术           大专')[0]
        >>> assert '|' not in major(school_1(education_xp(u'2007年9月至2010年7月        山东理工大学\\n\\n农业电气化及自动化 | 硕士学位')))
        >>> assert education_xp(u'  2000.09 - 2003.07  清华大学  工程物理系  硕士')[0]
        >>> assert education_xp(u'2002/09 - 2005/03   沈阳工业大学 �电力电子与电力传动 �硕士')[0]
        >>> assert u'法' not in name(school_1(education_xp(u'2007/09-2011/06   福建漳州师范学院��法学 �本科')))
        >>> assert u'电' not in name(school_1(education_xp(u'2011/09 - 2013/12   广东科技学院 电子信息科学与技术 大专')))
        >>> assert education_xp(u'（海外） 2015 /9 --至今  南京大学 人力资源管理 MBA')[0]
        >>> assert education_xp(u'1995 /9--1998 /7  衡阳医学院（现名“南华大学”）   临床医学与医学技术   大专')[0]
        >>> assert education_xp(u'2009.01 - 2010.06  印度大学(India University)  软件工程  硕士')[0]
        >>> assert education_xp(u'2012.09-2015.06        重庆大学             机械电子工程      硕   士')[0]
        >>> assert 2 == len(education(school_1(education_xp(u'2012.09-2015.06        重庆大学             机械电子工程      硕   士'))))
        >>> assert education_xp(u'2001.03 - 2002.11  悉尼科技大学 (University of Technology, Sydney)  其他  本科')[0]
        >>> assert education_xp(u'1999.02 - 2000.11  商业学院，悉尼大学  商业全科学 (Business Studies)  大专')[0]
        >>> assert education_xp(u'教育背景及培训：\\n\\n   1996.09-2000.07  西南学院 (西南科技大学)\\n 自动化  本科。')[0] == 1
        >>> assert education_xp(u'（海外） 2015/9-至今 南京大学 管理 MBA\\n双证班；\\n2007/1-2010/1 南京大学 资源管理 本科\\n管理')[0] == 2
        >>> assert 2 == education_xp(u'2010.09 - 2013.07  能科学研究院  原子核物理\\n 硕士2006.09 - 2010.07  理工大学  飞行器设计  本科')[0]
        >>> assert 2 == education_xp(u'2010.09-至今  科学研究院  原子核物理\\n 硕士2006.09 - 2010.07  理工大学  飞行器设计  本科')[0]
        >>> assert education_xp(u'2000/9―2003/3：同济大学 | 生物医学工程 | 硕士')[0]
        >>> assert education_xp(u'2006/09 --2010/06广东商学院 | 法学 | 学士')[0]
        >>> assert '|' not in name(school_1(education_xp(u'2009/09 --2012/07 \\n\\n电力职业技术学院 | 其自动化 | 大专')))
        >>> assert 'y' in name(school_1(education_xp(u'2010.09 - 2012.06  Northwestern University  生物医学工程  硕士')))
        >>> assert education_xp(u'? 2003.9-2006.4  西北工业大学  材料学院  材料加工工程，计算机模拟加工\\n 硕士')[0]
        >>> assert education_xp(u'''（海外） 2005/9 - 2006/1 国家大学－人文大学\\n专业：其它外语\\n学历： 本科''')[0]
        >>> assert education_xp(u'清华大学（1987.09 - 1992.07）\\n 专业：近代物理电子学  学历：本科  是否统招：是')[0]
        >>> assert education_xp(u'新乡学院�（ 2005.09-2008.07 ）�\\n\\n专业：机械设计制造�\\n\\n学历：大专�')[0]
        >>> assert education_xp(u'山东大学（ 2001.09 - 2005.07 ）\\n专业名称： 自动化   学历： 本科   是否统招： 是')[0]
        >>> assert education_xp(u'''湖北工业大学（2003.09—2007.07）\\n\\n电气工程\\n\\n学院名称： 工程学院\\n\\n学历： 本科''')[0]
        >>> assert education_xp(u'毕业院校： 浙江大学（原名：杭州学院）\\n就读时间：1986-09–1990-07\\n专业：食品卫生\\n学位：本科')[0]
        >>> assert not education_xp(u'2005-09 ～ 2009-06    ：   江南大学\\n\\n  轻化工程，本科')[0]    #FIXME
        >>> assert education_xp(u'2014-9 至 2017-6   计算机科学与技术华南师范大学\\n\\n硕士研究生\\n\\n云计算与大数据处理')[0]
        >>> assert education_xp(u'东华大学 工程学院（2006.09 - 至今）\\n专业：自动化专业  学历：硕士   是否统招：是')[0]
        >>> assert education_xp(u'2006-9\~ 2010-6     广东工业大学 轻工化工学院 生物工程  本科   统招')[0]
        >>> assert education_xp(u'2001/08 --2005/07  大连理工大学  机械设计制造及其自动化专业  学士')[0]
        >>>     #TODO replace 学士 by corresponding 学历
        >>> assert education_xp(u'学历：本科  毕业学校：湖南大学\\n\\n专业：汉语言文学  时间：2004.01 至2008.01\\n')[0]
        >>> assert 2 == len((schools(education_xp(u'中科院近代物理研究所       加速器物理         硕士   2010/09\~2013/07  兰州\\n\\n'
        ...         u'陕西师范大学           物理学 (排名：4/169)    学士      2006/09\~2010/07  西安'))))
        >>> assert education_xp(u'清华大学 | 博士 | 工程物理-加速器   2010年9月 - 2014年9月')
        >>> assert education_xp(u'2003/9 - 2007/5 湖南科技大学\\n\\n专业：生物科学，技术\\n\\n学历： 本科')[0]
        >>> assert education_xp(u'''2010年8月  --  2014年1月东北大学\\n\\n专业名称：其自动化\\n\\n学历/学位：博士 全日制统招：是''')[0]
        >>> assert education_xp(u'2011-9 至 2014-7   计算机软件与理论中山大学\\n\\n硕士研究生')[1]
        >>> assert u'广' in name(school_1(education_xp(u'''2001.09-2004.06        广东省广宁中学           高中''')))
        >>> assert education_xp(u'2010-9 至 2014-7   软件工程中山大学\\n\\n本科 丨GPA：3.7 丨班级名次：前30名')[1]
        >>> assert '|' not in major(school_1(education_xp(u'''工业学院\\n\\n2001年9月-2005年7月\\n\\n 无机非金属材料| 材料类| 本科 |济南''')))
        >>> assert education_xp(u'1.  2006年9月—2010年7 月，天津科技大学，机械设计制造及自动化，本科')
        >>> assert education_xp(u'2007/09-2010/03 天津科技大学，农产品加工及贮藏工程， 硕士学位')
        >>> assert not education_xp(u'''2005.09-2009.07         湖南工程学院      大学本科\\n其自动化''')[0]    #FIXME
        >>> assert not education_xp(u'2001 /9--2005 /7   华中农业大学   计算机科学与技术')[0]  #FIXME
        >>> assert not education_xp(u'2005 /9--2009 /7   广东药学院   生物技术（制药方向）')[0] #FIXME
        >>> assert not not education_xp(u'2010-9 至 2014-6   计算机科学与技术湖北经济学院\\n\\n本科 学士 丨班级名次：前20名')[1]  #FIXME
        >>>     #TODO 本科 学士 makes one for education and the other for major
        >>> assert not education_xp(u'2003年9月---2008年6月：华北煤炭医学院')[1]  #FIXME
        >>> assert not education_xp(u'最高学位：硕士 2009年11月\\n\\n毕业院校：巴斯大学（英国）中英口笔译')[0]  #FIXME
        >>> assert not education_xp(u'2004/9-2008/7         浙江大学\\n本科|生物科学，技术')[0] #FIXME

        MANDCTLMA related
        >>> assert 6 == len(name(school_1(education_xp(u'合肥工业大学 2006/09–2010/06   专业：材料成型及控制工程专业   学历：本科'))))

        RVHDCTLMA test:
        >>> assert u'本科' in school_1(education_xp(u'   1.  ##### 2007年6月  --  2011年4月北京人文大学\\n\\n> 专业名称：\\n>\\n'
        ...     u'> 机械设计制造及其自动化\\n>\\n> 学历/学位：\\n>\\n> 本科 全日制统招：是'))['education']
        >>> assert u'硕士' in school_1(education_xp(u'##### **2003年10月  --  2006年2月天津大学**\\n\\n> 专业名称：\\n>\\n'
        ...     u'> 制药工程\\n>\\n> 学历/学位：\\n>\\n> 硕士 全日制统招：是'))['education']
    """
    maj = 0
    out = []
    if PIPEEDMA.search(text):
        for r in PIPEEDMA.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    elif PIPEEDLASTMA.search(text):
        for r in PIPEEDLASTMA.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    elif PELASTMA.search(text):
        for r in PELASTMA.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    elif PIPELASTMA.search(text):
        for r in PIPELASTMA.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    elif MANDCTLMA.search(SHORTEN_BLANK(text)):
        for r in MANDCTLMA.finditer(SHORTEN_BLANK(text)):
            maj +=1
            format_output(out, r.groupdict())
    elif RVMANDCTLMA.search(SHORTEN_BLANK(text)):
        for r in RVMANDCTLMA.finditer(SHORTEN_BLANK(text)):
            maj +=1
            format_output(out, r.groupdict())
    elif HDCTLMA.search(SHORTEN_BLANK(text)):
        for r in HDCTLMA.finditer(SHORTEN_BLANK(text)):
            maj +=1
            format_output(out, r.groupdict())
    elif RVHDCTLMA.search(SHORTEN_BLANK(text)):
        for r in RVHDCTLMA.finditer(SHORTEN_BLANK(text)):
            maj +=1
            format_output(out, r.groupdict())
    elif HDVRTMA.search(text):
        for r in HDVRTMA.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    elif MAJFSTMA.search(text):
        for r in MAJFSTMA.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    elif NLSMLMA.search(text):
        for r in NLSMLMA.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    if not maj:
        if SENSEMA.search(text):
            out = []
            for r in SENSEMA.finditer(text):
                maj +=1
                format_output(out, r.groupdict())
        elif RVSENSEMA.search(text):
            out = []
            for r in RVSENSEMA.finditer(text):
                maj +=1
                format_output(out, r.groupdict())
    if not maj and SPSOLMA.search(text):
        out = []
        for r in SPSOLMA.finditer(text):
            if r.group('major'):
                maj +=1
                format_output(out, r.groupdict())
            elif summary:
                maj +=1
                format_output(out, r.groupdict(), summary)
            else:
                format_output(out, r.groupdict(), summary={'major': ''})
        out = sorted(out, key=lambda x: x['date_from'], reverse=True)
    if not maj and SPSOLMAEDFST.search(text):
        out = []
        for r in SPSOLMAEDFST.finditer(text):
            if r.group('major'):
                maj +=1
                format_output(out, r.groupdict())
            elif summary:
                maj +=1
                format_output(out, r.groupdict(), summary)
            else:
                format_output(out, r.groupdict(), summary={'major': ''})
    if not maj and UCSOLMA.search(text):
        out = []
        for r in UCSOLMA.finditer(text):
            if r.group('major'):
                maj +=1
                format_output(out, r.groupdict())
            elif summary:
                maj +=1
                format_output(out, r.groupdict(), summary)
            else:
                format_output(out, r.groupdict(), summary={'major': ''})
    if not maj and summary:
        RE = re.compile(u'^'+PREFIX+u'*'+ASP+u'*'+PERIOD+ASP+u'+(?P<school>%s)' %
                aspstrip(summary['school'].replace('(', '\(').replace(')', '\)'))+ASP+u'+(?P<major>%s)' % aspstrip(summary['major']), re.M)
        if RE.search(text):
            out = []
        for r in RE.finditer(text):
            maj +=1
            format_output(out, r.groupdict())
    return maj, out


def fix_output(processed):
    result = {}
    training = []
    if processed:
        for e in processed:
            if e['education'] == u'初中及以下':
                training.append(e)
        if training:
            result['training_history'] = sorted(training, key=lambda x:x['date_from'], reverse=True)
            for e in training:
                processed.remove(e)
        result['education_history'] = processed
    return result

def fix_liepin(d):
    u"""
        >>> assert fix_liepin(u'教育经历\\n----------\\n\\n----------\\n北京科技大学  2008/09–2012/07   计算机科学与技术   本科\\n----------')
        >>> assert u'网络' in fix_liepin(u'教育经历\\n   哈尔滨技师学院 （2007.09 - 2011.07）\\n'
        ...     u'专业：网络工程                         学历：大专   是否统招：否')['education_history'][0]['major']
        >>> assert u'齐齐' in fix_liepin(u'教育经历\\n   2002/9-2006/7 齐齐哈尔大学 工商管理 本科')['education_history'][0]['school']
    """
    maj = 0
    processed = []
    summary = {}
    for RE in [ED, AED]:
        res = RE.search(d)
        if res:
            remainer = d.replace(res.group('edu'), '')
            if SUMMARYMAJOR.search(remainer) and SUMMARYSCHOOL.search(remainer):
                summary['major'] = SUMMARYMAJOR.search(remainer).group('major')
                summary['school'] = SUMMARYSCHOOL.search(remainer).group('school')
            for r in SPSOLMA.finditer(res.group('edu')):
                if r.group('major'):
                    maj +=1
                    format_output(processed, r.groupdict(), summary)
            else:
                if maj:
                    return fix_output(processed)
            for r in RVSPSOLMA.finditer(res.group('edu')):
                maj +=1
                format_output(processed, r.groupdict(), summary)
            else:
                if maj:
                    return fix_output(processed)
            for r in HDCTLMA.finditer(res.group('edu')):
                maj +=1
                format_output(processed, r.groupdict(), summary)
            else:
                if maj:
                    return fix_output(processed)
            break
    return fix_output(processed)

def fix_zhilian(d):
    u"""
        >>> assert u'大学' in fix_zhilian(u'教育经历\\n  2006年9月  --  2010年6月\\n科技大学\\n专业名称：\\n电子信息工程\\n'
        ...         u'学历/学位：\\n本科\\n全日制统招：是')['education_history'][0]['school']
        >>> assert u'测绘' in fix_zhilian(u'教育\\n信息技术\\n培训\\n教育培训\\n展开全部\\n工作经验\\n教育背景\\n2007年9月-2011年7月\\n'
        ...         u'理工大学\\n专业名称：\\n测绘工程\\n学历/学位：\\n本科\\n全日制统招：是')['education_history'][0]['major']
    """
    maj = 0
    processed = []
    summary = {}
    ZHILIANED = re.compile(ED.pattern.replace(u'|((?(br)/?)[及与]?培训)', ''), re.DOTALL+re.M)
    ZHILIANAED = re.compile(AED.pattern.replace(u'|((?(br)/?)[及与]?培训)', ''), re.DOTALL+re.M)
    for RE in [ZHILIANED, ZHILIANAED]:
        res = RE.search(d)
        if res:
            remainer = d.replace(res.group('edu'), '')
            if SUMMARYMAJOR.search(remainer) and SUMMARYSCHOOL.search(remainer):
                summary['major'] = SUMMARYMAJOR.search(remainer).group('major')
                summary['school'] = SUMMARYSCHOOL.search(remainer).group('school')
            for r in RVHDCTLMA.finditer(res.group('edu')):
                maj +=1
                format_output(processed, r.groupdict(), summary)
            break
    return fix_output(processed)

def fix_jingying(d):
    u"""
        >>> assert u'云南' in fix_jingying(u'教育经历\\n   2010/9 -- 2012/12   云南师范大学   工商管理    硕士')['education_history'][0]['school']
        >>> assert 2 == len(fix_jingying(u'教育经历\\n2000/9 -- 2003/6   湖南省衡阳师范学院           教育学   大专\\n'
        ...     u'1997/9 -- 2000/7   湖南省衡阳市衡南县第二中学   理科     高中')['education_history'])
        >>> assert u'生物' in fix_jingying(u'教育经历\\n2009/9 -- 2013/6  北京联合大学生物化学工程学院   生物工程   本科\\n'
        ...     u'本科课程涉及生物化学')['education_history'][0]['major']
        >>> assert not u'科学' in fix_jingying(u'教育经历\\n2000/7 -- 2003/7   江苏大学   计算机科学   本科\\n学士学位')['education_history'][0]['major']   #FIXME
        >>> assert not u'法学' in fix_jingying(u'教育经历\\n2010/3-- 2013/3   苏州大学   法学   硕士\\n在职法律硕士')['education_history'][0]['major']  #FIXME
        >>> assert u'药学' in fix_jingying(u'教育经历\\n ----------------------------------------------------------- ------------ ------ ------\\n'
        ...     u'2006/9-- 2009/7                                             北京中医药大学   药学   大专')['education_history'][0]['major']
        >>> assert u'无' in fix_jingying(u'教育经历\\n\\n2001/12 -- 2006/12   陕西中学   边防检查   大专\\n'
        ...     u'1998/9 -- 2001/7     商洛中学   无         高中')['education_history'][1]['major']
        >>> assert u'江南' in fix_jingying(u'教育经历\\n----------------- ---------------------- ------------------ ------\\n'
        ...     u'2004/9-- 2008/7   黑龙江省江南职责学院                      本科')['education_history'][0]['school']
    """
    maj = 0
    processed = []
    summary = {}
    MA = re.compile(u'^('+SPSOLHDR+u')?'+SPSOLMA.pattern+'$', re.M)
    for RE in [ED, AED]:
        res = RE.search(d)
        if res:
            remainer = d.replace(res.group('edu'), '')
            if SUMMARYMAJOR.search(remainer) and SUMMARYSCHOOL.search(remainer):
                summary['major'] = SUMMARYMAJOR.search(remainer).group('major')
                summary['school'] = SUMMARYSCHOOL.search(remainer).group('school')
            col1 = 999
            for r in MA.finditer(res.group('edu')):
                if r.group('col1'):
                    col1 = len(r.group('col1'))
                maj +=1
                out = r.groupdict().copy()
                if len(r.group('period')) > col1+1:
                    out['major'] = r.groupdict()['school']
                    out['school'] = ''
                format_output(processed, out)
            else:
                if maj:
                    break
    return fix_output(processed)

def fix_yingcai(d):
    u"""
        >>> assert fix_yingcai(u'教育经历\\n燕山大学\\n2000.09 - 2004.07\\n本科\\n计算机科学与技术')['education_history']
        >>> assert fix_yingcai(u'教育经历\\n武汉生物工程学院\\n2016.07\\n本科\\n土木工程') # Incomplete period
        >>> assert fix_yingcai(u'本科\\n教育经历\\n 郑州科技学院\\n 1900.01 - 2016.07\\n 计算机科学与技术')
        >>> assert not fix_yingcai(u'教育经历\\n第一中学\\n1980.09 - 1983.07\\n高中\\n在校经历：我在')['education_history'][0]['major']
        >>> #assert u'技术' in fix_yingcai(u'教育经历\\n郑州工业 应用技术学院\\n2006.09 - 2009.07\\n大专\\n计算机科学与技术')['education_history'][0]['school']
    """
    maj = 0
    processed = []
    summary = {}
    for RE in [ED, AED]:
        res = RE.search(d)
        if res:
            for r in YIED.finditer(res.group('edu')):
                maj +=1
                format_output(processed, r.groupdict())
            break
    if not maj:
        r = SINGLEYIED.search(d)
        edu = re.compile(u'^'+ASP+u'*'+EDUCATION+u'$', re.M).search(d)
        try:
            education = edu.group('education')
        except AttributeError:
            education = ''
        if r:
            res = r.groupdict()
            res['education'] = education
            maj +=1
            format_output(processed, res)
        else:
            summary['education'] = education
    return fix_output(processed)

def fix(d):
    u"""
        >>> assert ED.search(u'教育背景              Education\\n\\n素质技能')
        >>> assert ED.search(u'教育背景              Education\\n\\n工作项目经历')
        >>> assert u'大' in name(fix(u'''【教育/培训】1991-09\~1995-07  师范大学 汉语言文学 本科\\n【工作经验】''')['education_history'][0])
        >>> assert fix(u'教育经历\\n2011/09 - 2013/12   广东科技学院 电子信息科学与技术 大专\\n语言能力')
        >>> assert fix(u'教育经历\\n\\n2008.09 - 2012.07  中南民族大学  网络工程  本科')
        >>> assert fix(u'学 历： 本科\\n 专 业： 医学影像\\n学 校： 医科大学\\n教育经历\\n\\n2012 /9--至今  医科大学  医学影像')
        >>> assert fix(u'''学　历：   本科\\n专　业：   会计学\\n学　校：   湖南大学\\n教育经历\\n1997 /9--2001 /10 湖南大学 会计学''')
        >>> assert fix(u'---\\n新疆大学 （ 2004.09-2008.06 ）\\n专业：计算机科学  学历：本科   是否统招：是\\n---')
        >>> assert fix(u'---\\nNortheastern University （ 2012.09-至今 ）\\n 专业：Software Engineering   学历：硕士   是否统招：是\\n---')
        >>> assert fix(u'''教育背景\\n\\n2004.9-2007.7\\n [测试计量技术及仪器](http://www.example.com)\\n 沈阳工业大学 硕士''')
        >>> assert fix(u'教育背景\\n1999年9月  --  2004年7月三峡大学\\n专业名称：影像医学\\n学历/学位：本科 全日制统招：是')
        >>> assert fix(u'教育背景及培训：\\n\\n   1996.09-2000.07  西南学院 (西南科技大学)\\n 自动化  本科。')
        >>> assert fix(u'学历： 本科专业： 公共事业管理学校： 湖南师范大学\\n\\n教育经历 \\n\\n'
        ...         u'2011-09 ～ 2015-06 | 湖南师范大学 | 公共事业管理 | 本科 \\n\\n语言能力')
        >>> assert not fix(u'学　历：   硕士\\n专　业：   电子信息工程\\n学校： 谢菲尔德大学(University of Sheffield)\\n'
        ...         u'教育经历\\n2011 /8--2012 /10 谢菲尔德大学(University of Sheffield)   电子信息工程\\n所获奖项')    #FIXME
        >>> assert len(fix(u'教育背景\\n2001.09-2004.06        广东省广宁中学                           高中\\n\\n'
        ...         u'2004.09-2008.07        华南理工大学           自动化            本科')['education_history']) == 2
        >>> assert fix(u'教 育 经 历2006/9--2010/7        湛江师范学院   计算机科学与技术（软件工程）    本科    在校获奖经历：')
        >>> assert fix(u'·教育背景\\n2011.9-2014.7   航天大学    软件工程 （移动云计算专业）  \\n 硕士学位')
        >>> assert fix(u'''----\\n时 间 学 校  专 业 学 历 证 书\\n2006-09\~2009-07   专科学校    旅游英语    大专\\n----''')
        >>> assert fix(u'毕业院校：理工大学 时间:2009.09 — 2013.06\\n学历：本科 专业：生物医学工程（医疗器械方向）')
        >>> assert fix(u'''教育背景: 硕士 (管理信息系统,管理科学), 学士 (土木工程)\\n 工作经验\\n 教育经历'''
        ...         u'''---\\n2004/9 -- 2006/5   亚利桑那大学   计算机信息管理   硕士\\n----''')
        >>> assert len(fix(u'''教育经历\\n 时    间  学 校 名 称  专    业  学历/学位 是否统招\\n'''
        ...         u'''2010年9月至 2012年 7月  中南大学  工商管理   研究生/硕士学位  是\\n'''
        ...         u'''1993年9月至1997年  7月  长春税务学院   货币银行学  本科  是\\n培训经历''')['education_history']) == 2
        >>> assert len(fix(u'''教育背景\\n时间段  学校  专业  学历\\n2001.09-2004.06  广东省广宁中学            高中'''
        ...         u'''2004.09-2008.07        华南理工大学           自动化            本科\\n工作经历''')['education_history']) == 2
        >>> assert fix(u'2012/09 --2014/06        \\n大连理工大学   | 物流管理 | 硕士')
        >>> assert fix(u'2010/09 --2013/05\\n航天大学 | 金融信息化 | 硕士（在职研究生）')
        >>> assert fix(u'        教育经历\\n\\n        2004/9 -- 2007/7     东南大学    机械电子工程/机电一体化   本科')
        >>> assert not fix(u'教育:\\n\\n1982-1986        哈尔滨工业大学计算机科学，本科') #FIXME
        >>> assert not fix(u'学习培训经历：\\n\\n2003年9月-2007年7月　    湖南城市学院　　\\n电子信息工程专业　　 本科')  #FIXME
        >>> assert not fix(u'----\\n1995.9—1999.7   长春光学精密机械学院       检测技术及仪器仪表   本科\\n----')   #FIXME
        >>> assert fix(u'**教育经历 **\\n\\n2004.09 - 2007.03  北京航空航天大学  测试计量技术及仪器  硕士')
        >>> assert fix(u'Education\\n\\n西安交通大学\\n\\n硕士, 临床医学\\n\\n2005 – 2012')
        >>> assert 4 == len(fix(u'Education\\n\\n西安交通大学\\n\\n硕士, [临床医学](http://www.linkedin.com/vsearch/p?trk=prof-edu-field_of_study)'
        ...         u'\\n\\n2005 – 2012')['education_history'][0]['major'])
        >>> assert 'Business' in name(fix(u'Education\\n\\n[Indiana University - Kelley School of\\nBusiness]\\n\\n'
        ...         u'MBA, [MBA]\\n\\n2005 – 2007')['education_history'][0])
        >>> assert 2 == len(fix(u'### **教育经历**\\n\\n2013.09 - 2016.06  中国科学院武汉物理与数学研究所  MRI仪器技术  硕士\\\\\\n'
        ...         u'2009.09 - 2013.06  华中科技大学  生物医学工程  本科\\n### **语言能力**')['education_history'])

    """
    maj = 0
    if is_jycv(d):
        return fix_jingying(d)
    elif is_lpcv(d) or is_nlpcv(d):
        return fix_liepin(d)
    elif is_zlcv(d):
        return fix_zhilian(d)
    elif is_yccv(d):
        return fix_yingcai(d)

    processed = []
    summary = {}
    res = ED.search(d)
    if res and re.compile(TABHDRMAJ, re.DOTALL+re.M).search(res.group('edu')):
        out = []
        for r in SPSOLMA.finditer(re.compile(TABHDRMAJ, re.DOTALL+re.M).search(res.group('edu')).group('edu')):
            if r.group('major'):
                maj +=1
                format_output(out, r.groupdict())
            elif summary:
                maj +=1
                format_output(out, r.groupdict(), summary)
            else:
                format_output(out, r.groupdict(), summary={'major': ''})
        processed = out
    if not maj and res:
        out = []
        for match in ED.finditer(d):
            remainer = d.replace(match.group('edu'), '')
            if SUMMARYMAJOR.search(remainer) and SUMMARYSCHOOL.search(remainer):
                summary['major'] = SUMMARYMAJOR.search(remainer).group('major')
                summary['school'] = SUMMARYSCHOOL.search(remainer).group('school')
            maj, out = education_xp(match.group('edu'), summary)
            if maj:
                processed = out
                break
    if maj:
        return fix_output(processed)
    if AED.search(d):
        remainer = AED.sub('', d)
        if SUMMARYMAJOR.search(remainer) and SUMMARYSCHOOL.search(remainer):
            summary['major'] = SUMMARYMAJOR.search(remainer).group('major')
            summary['school'] = SUMMARYSCHOOL.search(remainer).group('school')
        res = AED.search(d)
        maj, out = education_xp(res.group('edu'), summary)
        if maj or len(out):
            processed = out
    elif TED.search(d):
        maj = 0
        out = []
        for r in TED.finditer(d):
            maj +=1
            format_output(out, r.groupdict())
        processed = out
    elif THED.search(d):
        maj = 0
        out = []
        for r in UCSOLMA.finditer(THED.search(d).group('edu')):
            maj +=1
            format_output(out, r.groupdict())
        processed = out
    elif HDVRTMA.search(d):
        maj = 0
        out = []
        for r in HDVRTMA.finditer(d):
            maj +=1
            format_output(out, r.groupdict())
        processed = out
    elif SENSEMA.search(d):
        maj = 0
        out = []
        for r in SENSEMA.finditer(d):
            maj +=1
            format_output(out, r.groupdict())
        processed = out
    elif EED.search(d):
        maj = 0
        out = []
        res = EED.search(d).group('edu')
        for r in EMA.finditer(res):
            maj +=1
            format_output(out, r.groupdict())
        processed = out
    return fix_output(processed)
