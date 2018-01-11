CACHE_TYPE = "simple"
SECRET_KEY = "super secret key" # Need to be modified in the publishing environment
SESSION_TYPE = "filesystem"

ACCESS = {
    "SMS_ENABLE": False,
}

APP_CONFIG = {
    "debug": True,
    "host": "localhost",
    "port": 4888,
    "threaded": True,
#   "ssl_context": "adhoc",
}
