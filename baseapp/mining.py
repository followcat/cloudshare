import baseapp.loader
import services.mining
from baseapp.datadbs import SVC_CLS_CV
from baseapp.customer import SVC_CUSTOMERS


SVC_CUTWORD, SVC_MIN = baseapp.loader.load_mining(SVC_CUSTOMERS, SVC_CLS_CV, services.mining.silencer)
