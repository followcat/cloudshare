import functools

import services.base.service


class Multiple(services.base.service.Service):
    """"""
    combine_all = ('names', 'yamls')
    match_any = ('exists', 'unique', 'getmd', 'getmd_en', 'gethtml', 'getyaml',
                 'getuniqueid', 'private_keys',
                 'add', 'modify', 'remove', 'updateinfo', 'kick',
                 'search', 'setup', 'indexadd', 'updatesvc', 'upgradesvc',
                 'compare_excel',
                )

    def __init__(self, services):
        assert services
        super(Multiple, self).__init__()
        if isinstance(services, list):
            self.services = services
        else:
            self.services = [services]
        self.service_type = type(self.services[0])
        self.match_any_partial = {}
        for attr in self.match_any:
            self.match_any_partial[attr] = functools.partial(self.do_match_any, attr=attr)
        self.combine_all_partial = {}
        for attr in self.combine_all:
            self.combine_all_partial[attr] = functools.partial(self.do_combine_all, attr=attr)

    @property
    def ids(self):
        try:
            return self._ids
        except AttributeError:
            self._ids = set()
            for service in self.services:
                self._ids.update(service.ids)
            return self._ids

    def __getattr__(self, attr):
        if attr == 'get_id':
            super(Multiple, self).get_id
        elif attr in self.match_any_partial:
            return self.match_any_partial[attr]
        elif attr in self.combine_all_partial:
            return self.combine_all_partial[attr]
        raise AttributeError(attr)

    def do_match_any(self, *args, **kwargs):
        res = False
        attr = kwargs.pop('attr')
        for service in self.services:
            try:
                res = getattr(service, attr)(*args, **kwargs)
                if res:
                    break
            except IOError:
                continue
            except AttributeError:
                continue
        return res

    def do_combine_all(self, *args, **kwargs):
        results = list()
        attr = kwargs.pop('attr')
        for service in self.services:
            try:
                md = getattr(service, attr)(*args, **kwargs)
            except IOError:
                continue
            except AttributeError:
                continue
            if md not in results:
                results.append(md)
                yield md
        yield None

