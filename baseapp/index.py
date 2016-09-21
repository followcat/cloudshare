import services.index
from baseapp.multicv import SVC_MULT_CV


SVC_INDEX = services.index.ReverseIndexing('Index', SVC_MULT_CV)
SVC_INDEX.setup()
