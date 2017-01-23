    >>> from tests.settings import *
    >>> config = Config()
    >>> config.init_samplecv()
    >>> SVC_PRJ_TEST = config.SVC_PRJ_TEST
    >>> id = list(SVC_PRJ_TEST.cv_ids())[0]
    >>> SVC_PRJ_TEST.cv_updateyaml(id, 'name', 'modified', 'dev')
    {'name': 'modified'}
    >>> config.destory()
