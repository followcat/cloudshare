import os
import time

import utils.issue
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
        ("committer",           list),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
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
            self.update(classify, committer)

    def update(self, classify, committer=None):
        if not os.path.exists(self.cvpath):
            os.makedirs(self.cvpath)
        self.config['classify'] = [c for c in classify if c in sources.industry_id.industryID]
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
            utils.builtin.save_json(sorted(self.cvids), self.path, self.ids_file,
                                    indent=4)
            self.interface.add_files([bytes(self.ids_file),
                                      bytes(os.path.join(self.YAML_DIR, name))],
                                      message='Add new cv %s.'%id,
                                      committer=committer)
            result = True
        return result

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        return self.repo.gethtml(veren)

    def getinfo(self, id):
        if not self.exists(id):
            return None
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

    def saveinfo(self, id, info, message, committer):
        name = core.outputstorage.ConvertName(id).yaml
        utils.builtin.save_yaml(info, self.cvpath, name)
        self.interface.add_files([bytes(os.path.join(self.YAML_DIR, name))],
                                  message=message, committer=committer)

    @utils.issue.fix_issue('issues/update_name.rst')
    def updateinfo(self, id, key, value, committer):
        data = None
        projectinfo = self.getinfo(id)
        baseinfo = self.getyaml(id)
        if projectinfo is not None and (key in projectinfo or key in baseinfo):
            data = { key: value }
            if key == 'tag':
                data = self.addtag(id, value, committer)
            elif key == 'tracking':
                data = self.addtracking(id, value, committer)
            elif key == 'comment':
                data = self.addcomment(id, value, committer)
            else:
                projectinfo[key] = value
                self.saveinfo(id, projectinfo,
                              'Update %s key %s.' % (id, key), committer)
        return data

    def _infoframe(self, value, username):
        data = {'author': username,
                'content': value,
                'date': time.strftime('%Y-%m-%d %H:%M:%S')}
        return data

    def addtag(self, id, tag, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(tag, committer)
        info['tag'].insert(0, data)
        self.saveinfo(id, info, 'Add %s tag.'%id, committer)
        return data

    def addcomment(self, id, comment, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(comment, committer)
        info['comment'].insert(0, data)
        self.saveinfo(id, info, 'Add %s comment.'%id, committer)
        return data

    def addtracking(self, id, tracking, committer):
        assert self.exists(id)
        info = self.getinfo(id)
        data = self._infoframe(tracking, committer)
        info['tracking'].insert(0, data)
        self.saveinfo(id, info, 'Add %s tracking.'%id, committer)
        return data

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
