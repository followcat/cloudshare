import utils.builtin


def generate_keywords(path, projects):
    results = dict()
    if not os.path.exists(path):
        os.makedirs(path)
    for project in projects:
        for jd in project.jobdescription.lists():
            try:
                if jd['status'] == 'Closed':
                    continue
            except KeyError:
                continue
            jdname = jd['name']
            commentary = jd['commentary'].split('\n')
            companyname = project.company.getyaml(jd['company'])['name']
            if companyname not in results:
                results[companyname] = list()
            results[companyname].append({jdname: commentary})
    for companyname in results:
        utils.builtin.save_yaml(results[companyname], path, companyname+'.yaml')
