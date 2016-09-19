from baseapp.datadbs import SVC_ACCOUNT, SVC_CO, SVC_JD, SVC_CV, SVC_ADD_SYNC
from baseapp.index import SVC_INDEX
from baseapp.mining import SVC_MIN


import webapp.jsonencoder


RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}

UPLOAD_TEMP = 'output'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
