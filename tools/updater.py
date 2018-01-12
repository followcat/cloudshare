def update_cv_models(SVC_MIN, SVC_MEMBERS):
    def gen(lsimodel, cvs):
        for cv in cvs:
            if len(lsimodel.ids) != len(svcdict[cv].ids):
                for name in set(svcdict[cv].ids).difference(set(lsimodel.ids)):
                    yield (name, svcdict[cv].getmd(name))

    svcdict = dict([(mem.id, mem.curriculumvitae.services[0])
                     for mem in SVC_MEMBERS.members.values()])
    for modelname in SVC_MIN.sim.keys():
        lsimodel = SVC_MIN.lsi_model[modelname]
        if lsimodel.getconfig('autoupdate') is True:
            trains = gen(lsimodel, lsimodel.getconfig('origin'))
            updated = SVC_MIN.lsi_model[modelname].update(trains)
            if updated is True:
                SVC_MIN.lsi_model[modelname].save()


def gupdate(SVC_MIN, SVCS, modelname, gen, simname=None):
    for svc in SVCS:
        if simname is None:
            simname = svc.name
        simids = SVC_MIN.sim[modelname][simname].ids
        trains = gen(svc, simids)
        result = SVC_MIN.sim[modelname][simname].update(trains)
        if result is True:
            SVC_MIN.sim[modelname][simname].save()


def update_cv_sim(SVC_MIN, svc, modelname, simname):
    def gen(svc, simids):
        for id in svc.ids.difference(simids):
            yield (id, svc.getmd(id))

    gupdate(SVC_MIN, [svc], modelname, gen, simname=simname)


def update_cv_sims(SVC_MIN, SVC_MEMBERS, additionals=None):
    svcdict = dict([(mem.id, mem.curriculumvitae.services[0])
                     for mem in SVC_MEMBERS.members.values()])
    if additionals is not None:
        assert isinstance(additionals, dict)
        svcdict = additionals
    for modelname in SVC_MIN.sim.keys():
        for simname in SVC_MIN.sim[modelname]:
            if simname not in svcdict:
                continue
            svc = svcdict[simname]
            if len(svc.ids) != len(SVC_MIN.sim[modelname][simname].ids):
                update_cv_sim(SVC_MIN, svc, modelname, simname)


def update_jd_sims(modelname, SVC_MIN, SVC_JDS):
    def gen(svc, simids):
        for id in svc.ids.difference(simids):
            yield (id, svc.getyaml(id)['description'])

    gupdate(SVC_MIN, SVC_JDS, modelname, gen)


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

    gupdate(SVC_MIN, SVC_CVS, modelname, gen)


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

    gupdate(SVC_MIN, SVC_CVS, modelname, gen)


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

    gupdate(SVC_MIN, SVC_CVS, modelname, gen)
