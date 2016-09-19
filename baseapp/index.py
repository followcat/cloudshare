import services.index
from baseapp.multicv import SVC_CV


SVC_INDEX = services.index.ReverseIndexing('Index', SVC_CV)
SVC_INDEX.setup()
