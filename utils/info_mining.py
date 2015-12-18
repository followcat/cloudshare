# -*- coding: utf-8 -*-
import re
import os
import codecs

import jieba.posseg

import repointerface.gitinterface


class MarkdownStruct(object):
    def __init__(self, stream):
        self.splits = [line for line in stream.split('\n') if line]

    def get_strs_from_positions(self, ranges):
        minstr = max([range[0] for range in ranges])
        maxstr = max([range[1] for range in ranges])
        return self.splits[minstr:maxstr]


class Info(object):
    def __init__(self, lines, restr):
        self.regex = re.compile(restr)
        self.positions = []
        for index, data in enumerate(lines.splits):
            for item in self.regex.finditer(data):
                self.positions.append((index, item.pos))

    def ceiling(self, pos, level=0):
        try:
            nearest = min(self.positions, key=lambda x:abs(x[0]-pos[0]))
            index = self.positions.index(nearest)-level
            if index < 0:
                raise IndexError
        except IndexError:
            index = 0
        return self.positions[index]


    def floor(self, pos, level=0):
        try:
            nearest = min(self.positions, key=lambda x:abs(x[0]-pos[0]))
            index = self.positions.index(nearest)+level
            return self.positions[index]
        except IndexError:
            index -= level
            return self.positions[index]

    def range(self, pos, ceillev, floorlev):
        return self.ceiling(pos, ceillev)[0], self.floor(pos, floorlev)[0]


class WordCatcher(object):
    def __init__(self, restr):
        self.regex = re.compile(restr)
        self.word_list = []

    def bn_bn(self, stream):
        word = []
        for w in jieba.posseg.cut(stream):
            if w.flag[0] in ['b', 'n']:
                word.append(w)
            elif word:
                word.append(w)
                self.word_list.append(list(word))
                word = []
            else:
                word = []
        else:
            if word:
                self.word_list.append(list(word))

    def result(self):
        result = []
        for word in self.word_list:
            word_str = ''.join([c.word for c in word])
            for r in self.regex.findall(word_str):
                rstr = ''.join(r)
                result.append(rstr)
        return set(result)

    def reset(self):
        self.word_list = []

organization = (u'有限公司', U'公司', u'集团', u'院')
organization_restr = u'([a-zA-Z0-9\u4E00-\u9FA5]+)('
for each in organization:
    organization_restr += each + '|'
organization_restr = organization_restr[:-1] + ')'

time_restr = ur'\d{4}[/.\\年 ]+\d{1,2}[月]*'

with open('utils/position.txt', 'r') as f:
    position_key = f.read().decode('utf-8')
    position_keylist = position_key.split(' ')
position_restr = u'([\u4E00-\u9FA5]+)('
for each in position_keylist:
    position_restr += each
    position_restr += '|'
position_restr = position_restr[:-1] + ')'


wc = WordCatcher(position_restr)

def company(repo, searches, search_text):
    global wc
    result_dict = {}
    for search in searches:
        with codecs.open(os.path.join(repo.repo.path, search),
                         'r', encoding='utf-8') as file:
            md_data = file.read()
        ms = MarkdownStruct(md_data)
        key = Info(ms, search_text)
        filter1 = Info(ms, organization_restr)
        filter2 = Info(ms, time_restr)
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
