import services.index
import services.esindex
from baseapp.multicv import SVC_MULT_CV

def load_index():
    SVC_INDEX = services.esindex.ElasticsearchIndexing(SVC_MULT_CV.svcls)
    SVC_INDEX.setup()
    return SVC_INDEX

SVC_INDEX = load_index()