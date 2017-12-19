import core.basedata
import utils.companyexcel
import services.base.kv_storage
import extractor.information_explorer


class Bidding(services.base.kv_storage.KeyValueStorage):
    """
        >>> import shutil
        >>> import services.company
        >>> import core.basedata
        >>> import extractor.information_explorer
        >>> path = 'services/test_repo'
        >>> svc_co = services.bidding.Bidding(path)
        >>> name, committer, introduction = 'CompanyA', 'tester', 'This is Co.A'
        >>> metadata = extractor.information_explorer.catch_biddinginfo({'introduction': introduction,
        ...                                                         'name': name})
        >>> coobj = core.basedata.DataObject(metadata, data=introduction)
        >>> svc_co.add(coobj, 'Dever')
        True
        >>> co = svc_co.getyaml(metadata['id'])
        >>> co['name']
        'CompanyA'
        >>> co['introduction']
        'This is Co.A'
        >>> svc_co.add(coobj, 'Dever')
        False
        >>> list(svc_co.ids)
        ['4de25a98bc371bf87220e500215317f4b2c24933']
        >>> svc_co.getyaml('CompanyB') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        IOError...
        >>> shutil.rmtree(path)
    """
    YAML_DIR = 'YAML'
    YAML_TEMPLATE = extractor.information_explorer.bidding_template

    commitinfo = 'Bidding'

    def compare_excel(self, stream, committer):
        output = list()
        excels = utils.companyexcel.convert(stream)
        for excel in excels:
            metadata = extractor.information_explorer.catch_biddinginfo(excel)
            data = core.basedata.DataObject(metadata, excel)
            if not self.exists(data.name):
                output.append(('companyadd', metadata['id'], (metadata, excel, committer)))
        return output

