import baseapp.loader
import baseapp.searchengine


ES_CONFIG = baseapp.loader.config.es_config
SVC_INDEX = baseapp.loader.load_esindex(baseapp.searchengine.ES)
