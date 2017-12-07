import collections

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import sources.industry_id


class SearchKeywordAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        super(SearchKeywordAPI, self).__init__()
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('keyword', location='json')

    def post(self):
        args = self.reqparse.parse_args()
        keyword = args['keyword']
        tokens = self.svc_index.es.indices.analyze(self.svc_index.config['CV_MEM'],
                                                   analyzer='ik_max_word', text=keyword)
        results = dict()
        for each in tokens['tokens']:
            results[each['token']] = 1
        return {
            'code': 200,
            'data': results,
        }



class LsiSustain(Resource):

    decorators = [flask.ext.login.login_required]
    top = 20
    
    def __init__(self):
        super(LsiSustain, self).__init__()
        self.svc_min = flask.current_app.config['SVC_MIN']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()

    def getvec(self, model, doc, sort=False, reverse=True):
        vec_bow = model.lsi.id2word.doc2bow(model.slicer(doc))
        result = model.lsi[vec_bow]
        if sort is True:
            result = sorted(result, key=lambda x: abs(x[1]), reverse=reverse)
        return result

    def crosstopics(self, model, origin, out, top=None):
        if top is None:
            top = self.top
        origin_words = set(model.slicer(origin))
        origin_vec = self.getvec(model, origin)
        out_vec = self.getvec(model, out)

        near_topics = list()
        results_dict = collections.defaultdict(float)
        for i in range(model.lsi.num_topics):
            result = min(origin_vec[i][1], out_vec[i][1])/max(origin_vec[i][1],
                                                              out_vec[i][1])**3
            model_topic = model.topicsinfo[i]
            for each in model_topic:
                for word in each[0]:
                    if word in origin_words:
                        results_dict[word] += each[1]*result
        sort = sorted(results_dict.items(), key=lambda r: r[1], reverse=True)
        return sort[:top]


class LsiSustainCVByJDAPI(LsiSustain):

    def __init__(self):
        super(LsiSustainCVByJDAPI, self).__init__()
        self.reqparse.add_argument('cv', location='json')
        self.reqparse.add_argument('jd', location='json')
        self.reqparse.add_argument('top', type=int, location='json')
        self.reqparse.add_argument('project', location='json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        top = args['top']
        cvid = args['cv']
        jdid = args['jd']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        model = self.svc_min.lsi_model[project.modelname]
        md = project.cv_getmd(cvid)
        jdinfo = project.jd_get(jdid)
        datas = self.crosstopics(model, md, jdinfo['description'], top=top)
        return {
            'code': 200,
            'data': datas,
        }
