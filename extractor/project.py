# -*- coding: utf-8 -*-
import re
try:
    import regex
except ImportError:
    setattr(re, 'ASCII', 0)
    regex = re


from extractor.utils_parsing import *


PRTITLE = TITLE('project')
PJ = re.compile(SECTION('project')+u'(?=^'+PREFIX+u'*'+REMAINING_SECTIONS('project') +u')', re.DOTALL+re.M)
APJ = re.compile(ur'^'+SECTION('project'), re.DOTALL+re.M)

PPJ = re.compile(ur'^'+PREFIX+u'*'+ PRTITLE +POASP+u'*\n+'+BORDERTOP('pjborder') +u'?(?P<proj>.*?)^'+BORDERBOTTOM('pjborder')+u'^'+PREFIX+u'*(?='+ UNIBRALEFT +u'?(教'+ASP+u'?育'+ASP+u'?((经'+ASP+u'?[历验])|背景|培训))'+ UNIBRARIGHT +u'?)', re.DOTALL+re.M)
YPJ = re.compile(ur'^'+PREFIX+u'*工作职责和业绩[:：]'+ POASP+u'*\\\\\n(?P<proj>.*?)\n(?:\n|$)', re.DOTALL+re.M)

PR = re.compile(heading(PREFIX+u'*'+PERIOD+u'\**(('+ASP+u'?[:：'+SP+u']'+ASP+u'*)|([:：]?'+ASP+u'*))\**(?P<project>'+PROJECT+u')\**'+POASP+u'*$'), re.M)
# Use POESP to avoid matching LPR in DEFAULT_ITEM's __NORECURSIVE__
LPR = re.compile(heading(PREFIX+u'*'+PERIOD+u'\**'+POASP+u'+\**(?P<project>'+PROJECT+u')\**'+POESP+u'*$'), re.M)
JPR = re.compile(heading(PREFIX+u'*'+PERIOD+u'((?P<empty_project>'+POASP+u'*[:：])|\**(('+POASP+u'?[:：'+SP+u']'+POASP+u'*)|([:：]?'+POASP+u'*))\**(?P<project>'+PROJECT+u')\**'+POASP+u'*)$'), re.M)
IPR = re.compile(heading(PREFIX+u'*\**(?P<project>'+PROJECT+u')\**'+ASP+u'*'+PERIOD+u'(?:\\\\)?$'), re.M)

# Avoid conflict in group names when combining *CO and *PO
APERIOD = PERIOD.replace('from', 'afrom').replace('to', 'ato')
ADURATION = DURATION.replace('duration', 'aduration')

CHAR = u'[^:：\n]'

__PJDESCRIPTION__ = u'项目(?:描述|简介|内容)[:：]'

LP_EMBEDDED_TITLE = lambda STR: u'(?:(?:项目|责任)(?:职责|简介|描述)：'+POASP+u'*)*'+ STR
project_items = {
    'duration' : ((LP_EMBEDDED_TITLE(u'项目周期[:：]'), ADURATION+u'(?:[。;；]|\\\\)?$'), ),
    'customer' : ((LP_EMBEDDED_TITLE(u'客户情况[:：]'), DEFAULT_ITEM), ),
    'position': ((LP_EMBEDDED_TITLE(u'(?:项目职[务位]|担任角色)[:：]'), DEFAULT_ITEM), ),
    'company': ((LP_EMBEDDED_TITLE(u'(?:所[在属]公司)[:：]'), DEFAULT_ITEM), ),
    #'?????': ((u'(?:项目名称[:：]', DEFAULT_ITEM), ),
    #'?????': ((u'(?:项目贡献[:：]', DEFAULT_ITEM), ),
    #'howto': ((u'(?:项目执行[:：]', DEFAULT_ITEM), ),
    #'objective': ((u'(?:项目目标)[:：]', DEFAULT_ITEM), ),
    'achievement': ((LP_EMBEDDED_TITLE(u'(?:研究业绩|项目业绩|项目成果|咨询服务)[:：]'), DEFAULT_ITEM), ),
    'software': ((LP_EMBEDDED_TITLE(u'(?:软件环境)[:：]'), DEFAULT_ITEM), ),
    'hardware': ((LP_EMBEDDED_TITLE(u'(?:硬件环境)[:：]'), DEFAULT_ITEM), ),
    'language': ((LP_EMBEDDED_TITLE(u'(?:开发语言)[:：]'), DEFAULT_ITEM), ),
    'tools': ((LP_EMBEDDED_TITLE(u'(?:开发工具)[:：]'), DEFAULT_ITEM), ),
    'team': ((LP_EMBEDDED_TITLE(u'(?:项目团队)[:：]'), DEFAULT_ITEM), ),
    'budget' : ((LP_EMBEDDED_TITLE(u'项目投资[:：]'), DEFAULT_ITEM), ),
    'background': ((LP_EMBEDDED_TITLE(u'(?:(?:项目背景|背景描述|项目范围))[:：]'), DEFAULT_ITEM), ),
    'responsibility' : ((LP_EMBEDDED_TITLE(u'(?:责任描述|主要承担工作有)[:：]'), DEFAULT_ITEM), ),
    'resp_or_pos' : ((LP_EMBEDDED_TITLE(u'项目职责[:：]'), DEFAULT_ITEM), ),
    'description' : ((LP_EMBEDDED_TITLE(__PJDESCRIPTION__), DEFAULT_ITEM), ),
    }
