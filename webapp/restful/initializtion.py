import flask
import flask.ext.restful

from webapp.restful.mining import *
from webapp.restful.search import *
from webapp.restful.upload import *
from webapp.restful.account import *
from webapp.restful.company import *
from webapp.restful.jobdescription import *
from webapp.restful.curriculumvitae import *
from webapp.restful.feature import *
from webapp.restful.session import *

def initialize(app):
    api = flask.ext.restful.Api(app)
    api.add_resource(SessionAPI, '/api/session')
    api.add_resource(AccountAPI, '/api/accounts/<string:id>')
    api.add_resource(AccountListAPI, '/api/accounts', endpoint = 'accounts')
    api.add_resource(AccountHistoryAPI, '/api/accounthistory', endpoint = 'accounthistory')

    api.add_resource(CompanyAPI, '/api/company/<string:name>', endpoint = 'company')
    api.add_resource(CompanyListAPI, '/api/companylist', endpoint = 'companylist')

    api.add_resource(JobDescriptionAPI, '/api/jd/<string:id>',
                     endpoint = 'jobdescription')
    api.add_resource(JobDescriptionByNameAPI, '/api/jdbyname/<string:name>',
                     endpoint = 'jobdescriptionbyname')
    api.add_resource(JobDescriptionListAPI, '/api/jdlist',
                     endpoint = 'jobdescriptionlist')

    api.add_resource(CurrivulumvitaeAPI, '/api/cv/<string:id>',
                     endpoint = 'curriculumvitae')
    api.add_resource(CurrivulumvitaeMDAPI, '/api/cvmd/<string:id>',
                     endpoint = 'curriculumvitaemd')
    api.add_resource(CurrivulumvitaeYAMLAPI, '/api/cvyaml/<string:id>',
                     endpoint = 'curriculumvitaeyaml')

    api.add_resource(UploadCVAPI, '/api/uploadcv', endpoint = 'uploadcv')
    api.add_resource(UploadBatchCVAPI, '/api/uploadbatchcv', endpoint = 'uploadbatchcv')
    api.add_resource(UploadEnglishCVAPI, '/api/uploadengcv', endpoint = 'uploadengcv')

    api.add_resource(SearchbyTextAPI, '/api/search/<string:text>', endpoint = 'searchbytext')

    api.add_resource(RegionAPI, '/api/mining/region', endpoint = 'region')
    api.add_resource(CapacityAPI, '/api/mining/capacity', endpoint = 'capacity')
    api.add_resource(PositionAPI, '/api/mining/position/<string:text>', endpoint = 'position')

    api.add_resource(LSIbydocAPI, '/api/mining/lsibydoc', endpoint = 'lsibydoc')
    api.add_resource(LSIbyJDidAPI, '/api/mining/lsibyjdid/<string:id>', endpoint = 'lsibyjdid')

    api.add_resource(SimilarAPI, '/api/mining/similar/<string:id>', endpoint = 'similarapi')

    api.add_resource(ValuablebyJDidAPI, '/api/mining/valuablebyjdid/<string:id>',
                                        endpoint = 'valuablebyjdid')
    api.add_resource(ValuablebydocAPI, '/api/mining/valuablebydoc',
                                        endpoint = 'valuablebydoc')

    api.add_resource(FeatureAPI, '/api/feature',
                                        endpoint = 'feature')