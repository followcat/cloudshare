# -*- coding: utf-8 -*-
import yaml

import core.basedata
import extractor.unique_id
from extractor.information_explorer import *


def outputdict(path):
    import xlrd
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    l = list()
    for r in range(table.nrows):
        if r > 1:
            d = dict()
            for i in range(len(table.row_values(1))):
                d[table.row_values(1)[i]] = table.row_values(r)[i]
            l.append(d)
    return l

def chs_to_eng(d):
    nd = dict()
    nd['name'] = d[u'公司全称']
    nd['product'] = d[u'产品']
    nd['position'] = d[u'Open positions']   #[、，,]
    nd['website'] = d[u'网站']
    nd['clientcontact'] = d[u'联系人']       #
    nd['conumber'] = d[u'座机']
    nd['caller'] = d[u'陌拜人']              #
    nd['address'] = d[u'地址']
    nd['introduction'] = d[u'公司概况']
    nd['progress'] = d[u'陌拜情况']          #;\n；
    nd['updatednumber'] = d[u'联系电话']     #、；
    nd['email'] = d[u'邮箱']
    return nd

def reformat(item):
    import re
    if not isinstance(item['position'], list):
        item['position'] = [e for e in re.split(u'[、，,]', item['position']) if e]
    if not isinstance(item['clientcontact'], list):
        item['clientcontact'] = [e for e in re.split(u'', item['clientcontact']) if e]
    if not isinstance(item['caller'], list):
        item['caller'] = [e for e in re.split(u'', item['caller']) if e]
    if not isinstance(item['progress'], list):
        item['progress'] = [e for e in re.split(u'[;\n]', item['progress']) if e]
    if isinstance(item['updatednumber'], float):
        item['updatednumber'] = [int(item['updatednumber'])]
    elif not isinstance(item['updatednumber'], list):
        item['updatednumber'] = [e for e in re.split(u'[、；]', item['updatednumber']) if e]
    return item

def process(d):
    dos = list()
    for chs in d:
        eng = chs_to_eng(chs)
        format_eng = reformat(eng)
        metadata = catch_coinfo(format_eng, format_eng['name'])
        do = core.basedata.DataObject(metadata, format_eng)
        dos.append(do)
    return dos
###

def add(d, SVC_CO_REPO):
    dos = process(d)
    for each in dos:
        with open(os.path.join(SVC_CO_REPO.interface.path, each.name+'.yaml'), 'w') as fp:
            fp.write(yaml.safe_dump(each.metadata, allow_unicode=True))


def convert_repo(SVC_CO_REPO):
    for each in SVC_CO_REPO.ids:
        info = SVC_CO_REPO.getyaml(each)
        metadata = catch_coinfo(info, info['name'])
        do = core.basedata.DataObject(metadata, metadata)
        with open(os.path.join(SVC_CO_REPO.interface.path, do.name+'.yaml'), 'w') as fp:
            fp.write(yaml.safe_dump(do.metadata, allow_unicode=True))


def init_simid(SVC_CO_SIM, SVC_CO_REPO):
    for each in SVC_CO_REPO.ids:
        info = SVC_CO_REPO.getyaml(each)
        metadata = catch_coinfo(info, info['name'])
        do = core.basedata.DataObject(metadata, metadata)
        SVC_CO_SIM.add(do)

def init_siminfo(SVC_CO_SIM, d):
    dos = process(d)
    for key in ('position', 'clientcontact', 'caller', 'progress', 'updatednumber'):
        for chs in d:
            eng = chs_to_eng(chs)
            format_eng = reformat(eng)
            id = extractor.unique_id.company_id(format_eng['name'])
            caller = 'dev'
            if format_eng['caller']:
                caller = format_eng['caller'][0]
            for value in format_eng[key]:
                SVC_CO_SIM.updateinfo(id, key, value, caller)

