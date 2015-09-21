# -*- coding: utf-8 -*-
from flask import Flask, request, render_template

import os
import codecs
import os.path

import yaml
import pypandoc

import gitinterface
import outputstorage
import converterutils

app = Flask(__name__)
repo = gitinterface.GitInterface("repo")


@app.route("/")
def listdata():
    files = list(os.walk(outputstorage.OutputPath.markdown))[0][2]
    datas = []
    for f in files:
        conname = outputstorage.ConvertName(f)
        with open(os.path.join(
                  outputstorage.OutputPath.yaml, conname.yaml), 'r') as yf:
            stream = yf.read()
        yaml_data = yaml.load(stream)
        datas.append([os.path.splitext(f)[0],
                      yaml_data])
    return render_template('listdata.html', datas=datas)


@app.route("/showtest/<filename>")
def showtest(filename):
    with codecs.open(os.path.join(
                     outputstorage.OutputPath.markdown, filename),
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
        convertname = outputstorage.ConvertName(
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
