    >>> from tests.settings import *
    >>> config.init_samplecv()
    >>> SVC_PRJ_MED = config.SVC_PRJ_MED
    >>> id = list(SVC_PRJ_MED.cvids)[0]
    >>> SVC_PRJ_MED.updateinfo(id, 'name', 'modified', 'dev')
    {'name': 'modified'}
    >>> config.destory()
