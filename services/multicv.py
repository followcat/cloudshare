class MultiCV(object):

    def __init__(self, projects, repodb, additionals=None):
        self.default = projects[0]
        self.repodb = repodb
        self.projects = dict([tuple([p.name, p]) for p in projects])
        self.projectscv = dict([tuple([p.name, p.curriculumvitae]) for p in projects])
        if additionals is None:
            self.additionals = dict()
        else:
            self.additionals = additionals
        self.svcls = [p.curriculumvitae for p in projects] + self.additionals.values()

    def getproject(self, name=None):
        if name is not None:
            assert name in self.projects
            project = self.projects[name]
        else:
            project = self.default
        return project

    def add_md(self, cvobj, committer=None):
        return self.repodb.add_md(cvobj, committer)

    def modify(self, filename, stream, message=None, committer=None):
        return self.repodb.modify(filename, stream, message, committer)

    def yamls(self, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.cv_yamls()

    def datas(self, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.cv_datas()

    def search(self, keyword, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.cv_search(keyword)

    def search_yaml(self, keyword, projectname=None):
        cvservice = self.getproject(projectname)
        return cvservice.cv_search_yaml(keyword)

    def gethtml(self, id, projectname=None):
        cvservice = self.getproject(projectname)
        try:
            result = cvservice.cv_gethtml(id)
        except IOError:
            for each in self.additionals.values():
                result = each.gethtml(id)
                if result is not None:
                    break
        return result

    def getmd(self, id, projectname=None):
        cvservice = self.getproject(projectname)
        try:
            result = cvservice.cv_getmd(id)
        except IOError:
            for each in self.additionals.values():
                result = each.getmd(id)
                if result is not None:
                    break
        return result

    def getyaml(self, id, projectname=None):
        cvservice = self.getproject(projectname)
        try:
            result = cvservice.cv_getyaml(id)
        except IOError:
            result = None
        if result is None:
            try:
                result = self.repodb.getyaml(id)
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

    def getprjnums(self, projectname):
        result = dict()
        result['total'] = 0
        cvservice = self.getproject(projectname)
        classifies = cvservice.getclassify()
        for svc_cv in self.svcls:
            if svc_cv.name in classifies or svc_cv.name == projectname:
                result[svc_cv.name] = svc_cv.NUMS
                result['total'] += svc_cv.NUMS
        return result
