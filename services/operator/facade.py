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
        if attr == 'get_id':
            return super(Facade, self).get_id
        else:
            return getattr(self.data_service, attr)


class Application(Facade):
    """"""
    def __init__(self, data_service, operator_service):
        super(Application, self).__init__(data_service)
        self.operator_service = operator_service

    @property
    def ids(self):
        return self.operator_service.ids

    @property
    def NUMS(self):
        return self.operator_service.NUMS

    def add(self, *args, **kwargs):
        res = self.operator_service.add(*args, **kwargs)
        if res:
            res = self.data_service.add(*args, **kwargs)
        return res

    def modify(self, *args, **kwargs):
        res = self.operator_service.modify(*args, **kwargs)
        if res:
            res = self.data_service.modify(*args, **kwargs)
        return res

    def remove(self, *args, **kwargs):
        res = self.operator_service.remove(*args, **kwargs)
        if res:
            res = self.data_service.remove(*args, **kwargs)
        return res

