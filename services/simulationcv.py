import services.base.simulation
import services.curriculumvitae

import utils.pandocconverter
import extractor.information_explorer


class SimulationCV(services.base.simulation.Simulation,
                   services.curriculumvitae.CurriculumVitae):

    YAML_TEMPLATE = (
        ("committer",           str),
    )

    yaml_private_key = {
        "phone":                '[*****]',
        "email":                '[*****]',
        "name":                 '[*****]'
    }

    list_item = {}
    secrecy_default = False
    private_default = True

    def __init__(self, path, name, storages, iotype='git'):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> config.init_samplecv()
            >>> SVC_PRJ_TEST = config.SVC_PRJ_TEST
            >>> id = list(SVC_PRJ_TEST.cv_ids())[0]
            >>> SVC_PRJ_TEST.curriculumvitae.updateinfo(id, 'committer', 'dev', 'dev')
            {'committer': 'dev'}
            >>> config.destory()
        """
        super(SimulationCV, self).__init__(path, name, storages, iotype=iotype)

    def getmd_en(self, id):
        yamlinfo = self.getyaml(id)
        veren = yamlinfo['enversion']
        html = None
        for storage in self.storages:
            try:
                html = storage.gethtml(veren)
                break
            except IOError:
                continue
        return html

    def cleanprivate(self, id, source):
        result = source
        hidden = '[****]'
        info = self.getyaml(id, secrecy=False)
        for key in self.yaml_private_key:
            if info[key]:
                result = result.replace(info[key], hidden+' '*(len(info[key])-len(hidden)))
            elif key == 'phone':
                value = extractor.information_explorer.get_phone(result)
                result = result.replace(value, hidden+' '*(len(value)-len(hidden)))
        return result

    def gethtml(self, id, secrecy=True):
        md = self.getmd(id, secrecy=secrecy)
        html = utils.pandocconverter.md_to_html(md)
        return html

    def getuniqueid(self, id):
        result = None
        for storage in self.storages:
            try:
                result = storage.getuniqueid(id)
                break
            except IOError:
                continue
        return result

    def getmd(self, id, secrecy=True):
        result = super(SimulationCV, self).getmd(id)
        if secrecy is True and self.ishideprivate(id):
            result = self.cleanprivate(id, result)
        return result

    def getyaml(self, id, secrecy=True):
        result = super(SimulationCV, self).getyaml(id)
        if secrecy is True and self.ishideprivate(id):
            result.update(self.yaml_private_key)
        return result

    def getprivatekeys(self):
        return self.yaml_private_key.keys()

    def ishideprivate(self, id):
        return self.secrecy_default is True or (self.private_default is True and
                                                self.exists(id) is False)
