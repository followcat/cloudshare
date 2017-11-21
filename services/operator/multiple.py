import functools

import services.base.service


class Multiple(services.base.service.Service):
    """"""
    combine_all = ('getmd', 'getmd_en', 'gethtml', 'getyaml', 'getuniqueid',)
    match_any = ('exists',)

    def __init__(self, services):
        assert services
        self.services = services
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
        if attr == '_ids':
            raise AttributeError()
        elif attr in self.match_any_partial:
            return self.match_any_partial[attr]
        elif attr in self.combine_all_partial:
            return self.combine_all_partial[attr]
        raise AttributeError()

    def do_match_any(self, *args, **kwargs):
        id = args[0]
        attr = kwargs.pop('attr')
        for service in self.services:
            if service.exists(id):
                try:
                    return getattr(service, attr)(*args, **kwargs)
                except IOError:
                    continue

    def do_combine_all(self, *args, **kwargs):
        results = list()
        id = args[0]
        attr = kwargs.pop('attr')
        for service in self.services:
            if not service.exists(id):
                continue
            md = getattr(service, attr)(*args, **kwargs)
            if md not in results:
                results.append(md)
                yield md
