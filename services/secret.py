import services.operator.facade

import extractor.information_explorer


class Secret(services.operator.facade.Facade):

    secrecy_default = False
    private_default = True

    def cleanprivate(self, id, source):
        result = source
        hidden = '[****]'
        info = self.getyaml(id, secrecy=False)
        for key in self.service.yaml_private_key:
            if key in info and info[key]:
                result = result.replace(info[key], hidden+' '*(len(info[key])-len(hidden)))
            elif key == 'phone':
                value = extractor.information_explorer.get_phone(result)
                if len(value) > 6:
                    result = result.replace(value, hidden+' '*(len(value)-len(hidden)))
        return result

    def gethtml(self, id, secrecy=True):
        result = self.service.gethtml(id)
        if secrecy is True and self.ishideprivate(id):
            result = self.cleanprivate(id, result)
        return result

    def getmd(self, id, secrecy=True):
        result = self.service.getmd(id)
        if secrecy is True and self.ishideprivate(id):
            result = self.cleanprivate(id, result)
        return result

    def getyaml(self, id, secrecy=True):
        result = self.service.getyaml(id)
        if 'secrecy' not in result:
            result['secrecy'] = False
        if secrecy is True and self.ishideprivate(id):
            result.update(self.service.yaml_private_key)
        return result

    def getprivatekeys(self):
        return self.service.yaml_private_key.keys()

    def ishideprivate(self, id):
        return self.secrecy_default is True or (self.private_default is True and
                                                self.exists(id) is False)
