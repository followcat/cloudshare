import os
import xml
import shutil

import mimetypes

import pypandoc

import core.outputstorage
import utils.docprocessor.base
import utils.docprocessor.unoconverter
from utils.docprocessor.base import logger


class LibreOfficeProcessor(utils.docprocessor.base.Processor):

    converter = None

    def __init__(self, fileobj, name, output_base):
        super(LibreOfficeProcessor, self).__init__(fileobj, name, output_base)
        if self.converter is None:
            self.__class__.converter = utils.docprocessor.unoconverter.DocumentConverter()
        self.html_path = self.output_path.html
        self.docbook_path = self.output_path.docbook

        self.mimetype = self.mimetype()
        logger.info('Mimetype: %s' % self.mimetype)
        self.result = self.convert()

    def mimetype(self):
        mimetype = mimetypes.guess_type(os.path.join(
                                        self.source_path, self.name.origin))[0]
        return mimetype

    def convert_docfile(self, input, filename, output, outputname):
        result = True
        try:
            self.converter.convert(os.path.join(input, filename),
                                   os.path.join(output, outputname))
        except Exception as e:
            logger.info(e)
            result = False
        return result

    def remove_note(self):
        position = os.path.join(self.docbook_path, self.name.xml)
        e = xml.etree.ElementTree.parse(position)
        note_parent = e.findall('.//note/..')
        for parent in note_parent:
            while(parent.find('note') is not None):
                parent.remove(parent.find('note'))
        e.write(position, encoding='utf-8')

    def file_docbook_to_markdown(self):
        self.markdown_stream = str()
        input_file = os.path.join(self.docbook_path, self.name.xml)
        output_file = os.path.join(self.markdown_path, self.name.md)
        try:
            output = pypandoc.convert(input_file, 'markdown', format='docbook')
            with open(output_file, 'w') as f:
                for line in output.split('\n'):
                    data = line.lstrip(' ')+'\n'
                    encoded_data = data.encode('utf-8')
                    f.write(encoded_data)
                    self.markdown_stream += encoded_data
        except RuntimeError as e:
            pass

    def convert(self):
        """
            >>> import os
            >>> import shutil
            >>> import utils.docprocessor.libreoffice
            >>> import xml.etree.ElementTree
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.doc', 'r')
            >>> cv1 = utils.docprocessor.libreoffice.LibreOfficeProcessor(f, 'cv_1.doc', basepath)
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
        if self.mimetype in ["application/msword",
                             "application/vnd.openxmlformats-officedocument"
                             ".wordprocessingml.document"]:
            if self.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                shutil.copyfile(os.path.join(self.source_path, self.name),
                                os.path.join(self.docx_path, self.name.docx))
            elif self.mimetype == "application/msword":
                returncode = self.convert_docfile(self.source_path, self.name,
                                                  self.docx_path, self.name.docx)
            returncode = self.convert_docfile(self.docx_path, self.name.docx,
                                              self.docbook_path, self.name.xml)
            if not os.path.exists(os.path.join(
                                  self.docbook_path, self.name.xml)):
                logger.info('Not exists')
                self.resultcode = 2
                return False
            if returncode is False:
                self.resultcode = 3
                return False
            self.remove_note()
            self.file_docbook_to_markdown()
            logger.info(' '.join([self.base.base, self.name.base, 'Success']))
            self.resultcode = 0
            return True
        else:
            logger.info('Skip')
            self.resultcode = 1
            return False

    def renameconvert(self, new):
        """
            >>> import shutil
            >>> import os.path
            >>> import utils.docprocessor.libreoffice
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.doc', 'r')
            >>> cv1 = utils.docprocessor.libreoffice.LibreOfficeProcessor(f, 'cv_1.doc', basepath)
            >>> cv1.result
            True
            >>> os.path.isfile(os.path.join(cv1.markdown_path,
            ... cv1.name.md))
            True
            >>> cv1.renameconvert('newname.md')
            >>> os.path.isfile(os.path.join(cv1.markdown_path, cv1.name.md))
            False
            >>> os.path.isfile(os.path.join(cv1.markdown_path, 'newname.md'))
            True
            >>> f.close()
            >>> shutil.rmtree(basepath)
        """
        newname = core.outputstorage.ConvertName(new)

        oldfile = os.path.join(self.docx_path, self.name.docx)
        newfile = os.path.join(self.docx_path, newname.docx)
        if os.path.isfile(oldfile):
            os.rename(oldfile, newfile)

        oldfile = os.path.join(self.html_path, self.name.html)
        newfile = os.path.join(self.html_path, newname.html)
        if os.path.isfile(oldfile):
            os.rename(oldfile, newfile)

        oldfile = os.path.join(self.docbook_path, self.name.xml)
        newfile = os.path.join(self.docbook_path, newname.xml)
        if os.path.isfile(oldfile):
            os.rename(oldfile, newfile)

        oldfile = os.path.join(self.markdown_path, self.name.md)
        newfile = os.path.join(self.markdown_path, newname.md)
        if os.path.isfile(oldfile):
            os.rename(oldfile, newfile)

        oldfile = os.path.join(self.source_path, self.name)
        newfile = os.path.join(self.source_path, newname + self.name.suffix)
        if os.path.isfile(oldfile):
            os.rename(oldfile, newfile)


    def deleteconvert(self):
        """
            >>> import shutil
            >>> import os.path
            >>> import utils.docprocessor.libreoffice
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.doc', 'r')
            >>> cv1 = utils.docprocessor.libreoffice.LibreOfficeProcessor(f, 'cv_1.doc', basepath)
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
        filename = os.path.join(self.docbook_path, self.name.xml)
        if os.path.isfile(filename):
            os.remove(filename)
        filename = os.path.join(self.markdown_path, self.name.md)
        if os.path.isfile(filename):
            os.remove(filename)
