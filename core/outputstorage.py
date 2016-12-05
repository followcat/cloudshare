import os
import random
import string
import os.path


def save_stream(path, filename, stream):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, filename), 'wb') as localfile:
        localfile.write(stream)


class ConvertName(str):
    def __new__(cls, value):
        """
            >>> import core.outputstorage
            >>> name = 'base.cvs.doc'
            >>> convertname = core.outputstorage.ConvertName(name)
            >>> convertname.origin
            'base.cvs.doc'
            >>> convertname.xml
            'base.cvs.xml'
            >>> convertname.yaml
            'base.cvs.yaml'
            >>> convertname.doc
            'base.cvs.doc'
            >>> convertname.docx
            'base.cvs.docx'
            >>> convertname.md
            'base.cvs.md'
        """
        obj = str.__new__(cls, value)
        obj.base, obj.suffix = os.path.splitext(value)
        obj._origin = value
        obj._xml = obj._add_suffix('xml')
        obj._html = obj._add_suffix('html')
        obj._yaml = obj._add_suffix('yaml')
        obj._doc = obj._add_suffix('doc')
        obj._docx = obj._add_suffix('docx')
        obj._md = obj._add_suffix('md')
        obj._random = None
        return obj

    def _add_suffix(self, suffix):
        return self.base + '.' + suffix

    @property
    def origin(self):
        return self._origin

    @property
    def xml(self):
        return self._xml

    @property
    def html(self):
        return self._html

    @property
    def yaml(self):
        return self._yaml

    @property
    def doc(self):
        return self._doc

    @property
    def docx(self):
        return self._docx

    @property
    def md(self):
        return self._md

    @property
    def random(self):
        if self._random is None:
            self.reset_random()
        return ConvertName(self._random + self.suffix)

    def reset_random(self):
        self._random = ''.join(random.choice(
                               string.ascii_lowercase + string.digits)
                               for _ in range(32))


class OutputPath(object):
    """
        >>> import shutil
        >>> import os.path
        >>> import core.outputstorage
        >>> basepath = 'core/test_output'
        >>> outputpath = core.outputstorage.OutputPath(basepath)
        >>> os.path.exists(outputpath.basepath)
        False
        >>> outputpath.markdown
        'core/test_output/markdown'
        >>> os.path.exists(outputpath.basepath)
        True
        >>> os.path.exists('core/test_output/markdown')
        True
        >>> shutil.rmtree(basepath)
    """
    _yaml = 'yaml'
    _html = 'html'
    _docx = 'docx'
    _docbook = 'docbook'
    _markdown = 'markdown'
    _source = 'source'

    def __init__(self, basepath):
        self.basepath = basepath

    def getpath(self, name):
        path = os.path.join(self.basepath, name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @property
    def source(self):
        return self.getpath(self._source)

    @property
    def yaml(self):
        return self.getpath(self._yaml)

    @property
    def html(self):
        return self.getpath(self._html)

    @property
    def docx(self):
        return self.getpath(self._docx)

    @property
    def docbook(self):
        return self.getpath(self._docbook)

    @property
    def markdown(self):
        return self.getpath(self._markdown)
