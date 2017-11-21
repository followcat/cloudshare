import services.base.service


class Facade(services.base.service.Service):

    def __init__(self, service):
        self.service = service
        super(Facade, self).__init__(service.path)

    @property
    def ids(self):
        try:
            return self._ids
        except AttributeError:
            return self.service.ids

    def __getattr__(self, attr):
        if attr == '_ids':
            raise AttributeError()
        else:
            return getattr(self.service, attr)

