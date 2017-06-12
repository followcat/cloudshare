import utils.builtin
from baseapp.projects import *


def generate_keywords(path, projects=PRJ_LIST):
    results = dict()
    if not os.path.exists(path):
        os.makedirs(path)
    for project in PRJ_LIST:
        for jd in project.jobdescription.lists():
            jdname = jd['name']
            commentary = jd['commentary'].split('\n')
            companyname = project.company.getyaml(jd['company'])['name']
            if companyname not in results:
                results[companyname] = list()
            results[companyname].append({jdname: commentary})
    for companyname in results:
        utils.builtin.save_yaml(results[companyname], path, companyname+'.yaml')
