DEBUG = True
CACHE_TYPE = "simple"
SECRET_KEY = "default" # Need to be modified in the publishing environment
SESSION_TYPE = "filesystem"

ACCESS = {
    "SMS_ENABLE": False,
}

APP_CONFIG = {
    "host": "localhost",
    "port": 4888,
    "threaded": True,
#   "ssl_context": "adhoc",
}
