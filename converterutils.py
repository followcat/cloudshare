# -*- coding: utf-8 -*-
import os
import email
import logging
import os.path
import mimetypes
import subprocess
import logging.config
import xml.etree.ElementTree

import magic
import pypandoc
import emaildata.text

import information_explorer


logging.config.fileConfig("logger.conf")
logger = logging.getLogger("converterinfo")


class ConverName(str):
    def __new__(cls, value):
        """
            >>> import converterutils
            >>> name = 'base.cvs.doc'
            >>> convername = converterutils.ConverName(name)
            >>> convername.xml
            'base.cvs.xml'
            >>> convername.yaml
            'base.cvs.yaml'
            >>> convername.doc
            'base.cvs.doc'
            >>> convername.docx
            'base.cvs.docx'
            >>> convername.md
            'base.cvs.md'
        """
        obj = str.__new__(cls, value)
        obj.base, obj.suffix = os.path.splitext(value)
        obj._xml = obj._add_suffix('xml')
        obj._html = obj._add_suffix('html')
        obj._yaml = obj._add_suffix('yaml')
        obj._doc = obj._add_suffix('doc')
        obj._docx = obj._add_suffix('docx')
        obj._md = obj._add_suffix('md')
        return obj

    def _add_suffix(self, suffix):
        return self.base + '.' + suffix

    @property
    def xml(self):
        return self._xml

    @property
    def html(self):
        return self._html

    @property
    def yaml(self):
        return self._yaml

    @property
    def doc(self):
        return self._doc

    @property
    def docx(self):
        return self._docx

    @property
    def md(self):
        return self._md


def file_pdf_to_html(path, filename):
    p = subprocess.Popen(['pdftohtml', '-noframes', os.path.join(path, filename)],
                         stdout=subprocess.PIPE)
    p.communicate()


def file_html_to_md(path, filename):
    result = pypandoc.convert(os.path.join(path, filename), 'md', format='html')
    return result


def save_stream(path, filename, stream):
    with open(os.path.join(path, filename), 'wb') as localfile:
        localfile.write(stream)


def file_mht_to_html(path, filename):
    message = email.message_from_file(open(os.path.join(path, filename)))
    html = emaildata.text.Text.html(message)
    return html


def storage(filename, fileobj, repo):
    """
        >>> import shutil
        >>> import gitinterface
        >>> import converterutils
        >>> repo_name = 'test_repo'
        >>> interface = gitinterface.GitInterface(repo_name)
        >>> cv1_name = 'cv_1.doc'
        >>> cv2_name = 'cv_2.doc'
        >>> cv1_file = open('test/' + cv1_name, 'r')
        >>> cv2_file = open('test/' + cv2_name, 'r')
        >>> md1_str = converterutils.storage(cv1_name, cv1_file, interface)
        >>> md2_str = converterutils.storage(cv2_name, cv2_file, interface)
        >>> with open('test_repo/cv_1.md') as file:
        ...     md1_file = file.read()
        >>> with open('test_repo/cv_2.md') as file:
        ...     md2_file = file.read()
        >>> md1_str == md1_file
        True
        >>> md2_str == md2_file
        True
        >>> shutil.rmtree(repo_name)
    """
    mimetype = magic.Magic()
    stream = fileobj.read()
    path = repo.repo.path

    basename, _ = os.path.splitext(filename)
    localname = filename

    htmlname = basename + '.html'
    mdname = basename + '.md'
    mimetype = mimetype.from_buffer(stream)
    save_stream(path, localname, stream)
    if mimetype.startswith('PDF'):
        file_pdf_to_html(path, localname)
    elif mimetype.startswith('news or mail'):
        html_src = file_mht_to_html(path, localname)
        save_stream(path, htmlname, html_src)
    else:
        returncode = convert_docfile(repo.repo.path, localname,
                                     repo.repo.path, 'html')
    md = file_html_to_md(path, htmlname).encode('utf-8')
    save_stream(path, mdname, md)
    repo.add_file(path, mdname, md)
    return md


