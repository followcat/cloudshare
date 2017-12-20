import services.operator.facade
import services.operator.checker

import extractor.information_explorer


class Secret(services.operator.facade.Facade):

    def clean_plaintext(self, id, source):
        if not source:
            return source
        result = source
        hidden = '[****]'
        info = self.getyaml(id, secrecy=False)
        for key in self.service.private_keys():
            if key in info and info[key]:
                result = result.replace(info[key], hidden+' '*(len(info[key])-len(hidden)))
            elif key == 'phone':
                value = extractor.information_explorer.get_phone(result)
                if len(value) > 6:
                    result = result.replace(value, hidden+' '*(len(value)-len(hidden)))
        return result

    def clean_keyvalue(self, id, source):
        masks = self.service.private_keys()
        for key in [_ for _ in masks if _ in source]:
            source[key] = masks[key]
        return source

    def cleanprivate(self, id, source):
        if isinstance(source, dict):
            return self.clean_keyvalue(id, source)
        else:
            return self.clean_plaintext(id, source)

    def gethtml(self, id, secrecy=True):
        result = self.service.gethtml(id)
        if secrecy is True:
            result = self.clean_plaintext(id, result)
        return result

    def getmd(self, id, secrecy=True):
        result = self.service.getmd(id)
        if secrecy is True:
            result = self.clean_plaintext(id, result)
        return result

    def getyaml(self, id, secrecy=True):
        result = self.service.getyaml(id)
        if result and 'secrecy' not in result:
            result['secrecy'] = secrecy
        if secrecy is True:
            result = self.clean_keyvalue(id, result)
        return result


class Private(services.operator.checker.Filter):
    """
        >>> import os.path
        >>> import services.secret
        >>> import services.curriculumvitae
        >>> import services.operator.checker
        >>> import services.operator.multiple
        >>> from baseapp.datadbs import *
        >>> import baseapp.loader
        >>> basepath = baseapp.loader.config.storage_config['MEMBERS']
        >>> aipath = os.path.join(basepath, 'willendare/projects/ArtificialIntelligence/CV')

    Private service is using the operator_service as filter on exists()
        >>> sec = services.secret.Private(
        ...         data_service=services.operator.split.SplitData(
        ...             services.operator.multiple.Multiple([SVC_CV_REPO, SVC_CV_STO]),
        ...             services.simulationcv.SimulationCV(aipath, 'aicv')),
        ...         operator_service=services.simulationcv.SelectionCV(aipath, 'aicv'))
        >>> existing = '0015a72dad9196506ee820202a011dec2bc017db'
        >>> missing = '00f3ffce388e6175e5e18695892c69d4291a3b56'

    Private service will add secrecy for data that do not pass the filter:
        >>> assert sec.exists(existing)
        >>> assert not '[****]' in sec.getmd(existing)
        >>> assert not sec.exists(missing)
        >>> assert '[****]' in sec.getmd(missing)

    If you want the missing data to be not visible, use Filter operator directly:
        >>> repo = services.operator.checker.Filter(data_service=SVC_CV_REPO,
        ...         operator_service=services.simulationcv.SelectionCV(aipath, 'aicv'))
        >>> sec = services.secret.Private(
        ...         data_service=services.operator.split.SplitData(
        ...             services.operator.multiple.Multiple([repo, SVC_CV_STO]),
        ...             services.simulationcv.SimulationCV(aipath, 'aicv')),
        ...         operator_service=services.simulationcv.SelectionCV(aipath, 'aicv'))
        >>> assert sec.getmd(existing)
        >>> assert not sec.getmd(missing)
    """
    def __init__(self, data_service, operator_service):
        super(Private, self).__init__(Secret(data_service), operator_service)

    def apply_filter(self, *args, **kwargs):
        id = args[0]
        attr = kwargs.pop('attr')
        assert attr.startswith('get')
        if self.operator_service.exists(id):
            kwargs['secrecy'] = False
            return getattr(self.data_service, attr)(*args, **kwargs)
        else:
            kwargs['secrecy'] = True
            return getattr(self.data_service, attr)(*args, **kwargs)

