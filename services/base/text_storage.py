import os

import core.outputstorage
import services.base.storage


class PlainTextStorage(services.base.storage.BaseStorage):

    def add(self, bsobj, committer=None, unique=True, kv_file=True, text_file=True, do_commit=True):
        if unique is True and self.unique(bsobj) is False:
            self.info = "Exists File"
            return False
        name = core.outputstorage.ConvertName(bsobj.name)
        if text_file is True:
            message = "Add %s: %s data." % (self.commitinfo, name)
            return super(PlainTextStorage, self).add(name.md, bsobj.data, message, committer, do_commit)
        return True

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

    def search(self, keyword, selected=None):
        results = set()
        if selected and self.name in selected:
            allfile = self.interface.search(keyword)
            for result in allfile:
                id = core.outputstorage.ConvertName(result[0]).base
                results.add((id, result[1]))
        return results

    def datas(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).md, self.gettext(id)

    @property
    def ids(self):
        return set([os.path.splitext(f)[0]
                    for f in self.interface.lsfiles('.', '*.md')])

