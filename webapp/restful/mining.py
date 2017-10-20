import time
import datetime

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.mining.info
import core.mining.valuable
import core.outputstorage


class BaseAPI(Resource):

    numbers = 500
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(BaseAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('md_ids', type = list, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def calculate_work_month(self, begin_y, begin_m, end_y, end_m):
        year = int(end_y) - int(begin_y)
        month = int(end_m) - int(begin_m)
        return year * 12 + month



class PositionAPI(BaseAPI): 

    def __init__(self):
        super(PositionAPI, self).__init__()
        self.reqparse.add_argument('search_text', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        text = args['search_text']
        if args['md_ids'] and len(text) > 0:
            searches = args['md_ids']
        else:
            searches = project.cv_search(text)
        result = []
        for search in list(searches)[:self.numbers]:
            name = search[0]
            positions = []
            try:
                yaml_data = project.cv_getyaml(name)
            except IOError:
                continue
            if 'position' in yaml_data['experience']:
                positions = [p['name'] for p in yaml_data['experience']['position']]
            for position in positions:
                index = self.position_indexof(position, result)
                if index > -1:
                    result[index]['id_list'].append(name)
                else:
                    result.append({ 'position_name': position, 'id_list': [name] })
        return { 'code': 200, 'data': result }

    def position_indexof(self, position, result):
        for index, item in enumerate(result):
            if (item['position_name'] == position):
                return index
        return -1


class RegionAPI(BaseAPI):

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = []
        for id in args['md_ids'][:self.numbers]:
            stream = project.cv_getmd(id)
            result.append(core.mining.info.region(stream))
        return { 'result': result }


class CapacityAPI(BaseAPI):

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = []
        for id in args['md_ids'][:self.numbers]:
            stream = project.cv_getmd(id)
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return { 'result': result }


class AbilityAPI(BaseAPI):

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = []
        for id in args['md_ids']:
            month = 0
            doclen = 0
            actpoint = 0
            stream = project.cv_getmd(id)
            capacitys = core.mining.info.capacity(stream)
            if not capacitys:
                doclen = 100000
            for capacity in capacitys:
                if (len(capacity['begin']) and len(capacity['end'])):
                    month += self.calculate_work_month(capacity['begin'][0], capacity['begin'][1], capacity['end'][0], capacity['end'][1])
                actpoint += float(capacity['actpoint'])
                doclen += float(capacity['doclen'])
            result.append({ 'md': id, 'ability': { 'work_year': month/12, 'ability_value': (actpoint/doclen)*100 } })
        return { 'code': 200, 'data': result }


class ExperienceAPI(BaseAPI):

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = []
        for id in args['md_ids']:
            stream = project.cv_getmd(id)
            capacitys = core.mining.info.capacity(stream)
            month = 0
            actpoint = 0
            for capacity in capacitys:
                if (len(capacity['begin']) and len(capacity['end'])):
                    month += self.calculate_work_month(capacity['begin'][0], capacity['begin'][1], capacity['end'][0], capacity['end'][1])
                actpoint += capacity['actpoint']
            result.append({ 'md': id, 'experience': { 'work_year': month/12, 'experience_value': actpoint } })
        return { 'code': 200, 'data': result }


class LSIbaseAPI(Resource):

    top = 0.03
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(LSIbaseAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.miner = flask.current_app.config['SVC_MIN']
        self.index = flask.current_app.config['SVC_INDEX']
        self.sim_names = self.miner.addition_names()

    def process(self, project, doc, uses, filterdict, cur_page, eve_count=20):
        if not cur_page:
            cur_page = 1
        datas = []
        result = self.miner.probability(project.modelname, doc, uses=uses,
                                        top=self.top, minimum=1000)
        ids = set([cv[0] for cv in result])
        result = self.index.filter_ids(result, filterdict, ids, uses=uses)
        totals = len(result)
        if totals%eve_count != 0:
            pages = totals/eve_count + 1
        else:
            pages = totals/eve_count
        for name, score in result[(cur_page-1)*eve_count:cur_page*eve_count]:
            yaml_info = project.cv_getyaml(name)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            datas.append({ 'cv_id': name, 'yaml_info': yaml_info, 'info': info})
        return { 'datas': datas, 'pages': pages, 'totals': totals }


class LSIbyJDidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbyJDidAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('appendcomment', type = bool, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        jd_yaml = project.jd_get(id)
        doc = jd_yaml['description']
        append_comment = args['appendcomment'] if args['appendcomment'] else False
        if append_comment:
            doc += jd_yaml['commentary']
        uses = args['uses'] if args['uses'] else []
        filterdict = args['filterdict'] if args['filterdict'] else {}
        cur_page = args['page']
        result = self.process(project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class LSIbyAllJDAPI(LSIbaseAPI):

    cache = {}

    def __init__(self):
        super(LSIbyAllJDAPI, self).__init__()
        self.index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse.add_argument('fromcache', type=bool, location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')
        self.reqparse.add_argument('threshold', type=float, location = 'json')
        self.reqparse.add_argument('numbers', type=int, location = 'json')

    def fromcache(self, project, filterdict, threshold, cache=True):
        date = int(time.strftime('%Y%m%d',time.localtime(time.time())))
        projectname = project.name
        if cache is True:
            if projectname not in self.cache:
                bestjds = self.findbest(project, threshold)
                self.cache[projectname] = (date, bestjds)
            elif self.cache[projectname][0] < date:
                bestjds = self.findbest(project, threshold)
                self.cache[projectname] = (date, bestjds)
            else:
                bestjds = self.cache[projectname][1]
        else:
            bestjds = self.findbest(project, threshold)
        results = dict()
        for jdid in bestjds:
            output = {}
            output['CV'] = list()
            bestids = set([cv[0] for cv in bestjds[jdid]])
            filterids = self.index.filter_ids(bestjds[jdid], filterdict, bestids)
            for cv in filterids:
                cvinfo = project.cv_getyaml(cv[0])
                cvinfo['CVvalue'] = cv[1]
                output['CV'].append(cvinfo)
            if not output['CV']:
                continue
            jd = project.jd_get(jdid)
            output['id'] = jdid
            output['name'] = jd['name']
            output['description'] = jd['description']
            output['company'] = project.company_get(jd['company'])['name']
            results[jdid] = output
        return results

    def findbest(self, project, threshold=None):
        if threshold is None:
            threshold = 0.8
        results = {}
        for jd in project.jobdescription.lists():
            try:
                if jd['status'] == 'Closed':
                    continue
            except KeyError:
                continue
            doc = jd['description']
            doc += jd['commentary']
            result = self.miner.probability(project.modelname, doc,
                                            uses=[project.id]+project.getclassify(),
                                            top=0.01, minimum=3000)
            if result:
                candidates = filter(lambda x: float(x[1])>float(threshold), result)
                results[jd['id']] = candidates
        return results

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        threshold = args['threshold']
        fromcache = args['fromcache']
        projectname = args['project']
        filterdict = args['filterdict']
        numbers = args['numbers']
        results = list()
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        alls = self.fromcache(project, filterdict, threshold, cache=fromcache)
        for jdid in alls:
            results.append({'ID': jdid, 'name': alls[jdid]['name'],
                            'company': alls[jdid]['company'],
                            'description': alls[jdid]['description'],
                            'CV': alls[jdid]['CV'][0:numbers]})
        return { 'code': 200, 'data': results }


class LSIbyCVidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbyCVidAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        doc = project.cv_getmd(id)
        uses = args['uses'] if args['uses'] else []
        filterdict = args['filterdict'] if args['filterdict'] else {}
        cur_page = args['page']
        result = self.process(project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class LSIbydocAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbydocAPI, self).__init__()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        doc = args['doc']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        uses = args['uses'] if args['uses'] else []
        filterdict = args['filterdict'] if args['filterdict'] else {}
        cur_page = args['page']
        result = self.process(project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class SimilarAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(SimilarAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.miner = flask.current_app.config['SVC_MIN']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        doc = project.cv_getmd(id)
        uses = [projectname]
        project_classify = project.getclassify()
        for classify in project.cv_getyaml(id)['classify']:
            if classify in project_classify:
                uses.append(classify)
        top = 0
        datas = []
        for name, score in self.miner.probability(project.modelname, doc,
                                                  uses=uses, top=100):
            if id == core.outputstorage.ConvertName(name).base:
                continue
            if score < 0.8 or top==5:
                break
            yaml_info = project.cv_getyaml(name)
            datas.append({ 'id': name, 'yaml_info': yaml_info })
            top += 1
        return { 'code': 200, 'data': datas }


class ValuablebaseAPI(Resource):

    top = 0.05
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(ValuablebaseAPI, self).__init__()
        self.miner = flask.current_app.config['SVC_MIN']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name_list', type = list, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')

    def _get(self, doc, project):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        uses = args['uses'] if args['uses'] else []
        name_list = args['name_list']
        result = core.mining.valuable.rate(name_list, self.miner, project, doc, self.top)
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = project.cv_getyaml(name+'.yaml')
                yaml_data['match'] = match_item[1]
                values.append({ 'match': match_item[1],
                                'id': yaml_data['id'],
                                'name': yaml_data['name'],
                                'secrecy': yaml_data['secrecy'] })
            item['value'] = values
            datas.append(item)
        response['result'] = datas
        response['max'] = 100
        return response


class ValuablebyJDidAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuablebyJDidAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        jd_yaml = project.jd_get(id)
        doc = jd_yaml['description']
        result = self._get(doc, project)
        return { 'code': 200, 'data': result }

class ValuablebydocAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuablebydocAPI, self).__init__()
        self.reqparse.add_argument('doc', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        projectname = args['project']
        result = self._get(doc, projectname)
        return { 'result': result }


class ValuableAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuableAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        doc = ''
        if args['id']:
            jd_yaml = project.jd_get(args['id'])
            doc = jd_yaml['description']
        elif args['doc']:
            doc = args['doc']
        result = self._get(doc, project)
        return { 'code': 200, 'data': result }
