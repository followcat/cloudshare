import services.index
from baseapp.multicv import SVC_MULT_CV


def load_index():
    SVC_INDEX = services.index.ReverseIndexing('Index', SVC_MULT_CV)
    SVC_INDEX.setup()
    return SVC_INDEX

SVC_INDEX = load_index()
