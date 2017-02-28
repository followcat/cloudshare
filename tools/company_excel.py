# -*- coding: utf-8 -*-
import time
import yaml

import core.basedata
import utils.companyexcel
import extractor.unique_id
import services.simulationco
from extractor.information_explorer import *


def initexcel(path, SVC_CO_REPO, SVC_PRJ):
    stream = ''
    with open(path, 'r') as fp:
        stream = fp.read()
    SVC_CO_SIM = SVC_PRJ.company
    excels = utils.companyexcel.convert(stream)
    objs = add_repo(excels, SVC_CO_REPO)
    init_simid(SVC_CO_SIM, SVC_CO_REPO, [each.name for each in objs])
    init_siminfo(excels, SVC_CO_SIM)


def add_repo(excels, SVC_CO_REPO):
    objs = []
    for excel in excels:
        metadata = catch_coinfo(excel, excel['name'])
        bsobj = core.basedata.DataObject(metadata, excel)
        if 'date' not in bsobj.metadata or not bsobj.metadata['date']:
            bsobj.metadata['date'] = time.time()
        objs.append(bsobj)
    for each in objs:
        if not SVC_CO_REPO.exists(each.name):
            with open(os.path.join(SVC_CO_REPO.interface.path, each.name+'.yaml'), 'w') as fp:
                fp.write(yaml.safe_dump(each.metadata, allow_unicode=True))
    return objs


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
        SVC_CO_SIM.add(do, do_commit=False)


def init_siminfo(excels, SVC_CO_SIM):
    def update_list(id, info, excel, key, responsible):
        existvalues = [v['content'] for v in info[key]]
        for value in excel[key]:
            if value in existvalues:
                continue
            SVC_CO_SIM.updateinfo(id, key, value, responsible, do_commit=False)
    extractkeys = map(lambda k: k[0], services.simulationco.SimulationCO.YAML_TEMPLATE)
    for key in extractkeys:
        for excel in excels:
            responsible = 'dev'
            if excel['responsible']:
                responsible = excel['responsible']
            id = extractor.unique_id.company_id(excel['name'])
            info = SVC_CO_SIM.getyaml(id)
            if key not in info or key not in excel:
                continue
            if isinstance(info[key], list):
                update_list(id, info, excel, key, responsible)
            else:
                SVC_CO_SIM.updateinfo(id, key, excel[key], responsible, do_commit=False)


def delete_ununique(SVC_CO_SIM):
    extractkeys = map(lambda k: k[0], services.simulationco.SimulationCO.YAML_TEMPLATE)
    for key in extractkeys:
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

