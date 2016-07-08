import os
import yaml
import pypandoc

import utils._yaml
import extractor.information_explorer


class AdditionalSync(object):

    def __init__(self, interfaces):
        self.interfaces = interfaces

    def update(self):
        for i in self.interfaces:
            for id in set(i.lsid_raw()) - (set(i.lsid_yaml()) & set(i.lsid_md())):
                raw_html = i.getraw(id+'.html')
                raw_yaml = i.getraw(id+'.yaml')
                md = self.generate_md(raw_html)
                if len(md) < 100:
                    continue
                try:
                    info = self.generate_yaml(md, raw_yaml)
                except:
                    continue
                infostream = yaml.dump(info, Dumper=utils._yaml.SafeDumper, allow_unicode=True)
                i.addcv(id, md.encode('utf-8'), infostream)

    def generate_md(self, raw_html):
        return pypandoc.convert(raw_html, 'markdown', format='docbook')

    def generate_yaml(self, md, raw_yaml, selected=None):
        obj = yaml.load(raw_yaml)
        if selected is None:
            catchinfo = extractor.information_explorer.catch(md)
        else:
            catchinfo = extractor.information_explorer.catch_selected(md, selected)
        for key in catchinfo:
            if catchinfo[key]:
                obj[key] = catchinfo[key]
        return obj

    def upgrade_yaml(self, selected=None):
        for i in self.interfaces:
            for id in i.lsid_md():
                if selected is None:
                    origin_yaml = i.getraw(id+'.yaml')
                else:
                    origin_yaml = i.get(os.path.join(i.cvdir, id+'.yaml'))
                md = i.get(os.path.join(i.cvdir, id+'.md'))
                info = self.generate_yaml(md.decode('utf-8'), origin_yaml, selected)
                infostream = yaml.dump(info, Dumper=utils._yaml.SafeDumper, allow_unicode=True)
                i.addyaml(id, infostream)
