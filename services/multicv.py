class MultiCV(object):

    def __init__(self, defaultsvc, svc_list):
        self.default = defaultsvc
        self.svcls = svc_list

    def add(self, *args, **kwargs):
        return self.default.add(*args, **kwargs)

    def add_md(self, cvobj, committer=None):
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
                    break
                except IOError:
                    result = None
        if result is None:
            raise IOError
        else:
            return result
