import yaml


FIRST_PAGE = range(20)

kgr_file = 'tests/known_good_jd_cv_mapping.yaml'
with open(kgr_file) as f:
    datas = yaml.load(f)


def kgr_perfect(jd_id, jd_service, sim):
    """
        >>> from tests.test_model import *
        >>> from webapp.settings import *
        >>> jd_service = SVC_PRJ_MED.jobdescription
        >>> sim = SVC_MIN.sim['medical']['medical']
        >>> jd_id = '9bbc45a81e4511e6b7066c3be51cefca'
        >>> assert kgr_perfect(jd_id, jd_service, sim)
    """
    cvs = datas[jd_id]
    sucess_count = kgr(jd_id, cvs, jd_service, sim)
    return sucess_count == len(cvs)

def kgr(jd_id, cvs, jd_service, sim):
    job_desc = jd_service.get(jd_service.search(jd_id)[0])['description']
    score_board = sim.probability(job_desc)
    sucess_count = 0
    for _rank in ranks(score_board, cvs).values():
        if _rank in FIRST_PAGE:
            sucess_count += 1
    return sucess_count

def rank(score_board, cv_id):
    for _rank, (_c, _s) in enumerate(score_board):
        if cv_id == _c:
            return _rank

def ranks(score_board, cvs):
    ranks_dict = {}
    for cv_id in cvs:
        ranks_dict[cv_id] = rank(score_board, cv_id)
    return ranks_dict
