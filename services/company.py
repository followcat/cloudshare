import os
import time
import yaml

import utils._yaml
import core.outputstorage
import services.exception
import services.base.storage


class Company(services.base.storage.BaseStorage):
    """
        >>> import shutil
        >>> import services.company
        >>> import core.basedata
        >>> import interface.gitinterface
        >>> import extractor.information_explorer
        >>> repo_name = 'services/test_repo'
        >>> interface = interface.gitinterface.GitInterface(repo_name)
        >>> svc_co = services.company.Company(interface.path)
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
        NotExistsCompany
        >>> shutil.rmtree(repo_name)
    """
    commitinfo = 'Company'

    def getyaml(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        try:
            yaml_str = self.interface.get(name)
            if yaml_str is None:
                raise IOError
        except IOError:
            raise services.exception.NotExistsCompany
        return yaml.load(yaml_str, Loader=utils._yaml.SafeLoader)
