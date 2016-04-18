import re
import email
import logging
import os.path
import mimetypes
import logging.config
import xml.etree.ElementTree

import pypandoc
import emaildata.text

import utils.builtin
import utils.unoconverter
import core.exception
import core.outputstorage
import core.information_explorer


converter = utils.unoconverter.DocumentConverter()
logging.config.fileConfig("core/logger.conf")
logger = logging.getLogger("converterinfo")


def convert_docfile(input, filename, output, outputname):
    returncode = True
    try:
        converter.convert(os.path.join(input, filename), os.path.join(output, outputname))
    except Exception as e:
        logger.info(e)
        returncode = False
    return returncode

def md_to_html(stream):
    new_stream = stream
    res = re.findall(ur"([^- \n]+[- ]{4,}[-]+)", stream)
    for match in res:
        new_list = re.split(ur"[ ]+", match, maxsplit=1)
        new_list.reverse()
        new_str = "\n".join(new_list)
        new_stream = new_stream.replace(match, new_str)
    md = pypandoc.convert(new_stream, 'html', format='markdown')
    return md


class FileProcesser():

    def __init__(self, fileobj, name, output_base):
        self.yamlinfo = {}
        self.markdown_stream = ''

        self.base = core.outputstorage.ConvertName(name)
        self.name = self.base.random
        self.stream = fileobj.read()

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

        self.result = self.convert()

    def mimetype(self):
        mimetype = mimetypes.guess_type(os.path.join(
                                        self.source_path, self.name.origin))[0]
        return mimetype

    def copy(self, des=None, name=None):
        """
            >>> import shutil
            >>> import core.converterutils
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.doc', 'r')
            >>> cv1 = core.converterutils.FileProcesser(f, 'cv_1.doc', basepath)
            >>> cv1.result
            True
            >>> ori = cv1.name
            >>> des = cv1.copy()
            >>> cv1.name == ori
            False
            >>> f.close()
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
                                     self.docx_path, self.name.docx)
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
        self.markdown_stream = ''
        input_file = os.path.join(self.docbook_path, self.name.xml)
        output_file = os.path.join(self.markdown_path, self.name.md)
        try:
            output = pypandoc.convert(input_file, 'markdown', format='docbook')
            with open(output_file, 'w') as f:
                for line in output.split('\n'):
                    data = line.lstrip(' ')+'\n'
                    f.write(data.encode('utf-8'))
                    self.markdown_stream += data
        except RuntimeError as e:
            pass

    def convert(self):
        """
            >>> import os
            >>> import shutil
            >>> import core.converterutils
            >>> import xml.etree.ElementTree
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.doc', 'r')
            >>> cv1 = core.converterutils.FileProcesser(f, 'cv_1.doc', basepath)
            >>> cv1.result
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
            >>> f.close()
            >>> shutil.rmtree(basepath)
        """
        logger.info('Convert: %s' % self.base)
        if self.mimetype in ['application/msword',
                             "application/vnd.openxmlformats-officedocument"
                             ".wordprocessingml.document"]:
            if 'multipart/related' in self.stream:
                self.process_mht()
                returncode = convert_docfile(self.docx_path, self.name.docx,
                                             self.docbook_path, self.name.xml)
            else:
                returncode = convert_docfile(self.source_path, self.name,
                                             self.docbook_path, self.name.xml)
            if returncode is False:
                returncode = convert_docfile(self.source_path, self.name,
                                             self.docx_path, self.name.docx)
                returncode = convert_docfile(self.docx_path, self.name.docx,
                                             self.docbook_path, self.name.xml)
            if not os.path.exists(os.path.join(
                                  self.docbook_path, self.name.xml)):
                logger.info('Not exists')
                return False
            self.remove_note()
            self.file_docbook_to_markdown()
            self.yamlinfo = core.information_explorer.catch(
                self.markdown_path, self.name, self.base.base)
            utils.builtin.save_yaml(self.yamlinfo, self.yaml_path, self.name.yaml)
            logger.info('Success')
            return True
        else:
            logger.info('Skip')
            return False

    def deleteconvert(self):
        """
            >>> import shutil
            >>> import os.path
            >>> import core.converterutils
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.doc', 'r')
            >>> cv1 = core.converterutils.FileProcesser(f, 'cv_1.doc', basepath)
            >>> cv1.result
            True
            >>> os.path.isfile(os.path.join(cv1.markdown_path,
            ... cv1.name.md))
            True
            >>> cv1.deleteconvert()
            >>> os.path.isfile(os.path.join(cv1.markdown_path,
            ... cv1.name.md))
            False
            >>> f.close()
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
