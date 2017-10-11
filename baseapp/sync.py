import time
import functools

import interface.predator
import services.cvstoragesync

from baseapp.index import *
from baseapp.datadbs import *
from baseapp.loader import config


RAW_DB = dict()
if os.path.exists(config.storage_config['RAW']):
    for name in os.listdir(config.storage_config['RAW']):
        namepath = os.path.join(config.storage_config['RAW'], name)
        RAW_DB[name] = interface.predator.PredatorInterface(namepath, name=name)

SVC_ADD_SYNC = services.cvstoragesync.CVStorageSync(SVC_PEO_STO, SVC_CV_STO, RAW_DB)
lastday = SVC_INDEX.lastday()
lastdate = time.mktime(time.strptime(lastday, "%Y%m%d"))
update_bydate = functools.partial(services.cvstoragesync.update_bydate, lastdate=lastdate)
