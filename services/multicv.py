class MultiCV(object):

    def __init__(self, projects, additionals=None):
        self.default = projects[0]
        self.projects = dict([tuple([p.name, p]) for p in projects])
        if additionals is None:
            self.additionals = dict()
        else:
            self.additionals = additionals
        self.svcls = projects + self.additionals.values()

    def add(self, *args, **kwargs):
        return self.default.add(*args, **kwargs)

    def add_md(self, *args, **kwargs):
        return self.default.add_md(*args, **kwargs)

    def modify(self, *args, **kwargs):
        return self.default.modify(*args, **kwargs)

    def yamls(self, *args, **kwargs):
        return self.default.yamls(*args, **kwargs)

    def datas(self, *args, **kwargs):
        return self.default.datas(*args, **kwargs)

    def search(self, *args, **kwargs):
        return self.default.search(*args, **kwargs)

    def search_yaml(self, *args, **kwargs):
        return self.default.search_yaml(*args, **kwargs)

    def history(self, *args, **kwargs):
        return self.default.interface.history(*args, **kwargs)

    def gethtml(self, id):
        result = self.default.gethtml(id)
        if result is None:
            for each in self.svcls:
                result = each.gethtml(id)
                if result is not None:
                    break
        return result

    def getmd(self, id):
        result = self.default.getmd(id)
        if result is None:
            for each in self.svcls:
                result = each.getmd(id)
                if result is not None:
                    break
        return result

    def getyaml(self, id):
        try:
            result = self.default.getyaml(id)
        except IOError:
            result = None
        if result is None:
            for each in self.svcls:
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
