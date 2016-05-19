import os

import yaml

import services.exception


class Company(object):
    """
        >>> import shutil
        >>> import services.company
        >>> import interface.gitinterface
        >>> repo_name = 'webapp/views/test_repo'
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

    def __init__(self, repo):
        self.repo = repo
        self.repo_path = self.repo.repo.path + "/" + self.path
        self.file_path = os.path.join(self.repo_path, self.company_filename)
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    @property
    def COMPANYS(self):
        company_file = self.repo.repo.get_named_file(
            os.path.join('..', self.path, self.company_filename))
        if company_file is None:
            self.create()
            company_file = self.repo.repo.get_named_file(
                os.path.join('..', self.path, self.company_filename))
        data = yaml.load(company_file.read())
        company_file.close()
        return data

    def create(self):
        empty_list = []
        with open(self.file_path, 'w') as f:
            f.write(yaml.dump(empty_list))
        self.repo.add_files(self.file_path, "Add company file.")

    def add(self, name, introduction, committer):
        companys = self.COMPANYS
        for company in companys:
            if company['name'] == name:
                raise services.exception.ExistsCompany(name)
        data = {
            'name': name,
            'committer': committer,
            'introduction': introduction,
        }
        companys.append(data)
        dump_data = yaml.dump(companys)
        message = "Add company: " + name
        self.repo.modify(os.path.join(self.path, self.company_filename),
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
