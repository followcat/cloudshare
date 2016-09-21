import time
import pickle
import codecs
import os.path

import yaml
import flask
import flask.views
import flask.ext.login

import utils.builtin
import utils.chsname
import services.curriculumvitae
import core.outputstorage
import webapp.views.account
import services.exception

import json


class LoginRedirect(flask.views.MethodView):

    def get(self):
        return flask.render_template('gotologin.html')


class Search(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        if 'search_text' in flask.request.args:
            search_text = flask.request.args['search_text']
            cur_page = flask.request.args.get('page', '1')
            cur_page = int(cur_page)
            result = svc_mult_cv.search(search_text)
            yaml_result = svc_mult_cv.search_yaml(search_text)
            results = list()
            for name in result+yaml_result:
                cname = core.outputstorage.ConvertName(name).base
                if cname not in results:
                    results.append(cname)
            count = 20
            datas, pages = self.paginate(svc_mult_cv, results, cur_page, count)
            return flask.render_template('search_result.html',
                                         search_key=search_text,
                                         result=datas,
                                         cur_page = cur_page,
                                         pages = pages,
                                         nums=len(results))
        else:
            return flask.render_template('search.html')

    def paginate(self, svc_mult_cv, results, cur_page, eve_count):
        if not cur_page:
            cur_page = 1
        sum = len(results)
        if sum%eve_count != 0:
            pages = sum/eve_count + 1
        else:
            pages = sum/eve_count
        datas = []
        names = []
        for each in results[(cur_page-1)*eve_count:cur_page*eve_count]:
            base, suffix = os.path.splitext(each)
            name = core.outputstorage.ConvertName(base).md
            if name not in names:
                names.append(name)
            else:
                continue
            try:
                yaml_data = svc_mult_cv.getyaml(base)
            except IOError:
                names.remove(name)
                continue
            info = {
                'author': yaml_data['committer'],
                'time': utils.builtin.strftime(yaml_data['date'], '%Y-%m-%d'),
            }
            datas.append([name, yaml_data, info])
        return datas, pages


class Upload(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        network_file = flask.request.files['file']
        upobj = services.curriculumvitae.CurriculumVitaeObject(network_file.filename,
                                                network_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
        flask.session[user.id]['upload'] = pickle.dumps(upobj)
        flask.session.modified = True
        return str(upobj.result)


class UploadPreview(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        user = flask.ext.login.current_user
        upobj = pickle.loads(flask.session[user.id]['upload'])
        output = upobj.preview_markdown()
        yaml_info = upobj.filepro.yamlinfo
        return flask.render_template('upload_preview.html', markdown=output, yaml=yaml_info)


class ConfirmEnglish(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        name = core.outputstorage.ConvertName(flask.request.form['name'])
        yaml_data = svc_mult_cv.getyaml(name)
        upobj = pickle.loads(flask.session[user.id]['upload'])
        result = svc_mult_cv.add_md(upobj, user.id)
        yaml_data['enversion'] = upobj.filepro.name.md
        svc_mult_cv.modify(name.yaml, yaml.safe_dump(yaml_data, allow_unicode=True),
                           committer=user.id)
        return flask.jsonify(result=result, filename=yaml_data['id']+'.md')


class Show(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        md = svc_mult_cv.gethtml(filename)
        yaml_info = svc_mult_cv.getyaml(filename)
        yaml_info['date'] = utils.builtin.strftime(yaml_info['date'], '%Y-%m-%d %H:%M')
        user = flask.ext.login.current_user
        result = user.getbookmark()
        if yaml_info['id'] in result:
            yaml_info['collected'] = True
        else:
            yaml_info['collected'] = False
        return flask.render_template('cv_refactor.html', markdown=md, yaml=yaml_info)


class Edit(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        md = svc_mult_cv.gethtml(filename)
        return flask.render_template('edit.html', markdown=md)


class Modify(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        md_data = svc_mult_cv.getmd(filename)
        yaml_info = svc_mult_cv.getyaml(filename)
        return flask.render_template('modify.html', markdown=md_data, yaml=yaml_info)

    def post(self, filename):
        user = flask.ext.login.current_user
        md_data = flask.request.form['mddata']
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        name = core.outputstorage.ConvertName(filename)
        svc_mult_cv.modify(name.md, md_data.encode('utf-8'), committer=user.id)
        return "True"


class Preview(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        user = flask.ext.login.current_user
        upobj = pickle.loads(flask.session[user.id]['upload'])
        output = upobj.preview_markdown()
        _id = upobj.filepro.yamlinfo['id']
        return flask.render_template('upload_preview.html', markdown=output, id=_id)

    @flask.ext.login.login_required
    def post(self):
        md_data = flask.request.form['mddata']
        md = core.converterutils.md_to_html(md_data)
        return flask.render_template('preview.html', markdown=md)


class UpdateInfo(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        response = dict()
        result = True
        user = flask.ext.login.current_user
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        filename = flask.request.json['filename']
        updateinfo = flask.request.json['yamlinfo']
        id = core.outputstorage.ConvertName(filename).base
        for key, value in updateinfo.iteritems():
            data = svc_mult_cv.default.updateinfo(id, key, value, user.id)
            response = { 'result': result, 'data': data }
            if data is None:
                result = False
                response = { 'result': result, 'msg': 'Update information error.'}
                break
        return flask.jsonify(response)


class Index(flask.views.MethodView):

    def get(self):
        with codecs.open('webapp/features.md', 'r', encoding='utf-8') as fp:
            data = fp.read()
        return flask.render_template('index.html', features=data)


class GetBookmark(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        user = flask.ext.login.current_user
        result = user.getbookmark()
        return flask.jsonify(result=list(result))


class AddBookmark(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        bookid = flask.request.form['id']
        result = user.addbookmark(bookid)
        return flask.jsonify(result=result)


class DelBookmark(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        bookid = flask.request.form['id']
        result = user.delbookmark(bookid)
        return flask.jsonify(result=result)


#Render mange page of RESTful
class Manage(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('manage.html')


#Render uploader page of RESTful
class Uploader(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('upload.html')

#Render userinfo page of RESTful
class UserInfo(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('userinfo.html')