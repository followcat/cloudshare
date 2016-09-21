class MultiCV(object):

    def __init__(self, projects, repodb, additionals=None):
        self.default = projects[0]
        self.repodb = repodb
        self.projects = dict([tuple([p.name, p]) for p in projects])
        if additionals is None:
            self.additionals = dict()
        else:
            self.additionals = additionals
        self.svcls = projects + self.additionals.values()

    def getproject(self, name=None):
        if name is not None:
            assert name in self.projects
            projectcv = self.projects[name]
        projectcv = self.default
        return projectcv

    def add(self, cvobj, committer=None, unique=True, projectname=None):
        result = self.repodb.add(cvobj, committer, unique)
        if result is True and projectname is not None:
            project = self.getproject(projectname)
            project.add(cvobj.filepro.name.base)
        return result

    def add_md(self, cvobj, committer=None):
        return self.repodb.add_md(cvobj, committer)

    def modify(self, filename, stream, message=None, committer=None):
        return self.repodb.modify(filename, stream, message, committer)

    def yamls(self, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.yamls()

    def datas(self, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.datas()

    def search(self, keyword, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.search(keyword)

    def search_yaml(self, keyword, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.search_yaml(keyword)

    def gethtml(self, id, projectname=None):
        cvservice = self.getproject(projectname)
        result = cvservice.gethtml(id)
        if result is None:
            for each in self.additionals.values():
                result = each.gethtml(id)
                if result is not None:
                    break
        return result

    def getmd(self, id, projectname=None):
        cvservice = self.getproject(projectname)
        result = cvservice.getmd(id)
        if result is None:
            for each in self.additionals.values():
                result = each.getmd(id)
                if result is not None:
                    break
        return result

    def getyaml(self, id, projectname=None):
        cvservice = self.getproject(projectname)
        try:
            result = cvservice.getyaml(id)
        except IOError:
            result = None
        if result is None:
            for each in self.additionals.values():
                try:
                    result = each.getyaml(id)
                    if result is not None:
                        break
                except IOError:
                    result = None
        if result is None:
            raise IOError("No yaml file found for id: %s" % id)
        else:
            return result

    def getnums(self):
        result = dict()
        result['total'] = 0
        for svc_cv in self.svcls:
            result[svc_cv.name] = svc_cv.NUMS
            result['total'] += svc_cv.NUMS
        return result
