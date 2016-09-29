import yaml


FIRST_PAGE = range(20)

PERFECT = 100
GOOD = 50
MEDIUM = 25
POOR = 0

kgr_file = 'tests/known_good_jd_cv_mapping.yaml'
with open(kgr_file) as f:
    datas = yaml.load(f)


def kgr_percentage(jd_id, jd_service, sim, cvs=None, percentage=100):
    """
        >>> from tests.test_model import *
        >>> from webapp.settings import *
        >>> jd_service = SVC_PRJ_MED.jobdescription
        >>> sim = SVC_MIN.sim['medical']['medical']
        >>> assert kgr_percentage('9bbc45a81e4511e6b7066c3be51cefca', jd_service, sim, percentage=PERFECT)
        >>> assert kgr_percentage('098a91ca0b4f11e6abf46c3be51cefca', jd_service, sim, percentage=GOOD)
        >>> assert kgr_percentage('be97722a0cff11e6a3e16c3be51cefca', jd_service, sim, percentage=MEDIUM)
        >>> assert kgr_percentage('06fdc0680b5d11e6ae596c3be51cefca', jd_service, sim, percentage=POOR)
        >>> assert kgr_percentage('e290dd36428a11e6b2934ccc6a30cd76', jd_service, sim, percentage=33)
        >>> jd_id, cvs = '2fe1c53a231b11e6b7096c3be51cefca', ['3hffapdz', '2x5wx4aa']
        >>> assert kgr_percentage(jd_id, jd_service, sim, cvs=cvs, percentage=POOR)
    """
    if cvs is None:
        cvs = datas[jd_id]
    if not hasattr(cvs, '__iter__'):
        cvs = {cvs}
    success_count = kgr(jd_id, cvs, jd_service, sim)
    if percentage == PERFECT:
        return success_count == len(cvs)
    elif percentage == GOOD:
        return len(cvs)*0.5 <= success_count < len(cvs)
    elif percentage == MEDIUM:
        return len(cvs)*0.25 <= success_count < len(cvs)*0.5
    elif percentage == POOR:
        return success_count == 0
    elif 0 < percentage < 100:
        return len(cvs)*float(percentage)/100 <= success_count < len(cvs)

def kgr(jd_id, cvs, jd_service, sim):
    sucess_count = 0
    for _rank in ranks(jd_id, cvs, jd_service, sim).values():
        if _rank in FIRST_PAGE:
            sucess_count += 1
    return sucess_count

def ranks(jd_id, cvs, jd_service, sim):
    job_desc = jd_service.get(jd_service.search(jd_id)[0])['description']
    score_board = sim.probability(job_desc)
    ranks_dict = {}
    for cv_id in cvs:
        for _rank, (_c, _s) in enumerate(score_board):
            if cv_id == _c:
                ranks_dict[cv_id] = _rank
    return ranks_dict
