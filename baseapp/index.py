import services.index
from baseapp.multicv import SVC_MULT_CV

def load_index():
    SVC_INDEX = services.index.ReverseIndexing('Index', SVC_MULT_CV)
    SVC_INDEX.setup()
    return SVC_INDEX

def load_esindex():
    import services.esindex
    from baseapp.datadbs import SVC_CV_REPO, SVC_CV_STO
    SVC_INDEX = services.esindex.ElasticsearchIndexing([SVC_CV_REPO, SVC_CV_STO])
    SVC_INDEX.setup()
    return SVC_INDEX

SVC_INDEX = load_esindex()