#'description': ((u'(?P<desclabel>项目(?:描述|简介|内容))[:：]?', DEFAULT_ITEM), ),
key_items = project_items.copy()
project_items['achievement'] = ((u'(?<=[:：\s^])'+LP_EMBEDDED_TITLE(u'(?:研究业绩|项目业绩|项目成果|咨询服务)[:：]'), MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )
project_items['responsibility'] = ((u'(?<=[:：\s^])'+LP_EMBEDDED_TITLE(u'(?:责任描述|主要承担工作有)[:：]'), MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )
project_items['resp_or_pos'] = ((u'(?<=[:：\s^])'+LP_EMBEDDED_TITLE(u'项目职责[:：](?:\n参与[:：])?'), EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM), )
project_items['description'] = ((u'(?<=[:：\s^])'+LP_EMBEDDED_TITLE(u'(?P<desclabel>项目(?:描述|简介|内容))[:：]'), MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )

SET_DEFAULT_ZL = SET_ALL_DEFAULT(u'(?:[;；。]?)\n+')(u'')(u'(?=$|\|[^\\\\])')(key_items)
# TODO: replacement candidate for SET_DEFAULT_NS?
SET_ALL_ITEMS_YC = lambda DEFAULT: lambda DETAILS: lambda LABEL_SEPARATOR: DEFAULT(SPACESEPRTED(map(label_separated(LABEL_SEPARATOR), DETAILS.items())))
SET_DEFAULT_YC = SET_ALL_DEFAULT(ASP+u'+')(u'?')(u'(?=\s+(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\|[^\\\\]|$)')(key_items)
# YC project description do not have prefix as position description
SET_DEFAULT_YC_DESC = SET_ALL_DEFAULT(u'(?:[;；。]?)\n+')(u'')(u'(?=$|\|[^\\\\])')(key_items)
SET_DEFAULT = SET_ALL_DEFAULT(u'(?:[;；]|\\\\)\n')(u'')(u'(?=(?:\\\\)?$|\|)')(key_items)
#SET_DEFAULT = SET_ALL_DEFAULT(u'(?:(?:[;；]|\\\\)\n|(?<!\\\\)\n+(?=(?!'+POASP+u'*'+ANONPERIOD+u')))')(u'')(u'(?=(?:\\\\)?$|\|)')(key_items)
SET_DEFAULT_LP = SET_ALL_DEFAULT(u'\n')(u'')(u'')(key_items)

PROJECT_DETAILS = lambda DETAILS: lambda RE:BORDERTOP('dettab')+u'?\n*'+POASP+u'*\**'+RE.pattern+u'\n*'+DETAILS.replace('__NORECURSIVE__', RE.pattern)+u'\n*'+BORDERBOTTOM('dettab').replace('__NORECURSIVE__', RE.pattern)

project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT)(project_items)(newline_separated)+u'+')
empty_project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT)(project_items)(newline_separated)+u'*')

jy_project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT)(project_items)(newline_separated).replace('__NORECURSIVE__', '__NO_DELETE__')+u'+')
empty_jy_project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT)(project_items)(newline_separated).replace('__NORECURSIVE__', '__NO_DELETE__')+u'*')

