# -*- coding: utf-8 -*-
import os.path
import functools

import json
import yaml

from webapp.settings import *
from tests.jd_additional_words import added_words


test_cv_svc = services.simulationcv.SimulationCV('tests/cv_svc', 'lsisim_test', 
                                                 [SVC_CV_REPO], iotype='base')

FIRST_PAGE = range(len(test_cv_svc.ids)/90)

PERFECT = 100
GOOD = 50
POOR = 25
BAD = 0

count_in = [0]

kgr_file = 'tests/known_good_jd_cv_mapping.yaml'
with open(kgr_file) as f:
    datas = yaml.load(f)

med_co_cv_file = 'tests/co_cv_md_names.json'
with open(med_co_cv_file) as f:
    med_co_cv_ids = json.load(f)


def kgr_percentage(jd_id, jd_service, sim, cvs=None, index_service=None, filterdict=None, percentage=100, above_allow=False):
    """
        >>> from tests.test_model import *
        >>> from webapp.settings import *
        >>> from tests.multi_models import *
        >>> jd_service = SVC_PRJ_MED.jobdescription
        >>> names = list(test_cv_svc.ids)
        >>> texts = [SVC_CV_REPO.getmd(n) for n in names]
        >>> path = 'tests/lsisim/model'
        >>> model = build_lsimodel(path, SVC_MIN.lsi_model['medical'].slicer, names, texts, no_above=1./3, extra_samples=300)
        >>> sim_path = 'tests/lsisim/sim'
        >>> sim = build_sim(sim_path, model, [test_cv_svc])
        >>> assert kgr_perfect('9bbc45a81e4511e6b7066c3be51cefca', jd_service, sim)
        >>> assert kgr_perfect('098a91ca0b4f11e6abf46c3be51cefca', jd_service, sim)
        >>> assert kgr_poor('098a91ca0b4f11e6abf46c3be51cefca', jd_service, sim, above_allow=True)
        >>> assert kgr_percentage('be97722a0cff11e6a3e16c3be51cefca', jd_service, sim, percentage=int(float(2)/7*100))
        >>> assert kgr_bad('06fdc0680b5d11e6ae596c3be51cefca', jd_service, sim)
        >>> assert kgr_perfect('e290dd36428a11e6b2934ccc6a30cd76', jd_service, sim)
        >>> jd_id, cvs = '2fe1c53a231b11e6b7096c3be51cefca', ['3hffapdz', '2x5wx4aa']
        >>> assert kgr_good(jd_id, jd_service, sim, cvs=cvs)
        >>> assert kgr_bad('cce2a5be547311e6964f4ccc6a30cd76', jd_service, sim, cvs=['qfgwkkhg', 'nji2v4s7', 'qssipwf9'])
        >>> assert kgr_percentage('cce2a5be547311e6964f4ccc6a30cd76', jd_service, sim, cvs=['qfgwkkhg', 'nji2v4s7', 'qssipwf9'], index_service=SVC_INDEX, filterdict={'expectation_places': ['长沙'.decode('utf-8')]}, percentage=int(float(2)/3*100))
    """
    if cvs is None:
        cvs = datas[jd_id]
    if not hasattr(cvs, '__iter__'):
        cvs = {cvs}
    success_count = kgr(jd_id, cvs, jd_service, sim, index_service, filterdict)
    global count_in
    count_in[0] += success_count
    if percentage == PERFECT:
        result = success_count == len(cvs)
    elif percentage == GOOD:
        result = len(cvs)*0.5 <= success_count and (success_count < len(cvs) or above_allow)
    elif percentage == POOR:
        result = len(cvs)*0.25 <= success_count and (success_count < len(cvs)*0.5 or above_allow)
    elif percentage == BAD:
        result = success_count == 0 or above_allow
    elif 0 < percentage < 100:
        result = len(cvs)*float(percentage)/100 <= success_count and (success_count < len(cvs) or above_allow)
    return result

kgr_perfect = functools.partial(kgr_percentage, percentage=PERFECT)
kgr_good = functools.partial(kgr_percentage, percentage=GOOD)
kgr_poor = functools.partial(kgr_percentage, percentage=POOR)
kgr_bad = functools.partial(kgr_percentage, percentage=BAD)

def kgr(jd_id, cvs, jd_service, sim, index_service, filterdict):
    sucess_count = 0
    _ranks = ranks(jd_id, jd_service, sim, cvs, index_service, filterdict)
    for _rank in _ranks.values():
        if _rank in FIRST_PAGE:
            sucess_count += 1
    return sucess_count

def ranks(jd_id, jd_service, sim, cvs=None, index_service=None,
            filterdict=None):
    if cvs is None:
        cvs = datas[jd_id]
    job_desc = jd_service.get(jd_id)['description']
    if jd_id in added_words:
        a_words = added_words[jd_id]
        job_desc += a_words
    score_board = sim.probability(job_desc)
    if index_service is not None and filterdict is not None:
        filteset = index_service.get(filterdict)
        score_board = filter(lambda x: os.path.splitext(x[0])[0] in filteset,
                             score_board)
    ranks_dict = {}
    for cv_id in cvs:
        for _rank, (_c, _s) in enumerate(score_board):
            if cv_id == _c:
                ranks_dict[cv_id] = _rank
    return ranks_dict
