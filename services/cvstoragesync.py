import os
import time
import yaml
import logging

import bs4
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
                date = os.path.getmtime(filepath)
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
        md = generate_md(raw_html)
        logidname = os.path.join(rawdb.path, id)
        if len(md) < 100:
            self.logger.info((' ').join(["Skip", logidname]))
            return result
        t1 = time.time()
        try:
            info = generate_yaml(md, raw_yaml, name=dbname)
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


class LiepinPluginSyncObject(object):

    committer = 'PLUGIN'

    def __init__(self, url, htmlsource):
        self.url = url
        self.htmlsource = htmlsource
        self.raw_html, self.raw_yaml = self.parse_source()
        self.md = generate_md(self.raw_html)
        self.info = generate_yaml(self.md, self.raw_yaml, name='Liepin')
        self.logger = logging.getLogger("CVStorageSyncLogger.UPDATE")
        self.loginfo = ''

    def parse_source(self):
        bs = bs4.BeautifulSoup(self.htmlsource, 'lxml')

        details = dict()
        details['date'] = time.time()
        details['filename'] = self.url
        idtag = bs.find('span', attrs={'data-nick':'res_id'})
        details['id'] = idtag.text
        details['originid'] = idtag.text

        login_form = bs.find(class_='user-login-reg')
        if login_form is not None:
            raise Exception('NoLoginError')
        side = bs.find(class_='side')
        side.decompose()
        footer = bs.find('footer')
        footer.decompose()
        javascripts = bs.findAll('script')
        for js in javascripts:
            js.decompose()
        alinks = bs.findAll('a')
        for a in alinks:
            a.decompose()
        content = bs.find(class_='resume')
        return content.prettify(), details

    def add_new(self, cvstorage, peostorage):
        result = False
        if self.info['id']:
            dataobj = core.basedata.DataObject(data=self.md.encode('utf-8'),
                                               metadata=self.info)
            peoinfo = extractor.information_explorer.catch_peopinfo(self.info)
            peoobj = core.basedata.DataObject(data=peoinfo,
                                              metadata=peoinfo)
            result = cvstorage.addcv(dataobj, self.raw_html.encode('utf-8'))
            if result is True:
                result = peostorage.add(peoobj)
                if result is False:
                    self.loginfo = "add People failed."
            else:
                self.loginfo = cvstorage.info
        else:
            self.loginfo = "without ID."
        if result is True:
            self.logger.info((' ').join(["Plugin add Liepin", self.info['id']]))
        else:
            self.logger.info((' ').join(["Plugin add Liepin failed", self.loginfo]))
        return result
