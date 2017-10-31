def jobdescription_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0):
    results = list()
    simdict = SVC_MIN.sim['jdmatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        for index, value in result:
            id = sim.names[index]
            results.append((id, value, svc.getyaml(id)['description']))
    return results


def company_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0):
    results = list()
    simdict = SVC_MIN.sim['comatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        for index, value in result:
            longname = sim.names[index]
            id, name = longname.split('.', 1)
            info = svc.getyaml(id)
            for company in info['experience']['company']:
                if company['name'] == name:
                    results.append((name, value, company))
                    break
            else:
                raise Exception('Not found description')
    return results


def position_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0):
    results = list()
    simdict = SVC_MIN.sim['posmatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        for index, value in result:
            longname = sim.names[index]
            try:
                id, longname = longname.split('.', 1)
                company, name = longname.rsplit('.', 1)
            except ValueError:
                continue
            info = svc.getyaml(id)
            for position in info['experience']['position']:
                at_company = position['at_company']
                pos_company = info['experience']['company'][at_company]['name']
                if pos_company == company and position['name'] == name:
                    results.append((name, value, position))
                    break
            else:
                continue
    return results


def project_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0):
    results = list()
    simdict = SVC_MIN.sim['prjmatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        for index, value in result:
            longname = sim.names[index]
            try:
                id, longname = longname.split('.', 1)
                company, name = longname.rsplit('.', 1)
            except ValueError:
                continue
            info = svc.getyaml(id)
            for project in info['experience']['project']:
                if project['name'] == name:
                    description = project['description'] if 'description' in project else ''
                    responsibility = project['responsibility'] if 'responsibility' in project else ''
                    results.append((name, value, '\n'.join([description, responsibility])))
                    break
            else:
                raise Exception('Not found description')
    return results
