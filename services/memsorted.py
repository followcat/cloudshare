class MemerySorted(object):

    def __init__(self, service):
        self.service = service
        self.memdict = {}

    def sorted_ids(self, key, ids=None, reverse=True):
        if ids is None:
            ids = self.service.ids
        if key not in self.memdict:
            self.memdict[key] = {}
        for id in ids:
            if id not in self.memdict[key]:
                info = self.service.getinfo(id)
                if key not in info:
                    self.memdict[key][id] = 0
                else:
                   self.memdict[key][id] = info[key]
        return map(lambda k: k[0],
                   filter(lambda k: k[0] in ids,
                          sorted(self.memdict[key].items(), key=lambda k: k[1],
                                 reverse=reverse)))

    def update(self, key, id):
        if key not in self.memdict:
            self.memdict[key] = {}
        info = self.service.getinfo(id)
        if key not in info:
            self.memdict[key][id] = 0
        else:
           self.memdict[key][id] = info[key]
