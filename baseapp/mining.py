import baseapp.loader
import services.mining
from baseapp.datadbs import SVC_CLS_CV
from baseapp.member import SVC_MEMBERS


SVC_MIN = baseapp.loader.load_mining(services.mining.silencer)
baseapp.loader.load_cv_mining(SVC_MIN, SVC_MEMBERS)
