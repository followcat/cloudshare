import flask
import flask.ext.restful

from webapp.restful.people import *
from webapp.restful.mining import *
from webapp.restful.docmining import *
from webapp.restful.reload import *
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

    api.add_resource(DocMiningAPI, '/api/mining/analysisdoc', endpoint = 'docmining')
