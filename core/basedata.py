import core.outputstorage
import utils.pandocconverter


class DataObject(object):

    def __init__(self, metadata, data, raw=None):
        assert 'id' in metadata
        self.name = core.outputstorage.ConvertName(metadata['id'])
        self._raw = raw
        self._data = data
        self._metadata = metadata

    def __str__(self):
        try:
            return self._metadata['name']
        except KeyError:
            return self.ID

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
        output = utils.pandocconverter.md_to_html(self.data)
        return output
