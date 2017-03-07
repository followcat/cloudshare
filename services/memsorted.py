class MemerySorted(object):

    def __init__(self, service):
        self.service = service

    def sorted_ids(self, key, ids=None, reverse=True):
        if ids is None:
            ids = self.service.ids
        sortinfo = list()
        nokeyinfo = list()
        for id in ids:
            info = self.service.getinfo(id)
            info['id'] = id
            if key not in info:
                nokeyinfo.append(info)
            else:
                sortinfo.append(info)
        return map(lambda k: k['id'],
                   sorted(sortinfo, key=lambda k: k[key], reverse=reverse)+nokeyinfo)
