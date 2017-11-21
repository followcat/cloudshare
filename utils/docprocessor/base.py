import os
import logging
import logging.config

import core.outputstorage

logging.config.fileConfig("core/logger.conf")
logger = logging.getLogger("converterinfo")


class Processor(object):
    """
        result code:
            0 - success
            1 - can not generate docbook
            2 - convert exception
            3 - not support doc type
    """

    def __init__(self, fileobj, name, output_base):
        self.resultcode = None
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

    def copy(self, des=None, name=None):
        """
            >>> import shutil
            >>> import utils.docprocessor.base
            >>> basepath = 'core/test_output'
            >>> f = open('core/test/cv_1.docx', 'r')
            >>> cv1 = utils.docprocessor.base.Processor(f, 'cv_1.docx', basepath)
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
