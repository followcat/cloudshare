# -*- coding: utf-8 -*-
import yaml

import core.basedata
import utils.companyexcel
import extractor.unique_id
from extractor.information_explorer import *


def process(stream):
    excels = utils.companyexcel.convert(stream)
    for excel in excels:
        metadata = catch_coinfo(excel, excel['name'])
        do = core.basedata.DataObject(metadata, excel)
        dos.append(do)
    return dos


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


def init_siminfo(SVC_CO_SIM, stream):
    excels = process(d)
    for key in ('relatedcompany', 'position', 'clientcontact',
                'caller', 'progress', 'updatednumber'):
        for excel in excels:
            id = extractor.unique_id.company_id(excel['name'])
            info = SVC_CO_SIM.getyaml(id)
            if key not in info:
                continue
            existvalues = [v['content'] for v in info[key]]
            caller = 'dev'
            if excel['caller']:
                caller = excel['caller'][0]
            for value in excel[key]:
                if value in existvalues:
                    continue
                SVC_CO_SIM.updateinfo(id, key, value, caller)


def delete_ununique(SVC_CO_SIM):
    for key in ('relatedcompany', 'position', 'clientcontact',
                'caller', 'progress', 'updatednumber'):
        for id in SVC_CO_SIM.ids:
            info = SVC_CO_SIM.getyaml(id)
            caller = info['caller']
            info_set = set([(v['content'], v['author']) for v in info[key]])
            if len(info[key]) != len(info_set):
                delete_l = list()
                for v in info_set:
                    for dictv in info[key]:
                        if v[0] == dictv['content']:
                            delete_l.append(dictv)
                            break
                for each in delete_l:
                    info[key].remove(each)
                for v in info[key]:
                    SVC_CO_SIM.deleteinfo(id, key, v['content'], v['author'], v['date'])

