"""
    To use:
        cd $CLOUDSHARE_HOME
        nosetests tests/test_model.py
"""

import json
import yaml

kgr_file = 'tests/known_good_jd_cv_mapping.yaml'
with open(kgr_file) as f:
    datas = yaml.load(f)['datas']

scores = None


class NotInRankRange(RuntimeError):
    """"""

def get_job_description(jd_id, jd_service=None):
    if jd_service is None:
        import webapp.settings
        jd_service = webapp.settings.SVC_PRJ_MED.jobdescription
    jd = jd_service.get(jd_service.search(jd_id)[0])['description']
    return jd

def get_scores(job_desc, sim=None, json_file=None):
    if json_file is not None:
        with open(json_file) as _file:
            scores = json.load(_file)
        return scores
    scores = sim.probability(job_desc)
    return scores

def test_kgr_generator(sim=None, json_file=None):
    if json_file is None and sim is None:
        import webapp.settings
        sim = webapp.settings.SVC_MIN.sim['medical']['medical']
    for _d in datas:
        jd_id, cvs = _d.popitem()
        job_desc = get_job_description(jd_id,
                        webapp.settings.SVC_PRJ_MED.jobdescription)
        global scores
        scores = get_scores(job_desc, sim=sim, json_file=json_file)
        for cv_id in cvs:
            yield kgr, jd_id, cv_id

def kgr(jd_id, cv_id):
    global scores
    for current_rank, (_c, _s) in enumerate(scores):
        if cv_id == _c:
            if not current_rank < 20:
                raise NotInRankRange('rank: %d'%current_rank)
