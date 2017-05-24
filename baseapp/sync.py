import interface.predator
import services.cvstoragesync

from baseapp.datadbs import *


RAW_DIR = 'raw'
RAW_DB = dict()
if os.path.exists(RAW_DIR):
    for name in os.listdir(RAW_DIR):
        namepath = os.path.join(RAW_DIR, name)
        RAW_DB[name] = interface.predator.PredatorInterface(namepath)

SVC_ADD_SYNC = services.cvstoragesync.CVStorageSync(SVC_PEO_STO, SVC_CV_STO, RAW_DB)
