# -*- coding: utf-8 -*-
import os
import re
import json
import codecs

import jieba

import core.mining.spilter


class RegionSearcher(dict):
    def __init__(self, json_data):
        for each in json_data:
            for pos in json_data[each]:
                if 'name' in pos:
                    self[pos['name']] = pos
                if 'DisName' in pos:
                    self[pos['DisName']] = pos

    def get(self, x):
        city_x = x + u'市'
        dis_x = x + u'区'
        if x in self:
            return self[x]
        elif city_x in self:
            return self[city_x]
        elif dis_x in self:
            return self[dis_x]

region_json = json.load(open('core/mining/region.json'))
rs = RegionSearcher(region_json)

organization = (u'有限公司', U'公司', u'集团', u'院')
organization_restr = u'([a-zA-Z0-9\u4E00-\u9FA5]+'
for each in organization:
    organization_restr += each + '|'
organization_restr = organization_restr[:-1] + ')'

time_restr = ur'(\d{4})[/.\\年 ]+(\d{1,2})[月]*'

with codecs.open('core/mining/position.txt', 'r', encoding='utf-8') as f:
    position_key = f.read()
    position_keylist = position_key.split(' ')
position_restr = u'([\u4E00-\u9FA5]+)('
for each in position_keylist:
    position_restr += each
    position_restr += '|'
position_restr = position_restr[:-1] + ')'

wc = core.mining.spilter.WordCatcher(position_restr)


def position(repo, stream, search_text):
    global wc
    ms = core.mining.spilter.MarkdownStruct(stream)
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
        cleanstream = re.sub('[- ]+' ,' ' , findstream)
        wc.bn_bn(cleanstream)
    return wc.result()


def region(stream):
    ms = core.mining.spilter.MarkdownStruct(stream)
    filter1 = core.mining.spilter.Info(ms, organization_restr)
    filter2 = core.mining.spilter.Info(ms, time_restr)
    ranges = []
    for each in filter1.positions:
        try:
            range = filter2.range(each, 0, 1)
            ranges.append(range)
        except ValueError:
            pass
        if len(ranges) == 0:
            continue
    results = []
    for range in set(ranges):
        findstream = ''.join(ms.get_strs_from_positions([range]))
        cleanstream = re.sub('[- ]+' ,' ' , findstream)
        for w in jieba.posseg.cut(cleanstream, HMM=False):
            if w.flag == 'ns':
                result = rs.get(w.word)
                if result:
                    results.append(result)
    return results


def capacity(stream):
    ms = core.mining.spilter.MarkdownStruct(stream)
    filter1 = core.mining.spilter.Info(ms, organization_restr)
    filter2 = core.mining.spilter.Info(ms, time_restr)
    ranges = []
    for each in filter1.positions:
        try:
            range = filter2.range(each, 0, 1)
            ranges.append(range)
        except ValueError:
            pass
        if len(ranges) == 0:
            continue
    results = []
    for range in set(ranges):
        job_info = dict()
        findstream = ''.join(ms.get_strs_from_positions([range]))
        cleanstream = re.sub('[- ]+' ,' ' , findstream)
        wordcut = jieba.posseg.cut(cleanstream, HMM=False)
        count = 0
        for each in wordcut:
            if each.flag == 'v':
                count += 1
        if count == 0:
            continue
        job_info['doclen'] = len(cleanstream)
        job_info['actpoint'] = count
        timeline = re.findall(time_restr, findstream)
        job_info['begin'] = timeline[0]
        try:
            job_info['end'] = timeline[1]
        except IndexError:
            job_info['end'] = ''
        results.append(job_info)
    return results
