import time
import math
import datetime

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.mining.info
import core.outputstorage


class BaseAPI(Resource):

    numbers = 500
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(BaseAPI, self).__init__()
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
        member = user.getmember()
        text = args['search_text']
        if args['md_ids'] and len(text) > 0:
            searches = args['md_ids']
        else:
            index = member.es_config['CV_MEM']
            searches = member.cv_search(index=index, doctype=[member.id],
                                     filterdict={'name': text},
                                     size=self.numbers, onlyid=True)
        result = []
        for id in searches[:self.numbers]:
            positions = []
            try:
                yaml_data = member.cv_getyaml(id)
            except IOError:
                continue
            if 'position' in yaml_data['experience']:
                positions = [p['name'] for p in yaml_data['experience']['position']]
            for position in positions:
                index = self.position_indexof(position, result)
                if index > -1:
                    result[index]['id_list'].append(id)
                else:
                    result.append({ 'position_name': position, 'id_list': [id] })
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
        member = user.getmember()
        result = []
        for id in args['md_ids'][:self.numbers]:
            stream = member.cv_getmd(id)
            result.append(core.mining.info.region(stream))
        return { 'result': result }


class CapacityAPI(BaseAPI):

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        member = user.getmember()
        result = []
        for id in args['md_ids'][:self.numbers]:
            stream = member.cv_getmd(id)
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return { 'result': result }


class AbilityAPI(BaseAPI):

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        member = user.getmember()
        result = []
        for id in args['md_ids']:
            month = 0
            doclen = 0
            actpoint = 0
            stream = member.cv_getmd(id)
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
        member = user.getmember()
        result = []
        for id in args['md_ids']:
            stream = member.cv_getmd(id)
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

    top = 1000
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(LSIbaseAPI, self).__init__()
        self.miner = flask.current_app.config['SVC_MIN']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')
        self.reqparse.add_argument('size', type=int, default=20, location = 'json')

    def process(self, member, project, doc, uses, filterdict, cur_page, size=20):
        if not cur_page:
            cur_page = 1
        datas = list()
        iduses = list()
        index = set([member.es_config['CV_MEM']])
        doctype = [member.id]
        for use in uses:
            if use == member.name:
                iduses.append(member.id)
            else:
                iduses.append(use)
                index.add(member.es_config['CV_STO'])
                doctype.append(member.es_config['CV_STO'])
        totals, searchs = member.cv_search(index=list(index), doctype=doctype,
                                                filterdict=filterdict, size=5000, source=False)
        ids = [item['_id'] for item in searchs]
        results = self.miner.probability_by_ids(project.modelname, doc, ids, uses=iduses)
        """
        sort = {
                "_script" : {
                      "type" : "number",
                      "script" : {
                          "inline": "params.ids.indexOf(doc['id'].value)",
                          "params" : {
                              "ids": ids
                          }
                      },
                      "order" : "asc"
                  }
                }
        totals, searchs = member.cv_search(index=list(index), doctype=doctype,
                                               filterdict=filterdict,
                                               ids=ids,
                                               kwargs={'sort': sort,
                                                       '_source_exclude': ['content']},
                                               start=(cur_page-1)*size, size=size,
                                               source=True)
        """
        pages = int(math.ceil(float(len(searchs))/size))
        datas = list()
        for result in results[(cur_page-1)*size: cur_page*size]:
            yaml_info = member.cv_getyaml(result[0])
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': str(result[1])
            }
            datas.append({ 'cv_id': yaml_info['id'],
                           'yaml_info': yaml_info,
                           'info': info})
        return { 'datas': datas, 'pages': pages, 'totals': totals }


class LSIJDbyCVidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIJDbyCVidAPI, self).__init__()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        size = args['size']
        cur_page = args['page']
        projectname = args['project']
        filterdict = args['filterdict'] if args['filterdict'] else {}
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        doc = member.cv_getmd(id)
        totals, searchs = member.jd_search(filterdict=filterdict,
                                                size=5000, source=False, **project)
        ids = [item['_id'] for item in searchs]
        results = self.miner.probability_by_ids('jdmatch', doc, ids)
        pages = int(math.ceil(float(len(searchs))/totals))
        datas = list()
        project = member.getproject(projectname)
        for result in results[(cur_page-1)*size: cur_page*size]:
            yaml_info = project.jd_get(result[0])
            co_id = yaml_info['company']
            co_name = project.bd_getyaml(co_id)['name']
            yaml_info['company_name'] = co_name
            datas.append({ 'id': yaml_info['id'],
                           'yaml_info': yaml_info,
                           'match': result[1] })
        return { 'code': 200, 'data': datas }


class LSIbyJDidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbyJDidAPI, self).__init__()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('appendcomment', type = bool, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        cur_page = args['page']
        projectname = args['project']
        uses = args['uses'] if args['uses'] else []
        filterdict = args['filterdict'] if args['filterdict'] else {}
        append_comment = args['appendcomment'] if args['appendcomment'] else False
        member = user.getmember()
        project = member.getproject(projectname)
        jd_yaml = project.jd_get(id)
        doc = jd_yaml['description']
        if append_comment:
            doc += jd_yaml['commentary']
        result = self.process(member, project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class LSIbyAllJDAPI(LSIbaseAPI):

    cache = {}

    def __init__(self):
        super(LSIbyAllJDAPI, self).__init__()
        self.reqparse.add_argument('fromcache', type=bool, location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')
        self.reqparse.add_argument('threshold', type=float, location = 'json')
        self.reqparse.add_argument('numbers', type=int, location = 'json')

    def findbest(self, member, project, filterdict, threshold, numbers):
        results = dict()
        index = [member.es_config['CV_MEM'], member.es_config['CV_STO']]
        doctype = [member.id, 'cvstorage']
        searchids = member.cv_search(index=index, doctype=doctype,
                                     filterdict=filterdict, onlyid=True)
        for jd_id, jd in project.jobdescription.datas():
            try:
                if jd['status'] == 'Closed':
                    continue
            except KeyError:
                continue
            doc = jd['description']
            doc += jd['commentary']
            result = self.miner.probability_by_ids(project.modelname, doc, searchids, top=numbers)
            output = { 'CV': list() }
            for each in result:
                if each[1] > threshold:
                    cvinfo = member.cv_getyaml(each[0])
                    cvinfo['CVvalue'] = each[1]
                    output['CV'].append(cvinfo)
            if output['CV']:
                output['id'] = jd_id
                output['name'] = jd['name']
                output['description'] = jd['description']
                output['company'] = project.bd_getyaml(jd['company'])['name']
                results[jd_id] = output
        return results

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        threshold = args['threshold']
        projectname = args['project']
        filterdict = args['filterdict']
        numbers = args['numbers']
        results = list()
        member = user.getmember()
        project = member.getproject(projectname)
        alls = self.findbest(member, project, filterdict, threshold, numbers)
        for jdid in alls:
            results.append({'ID': jdid, 'name': alls[jdid]['name'],
                            'company': alls[jdid]['company'],
                            'description': alls[jdid]['description'],
                            'CV': alls[jdid]['CV'][0:numbers]})
        return { 'code': 200, 'data': results }


class LSIbyCVidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbyCVidAPI, self).__init__()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        cur_page = args['page']
        projectname = args['project']
        uses = args['uses'] if args['uses'] else []
        filterdict = args['filterdict'] if args['filterdict'] else {}
        member = user.getmember()
        project = member.getproject(projectname)
        doc = member.cv_getmd(id)
        result = self.process(member, project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class LSIbydocAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbydocAPI, self).__init__()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        doc = args['doc']
        cur_page = args['page']
        projectname = args['project']
        uses = args['uses'] if args['uses'] else []
        filterdict = args['filterdict'] if args['filterdict'] else {}
        member = user.getmember()
        project = member.getproject(projectname)
        result = self.process(member, project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class SimilarAPI(Resource):

    decorators = [flask.ext.login.login_required]
    HALF_YEAR_SECOENDS = 180*24*3600

    def __init__(self):
        super(SimilarAPI, self).__init__()
        self.miner = flask.current_app.config['SVC_MIN']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        doc = member.cv_getmd(id)
        datas = []
        index = [member.es_config['CV_MEM']]
        doctype = [member.id]
        totals, searchs = member.cv_search(index=index, doctype=doctype,
            filterdict={'date': [time.strftime('%Y%m%d', time.localtime(time.time()-
                                                         self.HALF_YEAR_SECOENDS)),
                                 time.strftime('%Y%m%d', time.localtime(time.time()))]},
            source=False)
        ids = [item['_id'] for item in searchs]
        for name, score in self.miner.probability_by_ids(project.modelname, doc, ids,
                                                         uses=doctype, top=6):
            if id == core.outputstorage.ConvertName(name).base:
                continue
            yaml_info = member.cv_getyaml(name)
            datas.append({ 'id': name, 'yaml_info': yaml_info, 'match': score })
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

    def _get(self, doc, member, modelname):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        uses = args['uses'] if args['uses'] else []
        name_list = args['name_list']
        result = self.miner.valuable_rate(name_list, modelname, member, doc, self.top)
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = member.cv_getyaml(name+'.yaml')
                yaml_data['match'] = match_item[1]
                try:
                    if yaml_data['secrecy'] is None:
                        yaml_data['secrecy'] = False
                except KeyError:
                    yaml_data['secrecy'] = False
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
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        jd_yaml = project.jd_get(id)
        doc = jd_yaml['description']
        result = self._get(doc, member, project.modelname)
        return { 'code': 200, 'data': result }

class ValuablebydocAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuablebydocAPI, self).__init__()
        self.reqparse.add_argument('doc', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        doc = args['doc']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        result = self._get(doc, member, project.modelname)
        return { 'result': result }


class ValuableAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuableAPI, self).__init__()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        doc = ''
        if args['id']:
            jd_yaml = project.jd_get(args['id'])
            doc = jd_yaml['description']
        elif args['doc']:
            doc = args['doc']
        result = self._get(doc, member, project.modelname)
        return { 'code': 200, 'data': result }
