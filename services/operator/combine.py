import services.operator.facade


class Combine(services.operator.facade.Facade):

    def __init__(self, data_service, **kwargs):
        super(Combine, self).__init__(data_service)
        self.prefix = {}
        for keyword, d in kwargs.items():
            for (key, value) in d.items():
                self.prefix[key] = keyword
                setattr(self, keyword, value)

    def __getattr__(self, attr):
        for key in self.prefix:
            if attr.startswith(key+'_'):
                return getattr(self, self.prefix[key]).__getattr__(attr.replace(key+'_', ''))
        return super(Combine, self).__getattr__(attr)

