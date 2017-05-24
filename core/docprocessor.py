import re
import logging
import os.path
import logging.config

import pypandoc

import core.outputstorage


logging.config.fileConfig("core/logger.conf")
logger = logging.getLogger("converterinfo")


class Processor():

    def __init__(self, fileobj, name, output_base):
        self.markdown_stream = str()

        self.base = core.outputstorage.ConvertName(name)
        self.name = self.base.random
        self.stream = fileobj.read()

        self.output_path = core.outputstorage.OutputPath(output_base)
        self.source_path = self.output_path.source
        self.docx_path = self.output_path.docx
        self.markdown_path = self.output_path.markdown

        location = self.copy()
        logger.info('Backup to: %s' % location)
        self.result = self.convert()

    def copy(self, des=None, name=None):
        """
            >>> import shutil
            >>> import core.docprocessor
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = core.docprocessor.Processor(f, 'cv_1.docx', basepath)
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
            self.name = self.base
            name = self.name
            location = os.path.join(des, name)
        with open(location, 'wb') as f:
            f.write(self.stream)
        return location

    def file_docx_to_markdown(self):
        self.markdown_stream = str()
        input_file = os.path.join(self.source_path, self.name)
        output_file = os.path.join(self.markdown_path, self.name.md)
        try:
            output = pypandoc.convert(input_file, 'markdown', format='docx')
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
            >>> import core.docprocessor
            >>> import xml.etree.ElementTree
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = core.docprocessor.Processor(f, 'cv_1.docx', basepath)
            >>> cv1.result
            True
            >>> '13888888888' in cv1.markdown_stream
            True
            >>> f.close()
            >>> shutil.rmtree(basepath)
        """
        logger.info('Convert: %s' % self.base)
        self.file_docx_to_markdown()
        if not os.path.exists(os.path.join(self.markdown_path, self.name.md)):
            return False
        logger.info(' '.join([self.base.base, self.name.base, 'Success']))
        return True

    def renameconvert(self, new):
        """
            >>> import shutil
            >>> import os.path
            >>> import core.docprocessor
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = core.docprocessor.Processor(f, 'cv_1.docx', basepath)
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
            >>> import core.docprocessor
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = core.docprocessor.Processor(f, 'cv_1.docx', basepath)
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
        filename = os.path.join(self.markdown_path, self.name.md)
        if os.path.isfile(filename):
            os.remove(filename)
