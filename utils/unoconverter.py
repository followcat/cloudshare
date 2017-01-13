import uno
import os.path
import subprocess

from com.sun.star.beans import PropertyValue
from com.sun.star.task import ErrorCodeIOException
from com.sun.star.connection import NoConnectException

import utils.builtin

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
        self.host = host
        self.port = port
        self.invisible = invisible
        self.startservice()
        self.localContext = uno.getComponentContext()
        self.resolver = self.localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",
                        self.localContext)

    def startservice(self):
        if not utils.builtin.is_port_open(self.host, self.port):
            command = ['libreoffice',
                       '--accept=socket,host=%s,port=%s;urp;'%(self.host, self.port)]
            if self.invisible is True:
                command.append('--invisible')
            self.p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

    def convert(self, inputFile, outputFile):
        try:
            context = self.resolver.resolve("uno:socket,host=localhost,port=%s;urp;StarOffice.ComponentContext" % self.port)
        except NoConnectException:
            self.startservice()
            if not utils.builtin.is_port_open(self.host, self.port):
                sout = self.p.stdout.readlines()
                serr = self.p.stderr.readlines()
                raise DocumentConversionException, "failed to connect to OpenOffice.org on port %s" % self.port
            context = self.resolver.resolve("uno:socket,host=localhost,port=%s;urp;StarOffice.ComponentContext" % self.port)
        self.desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)

        inputUrl = self._toFileUrl(inputFile)
        outputUrl = self._toFileUrl(outputFile)

        loadProperties = {"Hidden": True}

        document = self.desktop.loadComponentFromURL(inputUrl, "_blank", 0, self._toProperties(loadProperties))
        try:
            document.refresh()
        except AttributeError:
            pass

        family = self._detectFamily(document)

        outputExt = self._getFileExt(outputFile)
        storeProperties = self._getStoreProperties(document, outputExt)

        try:
            document.storeToURL(outputUrl, self._toProperties(storeProperties))
        finally:
            document.close(True)

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
