import baseapp.loader
import services.mining
from baseapp.datadbs import SVC_CLS_CV
from baseapp.member import SVC_MEMBERS


SVC_CUTWORD, SVC_MIN = baseapp.loader.load_mining(SVC_MEMBERS, SVC_CLS_CV, services.mining.silencer)
