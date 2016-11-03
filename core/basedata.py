import core.outputstorage


class CurriculumVitaeObject(object):

    def __init__(self, name, data, metadata, raw=None):
        self.name = core.outputstorage.ConvertName(name)
        self.raw = raw
        self.data = data
        self.metadata = metadata

    @property
    def ID(self):
        return self.name

    def markdown(self):
        return self.data

    def yaml(self):
        return self.metadata

    def preview_markdown(self):
        output = core.converterutils.md_to_html(self.data)
        return output
