from baseapp.datadbs import *
from baseapp.mining import *
from baseapp.multicv import *


import webapp.jsonencoder


RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}