project_decription_items = {}
# Only used in JY: anything not preceded by item label until the next blank line (accept escaped newlines)
project_decription_items['description'] = ((u'(?:'+__PJDESCRIPTION__+u')', u'(?=(?!'+BORDER+u'))(?=(?!__NORECURSIVE__))(?:(?:\\\\\n)(?P<followindent> {10,})\n(?(followindent))(?=(?!__NORECURSIVE__))|'+POASP+u'+(?=(?!__NORECURSIVE__))(?=\S)|\S)+'), )

DEFAULT_ITEM_SP = u'(?:(?:(?:[;；]|\\\\)\n+(?!(?:'+POASP+u'*'+ANONPERIOD+u'|'+POASP+u'*(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\s+(?=(?!(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\S)*?)(?=$|\|[^\\\\])'
SET_DEFAULT_SP = lambda x: x.replace(DEFAULT_ITEM, DEFAULT_ITEM_SP)
DEFAULT_ITEM_NS = u'(?:(?:(?:[;；]|\\\\)\n+(?!(?:'+POASP+u'*'+ANONPERIOD+u'|'+POASP+u'*(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\s+(?=(?!(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\-{3,}))|\S)+?)(?=$|\s*(?:'+RE_ANY(PRJ_ITEM_KEYS(key_items)).replace(u'[:：]?', u'[:：]')+u')|\|[^\\\\])'
SET_DEFAULT_NS = lambda x: x.replace(DEFAULT_ITEM, DEFAULT_ITEM_NS)

empty_project_details_spaceonly = lambda RE: u'\n*(?:\**'+SET_ALL_ITEMS_SPACE(SET_DEFAULT_SP)(project_items)(newline_separated)+u'\n*)*'
empty_project_description_details_spaceonly = lambda RE:u'\n*(?:'+SET_ALL_ITEMS(lambda x:x)(project_decription_items)(space_separated).replace('__NORECURSIVE__', RE.pattern)+u'\n*)?'+empty_project_details_spaceonly(RE)

lp_project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_LP)(project_items)(newline_separated)+u'+')
empty_lp_project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_LP)(project_items)(newline_separated)+u'*')

zl_project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_ZL)(project_items)(newline_separated)+u'+')
empty_zl_project_details = PROJECT_DETAILS(SET_ALL_ITEMS(SET_DEFAULT_ZL)(project_items)(newline_separated)+u'*')

yingcai_project_items = project_items.copy()
yingcai_project_items['responsibility'] = ((u'(?<=[:：\s^])(?:(?:责任描述|主要承担工作有)[:：])', MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+u'(?:'+SET_DEFAULT_YC_DESC(DEFAULT_ITEM)+u'|'+DEFAULT_ITEM+u')')), )
yingcai_project_items['achievement'] = ((LP_EMBEDDED_TITLE(u'(?:研究业绩|项目业绩|项目成果|咨询服务)[:：]'), EXCLUDE_ITEM_KEYS(key_items)+u'(?:'+SET_DEFAULT_YC_DESC(DEFAULT_ITEM)+u'|'+DEFAULT_ITEM+u')'), )
yingcai_project_items['resp_or_pos'] = ((u'(?<=[:：\s^])项目职责[:：](?:\n参与[:：])?', EXCLUDE_ITEM_KEYS(key_items)+u'(?:'+SET_DEFAULT_YC_DESC(DEFAULT_ITEM)+u'|'+DEFAULT_ITEM+u')'), )
yingcai_project_items['description'] = ((u'(?<=[:：\s^])(?P<desclabel>项目(?:描述|简介|内容))[:：]', MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+u'(?:'+SET_DEFAULT_YC_DESC(DEFAULT_ITEM)+u'|'+DEFAULT_ITEM+u')')), )
yingcai_project_description = {}
yingcai_project_description['description'] = ((u'(?<=[:：\s^])(?:(?P<desclabel>项目(?:描述|简介|内容))[:：])?', MATCH_SPACE_OR(EXCLUDE_ITEM_KEYS(key_items)+DEFAULT_ITEM)), )

yc_project_details = lambda RE:RE.pattern+BORDERTOP('detborder')+u'?(?:\n*)'+POASP+u'*'+SET_ALL_ITEMS(SET_DEFAULT_YC_DESC)(yingcai_project_description)(newline_separated).replace('__NORECURSIVE__', RE.pattern)+u'?\**'+SET_ALL_ITEMS_YC(SET_DEFAULT_YC)(yingcai_project_items)(newline_separated).replace('__NORECURSIVE__', RE.pattern)+u'*\**(?(detborder)\n*(?P<intro>[^-]{3}.*\n)?'+BORDERBOTTOM('detborder')+u')'


