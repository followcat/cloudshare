import os
import random
import string
import os.path


def save_stream(path, filename, stream):
    with open(os.path.join(path, filename), 'wb') as localfile:
        localfile.write(stream)


class ConvertName(str):
    def __new__(cls, value):
        """
            >>> import outputstorage
            >>> name = 'base.cvs.doc'
            >>> convertname = outputstorage.ConvertName(name)
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
        obj._random = ''.join(random.choice(
                              string.ascii_lowercase + string.digits)
                              for _ in range(8))
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
        return ConvertName(self._random + self.suffix)

    def reset_random(self):
        self._random = ''.join(random.choice(
                               string.ascii_lowercase + string.digits)
                               for _ in range(8))


class ClassProperty(property):
    def __get__(self, instance, cls):
        return classmethod(self.fget).__get__(instance, cls)()


class OutputPath(object):
    """
        >>> import shutil
        >>> import os.path
        >>> import outputstorage
        >>> output_backup = outputstorage.OutputPath._output
        >>> outputstorage.OutputPath._output = 'test_output'
        >>> os.path.exists('test_output')
        False
        >>> outputstorage.OutputPath.output
        'test_output'
        >>> os.path.exists('test_output')
        True
        >>> os.path.exists('test_output/markdown')
        False
        >>> outputstorage.OutputPath.markdown
        'test_output/markdown'
        >>> os.path.exists('test_output')
        True
        >>> shutil.rmtree('test_output')
        >>> outputstorage.OutputPath._output = output_backup
    """
    _output = 'output'
    _yaml = 'yaml'
    _html = 'html'
    _docx = 'docx'
    _docbook = 'docbook'
    _markdown = 'markdown'
    _source = 'source'

    @classmethod
    def getpath(cls, name):
        path = os.path.join(cls.output, name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @ClassProperty
    def output(self):
        if not os.path.exists(self._output):
            os.mkdir(self._output)
        return self._output

    @ClassProperty
    def source(self):
        return self.getpath(self._source)

    @ClassProperty
    def yaml(self):
        return self.getpath(self._yaml)

    @ClassProperty
    def html(self):
        return self.getpath(self._html)

    @ClassProperty
    def docx(self):
        return self.getpath(self._docx)

    @ClassProperty
    def docbook(self):
        return self.getpath(self._docbook)

    @ClassProperty
    def markdown(self):
        return self.getpath(self._markdown)
