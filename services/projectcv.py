import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.company
import services.exception
import services.simulationcv
import services.jobdescription


class ProjectCV(services.simulationcv.SimulationCV):

    config_file = 'config.yaml'

    def __init__(self, interface, repo, name):
        super(ProjectCV, self).__init__(interface.path, repo, interface)
        self.name = name
        self.interface = interface
        self.repo = repo
        self.path = interface.path
        self.company = services.company.Company(interface)
        self.jobdescription = services.jobdescription.JobDescription(interface)
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        self.config = utils.builtin.load_yaml(self.path, self.config_file)
        super(ProjectCV, self).load()

    def save(self):
        utils.builtin.save_yaml(self.config, self.path, self.config_file,
                                default_flow_style=False)
        super(ProjectCV, self).save()

    def setup(self, classify, committer=None):
        if not os.path.exists(self.path):
            self.update(classify, committer)

    def update(self, classify, committer=None):
        self.config['classify'] = [c for c in classify if c in sources.industry_id.industryID]
        self.save()

    def add(self, id, committer):
        return super(ProjectCV, self).add(id, committer, yamlfile=True)

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        return self.repo.gethtml(veren)

    def getclassify(self):
        return self.config['classify']

    def search(self, keyword):
        results = set()
        allfile = self.repo.search(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            if id in self.cvids:
                results.add(id)
        return results

    def search_yaml(self, keyword):
        results = set()
        allfile = self.interface.grep(keyword, self.YAML_DIR)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def company_add(self, name, introduction, committer):
        return self.company.add(name, introduction, committer)

    def company_get(self, name):
        return self.company.company(name)

    def company_names(self):
        return self.company.names()

    def jd_get(self, hex_id):
        return self.jobdescription.get(hex_id)

    def jd_add(self, company, name, description, committer, status=None):
        try:
            self.company_get(company)
        except services.exception.NotExistsCompany:
            return False
        return self.jobdescription.add(company, name, description, committer, status)

    def jd_modify(self, hex_id, description, status, committer):
        return self.jobdescription.modify(hex_id, description, status, committer)

    def jd_search(self, keyword):
        return self.jobdescription.search(keyword)

    def jd_lists(self):
        return self.jobdescription.lists()
