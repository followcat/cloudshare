def update_cv_sim(SVC_MIN, modelname, simname, svc, newmodel=False):
    names = SVC_MIN.sim[modelname][simname].names
    if len(names) != len(svc.ids):
        trains = [(name, svc.getmd(name)) for name in
                  set(svc.names()).difference(set(names))]
        SVC_MIN.sim[modelname][simname].update(trains, newmodel=newmodel)

def update_cv_sims(SVC_MIN, SVC_MEMBERS, additionals=None, newmodel=False):
    modelnames = set([prj.modelname for prj in SVC_MEMBERS.allprojects().values()])
    svcdict = dict([(prj.id, prj.curriculumvitae) for prj in SVC_MEMBERS.allprojects().values()])
    if additionals is not None:
        assert isinstance(additionals, dict)
        svcdict.update(additionals)
    for modelname in modelnames:
        for simname in SVC_MIN.sim[modelname]:
            if simname not in svcdict:
                continue
            svc = svcdict[simname]
            update_cv_sim(SVC_MIN, modelname, simname, svc, newmodel=newmodel)


def update_cv_models(SVC_MIN, SVC_MEMBERS, additionals=None):
    modelnames = set([prj.modelname for prj in SVC_MEMBERS.allprojects().values()])
    svcdict = dict([(prj.id, prj.curriculumvitae) for prj in SVC_MEMBERS.allprojects().values()])
    if additionals is not None:
        assert isinstance(additionals, dict)
        svcdict.update(additionals)
    for modelname in modelnames:
        lsimodel = SVC_MIN.lsi_model[modelname]
        if lsimodel.getconfig('autoupdate') is True:
            trains = list()
            for cv in lsimodel.getconfig('origin'):
                if len(lsimodel.names) != len(svcdict[cv].ids):
                    trains.extend([(name, svcdict[cv].getmd(name)) for name in
                                   set(svcdict[cv].names()).difference(set(lsimodel.names))])
            updated = SVC_MIN.lsi_model[modelname].update(trains)
            for simname in SVC_MIN.sim[modelname]:
                svc = svcdict[simname]
                update_cv_sim(SVC_MIN, modelname, simname, svc, newmodel=updated)


def update_jd_sims(modelname, SVC_MIN, SVC_JDS, newmodel=False):
    for svc in SVC_JDS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        trains.extend([(id, svc.getyaml(id)['description']) for id in
                        svc.ids.difference(simids)])
        SVC_MIN.sim[modelname][svc.name].update(trains, newmodel=newmodel)


def update_co_sims(modelname, SVC_MIN, SVC_CVS, newmodel=False):
    for svc in SVC_CVS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        for id in svc.ids.difference(simids):
            info = svc.getyaml(id)
            try:
                datas = info['experience']['company']
            except KeyError, TypeError:
                trains.append(('.'.join([id, '']), ''))
                continue
            for data in datas:
                if 'description' not in data:
                    trains.append(('.'.join([id, data['name']]).encode('utf-8'),
                                   ''))
                    continue
                trains.append(('.'.join([id, data['name']]).encode('utf-8'), data['description']))
        SVC_MIN.sim[modelname][svc.name].update(trains, newmodel=newmodel)


def update_pos_sims(modelname, SVC_MIN, SVC_CVS, newmodel=False):
    for svc in SVC_CVS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        for id in svc.ids.difference(simids):
            info = svc.getyaml(id)
            try:
                datas = info['experience']['position']
            except KeyError, TypeError:
                trains.append(('.'.join([id, '']), ''))
                continue
            for data in datas:
                if 'description' not in data:
                    trains.append(('.'.join([id,
                                         info['experience']['company'][data['at_company']]['name'],
                                         data['name']]).encode('utf-8'),
                                   ''))
                    continue
                trains.append(('.'.join([id,
                                         info['experience']['company'][data['at_company']]['name'],
                                         data['name']]).encode('utf-8'),
                               data['description']))
        SVC_MIN.sim[modelname][svc.name].update(trains, newmodel=newmodel)


def update_prj_sims(modelname, SVC_MIN, SVC_CVS, newmodel=False):
    for svc in SVC_CVS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        for id in svc.ids.difference(simids):
            info = svc.getyaml(id)
            try:
                datas = info['experience']['project']
            except KeyError, TypeError:
                trains.append(('.'.join([id, '']), ''))
                continue
            for data in datas:
                name = data['name'] if 'name' in data else '-'
                company = data['company'] if 'company' in data else '-'
                description = data['description'] if 'description' in data else ''
                responsibility = data['responsibility'] if 'responsibility' in data else ''
                if not description and not responsibility:
                    trains.append(('.'.join([id, company, name]).encode('utf-8'),
                                   ''))
                    continue
                trains.append(('.'.join([id, company, name]).encode('utf-8'),
                               '\n'.join([description, responsibility])))
        SVC_MIN.sim[modelname][svc.name].update(trains, newmodel=newmodel)
