import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.base.service
import services.simulationcv
import services.simulationco
import services.jobdescription


class Project(services.base.service.Service):

    CV_PATH = 'CV'
    CO_PATH = 'CO'
    JD_PATH = 'JD'
    config_file = 'config.yaml'

    def __init__(self, path, corepo, cvrepo, name, iotype='git'):
        super(Project, self).__init__(path, name, iotype)
        self.path = path
        self.corepo = corepo
        self.cvrepo = cvrepo
        cvpath = os.path.join(path, self.CV_PATH)
        copath = os.path.join(path, self.CO_PATH)
        jdpath = os.path.join(path, self.JD_PATH)
        idsfile = os.path.join(cvpath, services.simulationcv.SimulationCV.ids_file)
        self.curriculumvitae = services.simulationcv.SimulationCV.autoservice(
                                                        cvpath, name, cvrepo)
        self.company = services.simulationco.SimulationCO.autoservice(
                                                        copath, name, corepo)
        self.jobdescription = services.jobdescription.JobDescription(jdpath)
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

    def setup(self, classify, committer=None, config=None):
        if config is None:
            config = {}
        if not os.path.exists(os.path.join(self.path, self.config_file)):
            self.update(classify, committer)
        self.config.update(config)
        self.save()

    def update(self, classify, committer=None):
        self.config['classify'] = [c for c in classify if c in sources.industry_id.industryID]
        self.save()

    def getclassify(self):
        return self.config['classify']

    def cv_add(self, cvobj, committer=None, unique=True):
        return self.curriculumvitae.add(cvobj, committer, unique)

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

    def cv_deleteyaml(self, id, key, value, userid, date):
        return self.curriculumvitae.deleteinfo(id, key, value, userid, date)

    def cv_ids(self):
        return self.curriculumvitae.ids

    def cv_timerange(self, start_y, start_m, start_d, end_y, end_m, end_d):
        return self.curriculumvitae.timerange(start_y, start_m, start_d,
                                              end_y, end_m, end_d)

    def company_add(self, coobj, committer=None, unique=True, yamlfile=True, mdfile=False):
        self.corepo.add(coobj, committer, unique, yamlfile, mdfile)
        self.company.add(coobj, committer, unique, yamlfile, mdfile)
        return self.company.addcustomer(coobj.name, committer)

    def company_get(self, name):
        return self.company.getyaml(name)

    def company_customers(self):
        return self.company.customers

    def company_names(self):
        return self.company.ids

    def jd_get(self, hex_id):
        return self.jobdescription.get(hex_id)

    def jd_add(self, company, name, description, committer, status=None):
        try:
            self.company_get(company)
        except IOError:
            return False
        return self.jobdescription.add(company, name, description, committer, status)

    def jd_modify(self, hex_id, description, status, committer):
        return self.jobdescription.modify(hex_id, description, status, committer)

    def jd_search(self, keyword):
        return self.jobdescription.search(keyword)

    def jd_lists(self):
        return self.jobdescription.lists()

    def backup(self, path, bare=True):
        project_path = os.path.join(path, 'project')
        cv_path = os.path.join(path, 'curriculumvitae')
        jd_path = os.path.join(path, 'jobdescription')
        co_path = os.path.join(path, 'company')
        utils.builtin.assure_path_exists(project_path)
        utils.builtin.assure_path_exists(cv_path)
        utils.builtin.assure_path_exists(jd_path)
        utils.builtin.assure_path_exists(co_path)
        self.interface.backup(project_path, bare=bare)
        self.curriculumvitae.backup(cv_path, bare=bare)
        self.jobdescription.backup(jd_path, bare=bare)
        self.company.backup(co_path, bare=bare)
