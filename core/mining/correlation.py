def jobdescription_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0, page=0, numbers=0):
    begin = page*numbers
    end = (page+1)*numbers
    total = 0
    results = list()
    simdict = SVC_MIN.sim['jdmatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        total += len(result)
        for index, value in result[begin:end]:
            id = sim.names[index]
            results.append( {'id': id, 'value': value, 'data': svc.getyaml(id)} )
    return total, results


def company_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0, page=0, numbers=0):
    begin = page*numbers
    end = (page+1)*numbers
    total = 0
    results = list()
    simdict = SVC_MIN.sim['comatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        total += len(result)
        for index, value in result[begin:end]:
            longname = sim.names[index]
            id, name = longname.split('.', 1)
            info = svc.getyaml(id)
            for company in info['experience']['company']:
                if company['name'] == name:
                    results.append({ 'id': id, 'value': value, 'data': company })
                    break
            else:
                raise Exception('Not found description')
    return total, results


def position_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0, page=0, numbers=0):
    begin = page*numbers
    end = (page+1)*numbers
    total = 0
    results = list()
    simdict = SVC_MIN.sim['posmatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        total += len(result)
        for index, value in result[begin:end]:
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
                    results.append({ 'id': id, 'value': value, 'data': position })
                    break
            else:
                continue
    return total, results


def project_correlation(SVC_MIN, SVCS, doc, top=None, minimum=0, page=0, numbers=0):
    begin = page*numbers
    end = (page+1)*numbers
    total = 0
    results = list()
    simdict = SVC_MIN.sim['prjmatch']
    for svc in SVCS:
        sim = simdict[svc.name]
        result = sim.base_probability(doc, top=top, minimum=minimum)
        total += len(result)
        for index, value in result[begin:end]:
            longname = sim.names[index]
            try:
                id, longname = longname.split('.', 1)
                company, name = longname.rsplit('.', 1)
            except ValueError:
                continue
            info = svc.getyaml(id)
            for project in info['experience']['project']:
                if project['name'] == name:
                    results.append({ 'id': id, 'value': value, 'data': project })
                    break
            else:
                raise Exception('Not found description')
    return total, results
