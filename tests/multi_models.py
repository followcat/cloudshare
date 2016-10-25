import yaml

import services.mining
import core.mining.lsimodel
from baseapp.datadbs import *


kgr_file = 'tests/known_good_jd_cv_mapping.yaml'

with open(kgr_file) as f:
    datas = yaml.load(f)

def build_lsimodel(path, slicer, names=None, texts=None):
    topics = 100
    if len(names) < 10:
        topics = 5
    elif 10 <= len(names) < 30:
        topics = 10
    m = core.mining.lsimodel.LSImodel(path, topics=topics, slicer=slicer)
    try:
        m.load()
    except IOError:
        m.setup(names, texts)
        m.save()
    return m

def build_model(jds, name=None, path='tests/lsimodel'):
    names = []
    texts = []
    for jd_id in jds:
        cvs = datas[jd_id]
        for id in cvs:
            t = SVC_CV_REPO.getmd(id)
            if t is None:
                continue
            names.append(id)
            texts.append(t)
    path = path + '/%s/model'%name
    model = build_lsimodel(path, services.mining.silencer, names, texts)
    return model

def build_models(jds):
    models = {}
    for jd_id in jds:
        models[jd_id] = build_model([jd_id], name=jd_id)
    return models
