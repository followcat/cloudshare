import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.company
import services.exception
import services.simulationcv
import services.jobdescription


class ProjectCV(object):

    config_file = 'config.yaml'

    def __init__(self, interface, repo, name):
        self.name = name
        self.interface = interface
        self.repo = repo
        self.path = interface.path
        self.curriculumvitae = services.simulationcv.SimulationCV(name, interface.path,
                                                                  repo, interface)
        self.company = services.company.Company(interface)
        self.jobdescription = services.jobdescription.JobDescription(interface)
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        self.config = utils.builtin.load_yaml(self.path, self.config_file)

    def save(self):
        utils.builtin.save_yaml(self.config, self.path, self.config_file,
                                default_flow_style=False)

    def setup(self, classify, committer=None):
        if not os.path.exists(self.path):
            self.update(classify, committer)

    def update(self, classify, committer=None):
        self.config['classify'] = [c for c in classify if c in sources.industry_id.industryID]
        self.save()

    def add(self, id, committer):
        return super(ProjectCV, self).add(id, committer, yamlfile=True)

    def getclassify(self):
        return self.config['classify']

    def cv_add(self, id):
        return self.curriculumvitae.add(id, committer, yamlfile=True)

    def cv_yamls(self):
        return self.curriculumvitae.yamls()

    def cv_names(self):
        return self.curriculumvitae.names()

    def cv_datas(self):
        return self.curriculumvitae.datas()

    def cv_search(self, keyword):
        return self.curriculumvitae.search(keyword)

    def cv_search_yaml(self, keyword):
        return self.curriculumvitae.search_yaml(keyword)

    def cv_gethtml(self, id):
        return self.curriculumvitae.gethtml(id)

    def cv_getmd(self, id):
        return self.curriculumvitae.getmd(id)

    def cv_getmd_en(self, id):
        return self.curriculumvitae.getmd_en(id)

    def cv_getyaml(self, id):
        return self.curriculumvitae.getyaml(id)

    def cv_numbers(self):
        return self.curriculumvitae.NUMS

    def cv_history(self, author=None, entries=10, skip=0):
        return self.curriculumvitae.history(author, entries, skip)

    def cv_updateyaml(self, id, key, value, userid):
        return self.curriculumvitae.updateinfo(id, key, value, userid)

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
