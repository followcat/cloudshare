import core.outputstorage
import utils.pandocconverter


class DataObjectWithoutId(object):

    def __init__(self, metadata, data, raw=None):
        self._raw = raw
        self._data = data
        self._metadata = metadata

    def append_id(self, id):
        assert 'id' not in self._metadata
        self._metadata['id'] = id

    def __str__(self):
        try:
            return self._metadata['name']
        except KeyError:
            return self.ID

    @property
    def ID(self):
        try:
            return core.outputstorage.ConvertName(self._metadata['id'])
        except KeyError:
            return core.outputstorage.ConvertName(self._metadata['name'])

    @property
    def name(self):
        return self.ID

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


class DataObject(DataObjectWithoutId):

    def __init__(self, metadata, data, raw=None):
        assert 'id' in metadata
        super(DataObject, self).__init__(metadata, data, raw)

    def append_id(self, id):
        raise NotImplementedError()

