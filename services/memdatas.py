import services.operator.facade


class MemoryDatas(services.operator.facade.Facade):

    def __init__(self, service):
        self.service = service
        self.memdict = {}

    def search_key(self, key, value, ids=None):
        if ids is None:
            ids = self.ids
        self.updates(key, ids)
        result = list()
        for id in ids:
            formatted_value = value.__repr__().replace('u', '', 1).replace('\'', '')
            searched = self.memdict[key][id]
            if searched:
                if isinstance(searched, str) or isinstance(searched, unicode):
                    if value in searched:
                        result.append(id)
                elif isinstance(searched, list):
                    for i in searched:
                        if 'content' in i and value in i['content']:
                            result.append(id)
                            break
                else:
                    if value in unicode(searched):
                        result.append(id)
        return result

    def sorted_ids(self, key, ids=None, reverse=True):
        if ids is None:
            ids = self.ids
        self.updates(key, ids)
        return map(lambda k: k[0],
                   filter(lambda k: k[0] in ids,
                          sorted(self.memdict[key].items(), key=lambda k: k[1],
                                 reverse=reverse)))

    def updates(self, key, ids=None):
        if ids is None:
            ids = self.ids
        if key not in self.memdict:
            self.memdict[key] = {}
        for id in set(self.ids)-set(self.memdict[key].keys()):
            info = self.service.getyaml(id)
            if key not in info:
                self.memdict[key][id] = 0
            else:
               self.memdict[key][id] = info[key]

    def update(self, key, id):
        if key not in self.memdict:
            self.memdict[key] = {}
        info = self.getyaml(id)
        if key not in info:
            self.memdict[key][id] = 0
        else:
           self.memdict[key][id] = info[key]

    def remove(self, id):
        result = False
        for key in self.memdict:
            if id in self.memdict[key]:
                self.memdict[key].pop(id)
                result = True
        return result

