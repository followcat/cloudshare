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

import outputstorage
import information_explorer


logging.config.fileConfig("logger.conf")
logger = logging.getLogger("converterinfo")


class ConvertName(str):
    def __new__(cls, value):
        """
            >>> import converterutils
            >>> name = 'base.cvs.doc'
            >>> convertname = converterutils.ConvertName(name)
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


def convert_docfile(path, filename, output, format):
    p = subprocess.Popen(['libreoffice', '--headless', '--convert-to',
                          format, os.path.join(path, filename),
                          '--outdir', output],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    returncode = p.communicate()
    logger.info(returncode[0])
    return returncode


class FileProcesser():
    def __init__(self, root, name):
        self.root = root
        self.name = ConvertName(name)
        self.mimetype = self.mimetype()
        self.stream = self.load()
        self.docx_path = outputstorage.OutputPath.docx
        self.html_path = outputstorage.OutputPath.html
        self.yaml_path = outputstorage.OutputPath.yaml
        self.docbook_path = outputstorage.OutputPath.docbook
        self.markdown_path = outputstorage.OutputPath.markdown
        logger.info('Mimetype: %s' % self.mimetype)

    def mimetype(self):
        mimetype = mimetypes.guess_type(os.path.join(
                                        self.root, self.name))[0]
        return mimetype

    def load(self):
        data = ""
        with open(os.path.join(self.root, self.name), 'r') as f:
            data = f.read()
        return data

    def process_mht(self):
        message = email.message_from_string(self.stream)
        for part in message.walk():
            if part.get_content_charset() is not None:
                part.set_param('charset', 'utf-8')
        html_src = emaildata.text.Text.html(message)
        outputstorage.save_stream(self.html_path, self.name.html, html_src)
        returncode = convert_docfile(self.html_path, self.name.html,
                                     self.docx_path, 'docx:Office Open XML Text')
        return returncode

    def remove_note(self):
        position = os.path.join(self.docbook_path, self.name.xml)
        e = xml.etree.ElementTree.parse(position)
        note_parent = e.findall('.//note/..')
        for parent in note_parent:
            while(parent.find('note') is not None):
                parent.remove(parent.find('note'))
        e.write(position, encoding='utf-8')

    def file_docbook_to_markdown(self):
        input_file = os.path.join(self.docbook_path, self.name.xml)
        output_file = os.path.join(self.markdown_path, self.name.md)
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

    def convert(self):
        if self.mimetype in ['application/msword',
                             "application/vnd.openxmlformats-officedocument"
                             ".wordprocessingml.document"]:
            if 'multipart/related' in self.stream:
                self.process_mht()
                returncode = convert_docfile(self.docx_path, self.name.docx,
                                             self.docbook_path,
                                             'xml:DocBook File')
            else:
                returncode = convert_docfile(self.root, self.name,
                                             self.docbook_path,
                                             'xml:DocBook File')
            if "Error" in returncode[0]:
                returncode = convert_docfile(self.root, self.name,
                                             self.docx_path,
                                             'docx:Office Open XML Text')
                returncode = convert_docfile(self.docx_path, self.name.docx,
                                             self.docbook_path,
                                             'xml:DocBook File')
            if not os.path.exists(os.path.join(
                                  self.docbook_path, self.name.xml)):
                logger.info('Not exists')
                return
            self.remove_note()
            self.file_docbook_to_markdown()
            information_explorer.catch(self.markdown_path, self.name,
                                       self.yaml_path)
            logger.info('Success')
        else:
            logger.info('Skip')


def convert_folder(path):
    """
        >>> import os
        >>> import outputstorage
        >>> import converterutils
        >>> import xml.etree.ElementTree
        >>> output_backup = outputstorage.OutputPath._output
        >>> outputstorage.OutputPath._output = 'test_output'
        >>> converterutils.convert_folder('./test')
        >>> e = xml.etree.ElementTree.parse('test_output/docbook/cv_1.xml').getroot()
        >>> e.findall('para')[0].text
        'http://jianli.yjbys.com/'
        >>> with open('test_output/markdown/cv_1.md') as file:
        ...     data = file.read()
        >>> 'http://jianli.yjbys.com/' in data
        True
        >>> shutil.rmtree('test_output')
        >>> outputstorage.OutputPath._output = output_backup
    """
    for root, dirs, files in os.walk(path):
        for name in files:
            processfile = FileProcesser(root, name)
            logger.info('Convert: %s' % os.path.join(root, name))
            processfile.convert()
            logger.info('Finish')


def storage(filename, fileobj, repo):
    """
        >>> import shutil
        >>> import gitinterface
        >>> import converterutils
        >>> output_backup = outputstorage.OutputPath._output
        >>> outputstorage.OutputPath._output = 'test_output'
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
        >>> shutil.rmtree('test_output')
        >>> outputstorage.OutputPath._output = output_backup
    """
    path = repo.repo.path
    conname = ConvertName(filename)
    outputstorage.save_stream(path, conname, fileobj.read())
    processfile = FileProcesser(path, filename)
    processfile.convert()
    shutil.copy(os.path.join(outputstorage.OutputPath.markdown, conname.md),
                os.path.join(path, conname.md))
    repo.add_file(path, conname.md)
    with open(os.path.join(path, conname.md), 'r') as f:
        md = f.read()
    return md
