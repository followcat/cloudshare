import os
import functools

import services.mining
import services.multicv
import services.multiclsify
import services.analysis.cutword


LSI_PATH = 'lsimodel'
CUTWORD_PATH = 'cutwords'


def load_mult_classify(SVC_CV_STO):
    SVC_MULT_CLSIFY = services.multiclsify.MultiClassify(SVC_CV_STO)
    SVC_CLS_CV = SVC_MULT_CLSIFY.classifies
    return SVC_MULT_CLSIFY, SVC_CLS_CV


def load_mining(SVC_MULT_CV, silencer, lsipath=None, cutwordpath=None):
    global LSI_PATH, CUTWORD_PATH
    if lsipath is None:
        lsipath = LSI_PATH
    if cutwordpath is None:
        cutwordpath = CUTWORD_PATH
    SVC_CUTWORD = services.analysis.cutword.Cutword(cutwordpath)
    slicer = functools.partial(silencer, cutservice=SVC_CUTWORD)
    SVC_MIN = services.mining.Mining(lsipath, SVC_MULT_CV, slicer=slicer)
    SVC_MIN.setup()
    return SVC_CUTWORD, SVC_MIN


def load_mult_cv(PRJ_LIST, SVC_CV_REPO, SVC_CLS_CV):
    SVC_MULT_CV = services.multicv.MultiCV(PRJ_LIST, SVC_CV_REPO, SVC_CLS_CV)
    return SVC_MULT_CV

