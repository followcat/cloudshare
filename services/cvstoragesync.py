# -*- coding: utf-8 -*-
import os
import time
import yaml
import logging

import pypandoc

import utils._yaml
import core.basedata
import extractor.information_explorer


logger = logging.getLogger("CVStorageSyncLogger")
log_level = logging.DEBUG
log_file = 'cvstoragesync.log'
handler = logging.FileHandler(log_file)
formatter = logging.Formatter("[%(levelname)s][%(asctime)s]%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_level)


def update_bydate(yamlinfo, lastdate):
    return lastdate < yamlinfo['date']

def generate_md(raw_html):
    return pypandoc.convert(raw_html, 'markdown', format='docbook')

def generate_yaml(md, yamlobj, selected=None, name=None):
    if selected is None:
        catchinfo = extractor.information_explorer.catch(md, name=name)
    else:
        catchinfo = extractor.information_explorer.catch_selected(md, selected, name=name)
    for key in catchinfo:
        if catchinfo[key] or (selected is not None and key in selected):
            yamlobj[key] = catchinfo[key]
        elif key not in yamlobj:
            yamlobj[key] = catchinfo[key]
        elif not yamlobj[key] and type(yamlobj[key]) != type(catchinfo[key]):
            yamlobj[key] = catchinfo[key]
    return yamlobj


class CVStorageSync(object):

    def __init__(self, svc_peo_sto, svc_cv_sto, rawdb):
        self.cv_storage = svc_cv_sto
        self.peo_storage = svc_peo_sto
        self.rawdb = rawdb
        self.logger = logging.getLogger("CVStorageSyncLogger.UPDATE")

    def yamls_gen(self, raws=None, filterfunc=None):
        def filter(info):
            id = info['id']
            return not self.cv_storage.exists(id)
        if raws is None:
            raws = self.rawdb.keys()
        interfaces = dict([(name, self.rawdb[name])
                            for name in self.rawdb if name in raws])
        if filterfunc is None:
            filterfunc = filter
        for dbname in interfaces:
            raw_db = interfaces[dbname]
            for id in raw_db.lsid_raw():
                filepath = os.path.join(raw_db.rawpath, id+raw_db.yamlextention)
                try:
                    date = os.path.getmtime(filepath)
                except OSError:
                    self.logger.info((' ').join(["Error RAWYAML not exists", id]))
                    continue
                yamlinfo = {'date': date, 'id': id}
                if filterfunc(yamlinfo):
                    yield dbname, raw_db, yamlinfo
        """
            for yamlinfo in raw_db.lscly_yaml():
                yield dbname, raw_db, yamlinfo
        """

    def update(self, raws=None, filterfunc=None):
        for dbname, raw_db, yamlinfo in self.yamls_gen(raws, filterfunc):
            id = yamlinfo['id']
            if raw_db.exists(id+'.html'):
                if not self.cv_storage.exists(id):
                    result = self.add_new(raw_db, id, dbname)
                else:
                    result = self.update_exists(raw_db, id)

    def update_exists(self, rawdb, id):
        result = False
        raw_yaml = rawdb.getraw(id+'.yaml')
        raw_info = yaml.load(raw_yaml, Loader=utils._yaml.Loader)
        des_info = self.cv_storage.getyaml(id)
        if not raw_info['date'] == des_info['date']:
            result = self.cv_storage.updateinfo(id, 'date', raw_info['date'], 'DEV')
            logidname = os.path.join(rawdb.path, id)
            self.logger.info((' ').join(["Update", logidname, "date",
                                         "from", str(des_info['date']),
                                         "to", str(raw_info['date'])]))
        return result

    def add_new(self, rawdb, id, dbname):
        result = False
        raw_html = rawdb.getraw(id+'.html')
        raw_yaml = rawdb.getraw(id+'.yaml')
        raw_yaml_obj = yaml.load(raw_yaml, Loader=utils._yaml.Loader)
        md = generate_md(raw_html)
        logidname = os.path.join(rawdb.path, id)
        if len(md) < 100:
            self.logger.info((' ').join(["Skip", logidname]))
            return result
        t1 = time.time()
        try:
            info = generate_yaml(md, raw_yaml_obj, name=dbname)
        except KeyboardInterrupt:
            usetime = time.time() - t1
            self.logger.info((' ').join(["KeyboardInterrupt", logidname,
                                         "used", str(usetime)]))
            return result
        except Exception as e:
            self.logger.info((' ').join(["Error %s generate " % e, logidname]))
            return result
        usetime = time.time() - t1
        self.logger.info((' ').join(["Used", logidname, str(usetime)]))

        dataobj = core.basedata.DataObject(data=md.encode('utf-8'),
                                           metadata=info)
        peoinfo = extractor.information_explorer.catch_peopinfo(info)
        peoobj = core.basedata.DataObject(data=peoinfo,
                                          metadata=peoinfo)
        self.cv_storage.addcv(dataobj, raw_html.encode('utf-8'))
        self.peo_storage.add(peoobj)
        result = True
        return result
