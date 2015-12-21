# -*- coding: utf-8 -*-
import os
import codecs

import core.mining.spilter


organization = (u'有限公司', U'公司', u'集团', u'院')
organization_restr = u'([a-zA-Z0-9\u4E00-\u9FA5]+)('
for each in organization:
    organization_restr += each + '|'
organization_restr = organization_restr[:-1] + ')'

time_restr = ur'\d{4}[/.\\年 ]+\d{1,2}[月]*'

with codecs.open('core/mining/position.txt', 'r', encoding='utf-8') as f:
    position_key = f.read()
    position_keylist = position_key.split(' ')
position_restr = u'([\u4E00-\u9FA5]+)('
for each in position_keylist:
    position_restr += each
    position_restr += '|'
position_restr = position_restr[:-1] + ')'


wc = core.mining.spilter.WordCatcher(position_restr)


def company(repo, searches, search_text):
    global wc
    result_dict = {}
    for search in searches:
        with codecs.open(os.path.join(repo.repo.path, search),
                         'r', encoding='utf-8') as file:
            md_data = file.read()
        ms = core.mining.spilter.MarkdownStruct(md_data)
        key = core.mining.spilter.Info(ms, search_text)
        filter1 = core.mining.spilter.Info(ms, organization_restr)
        filter2 = core.mining.spilter.Info(ms, time_restr)
        wc.reset() 
        for each in key.positions:
            ranges = []
            try:
                range1 = filter1.range(each, 0, 1)
                ranges.append(range1)
            except ValueError:
                pass
            try:
                range2 = filter2.range(each, 1, 1)
                ranges.append(range2)
            except ValueError:
                pass
            if len(ranges) == 0:
                continue
            findstream = ''.join(ms.get_strs_from_positions(ranges))
            wc.bn_bn(findstream)
        page_result = wc.result()
        for each in page_result:
            if each not in result_dict:
                result_dict[each] = []
            result_dict[each].append(search)
    return result_dict