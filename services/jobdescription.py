import glob
import uuid
import os.path

import yaml

import services.base


class JobDescription(services.base.Service):
    """
        >>> import shutil
        >>> import services.company
        >>> import services.jobdescription
        >>> import interface.gitinterface

        >>> repo_name = 'services/test_repo'
        >>> interface = interface.gitinterface.GitInterface(repo_name)

        >>> svc_jd = services.jobdescription.JobDescription(interface)
        >>> svc_jd.add('CompanyA', 'JD-A', 'JD-A description', 'Dever')
        True
        >>> results = svc_jd.search('JD-A')
        >>> data = svc_jd.get(results[0])
        >>> data['description']
        'JD-A description'
        >>> svc_jd.modify(data['id'], 'JD-B description', 'Closed', 'Dever')
        True
        >>> data = svc_jd.get(results[0])
        >>> data['description']
        'JD-B description'
        >>> lists = svc_jd.lists()
        >>> lists[0]['company'], lists[0]['description']
        ('CompanyA', 'JD-B description')
        >>> shutil.rmtree(repo_name)
    """
    path = 'JD'

    def __init__(self, interface, name=None):
        super(JobDescription, self).__init__(interface, name)
        self.repo_path = self.interface.repo.path + "/" + self.path
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    def get(self, name):
        path_name = os.path.join(self.path, name)
        yaml_str = self.interface.get(path_name)
        return yaml.load(yaml_str)

    def add(self, company, name, description, committer, status=None):
        if status is None:
            status = 'Opening'

        id = uuid.uuid1()
        hex_id = id.get_hex()
        data = {
            'name': name,
            'id': hex_id,
            'company': company,
            'description': description,
            'committer': committer,
            'status': status
        }
        filename = self.filename(hex_id)
        file_path = os.path.join(self.repo_path, filename)
        self.interface.add(os.path.join(self.path, filename),
                           yaml.safe_dump(data, allow_unicode=True),
                           "Add job description file: " + filename)
        return True

    def modify(self, hex_id, description, status, committer):
        filename = self.filename(hex_id)
        data = self.get(filename)
        if data['description'] != description and data['committer'] != committer:
            return False
        data['description'] = description
        data['status'] = status
        dump_data = yaml.safe_dump(data, allow_unicode=True)
        self.interface.modify(os.path.join(self.path, filename), dump_data,
                              message="Modify job description: " + filename,
                              committer=committer)
        return True

    def filename(self, hex_id):
        return hex_id + '.yaml'

    def search(self, keyword):
        return self.interface.grep_yaml(keyword, self.path)

    def lists(self):
        results = []
        for pathfile in glob.glob(os.path.join(self.repo_path, '*.yaml')):
            filename = pathfile.split('/')[-1]
            data = self.get(filename)
            results.append(data)
        return results
