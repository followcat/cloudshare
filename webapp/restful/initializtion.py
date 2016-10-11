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
from webapp.restful.bookmark import *
from webapp.restful.databases import *

def initialize(app):
    api = flask.ext.restful.Api(app)
    api.add_resource(SessionAPI, '/api/session')
    api.add_resource(AccountAPI, '/api/accounts/<string:id>')
    api.add_resource(AccountListAPI, '/api/accounts', endpoint = 'accounts')
    api.add_resource(AccountHistoryAPI, '/api/accounthistory', endpoint = 'accounthistory')

    api.add_resource(BookmarkAPI, '/api/accounts/<string:id>/bookmark')

    api.add_resource(CompanyAPI, '/api/company', endpoint = 'company')
    api.add_resource(CompanyListAPI, '/api/companylist', endpoint = 'companylist')

    api.add_resource(JobDescriptionUploadAPI, '/api/uploadjd',
                     endpoint = 'jobdescriptionupload')
    api.add_resource(JobDescriptionAPI, '/api/jd/<string:id>',
                     endpoint = 'jobdescription')
    api.add_resource(JobDescriptionListAPI, '/api/jdlist',
                     endpoint = 'jobdescriptionlist')

    api.add_resource(CurrivulumvitaeAPI, '/api/cv/<string:id>',
                     endpoint = 'curriculumvitae')
    api.add_resource(CurrivulumvitaeMDAPI, '/api/cvmd/<string:id>',
                     endpoint = 'curriculumvitaemd')
    api.add_resource(CurrivulumvitaeYAMLAPI, '/api/cvyaml/<string:id>',
                     endpoint = 'curriculumvitaeyaml')

    api.add_resource(UploadCVAPI, '/api/uploadcv', endpoint = 'uploadcv')
    api.add_resource(UploadEnglishCVAPI, '/api/uploadengcv', endpoint = 'uploadengcv')
    api.add_resource(UploadCVPreviewAPI, '/api/uploadcv/preview')

    # api.add_resource(SearchbyTextAPI, '/api/search/<string:text>', endpoint = 'searchbytext')
    api.add_resource(SearchbyTextAPI, '/api/searchbytext', endpoint = 'searchbytext')

    api.add_resource(RegionAPI, '/api/mining/region', endpoint = 'region')
    api.add_resource(CapacityAPI, '/api/mining/capacity', endpoint = 'capacity')
    api.add_resource(PositionAPI, '/api/mining/position/<string:text>', endpoint = 'position')

    api.add_resource(AbilityAPI, '/api/mining/ability', endpoint = 'ability')
    api.add_resource(ExperienceAPI, '/api/mining/experience', endpoint = 'experience')

    api.add_resource(LSIbydocAPI, '/api/mining/lsibydoc', endpoint = 'lsibydoc')

    api.add_resource(LSIbyJDidAPI, '/api/mining/lsibyjdid', endpoint = 'lsibyjdid')

    api.add_resource(SimilarAPI, '/api/mining/similar/<string:id>', endpoint = 'similar')

    api.add_resource(ValuableAPI, '/api/mining/valuable')

    api.add_resource(ValuablebyJDidAPI, '/api/mining/valuablebyjdid',
                                        endpoint = 'valuablebyjdid')
    api.add_resource(ValuablebydocAPI, '/api/mining/valuablebydoc',
                                        endpoint = 'valuablebydoc')

    api.add_resource(FeatureAPI, '/api/feature', endpoint = 'feature')

    api.add_resource(ProjectNamesAPI, '/api/projectnames', endpoint = 'projectnames')
    api.add_resource(AdditionNamesAPI, '/api/additionnames', endpoint = 'additionnames')
    api.add_resource(DBNumberAPI, '/api/dbnumber/<string:name>', endpoint = 'dbnumber')
    api.add_resource(DBNumbersAPI, '/api/dbnumbers', endpoint = 'dbnumbers')
    api.add_resource(ClassifyAPI, '/api/classify', endpoint = 'classify')
