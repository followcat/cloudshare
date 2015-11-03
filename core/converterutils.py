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

import core.exception
import core.outputstorage
import core.uniquesearcher
import core.information_explorer


logging.config.fileConfig("core/logger.conf")
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

    def __init__(self, root, name, output_base):
        self.root = root
        self.base = core.outputstorage.ConvertName(name)
        self.name = self.base.random
        self.stream = self.load()
        self.output_path = core.outputstorage.OutputPath(output_base)
        self.source_path = self.output_path.source
        self.docx_path = self.output_path.docx
        self.html_path = self.output_path.html
        self.yaml_path = self.output_path.yaml
        self.docbook_path = self.output_path.docbook
        self.markdown_path = self.output_path.markdown
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
            >>> import core.outputstorage
            >>> import core.converterutils
            >>> basepath = 'core/test_output'
            >>> cv1 = core.converterutils.FileProcesser('core/test',
            ... 'cv_1.doc', basepath)
            >>> cv1.convert()
            True
            >>> ori = cv1.name
            >>> des = cv1.copy()
            >>> cv1.name == ori
            False
            >>> shutil.rmtree(basepath)
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
        core.outputstorage.save_stream(self.html_path, self.name.html, html_src)
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
            >>> import core.outputstorage
            >>> import core.converterutils
            >>> import xml.etree.ElementTree
            >>> basepath = 'core/test_output'
            >>> cv1 = core.converterutils.FileProcesser('core/test',
            ... 'cv_1.doc', basepath)
            >>> cv1.convert()
            True
            >>> e = xml.etree.ElementTree.parse(os.path.join(
            ... cv1.docbook_path, cv1.name.xml)).getroot()
            >>> e.findall('para')[0].text
            'http://jianli.yjbys.com/'
            >>> with open(os.path.join(cv1.markdown_path,
            ... cv1.name.md))as file:
            ...     data = file.read()
            >>> 'http://jianli.yjbys.com/' in data
            True
            >>> shutil.rmtree(basepath)
        """
        logger.info('Convert: %s' % os.path.join(self.root, self.base))
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
                return False
            self.remove_note()
            self.file_docbook_to_markdown()
            core.information_explorer.catch(self.markdown_path, self.name,
                                            self.base.base, self.yaml_path)
            logger.info('Success')
            return True
        else:
            logger.info('Skip')
            return False

    def deleteconvert(self):
        """
            >>> import shutil
            >>> import os.path
            >>> import core.outputstorage
            >>> import core.converterutils
            >>> basepath = 'core/test_output'
            >>> cv1 = core.converterutils.FileProcesser('core/test',
            ... 'cv_1.doc', basepath)
            >>> cv1.convert()
            True
            >>> os.path.isfile(os.path.join(cv1.markdown_path,
            ... cv1.name.md))
            True
            >>> cv1.deleteconvert()
            >>> os.path.isfile(os.path.join(cv1.markdown_path,
            ... cv1.name.md))
            False
            >>> shutil.rmtree(basepath)
        """
        filename = os.path.join(self.docx_path, self.name.docx)
        if os.path.isfile(filename):
            os.remove(filename)
        filename = os.path.join(self.html_path, self.name.html)
        if os.path.isfile(filename):
            os.remove(filename)
        filename = os.path.join(self.yaml_path, self.name.yaml)
        if os.path.isfile(filename):
            os.remove(filename)
        filename = os.path.join(self.docbook_path, self.name.xml)
        if os.path.isfile(filename):
            os.remove(filename)
        filename = os.path.join(self.markdown_path, self.name.md)
        if os.path.isfile(filename):
            os.remove(filename)

    def storage(self, repo, committer=None):
        """
            >>> import glob
            >>> import shutil
            >>> import os.path
            >>> import core.outputstorage
            >>> import core.converterutils
            >>> import repointerface.gitinterface
            >>> basepath = 'core/test_output'
            >>> repo_name = 'core/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> cv1 = core.converterutils.FileProcesser('core/test',
            ... 'cv_1.doc', basepath)
            >>> cv2 = core.converterutils.FileProcesser('core/test',
            ... 'cv_2.doc', basepath)
            >>> cv1.storage(interface)
            True
            >>> cv2.storage(interface)
            True
            >>> md_list = []
            >>> for position in glob.glob(os.path.join(repo_name, '*.md')):
            ...     with open(position) as f:
            ...         md_list.append(f.read())
            >>> yaml_list = []
            >>> for position in glob.glob(os.path.join(repo_name, '*.yaml')):
            ...     with open(position) as f:
            ...         yaml_list.append(f.read())
            >>> len(yaml_list)
            2
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(basepath)
        """
        path = repo.repo.path
        unique_checker = core.uniquesearcher.UniqueSearcher(repo)
        if unique_checker.unique_name(self.base.base) is False:
            logger.info(error)
            raise core.exception.DuplicateException(
                'Duplicate files: %s' % self.base.base)
        if self.convert() is False:
            return False
        shutil.copy(os.path.join(self.markdown_path, self.name.md),
                    os.path.join(path, self.name.md))
        shutil.copy(os.path.join(self.yaml_path, self.name.yaml),
                    os.path.join(path, self.name.yaml))
        repo.add_files([self.name.md, self.name.yaml],
                       committer=committer)
        logger.info('Finish')
        return True
