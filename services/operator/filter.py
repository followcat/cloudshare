import functools

import services.operator.facade


class Filter(services.operator.facade.Application):
    """"""
    @property
    def ids(self):
        return self.operator_service.ids

    @property
    def NUMS(self):
        return self.operator_service.NUMS

    def __getattr__(self, attr):
        if attr.startswith('get'):
            return functools.partial(self.apply_filter, attr=attr)
        else:
            super(Filter, self).__getattr__(attr)

    def apply_filter(self, *args, **kwargs):
        id = args[0]
        attr = kwargs.pop('attr')
        assert attr.startswith('get')
        if self.operator_service.exists(id):
            return super(Filter, self).__getattr__(attr)(*args, **kwargs)

