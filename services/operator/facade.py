import services.base.service


class Facade(services.base.service.Service):
    """"""
    def __init__(self, service):
        super(Facade, self).__init__()
        self.data_service = service
        self.service = self.data_service

    @property
    def ids(self):
        try:
            return self._ids
        except AttributeError:
            return self.data_service.ids

    def __getattr__(self, attr):
        if attr == '_ids':
            raise AttributeError()
        else:
            return getattr(self.data_service, attr)


class Application(Facade):
    """"""
    def __init__(self, data_service, operator_service):
        super(Application, self).__init__(data_service)
        self.operator_service = operator_service

