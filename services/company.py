import os
import time
import yaml

import utils._yaml
import utils.companyexcel
import core.outputstorage
import services.base.storage
import extractor.information_explorer


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

    def datas(self):
        for id in self.ids:
            yield id, self.getyaml(id)

    def compare_excel(self, stream, committer):
        output = list()
        excels = utils.companyexcel.convert(stream)
        for excel in excels:
            metadata = extractor.information_explorer.catch_coinfo(excel, excel['name'])
            data = core.basedata.DataObject(metadata, excel)
            if not self.exists(data.name):
                output.append('add', (data, committer))
        return output
