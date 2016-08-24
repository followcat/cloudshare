import os
import time
import yaml
import logging

import pypandoc

import utils._yaml
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

    def __init__(self, multicv):
        self.additionals = multicv.additionals
        self.interfaces = dict([(additional.name, additional.interface)
                                for additional in self.additionals])
        self.logger = logging.getLogger("AdditionalSyncLogger.UPDATE")

    def update(self, additionals=None):
        if additionals is None:
            additionals = self.additionals
        interfaces = dict([(additional.name, additional.interface)
                            for additional in self.additionals
                            if additional.name in additionals])
        for name, i in interfaces.items():
            for id in set(i.lsid_raw()) - (set(i.lsid_yaml()) & set(i.lsid_md())):
                raw_html = i.getraw(id+'.html')
                raw_yaml = i.getraw(id+'.yaml')
                md = self.generate_md(raw_html)
                logidname = os.path.join(i.path, id)
                if len(md) < 100:
                    self.logger.info((' ').join(["Skip", logidname]))
                    continue
                t1 = time.time()
                try:
                    info = self.generate_yaml(md, raw_yaml, name=name)
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
                infostream = yaml.dump(info, Dumper=utils._yaml.SafeDumper, allow_unicode=True)
                i.addcv(id, md.encode('utf-8'), infostream)

        for additional in additionals:
            additional.updatenums()

    def generate_md(self, raw_html):
        return pypandoc.convert(raw_html, 'markdown', format='docbook')

    def generate_yaml(self, md, raw_yaml, selected=None, name=None):
        obj = yaml.load(raw_yaml)
        if selected is None:
            catchinfo = extractor.information_explorer.catch(md, name)
        else:
            catchinfo = extractor.information_explorer.catch_selected(md, selected, name)
        for key in catchinfo:
            if catchinfo[key] or key in selected:
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
