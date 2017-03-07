# -*- coding: utf-8 -*-
import re

import xlrd


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
    nd['responsible'] =     loose(d, [u'跟进人'])                #
    nd['progress'] =        loose(d, [u'跟进情况'])              #;\n；
    nd['priority'] =        loose(d, [u'优先级', u'优先项'])
    return nd


def reformat(item):
    if not isinstance(item['relatedcompany'], list):
        item['relatedcompany'] = [e for e in re.split(u'[、，,;；]',
                                  unicode(item['relatedcompany'])) if e]
    if not isinstance(item['position'], list):
        item['position'] = [e for e in re.split(u'[、，,]',
                            unicode(item['position'])) if e]
    if not isinstance(item['clientcontact'], list):
        item['clientcontact'] = [e for e in re.split(u'',
                                 unicode(item['clientcontact'])) if e]
    if not isinstance(item['priority'], int):
        try:
            item['priority'] = int(item['priority'])
        except ValueError:
            item['priority'] = 0
    if not isinstance(item['progress'], list):
        item['progress'] = [e for e in re.split(u'[;\n]',
                            unicode(item['progress'])) if e]
    if isinstance(item['updatednumber'], float):
        item['updatednumber'] = [int(item['updatednumber'])]
    elif not isinstance(item['updatednumber'], list):
        item['updatednumber'] = [e for e in re.split(u'[、；]',
                                 unicode(item['updatednumber'])) if e]
    return item


def convert(stream):
    data = xlrd.open_workbook(file_contents=stream)
    l = list()
    for table in data.sheets():
        for r in range(table.nrows):
            if r > 0:
                d = dict()
                for i in range(len(table.row_values(0))):
                    d[table.row_values(0)[i]] = table.row_values(r)[i]
                eng = chs_to_eng(d)
                format_eng = reformat(eng)
                l.append(format_eng)
    return l