def convert_docfile(path, filename, output, format):
    p = subprocess.Popen(['libreoffice', '--headless', '--convert-to',
                          format, os.path.join(path, filename),
                          '--outdir', output],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    returncode = p.communicate()
    logger.info(returncode[0])
    return returncode


def file_docbook_to_markdown(path, convertname, output):
    input_file = os.path.join(path, convertname.xml)
    output_file = os.path.join(output, convertname.md)
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


def remove_note(path, convertname):
    e = xml.etree.ElementTree.parse(os.path.join(path, convertname))
    note_parent = e.findall('.//note/..')
    for parent in note_parent:
        while(parent.find('note') is not None):
            parent.remove(parent.find('note'))
    e.write(os.path.join(path, convertname), encoding='utf-8')


def process_mht(stream, docx_path, convertname):
    message = email.message_from_string(stream)
    for part in message.walk():
        if part.get_content_charset() is not None:
            part.set_param('charset', 'utf-8')
    html_src = emaildata.text.Text.html(message)
    save_stream(docx_path, convertname.html, html_src)
    returncode = convert_docfile(docx_path, convertname.html,
                                 docx_path, 'docx:Office Open XML Text')
    return returncode


def convert_folder(path):
    """
        >>> import os
        >>> import converterutils
        >>> import xml.etree.ElementTree
        >>> converterutils.convert_folder('./test')
        >>> e = xml.etree.ElementTree.parse('docbook_output/cv_1.xml').getroot()
        >>> e.findall('para')[0].text
        'http://jianli.yjbys.com/'
        >>> with open('md_output/cv_1.md') as file:
        ...     data = file.read()
        >>> 'http://jianli.yjbys.com/' in data
        True
        >>> os.remove('docbook_output/cv_1.xml')
        >>> os.remove('docbook_output/cv_2.xml')
        >>> os.remove('md_output/cv_1.md')
        >>> os.remove('md_output/cv_2.md')
    """
    docx_path = 'docx_output'
    markdown_path = 'md_output'
    docbook_path = 'docbook_output'
    yaml_path = 'yaml_output'
    if not os.path.exists(docx_path):
        os.mkdir(docx_path)
    if not os.path.exists(markdown_path):
        os.mkdir(markdown_path)
    if not os.path.exists(docbook_path):
        os.mkdir(docbook_path)
    if not os.path.exists(yaml_path):
        os.mkdir(yaml_path)
    for root, dirs, files in os.walk(path):
        for name in files:
            conname = ConverName(name)
            logger.info('Convert: %s' % os.path.join(root, conname))
            mimetype = mimetypes.guess_type(os.path.join(root, conname))[0]
            logger.info('Mimetype: %s' % mimetype)
            if mimetype in ['application/msword',
                            "application/vnd.openxmlformats-officedocument"
                            ".wordprocessingml.document"]:
                with open(os.path.join(root, conname), 'r') as f:
                    stream = f.read()
                if 'multipart/related' in stream:
                    process_mht(stream, docx_path, conname)
                    returncode = convert_docfile(docx_path, conname.docx,
                                                 docbook_path,
                                                 'xml:DocBook File')
                else:
                    returncode = convert_docfile(root, conname, docbook_path,
                                                 'xml:DocBook File')
                if "Error" in returncode[0]:
                    returncode = convert_docfile(root, conname, docx_path,
                                                 'docx:Office Open XML Text')
                    returncode = convert_docfile(docx_path, conname.docx,
                                                 docbook_path,
                                                 'xml:DocBook File')
                if not os.path.exists(os.path.join(
                                      docbook_path, conname.xml)):
                    logger.info('Not exists')
                    continue
                remove_note(docbook_path, conname.xml)
                file_docbook_to_markdown(docbook_path, conname,
                                         markdown_path)
                information_explorer.catch(markdown_path, conname,
                                           yaml_path)
                logger.info('Success')
            else:
                logger.info('Skip')
            logger.info('Finish')
