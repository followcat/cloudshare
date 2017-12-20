import services.operator.facade


class SplitData(services.operator.facade.Application):
    """"""
    def add(self, bsobj, committer=None, unique=True, kv_file=True, text_file=True, do_commit=True):
        res = self.data_service.add(bsobj, committer, unique, kv_file, text_file, do_commit=do_commit)
        if res:
            res = self.operator_service.add(bsobj, committer, unique, kv_file, text_file, do_commit=do_commit)
        return res

    def getyaml(self, id):
        """Simulation done by merging service and template data"""
        basetime = None
        templatetime = None
        try:
            baseinfo = self.operator_service.getyaml(id)
            if baseinfo:
                basetime = baseinfo['modifytime'] if 'modifytime' in baseinfo else 0
            else:
                baseinfo = {}
        except IOError:
            baseinfo = {}
        try:
            # No call to __getattr__ on ancestor class because getyaml() declaration is found here
            #templateinfo = super(SplitData, self).getyaml(id)
            templateinfo = super(SplitData, self).__getattr__('getyaml')(id)
            if templateinfo:
                templatetime = templateinfo['modifytime'] if 'modifytime' in templateinfo else 0
            else:
                templateinfo = {}
        except AttributeError:
            # assert type(self.operator_service) == services.base.text_storage.PlainTextStorage
            templateinfo = {}
        templateinfo.update(baseinfo)
        if templateinfo:
            templateinfo['modifytime'] = max(basetime, templatetime, 0)
        return templateinfo

    def datas(self):
        for name, text in self.operator_service.datas():
            yield name, text
