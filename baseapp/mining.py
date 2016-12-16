import os

import services.mining
import services.analysis.cutword
from baseapp.multicv import SVC_MULT_CV


LSI_PATH = 'lsimodel'
CUTWORD_PATH = 'cutwords'
SVC_CUTWORD = services.analysis.cutword.Cutword(CUTWORD_PATH)
SVC_MIN = services.mining.Mining(LSI_PATH, SVC_MULT_CV)
SVC_MIN.setup()
