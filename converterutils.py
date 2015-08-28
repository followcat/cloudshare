# -*- coding: utf-8 -*-
import email
import os.path
import mimetypes
import subprocess

import magic
import pypandoc
import emaildata.text


"""
def doc_to_docx(file_uri, output_dir):
    p = subprocess.Popen(['soffice', '--headless', '-convert-to',
                          'docx:MS Word 2007 XML', file_uri,
                          '--outdir', output_dir],
                         stdout=subprocess.PIPE)
    p.communicate()


def file_docx_to_md(file_uri):
    result = pypandoc.convert(file_uri, 'md', format='docx')
    return result
"""


def file_pdf_to_html(path, filename):
    p = subprocess.Popen(['pdftohtml', '-noframes', path + filename],
                         stdout=subprocess.PIPE)
    p.communicate()


def file_doc_to_html(path, filename):
    p = subprocess.Popen(['soffice', '--headless', '--convert-to',
                          'html', path + filename, '--outdir', path],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    returncode = p.communicate()
    return returncode


def file_html_to_md(path, filename):
    result = pypandoc.convert(path + filename, 'md', format='html')
    return result


def str_md_to_html(md_code):
    result = pypandoc.convert(md_code, 'html', format='md')
    return result


def save_stream(path, filename, stream):
    with open(path + filename, 'wb') as localfile:
        localfile.write(stream)


def file_mht_to_html(path, filename):
    message = email.message_from_file(open(path + filename))
    html = emaildata.text.Text.html(message)
    return html


def get_md_version(filename):
    basename, _ = os.path.splitext(filename)
    return basename + '.md'


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
    path = repo.repo.path + '/'

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
       returncode = file_doc_to_html(path, localname)
    md = file_html_to_md(path, htmlname).encode('utf-8')
    save_stream(path, mdname, md)
    repo.add_file(path, mdname, md)
    return md
