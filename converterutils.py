# -*- coding: utf-8 -*-
import email
import os.path
import mimetypes
import subprocess

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


def storage(file, repo):
    stream = file.read()
    path = repo.repo.path + '/'

    basename, _ = os.path.splitext(file.filename)
    localname = file.filename

    htmlname = basename + '.html'
    mdname = basename + '.md'
    mimetype = file.mimetype
    save_stream(path, localname, stream)
    if mimetype == 'application/pdf':
        file_pdf_to_html(path, localname)
    elif mimetype == 'application/msword':
        returncode = file_doc_to_html(path, localname)
        if 'Document is empty' in returncode[0]:
            html_src = file_mht_to_html(path, localname)
            save_stream(path, htmlname, html_src)
    md = file_html_to_md(path, htmlname).encode('utf-8')
    save_stream(path, mdname, md)
    repo.add_file(path, mdname, md)
    return md
