import os

import core.outputstorage
import services.base.storage


class PlainTextStorage(services.base.storage.BaseStorage):

    def add(self, bsobj, committer=None, unique=True, kv_file=True, text_file=True, do_commit=True):
        result = False
        if unique is True and self.unique(bsobj) is False:
            self.info = "Exists File"
            return True
        name = core.outputstorage.ConvertName(bsobj.name)
        if text_file is True:
            message = "Add %s: %s data." % (self.commitinfo, name)
            result = self.interface.modify(name.md, bsobj.data,
                            message, committer, do_commit=do_commit)
        return result

    def modify(self, *args, **kwargs):
        return False

    def getmd(self, name):
        """"""
        result = unicode()
        md = core.outputstorage.ConvertName(name).md
        markdown = self.interface.get(md)
        if markdown is None:
            result = None
        elif isinstance(markdown, unicode):
            result = markdown
        else:
            result = unicode(str(markdown), 'utf-8')
        return result

    gettext = getmd

    def datas(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).md, self.gettext(id)

    @property
    def ids(self):
        return set([os.path.splitext(f)[0]
                    for f in self.interface.lsfiles('.', '*.md')])

