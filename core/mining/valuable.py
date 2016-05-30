import numpy

import utils.builtin
import core.mining.info
import core.mining.lsimodel
import core.outputstorage


def rate(sim, doc, top=10, selected=5, name_list=None):
    result = []
    rating = next(sim, doc, top, name_list)
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

def next(sim, doc, top, name_list=None):
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
        new_data = minelist(sim, text, name_list)
        if len(filter(lambda x: float(x[1])> 0., new_data)) > 0:
            rating.append((text, extract(new_data)))
    return rating

def minetop(sim, doc, top):
    return sim.probability(doc)[:top]

def minelist(sim, doc, lists):
    return filter(lambda x: x[0] in lists, sim.probability(doc))
