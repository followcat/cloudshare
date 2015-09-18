# -*- coding: utf-8 -*-
import os
import email
import shutil
import logging
import os.path
import mimetypes
import subprocess
import logging.config
import xml.etree.ElementTree

import pypandoc
import emaildata.text

import information_explorer


logging.config.fileConfig("logger.conf")
logger = logging.getLogger("converterinfo")


class ConverName(str):
    def __new__(cls, value):
        """
            >>> import converterutils
            >>> name = 'base.cvs.doc'
            >>> convername = converterutils.ConverName(name)
            >>> convername.xml
            'base.cvs.xml'
            >>> convername.yaml
            'base.cvs.yaml'
            >>> convername.doc
            'base.cvs.doc'
            >>> convername.docx
            'base.cvs.docx'
            >>> convername.md
            'base.cvs.md'
        """
        obj = str.__new__(cls, value)
        obj.base, obj.suffix = os.path.splitext(value)
        obj._xml = obj._add_suffix('xml')
        obj._html = obj._add_suffix('html')
        obj._yaml = obj._add_suffix('yaml')
        obj._doc = obj._add_suffix('doc')
        obj._docx = obj._add_suffix('docx')
        obj._md = obj._add_suffix('md')
        return obj

    def _add_suffix(self, suffix):
        return self.base + '.' + suffix

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


class ClassProperty(property):
    def __get__(self, instance, cls):
        return classmethod(self.fget).__get__(instance, cls)()


class OutputPath(object):
    """
        >>> import os
        >>> import shutil
        >>> import converterutils
        >>> output_backup = converterutils.OutputPath._output
        >>> converterutils.OutputPath._output = 'test_output'
        >>> os.path.exists('test_output')
        False
        >>> converterutils.OutputPath.output
        'test_output'
        >>> os.path.exists('test_output')
        True
        >>> os.path.exists('test_output/markdown')
        False
        >>> converterutils.OutputPath.markdown
        'test_output/markdown'
        >>> os.path.exists('test_output')
        True
        >>> shutil.rmtree('test_output')
        >>> converterutils.OutputPath._output = output_backup
    """
    _output = 'output'
    _yaml = 'yaml'
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
    def docx(self):
        return self.getpath(self._docx)

    @ClassProperty
    def docbook(self):
        return self.getpath(self._docbook)

    @ClassProperty
    def markdown(self):
        return self.getpath(self._markdown)


def save_stream(path, filename, stream):
    with open(os.path.join(path, filename), 'wb') as localfile:
        localfile.write(stream)


