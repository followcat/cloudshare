import glob
import uuid
import os.path

import yaml

import utils.builtin
import services.exception


class JobDescription(object):
    """
        >>> import shutil
        >>> import utils.builtin
        >>> import services.company
        >>> import services.jobdescription
        >>> import interface.gitinterface
        
        >>> repo_name = 'webapp/views/test_repo'
        >>> interface = interface.gitinterface.GitInterface(repo_name)
        >>> company_ser = services.company.Company(interface)
        >>> company_ser.add('CompanyA', 'This is Co.A', 'Dever')
        True

        >>> repo_ser = services.jobdescription.JobDescription(interface, company_ser)
        >>> repo_ser.add('CompanyA', 'JD-A', 'JD-A description', 'Dever')
        True
        >>> results = repo_ser.search('JD-A')
        >>> data = utils.builtin.load_yaml(repo_ser.repo_path, results[0])
        >>> data['description']
        'JD-A description'
        >>> repo_ser.modify(data['id'], 'JD-B description', 'Dever')
        True
        >>> data = utils.builtin.load_yaml(repo_ser.repo_path, results[0])
        >>> data['description']
        'JD-B description'
        >>> lists = repo_ser.lists()
        >>> lists[0]['company'], lists[0]['description']
        ('CompanyA', 'JD-B description')
        >>> shutil.rmtree(repo_name)
    """
    path = 'JD'

    def __init__(self, repo, svc_co):
        self.repo = repo
        self.repo_path = self.repo.repo.path + "/" + self.path
        self.svc_co = svc_co
        self.info = ""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    def add(self, company, name, description, committer):
        try:
            self.svc_co.company(company)
        except services.exception.NotExistsCompany:
            self.info = "NotExistsCompany."
            return False

        id = uuid.uuid1()
        hex_id = id.get_hex()
        data = {
            'name': name,
            'id': hex_id,
            'company': company,
            'description': description,
            'committer': committer
        }
        filename = self.filename(hex_id)
        file_path = os.path.join(self.repo_path, filename)
        with open(file_path, 'w') as f:
            f.write(yaml.dump(data))
        self.repo.add_files(os.path.join(self.path, filename),
                            "Add job description file: " + filename)
        return True

    def modify(self, hex_id, description, committer):
        filename = self.filename(hex_id)
        data = utils.builtin.load_yaml(self.repo_path, filename)
        if data['committer'] != committer:
            return False
        data['description'] = description
        dump_data = yaml.dump(data)
        self.repo.modify(os.path.join(self.path, filename), dump_data,
                         message="Modify job description: " + filename,
                         committer=committer)
        return True

    def filename(self, hex_id):
        return hex_id + '.yaml'

    def search(self, keyword):
        return self.repo.grep_yaml(keyword, self.path)

    def lists(self):
        results = []
        for pathfile in glob.glob(os.path.join(self.repo_path, '*.yaml')):
            filename = pathfile.split('/')[-1]
            data = utils.builtin.load_yaml(self.repo_path, filename)
            results.append(data)
        return results
