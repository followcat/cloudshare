import core.docprocessor

SUPPORT_DOCPROCESSOR = {'pandoc': core.docprocessor.PandocProcessor,
                     'libreoffice': core.docprocessor.LibreOfficeProcessor}
SVC_DOCPROCESSOR = SUPPORT_DOCPROCESSOR['libreoffice']
