import numpy

import utils.builtin
import core.mining.info
import core.mining.lsimodel
import core.outputstorage


def rate(lsi, doc, top=5, name_list=None):
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
                score.append((float(reference[i][2]) - float(rate[high.index(n)][2]))*1000)
                if score[-1] < 0.:
                    score[-1] = 0.
        if numpy.average(score) <= numpy.average([float(r[2]) for r in reference]):
            continue
        else:
            result.append((text, zip(candidate, score)))
    return result
    
def extract(datas):
    result = []
    for i, d in enumerate(datas):
        result.append((i, d[0].split('.')[0], d[-1]['match']))
    return result

def next(lsi, doc, top, name_list):
    rating = []
    if name_list is None:
        data_full = mine(lsi, doc, top)
        rating.append(('', extract(data_full)))
        for text in doc.split('\n'):
            if not text:
                continue
            new_doc = doc.replace(text, '')
            new_data = mine(lsi, new_doc, top)
            rating.append((text, extract(new_data)))
    else:
        data_full = checkbox_mine(lsi, doc, name_list)
        rating.append(('', extract(data_full)))
        for text in doc.split('\n'):
            if not text:
                continue
            new_doc = doc.replace(text, '')
            new_data = checkbox_mine(lsi, new_doc, name_list)
            rating.append((text, extract(new_data)))
    return rating

def mine(lsi, doc, top):
    result = lsi.probability(doc)
    kv = dict()
    datas = []
    for each in result[:top]:
        kv[each[0]] = str(each[1])
        name = core.outputstorage.ConvertName(lsi.names[each[0]])
        yaml_info = utils.builtin.load_yaml('repo', name.yaml)
        info = {
            'author': yaml_info['committer'],
            'time': utils.builtin.strftime(yaml_info['date']),
            'match': str(each[1])
        }
        datas.append([name, yaml_info, info])
    return datas

def checkbox_mine(lsi, doc, lists):
    result = lsi.probability(doc)
    kv = dict()
    datas = []
    for e in lists:
        for each in result:
            kv[each[0]] = str(each[1])
            name = core.outputstorage.ConvertName(lsi.names[each[0]])
            if ( name == e ):
                yaml_info = utils.builtin.load_yaml('repo', name.yaml)
                info = {
                    'author': yaml_info['committer'],
                    'time': utils.builtin.strftime(yaml_info['date']),
                    'match': str(each[1])
                }
                datas.append([name, yaml_info, info])
            else:
                continue
    return datas