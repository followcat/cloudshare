import os

import core.basedata
import utils.builtin
from baseapp.datadbs import *


def init_prjpeo(SVC_PRJ):
    for id in SVC_PRJ.curriculumvitae.ids:
        uniqueid = SVC_PRJ.curriculumvitae.getuniqueid(id)
        info = SVC_PRJ.curriculumvitae.getyaml(id)
        md = SVC_PRJ.curriculumvitae.getmd(id)
        baseobj = core.basedata.DataObject({'id': uniqueid}, md)
        SVC_PRJ.people.add(baseobj, info['committer'], do_commit=False)


def convert_infos(SVC_PRJ):
    for id in SVC_PRJ.people.ids:
        peoinfo = SVC_PRJ.people.getinfo(id)
        peoyaml = SVC_PRJ.people.getyaml(id)
        for cv in peoyaml['cv']:
            if not SVC_PRJ.curriculumvitae.exists(cv):
                continue
            cvinfo = SVC_PRJ.curriculumvitae.getinfo(cv)
            print cvinfo
            for key in SVC_PRJ.people.list_item:
                peoinfo[key].extend(cvinfo[key])
        utils.builtin.save_yaml(peoinfo, os.path.join(SVC_PRJ.people.path,
                                SVC_PRJ.people.YAML_DIR), id+'.yaml')
        for cv in peoyaml['cv']:
            if not SVC_PRJ.curriculumvitae.exists(cv):
                continue
            cvinfo = SVC_PRJ.curriculumvitae.getinfo(cv)
            for key in SVC_PRJ.people.list_item:
                cvinfo.pop(key)
            utils.builtin.save_yaml(cvinfo, os.path.join(SVC_PRJ.curriculumvitae.path,
                                    SVC_PRJ.curriculumvitae.YAML_DIR), cv+'.yaml')

