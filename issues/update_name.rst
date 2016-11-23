    >>> from tests.settings import *
    >>> config = Config()
    >>> config.init_samplecv()
    >>> SVC_PRJ_MED = config.SVC_PRJ_MED
    >>> id = list(SVC_PRJ_MED.cv_ids())[0]
    >>> SVC_PRJ_MED.cv_updateyaml(id, 'name', 'modified', 'dev')
    {'name': 'modified'}
    >>> config.destory()
