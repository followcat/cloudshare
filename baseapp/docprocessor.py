SUPPORT_DOCPROCESSOR = {}

try:
    import utils.docprocessor.pandoc
    SUPPORT_DOCPROCESSOR['pandoc'] = utils.docprocessor.pandoc.PandocProcessor
except ImportError:
    pass

try:
    import utils.docprocessor.libreoffice
    SUPPORT_DOCPROCESSOR['libreoffice'] = utils.docprocessor.libreoffice.LibreOfficeProcessor
except ImportError:
    pass

SVC_DOCPROCESSOR = SUPPORT_DOCPROCESSOR['libreoffice']
