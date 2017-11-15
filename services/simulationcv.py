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
        "name":                 '[*****]',
        "committer":            '[*****]',
        "origin":               '[*****]'
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

    def cleanprivate(self, md, yaml):
        result = md
        hidden = '[****]'
        for key in self.yaml_private_key:
            if key in yaml and yaml[key]:
                result = result.replace(yaml[key], hidden+' '*(len(yaml[key])-len(hidden)))
            elif key == 'phone':
                value = extractor.information_explorer.get_phone(result)
                if len(value) > 6:
                    result = result.replace(value, hidden+' '*(len(value)-len(hidden)))
        return result

    def gethtml(self, id, secrecy=True):
        result = None
        for storage in self.storages:
            try:
                result = storage.gethtml(id)
                if secrecy is True and self.ishideprivate(id):
                    result = self.secretsmd(id, md)
                break
            except IOError:
                continue
        return result

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
        if secrecy is True:
            result = self.secretsmd(id, result)
        return result

    def getyaml(self, id, secrecy=True):
        result = super(SimulationCV, self).getyaml(id)
        if 'secrecy' not in result:
            result['secrecy'] = False
        if secrecy is True:
            result = self.secretsyaml(id, result)
        return result

    def secretsyaml(self, id, info):
        if self.ishideprivate(id):
            info.update(self.yaml_private_key)
            info['secrecy'] = True
        return info

    def secretsmd(self, id, md, info=None):
        result = md
        if self.ishideprivate(id):
            if info is None:
                info = self.getyaml(id, secrecy=False)
            result = self.cleanprivate(md, info)
        return result

    def getprivatekeys(self):
        return self.yaml_private_key.keys()

    def ishideprivate(self, id):
        return self.secrecy_default is True or (self.private_default is True and
                                                self.exists(id) is False)
