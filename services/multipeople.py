class MultiPeople(object):

    def __init__(self, svc_peos):
        self.peoples = svc_peos

    def unique(self, peoobj):
        id = peoobj.ID
        return not self.exists(id)

    def exists(self, id):
        result = False
        for people in self.peoples:
            if people.exists(id):
                result = True
                break
        return result

    def getmd(self, id):
        results = list()
        for people in self.peoples:
            if not people.exists(id):
                continue
            for md in people.getmd(id):
                if md not in results:
                    results.append(md)
        for result in results:
            yield result

    def getinfo(self, id):
        results = list()
        for people in self.peoples:
            if not people.exists(id):
                continue
            for info in people.getinfo(id):
                if info not in results:
                    results.append(info)
        for result in results:
            yield result

    def getyaml(self, id):
        result = None
        for people in self.peoples:
            if not people.exists(id):
                continue
            info = people.getyaml(id)
            if result is None:
                result = info
            else:
                for cv in info['cv']:
                    result['cv'].append(cv)
        return result
