import os
import os.path


def save_stream(path, filename, stream):
    with open(os.path.join(path, filename), 'wb') as localfile:
        localfile.write(stream)


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
