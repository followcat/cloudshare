# -*- coding: utf-8 -*-

import os.path
import mimetypes

from flask import Flask, request, render_template

import gitinterface
import converterutils

app = Flask(__name__)
repo = gitinterface.GitInterface("repo")


@app.route("/", methods=['GET', 'POST'])
@app.route("/demo", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        stream = file.read()
        localname = '/tmp/' + file.filename
        converterutils.save_stream(stream, localname)
        format, _ = mimetypes.guess_type(localname)
        basename, _ = os.path.splitext(localname)
        htmlname = basename + '.html'
        if format == 'application/pdf':
            converterutils.pdf_to_html(localname)
        elif format in ['application/msword',
                        'application/vnd.openxmlformats-officedocument.\
                        wordprocessingml.document']:
            returncode = converterutils.doc_to_html(localname, '/tmp')
            if 'error' in returncode[0]:
                html_src = converterutils.file_mht_to_html(localname)
                converterutils.save_stream(html_src, htmlname)
        md = converterutils.file_html_to_md(htmlname)
        format_md = md.replace('\\\n', '\n\n')
        return render_template('index.html', markdown=format_md)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4888)
