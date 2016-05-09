import numpy

import utils.builtin
import core.mining.info
import core.mining.lsimodel
import core.outputstorage


def rate(lsi, doc, top=10, selected=5, name_list=None):
    result = []
    rating = next(lsi, doc, top, name_list)
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
        result.append((i, d[0].split('.')[0], d[-1]['match']))
    return result

def next(lsi, doc, top, name_list=None):
    rating = []
    top_data_full = minetop(lsi, doc, top)
    extract_data_full = extract(top_data_full)
    if name_list is not None:
        names_data_full = minelist(lsi, doc, name_list)
        extract_data_full.extend(extract(names_data_full))
    else:
        name_list = []
        name_list.extend([core.outputstorage.ConvertName(each[1]).md
                          for each in extract_data_full])
    rating.append((doc, extract_data_full))
    for text in doc.split('\n'):
        if not text:
            continue
        new_data = minelist(lsi, text, name_list)
        rating.append((text, extract(new_data)))
    return rating

def minetop(lsi, doc, top):
    result = lsi.probability(doc)
    datas = []
    for each in result[:top]:
        name = core.outputstorage.ConvertName(lsi.names[each[0]])
        yaml_info = utils.builtin.load_yaml('repo', name.yaml)
        info = {
            'author': yaml_info['committer'],
            'time': utils.builtin.strftime(yaml_info['date']),
            'match': str(each[1])
        }
        datas.append([name, yaml_info, info])
    return datas

def minelist(lsi, doc, lists):
    result = lsi.probability(doc)
    datas = []
    for e in lists:
        for each in result:
            name = core.outputstorage.ConvertName(lsi.names[each[0]])
            if ( name == e ):
                yaml_info = utils.builtin.load_yaml('repo', name.yaml)
                info = {
                    'author': yaml_info['committer'],
                    'time': utils.builtin.strftime(yaml_info['date']),
                    'match': str(each[1])
                }
                datas.append([name, yaml_info, info])
    return datas
