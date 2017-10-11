import glob
import uuid
import os.path

import yaml

import core.outputstorage
import services.base.storage


class JobDescription(services.base.storage.BaseStorage):

    commitinfo = 'JobDescription'

    YAML_TEMPLATE = (
        ("name",            str),
        ("id",              str),
        ("company",         str),
        ("description",     str),
        ("committer",       str),
        ("commentary",      str),
        ("followup",        str),
        ("status",          str),
    )

    def __init__(self, path, name=None, searchengine=None, iotype=None):
        """
            >>> import shutil
            >>> import services.jobdescription

            >>> path = 'services/test_repo'

            >>> svc_jd = services.jobdescription.JobDescription(path, 'testjd')
            >>> svc_jd.add('CompanyA', 'JD-A', 'JD-A description', 'Dever')
            True
            >>> results = list(svc_jd.search('JD-A'))
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description']
            'JD-A description'
            >>> svc_jd.modify(data['id'], 'JD-B description', 'Closed', '', '', 'Dever')
            True
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description']
            'JD-B description'
            >>> lists = list(svc_jd.datas())
            >>> lists[0][1]['company'], lists[0][1]['description']
            ('CompanyA', 'JD-B description')
            >>> svc_jd.add('CompanyC', 'JD-C', 'JD-C description', 'Dever',
            ...     commentary='this is JD-C commentary', followup='JD-C followup')
            True
            >>> results = list(svc_jd.search('JD-C'))
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description'], data['commentary']
            ('JD-C description', 'this is JD-C commentary')
            >>> svc_jd.modify(data['id'], 'JD-C description', 'Opening',
            ...     'this is UPDATED JD-C commentary', 'UPDATED JD-C followup', 'Dever')
            True
            >>> data = svc_jd.getyaml(results[0][0])
            >>> data['description'], data['commentary'], data['followup']
            ('JD-C description', 'this is UPDATED JD-C commentary', 'UPDATED JD-C followup')
            >>> shutil.rmtree(path)
        """
        super(JobDescription, self).__init__(path, name=name,
                                             searchengine=searchengine, iotype=iotype)
        self.path = path

    def add(self, company, name, description, committer, status=None,
            commentary='', followup=''):
        if status is None:
            status = 'Opening'

        id = uuid.uuid1().get_hex()
        data = {
            'name': name,
            'id': id,
            'company': company,
            'description': description,
            'committer': committer,
            'commentary': commentary,
            'followup': followup,
            'status': status
        }
        name = core.outputstorage.ConvertName(id)
        self.interface.add(name.yaml, yaml.safe_dump(data, allow_unicode=True),
                           "Add job description file: " + name)
        return True

    def modify(self, id, description, status, commentary, followup, committer):
        data = self.getyaml(id)
        if data['description'] != description and data['committer'] != committer:
            return False
        data['status'] = status
        data['description'] = description
        data['commentary'] = commentary
        data['followup'] = followup
        dump_data = yaml.safe_dump(data, allow_unicode=True)
        name = core.outputstorage.ConvertName(id)
        super(JobDescription, self).modify(name.yaml, dump_data,
                                           message="Modify job description: " + name,
                                           committer=committer)
        return True

    def datas(self):
        for id in self.ids:
            result = self.getyaml(id)
            yield id, result