def output_cleanup(groupdict):
    for item in ['project']:
        try:
            if u'[' in groupdict[item] and groupdict[item][0] == u'[':
                end = groupdict[item].index(u']')
                groupdict[item] = groupdict[item][1:end]
        except KeyError:
            continue
        except TypeError:
            continue

def project_output(output, groupdict, begin='', end='', company=''):
    if 'project' in groupdict and groupdict['project']:
        result = {}
        output_cleanup(groupdict)
        if 'from' in groupdict and groupdict['from']:
            result['date_from'] = fix_date(groupdict['from'])
            result['date_to'] = fix_date(groupdict['to'])
        else:
            result['date_from'] = fix_date(groupdict['afrom'])
            result['date_to'] = fix_date(groupdict['ato'])
        result['name'] = fix_name(groupdict['project'])
        for key in project_items:
            if key == 'resp_or_pos':
                continue
            if key == 'duration':
                if 'aduration' in groupdict and groupdict['aduration']:
                    result['duration'] = fix_duration(groupdict['aduration'])
                    continue
            if key in groupdict and groupdict[key]:
                # FIXME result[key] = groupdict[key]
                result[key] = fix_name(groupdict[key])
        if 'resp_or_pos' in groupdict and groupdict['resp_or_pos']:
            if not 'responsibility' in result:
                result['responsibility'] = fix_name(groupdict['resp_or_pos'])
            elif not 'position' in result:
                result['position'] = fix_name(groupdict['resp_or_pos'])
        if 'duration' not in result or not result['duration']:
            result['duration'] = compute_duration(result['date_from'], result['date_to'])
        output['project'].append(result)

name = lambda project: project['name']
description = lambda project: project['description']
responsibility = lambda project: project['responsibility']
budget = lambda project: project['budget']
duration = lambda project: project['duration']
position = lambda project: project['position']
projects = lambda output: len(output[1]['project'])
project_1 = lambda x: x[1]['project'][0]
project_2 = lambda x: x[1]['project'][1]


