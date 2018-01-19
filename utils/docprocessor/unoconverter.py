import uno
import time
import os.path
import subprocess

from com.sun.star.beans import PropertyValue
from com.sun.star.task import ErrorCodeIOException
from com.sun.star.connection import NoConnectException

import utils.builtin
import utils.timeout.thread
import utils.timeout.exception
from utils.docprocessor.base import logger

DEFAULT_OPENOFFICE_PORT = 8100

FAMILY_TEXT = "Text"
FAMILY_WEB = "Web"
FAMILY_SPREADSHEET = "Spreadsheet"
FAMILY_PRESENTATION = "Presentation"
FAMILY_DRAWING = "Drawing"

# http://wiki.services.openoffice.org/wiki/Framework/Article/Filter

EXPORT_FILTER_MAP = {
    "xml": {
        FAMILY_TEXT: {"FilterName": "DocBook File"},
        FAMILY_WEB: {"FilterName": "DocBook File"},
    },
    "odt": {
        FAMILY_TEXT: {"FilterName": "writer8"},
        FAMILY_WEB: {"FilterName": "writerweb8_writer"}
    },
    "doc": {
        FAMILY_TEXT: {"FilterName": "MS Word 97"},
        FAMILY_WEB: {"FilterName": "MS Word 97"}
    },
    "docx": {
        FAMILY_TEXT: {"FilterName": "Office Open XML Text"},
        FAMILY_WEB: {"FilterName": "Office Open XML Text"}
    },
}


class DocumentConversionException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class DocumentConverter:

    def __init__(self, host='localhost', port=DEFAULT_OPENOFFICE_PORT, invisible=True):
        self.p = None
        self.host = host
        self.port = port
        self.invisible = invisible
        self.startservice()
        self.localContext = uno.getComponentContext()
        self.resolver = self.localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",
                        self.localContext)

    def startservice(self):

        def close_soffice():
            command = ['pkill', '-9', 'soffice.bin']
            subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

        def wait_until_port_open(timeout=10):
            count = 0
            while(not utils.builtin.is_port_open(self.host, self.port)):
                time.sleep(0.01)
                count += 0.01
                if count > timeout:
                    print "Can not connect unoconverter server."
                    logger.info("Can not connect unoconverter server.")
                    break

        close_soffice()
        if not utils.builtin.is_port_open(self.host, self.port):
            command = ['libreoffice',
                       '--accept=socket,host=%s,port=%s;urp;'%(self.host, self.port)]
            if self.invisible is True:
                command.append('--invisible')
            if self.p:
                self.p.kill()
            self.p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
            wait_until_port_open()

    def restartservice(self):
        if self.p:
            self.p.terminate()
        self.startservice()

    def makedesktop(self):
        while(True):
            try:
                context = self.resolver.resolve("uno:socket,host=localhost,port=%s;urp;StarOffice.ComponentContext" % self.port)
                self.desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
                break
            except Exception as e:
                self.restartservice()
                logger.info("%s. Restart service and rebuild desktop." % e)
            if not utils.builtin.is_port_open(self.host, self.port):
                raise DocumentConversionException, "failed to connect to OpenOffice.org on port %s" % self.port

    def convert(self, inputFile, outputFile):
        retry = 0
        inputUrl = self._toFileUrl(inputFile)
        outputUrl = self._toFileUrl(outputFile)
        loadProperties = {"Hidden": True}
        self.makedesktop()
        while(True and retry<3):
            try:
                document = utils.timeout.thread.timeout_call(self.desktop.loadComponentFromURL, 30,
                                                             kill_wait=1,
                                                             args=(inputUrl, "_blank", 0,
                                                                   self._toProperties(loadProperties)))
                document.refresh()
                family = self._detectFamily(document)
                outputExt = self._getFileExt(outputFile)
                storeProperties = self._getStoreProperties(document, outputExt)
                try:
                    document.storeToURL(outputUrl, self._toProperties(storeProperties))
                finally:
                    document.close(True)
                break
            except utils.timeout.exception.ExecTimeout as e:
                logger.info("DocumentConverter timeout.")
                logger.info("Restart service and rebuild desktop.")
                self.restartservice()
                self.makedesktop()
            except Exception as e:
                # com.sun.star.uno.RuntimeException:
                # Binary URP bridge already disposed
                logger.info(e)
                logger.info("Restart service and rebuild desktop.")
                self.restartservice()
                self.makedesktop()
            retry += 1

    def _getStoreProperties(self, document, outputExt):
        family = self._detectFamily(document)
        try:
            propertiesByFamily = EXPORT_FILTER_MAP[outputExt]
        except KeyError:
            raise DocumentConversionException, "unknown output format: '%s'" % outputExt
        try:
            return propertiesByFamily[family]
        except KeyError:
            raise DocumentConversionException, "unsupported conversion: from '%s' to '%s'" % (family, outputExt)

    def _detectFamily(self, document):
        if document.supportsService("com.sun.star.text.WebDocument"):
            return FAMILY_WEB
        if document.supportsService("com.sun.star.text.GenericTextDocument"):
            # must be TextDocument or GlobalDocument
            return FAMILY_TEXT
        if document.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
            return FAMILY_SPREADSHEET
        if document.supportsService("com.sun.star.presentation.PresentationDocument"):
            return FAMILY_PRESENTATION
        if document.supportsService("com.sun.star.drawing.DrawingDocument"):
            return FAMILY_DRAWING
        raise DocumentConversionException, "unknown document family: %s" % document

    def _getFileExt(self, path):
        ext = os.path.splitext(path)[1]
        if ext is not None:
            return ext[1:].lower()

    def _toFileUrl(self, path):
        return uno.systemPathToFileUrl(os.path.abspath(path))

    def _toProperties(self, dict):
        props = []
        for key in dict:
            prop = PropertyValue()
            prop.Name = key
            prop.Value = dict[key]
            props.append(prop)
        return tuple(props)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("USAGE: python %s <input-file> <output-file>" % sys.argv[0])
        sys.exit(255)
    if not os.path.isfile(sys.argv[1]):
        print("no such input file: %s" % sys.argv[1])
        sys.exit(1)

    try:
        converter = DocumentConverter()
        converter.convert(sys.argv[1], sys.argv[2])
    except DocumentConversionException, exception:
        print("ERROR! " + str(exception))
        sys.exit(1)
    except ErrorCodeIOException, exception:
        print("ERROR! ErrorCodeIOException %d" % exception.ErrCode)
        sys.exit(1)
