import os

import pypandoc

import core.outputstorage
import utils.docprocessor.base
from utils.docprocessor.base import logger


class PandocProcessor(utils.docprocessor.base.Processor):

    def __init__(self, fileobj, name, output_base):
        super(PandocProcessor, self).__init__(fileobj, name, output_base)
        self.result = self.convert()

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
            >>> import utils.docprocessor.pandoc
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = utils.docprocessor.pandoc.PandocProcessor(f, 'cv_1.docx', basepath)
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
            self.resultcode = 2
            return False
        logger.info(' '.join([self.base.base, self.name.base, 'Success']))
        self.resultcode = 0
        return True

    def renameconvert(self, new):
        """
            >>> import shutil
            >>> import os.path
            >>> import utils.docprocessor.pandoc
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = utils.docprocessor.pandoc.PandocProcessor(f, 'cv_1.docx', basepath)
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
            >>> import utils.docprocessor.pandoc
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = utils.docprocessor.pandoc.PandocProcessor(f, 'cv_1.docx', basepath)
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
