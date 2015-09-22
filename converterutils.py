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
        self.base = outputstorage.ConvertName(name)
        self.name = self.base.random
        self.stream = self.load()
        self.source_path = outputstorage.OutputPath.source
        self.docx_path = outputstorage.OutputPath.docx
        self.html_path = outputstorage.OutputPath.html
        self.yaml_path = outputstorage.OutputPath.yaml
        self.docbook_path = outputstorage.OutputPath.docbook
        self.markdown_path = outputstorage.OutputPath.markdown
        self.mimetype = self.mimetype()
        logger.info('Mimetype: %s' % self.mimetype)
        location = self.copy()
        logger.info('Backup to: %s' % location)

    def mimetype(self):
        mimetype = mimetypes.guess_type(os.path.join(
                                        self.source_path, self.name.origin))[0]
        return mimetype

    def load(self):
        data = ""
        with open(os.path.join(self.root, self.base), 'r') as f:
            data = f.read()
        return data

    def copy(self, des=None, name=None):
        """
            >>> import shutil
            >>> import outputstorage
            >>> import converterutils
            >>> output_backup = outputstorage.OutputPath._output
            >>> outputstorage.OutputPath._output = 'test_output'
            >>> cv1 = converterutils.FileProcesser('./test', 'cv_1.doc')
            >>> cv1.convert()
            >>> ori = cv1.name
            >>> des = cv1.copy()
            >>> cv1.name == ori
            False
            >>> shutil.rmtree('test_output')
            >>> outputstorage.OutputPath._output = output_backup
        """
        if des is None:
            des = self.source_path
        if name is None:
            name = self.name
        location = os.path.join(des, name)
        while os.path.isfile(location) is True:
            self.base.reset_random()
            self.name = self.base.random
            name = self.name
            location = os.path.join(des, name)
        with open(location, 'wb') as f:
            f.write(self.stream)
        return location

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
        """
            >>> import os
            >>> import shutil
            >>> import outputstorage
            >>> import converterutils
            >>> import xml.etree.ElementTree
            >>> output_backup = outputstorage.OutputPath._output
            >>> outputstorage.OutputPath._output = 'test_output'
            >>> cv1 = converterutils.FileProcesser('./test', 'cv_1.doc')
            >>> cv1.convert()
            >>> e = xml.etree.ElementTree.parse(os.path.join(
            ... cv1.docbook_path, cv1.name.xml)).getroot()
            >>> e.findall('para')[0].text
            'http://jianli.yjbys.com/'
            >>> with open(os.path.join(cv1.markdown_path,
            ... cv1.name.md))as file:
            ...     data = file.read()
            >>> 'http://jianli.yjbys.com/' in data
            True
            >>> shutil.rmtree('test_output')
            >>> outputstorage.OutputPath._output = output_backup
        """
        if self.mimetype in ['application/msword',
                             "application/vnd.openxmlformats-officedocument"
                             ".wordprocessingml.document"]:
            if 'multipart/related' in self.stream:
                self.process_mht()
                returncode = convert_docfile(self.docx_path, self.name.docx,
                                             self.docbook_path,
                                             'xml:DocBook File')
            else:
                returncode = convert_docfile(self.source_path, self.name,
                                             self.docbook_path,
                                             'xml:DocBook File')
            if "Error" in returncode[0]:
                returncode = convert_docfile(self.source_path, self.name,
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
                                       self.base.base, self.yaml_path)
            logger.info('Success')
        else:
            logger.info('Skip')


def convert_folder(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            processfile = FileProcesser(root, name)
            logger.info('Convert: %s' % os.path.join(root, name))
            processfile.convert()
            logger.info('Finish')


def storage(filename, fileobj, repo):
    """
        >>> import glob
        >>> import shutil
        >>> import os.path
        >>> import gitinterface
        >>> import outputstorage
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
        >>> data_list = []
        >>> for position in glob.glob(os.path.join(repo_name, '*.md')):
        ...     with open(position) as f:
        ...         data_list.append(f.read())
        >>> md1_str in data_list
        True
        >>> md2_str in data_list
        True
        >>> shutil.rmtree(repo_name)
        >>> shutil.rmtree('test_output')
        >>> outputstorage.OutputPath._output = output_backup
    """
    path = repo.repo.path
    outputstorage.save_stream(path, filename, fileobj.read())
    processfile = FileProcesser(path, filename)
    processfile.convert()
    shutil.copy(os.path.join(outputstorage.OutputPath.markdown, processfile.name.md),
                os.path.join(path, processfile.name.md))
    repo.add_file(path, processfile.name.md)
    with open(os.path.join(path, processfile.name.md), 'r') as f:
        md = f.read()
    return md
