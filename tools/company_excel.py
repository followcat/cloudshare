# -*- coding: utf-8 -*-
import time
import yaml

import core.basedata
import utils.companyexcel
import extractor.unique_id
import services.simulationco
from extractor.information_explorer import *


def add(stream, SVC_CO_REPO):
    dos = []
    excels = utils.companyexcel.convert(stream)
    for excel in excels:
        metadata = catch_coinfo(excel, excel['name'])
        bsobj = core.basedata.DataObject(metadata, excel)
        if 'date' not in bsobj.metadata or not bsobj.metadata['date']:
            bsobj.metadata['date'] = time.time()
        dos.append(bsobj)
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
        SVC_CO_SIM.add(do, do_commit=False)


def init_siminfo(SVC_CO_SIM, stream):
    def update_list(id, info, excel, key):
        existvalues = [v['content'] for v in info[key]]
        for value in excel[key]:
            if value in existvalues:
                continue
            SVC_CO_SIM.updateinfo(id, key, value, responsible, do_commit=False)
    excels = utils.companyexcel.convert(stream)
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
                update_list(id, info, excel, key)
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