def project_xp(RE, text):
    u"""
    General project matching
        >>> assert 2 == projects(project_xp(PR, u'2011年7月  --  至今\\n江苏维福特科技发展有限公司\\n项目职责：\\n股权收购，增资扩股。\\n'
        ...         u'2004年9月  --  2009年8月\\n案例\\n项目描述：\\n代理原告，基本胜诉。\\n项目职责：\\n律师'))
        >>> assert not 'project' in  name(project_1(project_xp(PR, u'2003年7月  --  2007年3月\\n'
        ...         u'Artermis / Athena (Notebook computer\\nproject)\\n项目描述：\\n客户为日本SHARP和NEC')))   # FIXME
        >>> assert not 'THERMOS' in name(project_1(project_xp(PR, u'2007年4月  --  2007年12月\\n'
        ...         u'THERMOS膳魔师昆山厂QCC现场改善（2007/04–2007/11\\n项目职位：\\n咨询师'))) # FIXME
        >>> assert u'6个月' == duration(project_1(project_xp(PR, u'2008年3月  --  2008年6月\\n人力资源管理咨询项目\\n项目描述：\\n项目周期：6个月')))
        >>> assert u'需求提炼' in description(project_1(project_xp(PR, u'2006年11月  --  2007年1月\\n供应商管理方案设计咨询项目\\n项目描述：\\n'
        ...         u'大型公共交通设施企业的管控模式设计；\\n大型公共交通设施企业供应商流程优化暨信息化需求提炼\\n项目职责：\\n项目成员')))
        >>> assert u'\\n' not in description(project_1(project_xp(PR, u'2008年3月  --  2008年6月\\n大型三甲医院人力资源管理咨询项目\\n'
        ...         u'项目描述：\\n项目内容：医院组织结构调整、全员人员的定岗定编、医院的薪酬体系建立；\\n项目职责：\\n项目成员')))
        >>> assert u'开发' in description(project_1(project_xp(PR, u'2015/2 -- 2015/11 ： GE Energy 油气分配器开发项目\\n\\n'
        ...         u'   项目描述：       项目职务： 工程经理\\\\\\n项目描述： 开发新型号油气分配器')))
        >>> assert not u'专利' in description(project_1(project_xp(PR, u'2008/8-- 2010/4： 贝类毒素细胞检测技术的建立\\n项目描述：建立贝类毒素\\n'
        ...         u'责任描述：      细胞培养、ELISA检测和小鼠生物法检测。\\\\n 研究成果获发明专利'))) # FIXME
        >>> assert u'ITEQ' in description(project_1(project_xp(PR, u'2006年6月  --  2006年12月\\n喷墨打印机打印头不良递减\\n'
        ...         u'项目描述：\\n■2006年在ITEQ（日本培训公司）')))
        >>> assert u':' not in responsibility(project_1(project_xp(PR, u'2010年10月  --  2011年10月\\n'
        ...         u'福耀集团EHR(电子化人力资源管理)项目\\n项目职责：\\n参与:规划、实施、监控、调试')))
        >>> assert u'宁夏电力' in responsibility(project_1(project_xp(PR, u'2010年8月  --  2010年11月\\n宁夏电力ERP全覆盖推广项目\\n'
        ...         u'项目描述：\\n责任描述：负责宁夏电力一家直属单位。\\n项目职责：\\nPS模块实施顾问')))
        >>> assert u'用户培训' in responsibility(project_1(project_xp(PR, u'2010年12月  --  2011年4月\\n宁夏电力高级应用项目二期\\n'
        ...         u'项目职责：\\n主要承担工作有：\\n1.国网要求报表表样制作；\\n8.用户培训。')))
        >>> assert u'SAP使用' in responsibility(project_1(project_xp(PR, u'   2011/3-- 2011/9： SAP内部实施项目\\n'
        ...         u'    项目描述：      建立SAP系统。\\n 责任描述：  1\\\\. 参与制定SAP项目实施计划（批准号：P）；\\\\\\n 5. SAP使用培训。')))
        >>> assert responsibility(project_1(project_xp(PR, u'  2015/10 -- 2016/1 ： 浙江长龙航空存储双活项目\\n'
        ...         u'项目描述：  项目简介：NetApp 四控制器双活存储系统。\\n责任描述：  责任描述：负责netapp存储系统上线工作。'))) # data: 1509472680
        >>> assert u'350' in budget(project_1(project_xp(PR, u'2012/1 -- 2012/12 ： ERP项目\\n项目描述：   ERP系统建设\\\\\\n'
        ...         u'   项目范围：\\\\\\n1.实施计划、物资、资产、投产四个模块\\\\\\n项目投资：超过350万')))
    """
    out = {'project': []}
    if not len(out['project']):
        if RE.search(text):
            out = {'project': []}
            if not len(out['project']):
                MA = regex.compile(project_details(RE), re.M)
                if not MA.search(text):
                    MA = regex.compile(empty_project_details(RE), re.M)
                for r in MA.finditer(text):
                    project_output(out, r.groupdict())
    return len(out['project']), out


def project_xp_zhilian(RE, text):
    u"""
    """
    out = {'project': []}
    if not len(out['project']):
        if RE.search(text):
            out = {'project': []}
            if not len(out['project']):
                MA = regex.compile(zl_project_details(RE), re.M)
                if not MA.search(text):
                    MA = regex.compile(empty_zl_project_details(RE), re.M)
                for r in MA.finditer(text):
                    project_output(out, r.groupdict())
    return len(out['project']), out

def project_description_output(out, groupdict):
    d = groupdict.copy()
    if d['description']:
        description = d.pop('description')

        pj_items = project_items.copy()
        pj_items.pop('resp_or_pos')
        pj_items.pop('description')
        for key in pj_items.copy():
            resp_items = {}
            resp_items[key] = pj_items[key]
            MARESP = regex.compile(SET_ALL_ITEMS_NOSPACE(SET_DEFAULT_NS)(resp_items)(space_separated).replace(u'[:：]?', u'[:：]'), re.M)
            if len(MARESP.findall(description)) > 1:
                pj_items.pop(key)

        MAPJ = regex.compile(SET_ALL_ITEMS_NOSPACE(SET_DEFAULT_NS)(pj_items)(space_separated).replace(u'[:：]?', u'[:：]'), re.M)

        desc = description
        for res in MAPJ.finditer(description):
            r = {}
            for key in res.groupdict():
                if res.groupdict()[key]:
                    r[key] = res.groupdict()[key]
            d.update(r)
            # Must avoid replacing all ASP/POASP is spurious match
            if set(r).intersection(project_items):
                desc = desc.replace(res.group(), '')
        d['description'] = desc
    project_output(out, d)