def convert_docfile(path, filename, output, format):
    p = subprocess.Popen(['libreoffice', '--headless', '--convert-to',
                          format, os.path.join(path, filename),
                          '--outdir', output],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    returncode = p.communicate()
    logger.info(returncode[0])
    return returncode


def file_docbook_to_markdown(path, convertname, output):
    input_file = os.path.join(path, convertname.xml)
    output_file = os.path.join(output, convertname.md)
    try:
        pypandoc.convert(input_file, 'markdown', format='docbook', outputfile=output_file)
        with open(output_file, 'r') as f:
            reformat = []
            for each in f.readlines():
                reformat.append(each)
                if each[0] == '-':
                    break
            else:
                with open(output_file, 'w') as f:
                    for line in reformat:
                        f.write(line.lstrip(' '))
    except RuntimeError as e:
        pass


def remove_note(path, convertname):
    e = xml.etree.ElementTree.parse(os.path.join(path, convertname))
    note_parent = e.findall('.//note/..')
    for parent in note_parent:
        while(parent.find('note') is not None):
            parent.remove(parent.find('note'))
    e.write(os.path.join(path, convertname), encoding='utf-8')


def process_mht(stream, docx_path, convertname):
    message = email.message_from_string(stream)
    for part in message.walk():
        if part.get_content_charset() is not None:
            part.set_param('charset', 'utf-8')
    html_src = emaildata.text.Text.html(message)
    save_stream(docx_path, convertname.html, html_src)
    returncode = convert_docfile(docx_path, convertname.html,
                                 docx_path, 'docx:Office Open XML Text')
    return returncode


def convert_file(root, conname):
    mimetype = mimetypes.guess_type(os.path.join(root, conname))[0]
    logger.info('Mimetype: %s' % mimetype)
    if mimetype in ['application/msword',
                    "application/vnd.openxmlformats-officedocument"
                    ".wordprocessingml.document"]:
        with open(os.path.join(root, conname), 'r') as f:
            stream = f.read()
        if 'multipart/related' in stream:
            process_mht(stream, OutputPath.docx, conname)
            returncode = convert_docfile(OutputPath.docx, conname.docx,
                                         OutputPath.docbook,
                                         'xml:DocBook File')
        else:
            returncode = convert_docfile(root, conname, OutputPath.docbook,
                                         'xml:DocBook File')
        if "Error" in returncode[0]:
            returncode = convert_docfile(root, conname, OutputPath.docx,
                                         'docx:Office Open XML Text')
            returncode = convert_docfile(OutputPath.docx, conname.docx,
                                         OutputPath.docbook,
                                         'xml:DocBook File')
        if not os.path.exists(os.path.join(
                              OutputPath.docbook, conname.xml)):
            logger.info('Not exists')
            return
        remove_note(OutputPath.docbook, conname.xml)
        file_docbook_to_markdown(OutputPath.docbook, conname,
                                 OutputPath.markdown)
        information_explorer.catch(OutputPath.markdown, conname,
                                   OutputPath.yaml)
        logger.info('Success')
    else:
        logger.info('Skip')


def convert_folder(path):
    """
        >>> import os
        >>> import converterutils
        >>> import xml.etree.ElementTree
        >>> converterutils.convert_folder('./test')
        >>> e = xml.etree.ElementTree.parse('output/docbook/cv_1.xml').getroot()
        >>> e.findall('para')[0].text
        'http://jianli.yjbys.com/'
        >>> with open('output/markdown/cv_1.md') as file:
        ...     data = file.read()
        >>> 'http://jianli.yjbys.com/' in data
        True
        >>> os.remove('output/docbook/cv_1.xml')
        >>> os.remove('output/docbook/cv_2.xml')
        >>> os.remove('output/markdown/cv_1.md')
        >>> os.remove('output/markdown/cv_2.md')
    """
    for root, dirs, files in os.walk(path):
        for name in files:
            conname = ConverName(name)
            logger.info('Convert: %s' % os.path.join(root, conname))
            convert_file(root, conname)
            logger.info('Finish')


def storage(filename, fileobj, repo):
    """
        >>> import shutil
        >>> import gitinterface
        >>> import converterutils
        >>> repo_name = 'test_repo'
        >>> interface = gitinterface.GitInterface(repo_name)
        >>> cv1_name = 'cv_1.doc'
        >>> cv2_name = 'cv_2.doc'
        >>> cv1_file = open('test/' + cv1_name, 'r')
        >>> cv2_file = open('test/' + cv2_name, 'r')
        >>> md1_str = converterutils.storage(cv1_name, cv1_file, interface)
        >>> md2_str = converterutils.storage(cv2_name, cv2_file, interface)
        >>> with open('test_repo/cv_1.md') as file:
        ...     md1_file = file.read()
        >>> with open('test_repo/cv_2.md') as file:
        ...     md2_file = file.read()
        >>> md1_str == md1_file
        True
        >>> md2_str == md2_file
        True
        >>> shutil.rmtree(repo_name)
    """
    path = repo.repo.path
    conname = ConverName(filename)
    save_stream(path, conname, fileobj.read())
    convert_file(path, conname)
    shutil.copy(os.path.join(OutputPath.markdown, conname.md),
                os.path.join(path, conname.md))
    repo.add_file(path, conname.md)
    with open(os.path.join(path, conname.md), 'r') as f:
        md = f.read()
    return md
