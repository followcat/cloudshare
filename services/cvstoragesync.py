import os
import time
import yaml
import logging

import pypandoc

import utils._yaml
import core.basedata
import interface.predator
import services.curriculumvitae
import extractor.information_explorer


logger = logging.getLogger("CVStorageSyncLogger")
log_level = logging.DEBUG
log_file = 'cvstoragesync.log'
handler = logging.FileHandler(log_file)
formatter = logging.Formatter("[%(levelname)s][%(asctime)s]%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_level)


class CVStorageSync(object):

    def __init__(self, svc_peo_sto, svc_cv_sto, rawdb):
        self.cv_storage = svc_cv_sto
        self.peo_storage = svc_peo_sto
        self.rawdb = rawdb
        self.logger = logging.getLogger("CVStorageSyncLogger.UPDATE")

    def update(self, raws=None):
        if raws is None:
            raws = self.rawdb.keys()
        interfaces = dict([(name, self.rawdb[name])
                            for name in self.rawdb if name in raws])

        for dbname in interfaces:
            raw_db = interfaces[dbname]
            for id in set(raw_db.lsid_raw())-set(self.cv_storage.ids):
                raw_html = raw_db.getraw(id+'.html')
                raw_yaml = raw_db.getraw(id+'.yaml')
                md = self.generate_md(raw_html)
                logidname = os.path.join(raw_db.path, id)
                if len(md) < 100:
                    self.logger.info((' ').join(["Skip", logidname]))
                    continue
                t1 = time.time()
                try:
                    info = self.generate_yaml(md, raw_yaml, name=dbname)
                except KeyboardInterrupt:
                    usetime = time.time() - t1
                    self.logger.info((' ').join(["KeyboardInterrupt", logidname,
                                                 "used", str(usetime)]))
                    continue
                except Exception as e:
                    self.logger.info((' ').join(["Error %s generate " % e, logidname]))
                    continue
                usetime = time.time() - t1
                self.logger.info((' ').join(["Used", logidname, str(usetime)]))

                dataobj = core.basedata.DataObject(data=md.encode('utf-8'),
                                                   metadata=info)
                peoinfo = extractor.information_explorer.catch_peopinfo(info)
                peoobj = core.basedata.DataObject(data=peoinfo,
                                                   metadata=peoinfo)
                self.cv_storage.addcv(dataobj, raw_html.encode('utf-8'))
                self.peo_storage.add(peoobj)

    def generate_md(self, raw_html):
        return pypandoc.convert(raw_html, 'markdown', format='docbook')

    def generate_yaml(self, md, raw_yaml, selected=None, name=None):
        obj = yaml.load(raw_yaml)
        if selected is None:
            catchinfo = extractor.information_explorer.catch(md, name=name)
        else:
            catchinfo = extractor.information_explorer.catch_selected(md, selected, name=name)
        for key in catchinfo:
            if catchinfo[key] or (selected is not None and key in selected):
                obj[key] = catchinfo[key]
            elif key not in obj:
                obj[key] = catchinfo[key]
        return obj