def project_xp_jingying(RE, text):
    u"""
    """
    out = {'project': []}
    if not len(out['project']):
        if RE.search(text):
            out = {'project': []}
            if not len(out['project']):
                MA = regex.compile(RE.pattern+empty_project_description_details_spaceonly(RE), re.M)
                for r in MA.finditer(text):
                    d = r.groupdict()
                    if d['empty_project']:
                        d['project'] = '\*\*\*'
                    project_description_output(out, d)
            if not len(out['project']):
                MA = regex.compile(jy_project_details(RE), re.M)
                if not MA.search(text):
                    MA = regex.compile(empty_jy_project_details(RE), re.M)
                for r in MA.finditer(text):
                    d = r.groupdict().copy()
                    if d['empty_project']:
                        d['project'] = '\*\*\*'
                    project_output(out, d)
    return len(out['project']), out

def project_xp_liepin(RE, text):
    u"""
    """
    out = {'project': []}
    if not len(out['project']):
        if RE.search(text):
            out = {'project': []}
            if not len(out['project']):
                MA = regex.compile(lp_project_details(RE), re.M)
                if not MA.search(text):
                    MA = regex.compile(empty_lp_project_details(RE), re.M)
                for r in MA.finditer(text):
                    project_output(out, r.groupdict())
    return len(out['project']), out

def project_xp_yingcai(RE, text):
    u"""
    """
    out = {'project': []}
    if not len(out['project']):
        if RE.search(text):
            out = {'project': []}
            if not len(out['project']):
                MA = regex.compile(yc_project_details(RE), re.M)
                for r in MA.finditer(text):
                    project_output(out, r.groupdict())
    return len(out['project']), out


def fix_output(processed, as_date=None):
    result = {}
    if processed['project']:
        processed['project'] = sorted(processed['project'], key=lambda x: x['date_to'], reverse=True)
        for project in processed['project']:
            project['duration'] = compute_duration(project['date_from'], project['date_to'], as_date)
        result['experience'] = processed
    return result

def fix_zhilian(d, as_date=None):
    u"""
    """
    processed = {'project': []}
    for RE in [PJ, ]:
        res = RE.search(d)
        if res:
            pos, out = project_xp_zhilian(PR, res.group('proj'))
            if not pos and len(out['project']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed, as_date)

def fix_liepin(d, as_date=None):
    u"""
    """
    processed = {'project': []}
    for RE in [PJ, APJ]:
        res = RE.search(d)
        if res:
            pos, out = project_xp_liepin(LPR, res.group('proj'))
            if not pos and len(out['project']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed, as_date)

def fix_jingying(d, as_date=None):
    u"""
    """
    processed = {'project': []}
    for RE in [PJ, APJ]:
        res = RE.search(d)
        if res:
            pos, out = project_xp_jingying(JPR, res.group('proj'))
            if not pos and len(out['project']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed, as_date)

def fix_yingcai(d, as_date=None):
    u"""
    """
    processed = {'project': []}
    for RE in [PJ, APJ]:
        res = RE.search(d)
        if res:
            pos, out = project_xp_yingcai(IPR, res.group('proj'))
            if not pos and len(out['project']) == 0:
                pass
            else:
                processed = out
            break
    return fix_output(processed, as_date)

def fix(d, as_date=None):
    u"""
    """
    if is_jycv(d):
        return fix_jingying(d, as_date)
    elif is_lpcv(d):
        return fix_liepin(d, as_date)
    elif is_zlcv(d):
        return fix_zhilian(d, as_date)
    elif is_yccv(d):
        return fix_yingcai(d, as_date)
    elif is_nlpcv(d):
        return fix_liepin(d, as_date)

    reject = 0
    processed = {'project': []}
    res = PJ.search(d)
    if res:
        pos, out = project_xp(PR, res.group('proj'))
        processed = out
    else:
        res = APJ.search(d)
        if res:
            pos, out = project_xp(PR, res.group('proj'))
            processed = out
        else:
            reject = 4
    return fix_output(processed, as_date)
