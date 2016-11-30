import os
import time
import yaml

import utils._yaml
import core.outputstorage
import services.base.storage


class Company(services.base.storage.BaseStorage):
    """
        >>> import shutil
        >>> import services.company
        >>> import core.basedata
        >>> import interface.gitinterface
        >>> import extractor.information_explorer
        >>> DIR = 'services/test_repo'
        >>> svc_co = services.company.Company(DIR)
        >>> name, committer, introduction = 'CompanyA', 'tester', 'This is Co.A'
        >>> metadata = extractor.information_explorer.catch_coinfo({'introduction': introduction,}, name)
        >>> coobj = core.basedata.DataObject(metadata, data=introduction)
        >>> svc_co.add(coobj, 'Dever')
        True
        >>> co = svc_co.getyaml(metadata['id'])
        >>> co['name']
        'CompanyA'
        >>> co['introduction']
        'This is Co.A'
        >>> svc_co.add(coobj, 'Dever') # doctest: +ELLIPSIS
        False
        >>> list(svc_co.ids)
        ['4de25a98bc371bf87220e500215317f4b2c24933']
        >>> svc_co.getyaml('CompanyB') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        IOError...
        >>> shutil.rmtree(DIR)
    """
    commitinfo = 'Company'
