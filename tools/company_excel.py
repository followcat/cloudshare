# -*- coding: utf-8 -*-
import re

import yaml

import core.basedata
import extractor.unique_id
from extractor.information_explorer import *


def outputdict(path):
    import xlrd
    data = xlrd.open_workbook(path)
    l = list()
    for table in data.sheets():
        for r in range(table.nrows):
            if r > 0:
                d = dict()
                for i in range(len(table.row_values(0))):
                    d[table.row_values(0)[i]] = table.row_values(r)[i]
                l.append(d)
    return l

def chs_to_eng(d):
    def loose(d, words):
        for word in words:
            if word in d:
                return d[word]
        else:
            return ''
    nd = dict()
    nd['district'] =        loose(d, [u'区域'])
    nd['name'] =            loose(d, [u'公司全称'])
    nd['introduction'] =    loose(d, [u'公司概况'])
    nd['relatedcompany'] =  loose(d, [u'关联公司'])             #[、，,]
    nd['product'] =         loose(d, [u'产品'])
    nd['address'] =         loose(d, [u'公司地址', u'地址'])
    nd['website'] =         loose(d, [u'公司网站', u'网站'])
    nd['position'] =        loose(d, [u'近期招聘职位'])          #[、，,]
    nd['updatednumber'] =   loose(d, [u'联系电话'])              #、；
    nd['email'] =           loose(d, [u'邮箱'])
    nd['clientcontact'] =   loose(d, [u'联系人'])                #
    nd['conumber'] =        loose(d, [u'座机'])
    nd['caller'] =          loose(d, [u'跟进人', u'陌拜人'])      #
    nd['progress'] =        loose(d, [u'跟进情况', u'陌拜情况'])   #;\n；
    return nd

def reformat(item):
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


def init_simid(SVC_CO_SIM, SVC_CO_REPO, ids):
    for each in ids:
        info = SVC_CO_REPO.getyaml(each)
        metadata = catch_coinfo(info, info['name'])
        do = core.basedata.DataObject(metadata, metadata)
        SVC_CO_SIM.add(do)


def init_siminfo(SVC_CO_SIM, d):
    dos = process(d)
    for key in ('relatedcompany', 'position', 'clientcontact',
                'caller', 'progress', 'updatednumber'):
        for chs in d:
            eng = chs_to_eng(chs)
            format_eng = reformat(eng)
            id = extractor.unique_id.company_id(format_eng['name'])
            caller = 'dev'
            if format_eng['caller']:
                caller = format_eng['caller'][0]
            for value in format_eng[key]:
                SVC_CO_SIM.updateinfo(id, key, value, caller)

