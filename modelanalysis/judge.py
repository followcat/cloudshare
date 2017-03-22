import numpy


def probably(requirement, model):
    reqset = set(model.slicer(requirement))
    gain = len(reqset.intersection(model.dictionary.values()))
    percentage = float(len(reqset))/len(model.dictionary)
    return gain*percentage + linalg(requirement, model)


def linalg(requirement, model):
    pro = model.probability(requirement)
    vec = numpy.array([e[1] for e in pro])
    return numpy.linalg.norm(vec-[0]*len(vec))


def judgement(requirement, defmodel, challenger):
    linalg_def = linalg(requirement, defmodel)
    linalg_ceg = linalg(requirement, challenger)
    return linalg_def < linalg_ceg