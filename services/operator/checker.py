import functools

import core.exception
import services.operator.facade


class Filter(services.operator.facade.Application):
    """"""
    def __getattr__(self, attr):
        if attr == 'get_id':
            return super(Filter, self).get_id
        elif attr in ('ids', 'customers'):
            return self.operator_service.ids
        elif attr.startswith('get'):
            return functools.partial(self.apply_filter, attr=attr)
        else:
            return super(Filter, self).__getattr__(attr)

    def apply_filter(self, *args, **kwargs):
        id = args[0]
        attr = kwargs.pop('attr')
        assert attr.startswith('get')
        if self.operator_service.exists(id):
            return super(Filter, self).__getattr__(attr)(*args, **kwargs)


class Selector(Filter):
    """"""
    def selection(self, x):
        return tuple([x])

    def apply_filter(self, *args, **kwargs):
        id = args[0]
        attr = kwargs.pop('attr')
        assert attr.startswith('get')
        if self.operator_service.exists(id):
            copied_args = list(args)
            for selected_id in self.selection(id):
                copied_args.pop(0)
                copied_args.insert(0, selected_id)
                yield super(Selector, self).__getattr__(attr)(*copied_args, **kwargs)

    def add(self, *args, **kwargs):
        try:
            assert self.data_service.exists(args[0].ID)
            return self.operator_service.add(*args, **kwargs)
        except AssertionError:
            return False

    def remove(self, *args, **kwargs):
        return self.operator_service.remove(*args, **kwargs)


class Checker(Filter):
    """ CheckData enforce existence check before execution """

    def apply_filter(self, *args, **kwargs):
        id = args[0]
        attr = kwargs['attr']
        result = super(Checker, self).apply_filter(*args, **kwargs)
        if not result:
            raise core.exception.NotExistsIDException(id)
        return result

    def remove(self, id, committer=None, do_commit=True):
        result = False
        if self.exists(id):
            self.data_service.remove(id, committer, do_commit)
            self.operator_service.remove(id, committer, do_commit)
            result = True
        return result


