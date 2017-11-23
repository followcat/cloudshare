import glob
import uuid
import os.path

import yaml

import core.outputstorage
import services.base.storage


class JobDescription(services.base.storage.BaseStorage):
    """
        >>> import shutil
        >>> import services.jobdescription

        >>> repo_name = 'services/test_repo'
        >>> svc_jd = services.jobdescription.JobDescription(repo_name)
        >>> svc_jd.add('CompanyA', 'JD-A', 'JD-A description', 'Dever')
        True
        >>> results = svc_jd.search('JD-A')
        >>> data = svc_jd.get(results[0][0])
        >>> data['description']
        'JD-A description'
        >>> svc_jd.modify(data['id'], 'JD-B description', 'Closed', '', '', 'Dever')
        True
        >>> data = svc_jd.get(results[0][0])
        >>> data['description']
        'JD-B description'
        >>> lists = svc_jd.lists()
        >>> lists[0]['company'], lists[0]['description']
        ('CompanyA', 'JD-B description')
        >>> svc_jd.add('CompanyC', 'JD-C', 'JD-C description', 'Dever',
        ...     commentary='this is JD-C commentary', followup='JD-C followup')
        True
        >>> results = svc_jd.search('JD-C')
        >>> data = svc_jd.get(results[0][0])
        >>> data['description'], data['commentary']
        ('JD-C description', 'this is JD-C commentary')
        >>> svc_jd.modify(data['id'], 'JD-C description', 'Opening',
        ...     'this is UPDATED JD-C commentary', 'UPDATED JD-C followup', 'Dever')
        True
        >>> data = svc_jd.get(results[0][0])
        >>> data['description'], data['commentary'], data['followup']
        ('JD-C description', 'this is UPDATED JD-C commentary', 'UPDATED JD-C followup')
        >>> shutil.rmtree(repo_name)
    """

    def get(self, hex_id):
        name = self.filename(hex_id)
        yaml_str = self.interface.get(name)
        return yaml.load(yaml_str)

    def add(self, company, name, description, committer, status=None,
            commentary='', followup=''):
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
            'commentary': commentary,
            'followup': followup,
            'status': status
        }
        filename = self.filename(hex_id)
        self.interface.add(filename,
                           yaml.safe_dump(data, allow_unicode=True),
                           "Add job description file: " + filename)
        return True

    def modify(self, hex_id, description, status, commentary, followup, committer):
        data = self.get(hex_id)
        if data['description'] != description and data['committer'] != committer:
            return False
        filename = self.filename(hex_id)
        data['status'] = status
        data['description'] = description
        data['commentary'] = commentary
        data['followup'] = followup
        dump_data = yaml.safe_dump(data, allow_unicode=True)
        self.interface.modify(filename, dump_data,
                              message="Modify job description: " + filename,
                              committer=committer)
        return True

    def filename(self, hex_id):
        output = core.outputstorage.ConvertName(hex_id)
        return output.yaml

    def search(self, keyword):
        results = self.interface.search_yaml(keyword)
        return results

    def lists(self):
        results = []
        for pathfile in glob.glob(os.path.join(self.path, '*.yaml')):
            filename = pathfile.split('/')[-1]
            hex_id = os.path.splitext(filename)[0]
            data = self.get(hex_id)
            results.append(data)
        return results
