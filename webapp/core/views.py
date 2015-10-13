
import os
import glob
import codecs
import os.path

import yaml
import flask
import pypandoc
import flask.views

import core.outputstorage
import core.converterutils
import repointerface.gitinterface

repo = repointerface.gitinterface.GitInterface("repo")


class Search(flask.views.MethodView):
    def get(self):
        return flask.render_template('search.html')

    def post(self):
        search_text = flask.request.form['search_text']
        result = repo.grep(search_text)
        datas = []
        for each in result:
            base, suffix = os.path.splitext(each)
            name = core.outputstorage.ConvertName(base)
            with open(os.path.join(repo.repo.path, name.yaml), 'r') as yf:
                stream = yf.read()
            yaml_data = yaml.load(stream)
            datas.append([os.path.join(repo.repo.path, name), yaml_data])
        return flask.render_template('search_result.html',
                                     search_key=search_text,
                                     result=datas)


class Listdata(flask.views.MethodView):
    def get(self):
        datas = []
        for position in glob.glob(os.path.join(repo.repo.path, '*.yaml')):
            with open(position, 'r') as yf:
                stream = yf.read()
            yaml_data = yaml.load(stream)
            datas.append([os.path.splitext(position)[0],
                          yaml_data])
        return flask.render_template('listdata.html', datas=datas)


class Upload(flask.views.MethodView):
    def get(self):
        return flask.render_template('upload.html')

    def post(self):
        network_file = flask.request.files['file']
        convertname = core.outputstorage.ConvertName(
            network_file.filename.encode('utf-8'))
        path = '/tmp'
        core.outputstorage.save_stream(path, convertname, network_file.read())
        storage_file = core.converterutils.FileProcesser(path, convertname)
        try:
            result = storage_file.convert()
            if result is False:
                return flask.render_template('upload.html', result='Can not Convert')
        except:
            return flask.render_template('upload.html', result='Exist File')
        md_html = showtest(os.path.join(core.outputstorage.OutputPath.markdown,
                                        storage_file.name.md))
        storage_file.deleteconvert()
        return md_html


class Showtest(flask.views.MethodView):
    def get(self, filename):
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
        output = pypandoc.convert(data, 'html', format='markdown')
        return flask.render_template('cv.html', markdown=output)
