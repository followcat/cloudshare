import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.simulationcv


class ProjectCV(services.simulationcv.SimulationCV):

    YAML_DIR = "CV"

    YAML_TEMPLATE = (
        ("comment",             []),
        ("tag",                 []),
        ("tracking",            []),
    )

    def __init__(self, interface, repo, name, cvstorage):
        self.interface = interface
        self.repo = repo
        self.path = interface.path
        super(ProjectCV, self).__init__(name, self.path, cvstorage)
        self.cvpath = os.path.join(self.path, self.YAML_DIR)

    def setup(self, classify, committer=None):
        if not os.path.exists(self.cvpath):
            os.makedirs(self.cvpath)
            self.config['classify'] = classify
            self.save()
            self.interface.add_files([os.path.join(self.path, self.config_file),
                                      os.path.join(self.path, self.ids_file)],
                                      message='Create new project %s.'%self.name,
                                      committer=committer)

    def add(self, id, committer):
        result = False
        if not self.exists(id):
            self._add(id)
            info = generate_yaml_template()
            name = core.outputstorage.ConvertName(name).yaml
            utils.builtin.save_yaml(info, self.cvpath, name)
            self.interface.add_files([os.path.join(self.path, self.ids_file),
                                      os.path.join(self.cvpath, name)],
                                      message='Add new cv %s.'%id,
                                      committer=committer)
            result = True
        return result

    def generate_info_template(self):
        info = {}
        for each in self.yaml_template:
            info[each[0]] = each[1]
        return info

    def getinfo(self, id):
        name = core.outputstorage.ConvertName(id).yaml
        return utils.builtin.load_yaml(self.cvpath, name)

    def getyaml(self, id):
        yaml = super(ProjectCV, self).getyaml(id)
        info = self.getinfo(id)
        yaml.update(info)
        return yaml

    def getclassify(self):
        return self.config['classify']

    def updateinfo(self, id, info, message, committer):
        name = core.outputstorage.ConvertName(id).yaml
        utils.builtin.save_yaml(info, self.cvpath, name)
        self.interface.add_files([os.path.join(self.cvpath, name)],
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
        for each in allmd:
            name = core.outputstorage.ConvertName(id).base
            if name in self.cvids:
                result.append(each)
        return result
