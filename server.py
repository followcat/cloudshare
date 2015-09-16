# -*- coding: utf-8 -*-
from flask import Flask, request, render_template

import os
import codecs

import pypandoc
import markdown

import gitinterface
import converterutils

app = Flask(__name__)
repo = gitinterface.GitInterface("repo")


@app.route("/")
def listdata():
    files = list(os.walk('./output/markdown'))[0][2]
    datas = [f.decode('utf-8').split('.')[0] for f in files]
    return render_template('listdata.html', datas=datas)


@app.route("/showtest/<filename>")
def showtest(filename):
    with codecs.open('./output/markdown/%s' % filename,
                     'r', encoding='utf-8') as file:
        data = file.read()
    output = pypandoc.convert(data, 'html', format='markdown')
    return render_template('cv.html', markdown=output)


@app.route("/upload", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        network_file = request.files['file']
        if network_file.mimetype == 'application/octet-stream':
            return render_template('index.html', error='Please enter filename.')
        convertname = converterutils.ConverName(
            network_file.filename.encode('utf-8'))
        local_file = repo.repo.get_named_file('../' + convertname.md)
        if local_file is not None:
            md = local_file.read()
            local_file.close()
        else:
            md = converterutils.storage(convertname,
                                        network_file, repo)
        format_md = md.decode('utf-8').replace('\\\n', '\n\n')
        return render_template('upload.html', markdown=format_md)
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4888)
