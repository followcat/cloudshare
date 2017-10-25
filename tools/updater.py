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
            names = SVC_MIN.sim[modelname][simname].names
            if len(names) != len(svc.ids):
                trains = [(name, svc.getmd(name)) for name in
                          set(svc.names()).difference(set(names))]
                SVC_MIN.sim[modelname][simname].update(trains, newmodel=newmodel)


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
                if len(lsimodel.names) != len(svc.ids):
                    trains.extend([(name, svc.getmd(name)) for name in
                                   set(svc.names()).difference(set(lsimodel.names))])
            updated = SVC_MIN.lsi_model[modelname].update(trains)
            SVC_MIN.update_sims(newmodel=updated)


def update_jd_sims(modelname, SVC_MIN, SVC_JDS, newmodel=False):
    for svc in SVC_JDS:
        trains = list()
        names = SVC_MIN.sim[modelname][svc.name].names
        trains.extend([(id, svc.getyaml(id)['description']) for id in
                        svc.ids.difference(set(names))])
        SVC_MIN.sim[modelname][svc.name].update(trains, newmodel=newmodel)
