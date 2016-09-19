from baseapp.settings import *


import webapp.jsonencoder


RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}

UPLOAD_TEMP = 'output'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
