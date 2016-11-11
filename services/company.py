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
        >>> repo_name = 'services/test_repo'
        >>> interface = interface.gitinterface.GitInterface(repo_name)
        >>> svc_co = services.company.Company(interface.path)
        >>> name, committer, introduction = 'CompanyA', 'tester', 'This is Co.A'
        >>> metadata = { 'name': name, 'committer': committer, 'introduction': introduction,}
        >>> coobj = core.basedata.DataObject(name, introduction, metadata)
        >>> svc_co.add(coobj, 'Dever')
        True
        >>> co = svc_co.getyaml('CompanyA')
        >>> co['name']
        'CompanyA'
        >>> co['introduction']
        'This is Co.A'
        >>> svc_co.add(coobj, 'Dever') # doctest: +ELLIPSIS
        False
        >>> list(svc_co.ids)
        ['CompanyA']
        >>> svc_co.getyaml('CompanyB') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        NotExistsCompany
        >>> shutil.rmtree(repo_name)
    """
    CO_DIR = 'CO'
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
