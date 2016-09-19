import services.mining
from baseapp.multicv import SVC_CV


LSI_PATH = 'lsimodel'
SVC_MIN = services.mining.Mining(LSI_PATH, SVC_CV)
SVC_MIN.setup('all')
