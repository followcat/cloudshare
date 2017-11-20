def update_cv_sim(SVC_MIN, modelname, simname, svc):
    ids = SVC_MIN.sim[modelname][simname].ids
    if len(ids) != len(svc.ids):
        trains = iter([(name, svc.getmd(name)) for name in
                       svc.ids.difference(ids)])
        result = SVC_MIN.sim[modelname][simname].update(trains)
        if result is True:
            SVC_MIN.sim[modelname][simname].save()

def update_cv_sims(SVC_MIN, SVC_MEMBERS, additionals=None):
    modelnames = set([prj.modelname for prj in SVC_MEMBERS.allprojects().values()])
    svcdict = dict([(prj.id, prj.curriculumvitae) for prj in
                     SVC_MEMBERS.allprojects().values()])
    if additionals is not None:
        assert isinstance(additionals, dict)
        svcdict.update(additionals)
    for modelname in modelnames:
        if modelname not in SVC_MIN.sim:
            continue
        for simname in SVC_MIN.sim[modelname]:
            if simname not in svcdict:
                continue
            svc = svcdict[simname]
            update_cv_sim(SVC_MIN, modelname, simname, svc)


def update_cv_models(SVC_MIN, SVC_MEMBERS):
    def gen(lsimodel, cvs):
        for cv in cvs:
            if len(lsimodel.ids) != len(svcdict[cv].ids):
                for name in set(svcdict[cv].ids).difference(set(lsimodel.ids)):
                    yield (name, svcdict[cv].getmd(name))

    modelnames = set([prj.modelname for prj in SVC_MEMBERS.allprojects().values()])
    svcdict = dict([(prj.id, prj.curriculumvitae) for prj in
                     SVC_MEMBERS.allprojects().values()])
    for modelname in modelnames:
        if modelname not in SVC_MIN.sim:
            continue
        lsimodel = SVC_MIN.lsi_model[modelname]
        if lsimodel.getconfig('autoupdate') is True:
            trains = gen(lsimodel, lsimodel.getconfig('origin'))
            updated = SVC_MIN.lsi_model[modelname].update(trains)
            if updated is True:
                SVC_MIN.lsi_model[modelname].save()


def update_jd_sims(modelname, SVC_MIN, SVC_JDS):
    for svc in SVC_JDS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        trains = iter([(id, svc.getyaml(id)['description']) for id in
                       svc.ids.difference(simids)])
        result = SVC_MIN.sim[modelname][svc.name].update(trains)
        if result is True:
            SVC_MIN.sim[modelname][svc.name].save()


def update_co_sims(modelname, SVC_MIN, SVC_CVS):
    def gen(svc, simids):
        for id in svc.ids.difference(simids):
            info = svc.getyaml(id)
            try:
                datas = info['experience']['company']
            except KeyError, TypeError:
                yield ('.'.join([id, '']), '')
                continue
            for data in datas:
                if 'description' not in data:
                    continue
                yield ('.'.join([id, data['name']]),
                       data['description'])

    for svc in SVC_CVS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        trains = gen(svc, simids)
        result = SVC_MIN.sim[modelname][svc.name].update(trains)
        if result is True:
            SVC_MIN.sim[modelname][svc.name].save()


def update_pos_sims(modelname, SVC_MIN, SVC_CVS):
    def gen(svc, simids):
        for id in svc.ids.difference(simids):
            info = svc.getyaml(id)
            try:
                datas = info['experience']['position']
            except KeyError, TypeError:
                continue
            for data in datas:
                if 'description' not in data:
                    continue
                yield ('.'.join([id,
                                 info['experience']['company'][data['at_company']]['name'],
                                 data['name']]),
                       data['description'])

    for svc in SVC_CVS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        trains = gen(svc, simids)
        result = SVC_MIN.sim[modelname][svc.name].update(trains)
        if result is True:
            SVC_MIN.sim[modelname][svc.name].save()


def update_prj_sims(modelname, SVC_MIN, SVC_CVS):
    def gen(svc, simids):
        for id in svc.ids.difference(simids):
            info = svc.getyaml(id)
            try:
                datas = info['experience']['project']
            except KeyError, TypeError:
                continue
            for data in datas:
                name = data['name'] if 'name' in data else '-'
                company = data['company'] if 'company' in data else '-'
                description = data['description'] if 'description' in data else ''
                responsibility = data['responsibility'] if 'responsibility' in data else ''
                if not description and not responsibility:
                    continue
                yield (('.'.join([id, company, name]),
                        '\n'.join([description, responsibility])))

    for svc in SVC_CVS:
        trains = list()
        simids = SVC_MIN.sim[modelname][svc.name].ids
        trains = gen(svc, simids)
        result = SVC_MIN.sim[modelname][svc.name].update(trains)
        if result is True:
            SVC_MIN.sim[modelname][svc.name].save()
