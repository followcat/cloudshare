import services.operator.facade


class SplitData(services.operator.facade.Application):
    """"""
    def getyaml(self, id):
        """Simulation done by merging service and template data"""
        result = dict()
        templateinfo = self.operator_service.getinfo(id)
        try:
            # No call to __getattr__ on ancestor class because getyaml() declaration is found here
            #baseinfo = super(SplitData, self).getyaml(id)
            baseinfo = super(SplitData, self).__getattr__('getyaml')(id)
        except AttributeError:
            # assert type(self.operator_service) == services.base.text_storage.PlainTextStorage
            baseinfo = templateinfo
        if baseinfo:
            result.update(baseinfo)
            for key in templateinfo:
                if templateinfo[key]:
                    result[key] = templateinfo[key]
        return result

    def datas(self):
        for name, text in self.operator_service.datas():
            yield name, text

    def compare_excel(self, *args, **kwargs):
        res = list(self.data_service.compare_excel(*args, **kwargs)) + list(
                   self.operator_service.compare_excel(*args, **kwargs))
        return res
