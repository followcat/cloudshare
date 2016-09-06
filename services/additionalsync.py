import os
import time
import yaml
import logging

import pypandoc

import utils._yaml
import interface.predator
import sources.industry_id
import services.curriculumvitae
import extractor.information_explorer


logger = logging.getLogger("AdditionalSyncLogger")
log_level = logging.DEBUG
log_file = 'additionalsync.log'
handler = logging.FileHandler(log_file)
formatter = logging.Formatter("[%(levelname)s][%(asctime)s]%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_level)


class AdditionalSync(object):

    INDUSTRY_DIR = "JOBTITLES"

    def __init__(self, addsvc, addpath, rawdb):
        self.raws = rawdb
        self.additional_path = addpath
        self.additionals = addsvc
        self.interfaces = dict([(name, self.additionals[name].interface)
                                for name in self.additionals])
        self.logger = logging.getLogger("AdditionalSyncLogger.UPDATE")

    def update(self, additionals=None):
        if additionals is None:
            additionals = sources.industry_id.industryID.keys()
        interfaces = dict([(name, self.additionals[name].interface)
                            for name in self.additionals if name in additionals])

        for in_name, in_id in sources.industry_id.industryID.items():
            if in_name not in additionals:
                continue
            if in_name not in self.additionals:
                namepath = os.path.join(self.additional_path, in_name)
                add_db = interface.predator.PredatorInterface(namepath)
                add_svc = services.curriculumvitae.CurriculumVitae(add_db, in_name)
                self.additionals[in_name] = add_svc
                self.interfaces[in_name] = add_db
                interfaces[in_name] = add_db
            add_db = interfaces[in_name]
            for dbname in self.raws:
                raw_db = self.raws[dbname]
                urls_str = raw_db.get(os.path.join(self.INDUSTRY_DIR, in_id+'.yaml'))
                if urls_str is None:
                    continue
                results = yaml.load(urls_str, Loader=utils._yaml.Loader)['datas']
                ids = [id for id in results]
                results = None
                for id in (set(ids) & set(raw_db.lsid_raw()))-(
                            set(add_db.lsid_yaml()) & set(add_db.lsid_md())):
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
                        info['classify'] = in_name
                    except KeyboardInterrupt:
                        usetime = time.time() - t1
                        self.logger.info((' ').join(["KeyboardInterrupt", logidname,
                                                     "used", str(usetime)]))
                        continue
                    except:
                        self.logger.info((' ').join(["Error generate", logidname]))
                        continue
                    usetime = time.time() - t1
                    self.logger.info((' ').join(["Used", logidname, str(usetime)]))
                    infostream = yaml.dump(info, Dumper=utils._yaml.SafeDumper,
                                           allow_unicode=True)
                    add_db.addcv(id, md.encode('utf-8'), infostream)
                    add_db.addraw(id, raw_html.encode('utf-8'), raw_yaml.encode('utf-8'))

        for name in self.additionals:
            self.additionals[name].updatenums()

    def generate_md(self, raw_html):
        return pypandoc.convert(raw_html, 'markdown', format='docbook')

    def generate_yaml(self, md, raw_yaml, selected=None, name=None):
        obj = yaml.load(raw_yaml)
        if selected is None:
            catchinfo = extractor.information_explorer.catch(md, name)
        else:
            catchinfo = extractor.information_explorer.catch_selected(md, selected, name)
        for key in catchinfo:
            if catchinfo[key] or (selected is not None and key in selected):
                obj[key] = catchinfo[key]
        return obj

    def upgrade_yaml(self, selected=None, additionals=None):
        if additionals is None:
            interfaces = self.interfaces
        else:
            interfaces = dict([(additional.name, additional.interface)
                                for additional in self.additionals
                                if additional.name in additionals])
        for name, i in interfaces.items():
            for id in i.lsid_md():
                if selected is None:
                    origin_yaml = i.getraw(id+'.yaml')
                else:
                    origin_yaml = i.get(os.path.join(i.cvdir, id+'.yaml'))
                logidname = os.path.join(i.path, id)
                md = i.get(os.path.join(i.cvdir, id+'.md'))
                t1 = time.time()
                try:
                    info = self.generate_yaml(md.decode('utf-8'), origin_yaml, selected, name)
                except Exception:
                    self.logger.info((' ').join(["Upgrade Error generate", logidname]))
                    continue
                usetime = time.time() - t1
                self.logger.info((' ').join(["Upgrade Used", logidname, str(usetime)]))
                infostream = yaml.dump(info, Dumper=utils._yaml.SafeDumper, allow_unicode=True)
                i.addyaml(id, infostream)

    def upgrade_key(self, key, additionals=None):
        if additionals is None:
            additionals = self.additionals
        else:
            additionals = dict([(additional.name, additional)
                                for additional in self.additionals
                                if additional.name in additionals])
        for additional in additionals:
            a = additional
            i = additional.interface
            for yamlname in a.yamls():
                raw_yamlstr = i.getraw(yamlname)
                raw_yaml = yaml.load(raw_yamlstr, Loader=utils._yaml.SafeLoader)
                if key not in raw_yaml:
                    continue
                cv_yaml = a.getyaml(yamlname)
                cv_yaml[key] = raw_yaml[key]
                yamlstr = yaml.dump(cv_yaml, Dumper=utils._yaml.SafeDumper, allow_unicode=True)
                a.modify(yamlname, yamlstr)
