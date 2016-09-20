import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.company
import services.exception
import services.simulationcv
import services.jobdescription


class ProjectCV(services.simulationcv.SimulationCV):

    YAML_DIR = "CV"

    YAML_TEMPLATE = (
        ("committer",           []),
        ("comment",             []),
        ("tag",                 []),
        ("tracking",            []),
    )

    def __init__(self, interface, repo, name):
        super(ProjectCV, self).__init__(name, interface.path, repo)
        self.interface = interface
        self.repo = repo
        self.path = interface.path
        self.cvpath = os.path.join(self.path, self.YAML_DIR)
        self.company = services.company.Company(interface)
        self.jobdescription = services.jobdescription.JobDescription(interface)
        try:
            self.load()
        except IOError:
            pass

    def setup(self, classify, committer=None):
        if not os.path.exists(self.cvpath):
            os.makedirs(self.cvpath)
            self.config['classify'] = classify
            self.save()
            self.interface.add_files([bytes(self.config_file), bytes(self.ids_file)],
                                      message='Create new project %s.'%self.name,
                                      committer=committer)

    def add(self, id, committer):
        result = False
        if not self.exists(id):
            self._add(id)
            info = self.generate_info_template()
            info['committer'] = committer
            name = core.outputstorage.ConvertName(id).yaml
            utils.builtin.save_yaml(info, self.cvpath, name)
            self.interface.add_files([bytes(self.ids_file),
                                      bytes(os.path.join(self.YAML_DIR, name))],
                                      message='Add new cv %s.'%id,
                                      committer=committer)
            result = True
        return result

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]
        return info

    def getinfo(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        return utils.builtin.load_yaml(self.cvpath, name)

    def getyaml(self, id):
        yaml = super(ProjectCV, self).getyaml(id)
        if yaml is not None:
            info = self.getinfo(id)
            yaml.update(info)
        return yaml

    def getclassify(self):
        return self.config['classify']

    def updateinfo(self, id, info, message, committer):
        name = core.outputstorage.ConvertName(id).yaml
        utils.builtin.save_yaml(info, self.cvpath, name)
        self.interface.add_files([bytes(os.path.join(self.YAML_DIR, name))],
                                  message=message, committer=committer)

    def addtag(self, id, tag, committer):
        info = self.getinfo(id)
        info['tag'].append(tag)
        self.updateinfo(id, info, 'Add %s tag.'%id, committer)

    def addcomment(self, id, comment, committer):
        info = self.getinfo(id)
        info['comment'].append(comment)
        self.updateinfo(id, info, 'Add %s comment.'%id, committer)

    def addtracking(self, id, tracking, committer):
        info = self.getinfo(id)
        info['tracking'].append(tracking)
        self.updateinfo(id, info, 'Add %s tracking.'%id, committer)

    def search(self, keyword):
        allmd = self.repo.search(keyword)
        result = []
        for md in allmd:
            name = core.outputstorage.ConvertName(md).base
            if name in self.cvids:
                result.append(md)
        return result

    def search_yaml(self, keyword):
        results = self.interface.grep_yaml(keyword, self.YAML_DIR)
        return results

    def company_add(self, name, introduction, committer):
        return self.company.add(name, introduction, committer)

    def company_get(self, name):
        return self.company.company(name)

    def company_names(self):
        return self.company.names()

    def jd_get(self, name):
        return self.jobdescription.get(name)

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
