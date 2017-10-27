import baseapp.loader
import services.mining
from baseapp.datadbs import SVC_JD_REPO, SVC_CV_REPO
from baseapp.member import SVC_MEMBERS


SVC_MIN = baseapp.loader.load_mining(services.mining.silencer)
baseapp.loader.load_cv_mining(SVC_MIN, SVC_MEMBERS)
baseapp.loader.load_jd_mining(SVC_MIN, [SVC_JD_REPO])
baseapp.loader.load_co_mining(SVC_MIN, [SVC_CV_REPO])
