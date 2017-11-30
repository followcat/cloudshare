import services.operator.facade


class SplitData(services.operator.facade.Application):
    """"""
    def add(self, bsobj, committer=None, unique=True, kv_file=True, text_file=True, do_commit=True):
        res = self.data_service.add(bsobj, committer, unique, kv_file, text_file, do_commit=do_commit)
        if res:
            res = self.operator_service.add(bsobj, committer, unique, kv_file, text_file, do_commit=do_commit)
        return res

    def getmd(self, name):
        return self.operator_service.getmd(name)

    def search(self, keyword, selected=None):
        return self.operator_service.search(keyword, selected)

    def datas(self):
        for name, text in self.operator_service.datas():
            yield name, text
