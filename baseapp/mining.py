import baseapp.loader
import services.mining
from baseapp.multicv import SVC_MULT_CV


SVC_CUTWORD, SVC_MIN = baseapp.loader.load_mining(SVC_MULT_CV, services.mining.silencer)
