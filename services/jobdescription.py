import glob
import uuid
import os.path

import yaml

import services.base.service


class JobDescription(services.base.service.Service):
    """
        >>> import shutil
        >>> import services.company
        >>> import services.jobdescription
        >>> import interface.gitinterface

        >>> repo_name = 'services/test_repo'
        >>> interface = interface.gitinterface.GitInterface(repo_name)

        >>> svc_jd = services.jobdescription.JobDescription(interface.path)
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

    def __init__(self, interface, name=None):
        super(JobDescription, self).__init__(interface, name)
        self.path = self.interface.path

    def get(self, hex_id):
        name = self.filename(hex_id)
        yaml_str = self.interface.get(name)
        return yaml.load(yaml_str)

    def add(self, company, name, description, committer, status=None, do_commit=True):
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
        self.interface.add(filename,
                           yaml.safe_dump(data, allow_unicode=True),
                           "Add job description file: " + filename, do_commit=do_commit)
        return True

    def modify(self, hex_id, description, status, committer, do_commit=True):
        data = self.get(hex_id)
        if data['description'] != description and data['committer'] != committer:
            return False
        filename = self.filename(hex_id)
        data['status'] = status
        data['description'] = description
        dump_data = yaml.safe_dump(data, allow_unicode=True)
        self.interface.modify(filename, dump_data,
                              message="Modify job description: " + filename,
                              committer=committer, do_commit=do_commit)
        return True

    def filename(self, hex_id):
        return hex_id + '.yaml'

    def search(self, keyword):
        results = list()
        for name in self.interface.grep_yaml(keyword):
            results.append(os.path.splitext(name)[0])
        return results

    def lists(self):
        results = []
        for pathfile in glob.glob(os.path.join(self.path, '*.yaml')):
            filename = pathfile.split('/')[-1]
            hex_id = os.path.splitext(filename)[0]
            data = self.get(hex_id)
            results.append(data)
        return results
