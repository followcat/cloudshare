import yaml

import services.mining
import core.mining.lsimodel
import core.mining.lsisimilarity
from baseapp.datadbs import *


kgr_file = 'tests/kgr_updated.yaml'
uav_file = 'tests/uav.yaml'
sw_file = 'tests/sw.yaml'
mix_file = 'tests/mix_avg.yaml'

with open(kgr_file) as f:
    datas = yaml.load(f)

with open(uav_file) as f:
    datas.update(yaml.load(f))

with open(sw_file) as f:
    datas.update(yaml.load(f))

with open(mix_file) as f:
    datas.update(yaml.load(f))

def build_lsimodel(path, slicer, names=None, texts=None, no_above=1.,
                    topics=None, extra_samples=300, power_iters=6, tfidf_local=None):
    if topics is None:
        if len(names) < 10:
            topics = 5
        elif 10 <= len(names) < 100:
            topics = 5
        elif 100 <= len(names) < 200:
            topics = 30
        else:
            topics = 100
    m = core.mining.lsimodel.LSImodel(path,
                                      no_above=no_above,
                                      topics=topics,
                                      power_iters=power_iters,
                                      extra_samples=extra_samples,
                                      tfidf_local=tfidf_local,
                                      slicer=slicer)
    try:
        m.load()
    except IOError:
        m.setup(names, texts)
        m.save()
    return m

def get_cv_md(id):
    t = SVC_CV_REPO.getmd(id)
    if t is None:
        t = SVC_CV_STO.getmd(id)
    return t

def build_model(jds, name=None, path='tests/lsimodel'):
    names = []
    texts = []
    for jd_id in jds:
        cvs = datas[jd_id]
        for id in cvs:
            t = get_cv_md(id)
            if t is None:
                continue
            names.append(id)
            texts.append(t)
    path = path + '/%s/model'%name
    model = build_lsimodel(path, services.mining.silencer, names, texts,
                            tfidf_local=core.mining.lsimodel.tf_cal)
    return model

def build_models(jds, path):
    models = {}
    for jd_id in jds:
        models[jd_id] = build_model([jd_id], name=jd_id, path=path)
    return models

def build_sim(path, model, svcs):
    sim = core.mining.lsisimilarity.LSIsimilarity(path, model)
    try:
        sim.load()
    except IOError:
        sim.build(svcs)
        sim.save()
    return sim
