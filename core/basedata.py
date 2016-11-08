import core.outputstorage
import core.docprocessor


class DataObject(object):

    def __init__(self, name, data, metadata, raw=None):
        self.name = core.outputstorage.ConvertName(name)
        self._raw = raw
        self._data = data
        self._metadata = metadata

    @property
    def ID(self):
        return self.name

    @property
    def raw(self):
        return self._raw

    @property
    def data(self):
        return self._data

    @property
    def metadata(self):
        return self._metadata

    def preview_data(self):
        output = core.docprocessor.md_to_html(self.data)
        return output
