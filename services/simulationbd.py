import core.basedata
import utils.companyexcel
import services.base.frame_storage
import services.base.name_storage
import extractor.information_explorer


class SelectionBD(services.base.name_storage.NameStorage):
    """"""

    def compare_excel(self, stream, committer):
        output = list()
        excels = utils.companyexcel.convert(stream)
        for excel in excels:
            metadata = extractor.information_explorer.catch_biddinginfo(excel)
            data = core.basedata.DataObject(metadata, excel)
            if not self.exists(data.name):
                output.append(('projectadd', metadata['id'], (metadata, excel, committer)))
        return output


class SimulationBD(services.base.frame_storage.ListFrameStorage):

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = (
        ("relatedcompany",     list),
        ("position",           list),
        ("clientcontact",      list),
        ("progress",           list),
        ("updatednumber",      list),
        ("reminder",           list),
        ("priority",           int),
        ("responsible",        str),
    )

    fix_item  = {"id", "name"}

    def _templateinfo(self, committer):
        info = super(SimulationBD, self)._templateinfo(committer)
        info['responsible'] = committer
        return info

    def compare_excel(self, stream, committer):
        output = list()
        excels = utils.companyexcel.convert(stream)
        for excel in excels:
            metadata = extractor.information_explorer.catch_biddinginfo(excel)
            data = core.basedata.DataObject(metadata, excel)
            id = data.name
            responsible = excel['responsible'] if excel['responsible'] else committer
            info = dict()
            if self.exists(id):
                info = self.getyaml(id)
            for key in dict(self.YAML_TEMPLATE):
                if dict(self.YAML_TEMPLATE)[key] == list:
                    existvalues = list()
                    if key in info:
                        existvalues = [v['content'] for v in info[key]]
                    if key in excel:
                        for value in excel[key]:
                            if value in existvalues:
                                continue
                            existvalues.append(value)
                            output.append(('listadd', id, (id, key, value, responsible)))
                else:
                    if not self.exists(id) or info[key] != excel[key]:
                        output.append(('listadd', id,
                                       (id, key, excel[key], responsible)))
        return output

