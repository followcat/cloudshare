import os

import yaml

import services.base
import services.exception


class Company(services.base.Service):
    """
        >>> import shutil
        >>> import services.company
        >>> import interface.gitinterface
        >>> repo_name = 'services/test_repo'
        >>> interface = interface.gitinterface.GitInterface(repo_name)
        >>> svc_co = services.company.Company(interface)
        >>> svc_co.COMPANYS
        []
        >>> svc_co.add('CompanyA', 'This is Co.A', 'Dever')
        True
        >>> co = svc_co.company('CompanyA')
        >>> co['name']
        'CompanyA'
        >>> co['introduction']
        'This is Co.A'
        >>> svc_co.add('CompanyA', 'This is Co.A', 'Dever') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ExistsCompany: CompanyA
        >>> svc_co.names()
        ['CompanyA']
        >>> svc_co.company('CompanyB') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        NotExistsCompany
        >>> shutil.rmtree(repo_name)
    """
    company_filename = 'company.yaml'
    path = 'CO'

    def __init__(self, interface, name=None):
        super(Company, self).__init__(interface, name)
        self.repo_path = self.interface.repo.path + "/" + self.path
        self.file_path = os.path.join(self.path, self.company_filename)
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    @property
    def COMPANYS(self):
        data = self.interface.get(self.file_path)
        if data is None:
            self.create()
            data = self.interface.get(self.file_path)
        return yaml.load(data)

    def create(self):
        empty_list = []
        self.interface.add(self.file_path,
                           yaml.safe_dump(empty_list, allow_unicode=True),
                           "Add company file.")

    def add(self, name, committer):
        companys = self.COMPANYS
        for company in companys:
            if company['name'] == name:
                raise services.exception.ExistsCompany(name)
        data = {
            'name': name,
            'committer': committer,
        }
        companys.append(data)
        dump_data = yaml.safe_dump(companys, allow_unicode=True)
        message = "Add company: " + name
        self.interface.modify(os.path.join(self.path, self.company_filename),
                              dump_data, message=message.encode('utf-8'),
                              committer=committer)
        return True

    def company(self, name):
        result = None
        companys = self.COMPANYS
        for company in companys:
            if company['name'] == name:
                result = company
                break
        else:
            raise services.exception.NotExistsCompany
        return result

    def names(self):
        names = [company['name'] for company in self.COMPANYS]
        return names
