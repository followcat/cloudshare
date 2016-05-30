# -*- coding: utf-8 -*-
import re
import numpy

import utils.builtin
import core.mining.info
import core.mining.lsimodel
import core.outputstorage

EDUCATION = re.compile(ur'(?P<education>.+)[及或]?以上学历')


def rate(sim, svc_cv, doc, top=10, selected=5, name_list=None):
    result = []
    rating = next(sim, svc_cv, doc, top, name_list)
    blank, reference = rating.pop(0)
    candidate = [r[1] for r in reference]
    for text, rate in rating:
        score = []
        high = [r[1] for r in rate]
        for i, n in enumerate(candidate):
            if n not in high:
                score.append(0.)
            else:
                score.append(float(rate[high.index(n)][2]))
        best = max(score)
        precent = [(float(each))*100 for each in score]
        if name_list is not None:
            namelist_candidate = []
            namelist_precent = []
            namelist_score = []
            for name in name_list:
                id = name.split('.')[0]
                index = candidate.index(id)
                namelist_candidate.append(candidate[index])
                namelist_precent.append(precent[index])
                namelist_score.append(score[index])
            result.append((text, zip(namelist_candidate,
                                     namelist_precent, namelist_score)))
        else:
            result.append((text, zip(candidate[:selected],
                                     precent[:selected],
                                     score[:selected])))
    return result
    
def extract(datas):
    result = []
    for i, d in enumerate(datas):
        result.append((i, d[0].split('.')[0], d[1]))
    return result

def next(sim, svc_cv, doc, top, name_list=None):
    rating = []
    top_data_full = minetop(sim, doc, top)
    extract_data_full = extract(top_data_full)
    if name_list is not None:
        names_data_full = minelist(sim, doc, name_list)
        extract_data_full.extend(extract(names_data_full))
    else:
        name_list = []
        name_list.extend([core.outputstorage.ConvertName(each[1]).md
                          for each in extract_data_full])
    rating.append((doc, extract_data_full))
    for text in doc.split('\n'):
        if not text.strip():
            continue
        education_requirement = EDUCATION.match(text)
        if education_requirement:
            new_data = mine_education(svc_cv,
                education_requirement.group('education'), name_list)
        else:
            new_data = minelist(sim, text, name_list)
        if len(filter(lambda x: float(x[1])> 0., new_data)) > 0:
            rating.append((text, extract(new_data)))
    return rating

def mine_education(svc_cv, text, name_list):
    education_list = {
        1: (u'中技', u'中专', u'高中'),
        2: (u'大专', ),
        #3: Show clearly step before graduate
        4: (u'本科', u'金融学学士', u'文学学士', u'全日制本科', u'统招本科'),
        5: (u'在职硕士'),
        6: (u'硕士', u'硕士研究生', u'MBA', u'MBA/EMBA'),
        7: (u'博士', u'博士研究生'),
        8: (u'博士后', )
        }

    def education_rate(education):
        for k,v in education_list.items():
            RE = re.compile(u'(((\s|(\xc2\xa0))*'+ u'(\s|(\xc2\xa0))*)|((\s|(\xc2\xa0))*'.join(v) + u'(\s|(\xc2\xa0))*))')
            if RE.match(education):
                return k
        else:
            return 0

    assert text
    assert name_list
    datas = []
    for name in name_list:
        education = education_rate(svc_cv.getyaml(name)['education'])
        req = education_rate(text)
        if education and req:
            datas.append((name, str((5 + education - req)*0.1)))
    return datas

def minetop(sim, doc, top):
    return sim.probability(doc)[:top]

def minelist(sim, doc, lists):
    return filter(lambda x: x[0] in lists, sim.probability(doc))
