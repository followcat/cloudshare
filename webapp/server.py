# -*- coding: utf-8 -*-
from flask import Flask, request, render_template

import os
import glob
import codecs
import os.path

import yaml
import pypandoc

import core.outputstorage
import core.converterutils
import repointerface.gitinterface

app = Flask(__name__)
repo = repointerface.gitinterface.GitInterface("repo")


@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_text = request.form['search_text']
        result = repo.grep(search_text)
        datas = []
        for each in result:
            base, suffix = os.path.splitext(each)
            name = core.outputstorage.ConvertName(base)
            with open(os.path.join(repo.repo.path, name.yaml), 'r') as yf:
                stream = yf.read()
            yaml_data = yaml.load(stream)
            datas.append([os.path.join(repo.repo.path, name), yaml_data])
        return render_template('search_result.html',
                               search_key=search_text,
                               result=datas)
    else:
        return render_template('search.html')


@app.route("/listdata")
def listdata():
    datas = []
    for position in glob.glob(os.path.join(repo.repo.path, '*.yaml')):
        with open(position, 'r') as yf:
            stream = yf.read()
        yaml_data = yaml.load(stream)
        datas.append([os.path.splitext(position)[0],
                      yaml_data])
    return render_template('listdata.html', datas=datas)


@app.route("/showtest/<path:filename>")
def showtest(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
    output = pypandoc.convert(data, 'html', format='markdown')
    return render_template('cv.html', markdown=output)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        network_file = request.files['file']
        convertname = core.outputstorage.ConvertName(
            network_file.filename.encode('utf-8'))
        path = '/tmp'
        core.outputstorage.save_stream(path, convertname, network_file.read())
        storage_file = core.converterutils.FileProcesser(path, convertname)
        try:
            result = storage_file.convert()
            if result is False:
                return render_template('upload.html', result='Can not Convert')
        except:
            return render_template('upload.html', result='Exist File')
        md_html = showtest(os.path.join(core.outputstorage.OutputPath.markdown,
                                        storage_file.name.md))
        storage_file.deleteconvert()
        return md_html
    else:
        return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4888)
