import email
import pypandoc
import subprocess

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


def pdf_to_html(file_uri):
    p = subprocess.Popen(['pdftohtml', '-noframes', file_uri],
                         stdout=subprocess.PIPE)
    p.communicate()


def doc_to_html(file_uri, output_dir):
    p = subprocess.Popen(['soffice', '--headless', '--convert-to',
                          'html', file_uri, '--outdir', output_dir],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    returncode = p.communicate()
    return returncode


def file_html_to_md(file_uri):
    result = pypandoc.convert(file_uri, 'md', format='html')
    return result


def str_md_to_html(md_code):
    result = pypandoc.convert(md_code, 'html', format='md')
    return result


def save_stream(stream, file_uri):
    with open(file_uri, 'wb') as localfile:
        localfile.write(stream)


def file_mht_to_html(file_uri):
    message = email.message_from_file(open(file_uri))
    html = emaildata.text.Text.html(message)
    return html
