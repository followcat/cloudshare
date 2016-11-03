import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.base
import services.company
import services.exception
import services.simulationcv
import services.curriculumvitae
import services.jobdescription


class Project(services.base.Service):

    config_file = 'config.yaml'

    def __init__(self, path, corepo, cvrepo, name, iotype='git'):
        super(Project, self).__init__(path, name, iotype)
        self.path = path
        if os.path.exists(os.path.join(path,
                          services.simulationcv.SimulationCV.YAML_DIR)) and not (
        os.path.exists(os.path.join(path,
                       services.simulationcv.SimulationCV.ids_file))):
            self.curriculumvitae = services.curriculumvitae.CurriculumVitae(self.path)
        else:
            self.curriculumvitae = services.simulationcv.SimulationCV(name, path,
                                                                      cvrepo, self.interface)
        self.company = corepo
        self.jobdescription = services.jobdescription.JobDescription(path)
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
        if not os.path.exists(os.path.join(self.path, self.config_file)):
            self.update(classify, committer)

    def update(self, classify, committer=None):
        self.config['classify'] = [c for c in classify if c in sources.industry_id.industryID]
        self.save()

    def getclassify(self):
        return self.config['classify']

    def cv_add(self, cvobj, committer=None, unique=True, yamlfile=True):
        return self.curriculumvitae.add(cvobj, committer, unique, yamlfile)

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

    def cv_ids(self):
        return self.curriculumvitae.cvids

    def company_add(self, cvobj, committer=None, unique=True, yamlfile=True):
        return self.company.add(cvobj, committer, unique, yamlfile)

    def company_get(self, name):
        return self.company.getyaml(name)

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
