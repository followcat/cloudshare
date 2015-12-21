import re

import jieba.posseg


class MarkdownStruct(object):
    def __init__(self, stream):
        self.splits = [line for line in stream.split('\n') if line]

    def get_strs_from_positions(self, ranges):
        """
            >>> import core.mining.spilter
            >>> stream = "\\n0\\n1x\\n2\\n3x\\n4\\n5x\\n6\\n7x\\n8\\n9x"
            >>> ms = core.mining.spilter.MarkdownStruct(stream)
            >>> ms.get_strs_from_positions([(2, 7), (3, 5)])
            ['3x', '4', '5x', '6']
        """
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
        """
            >>> import core.mining.spilter
            >>> stream = "\\n0\\n1x\\n2\\n3x\\n4\\n5x\\n6\\n7x\\n8\\n9x"
            >>> ms = core.mining.spilter.MarkdownStruct(stream)
            >>> info = core.mining.spilter.Info(ms, r'\\d{1}x')
            >>> info.positions
            [(1, 0), (3, 0), (5, 0), (7, 0), (9, 0)]
            >>> info.ceiling((5, 0))
            (5, 0)
            >>> info.ceiling((4, 0))
            (3, 0)
            >>> info.ceiling((4, 0), level=1)
            (1, 0)
            >>> info.ceiling((1, 0), level=1)
            (1, 0)
        """
        try:
            nearest = min(self.positions, key=lambda x:abs(x[0]-pos[0]))
            index = self.positions.index(nearest)-level
            if index < 0:
                raise IndexError
        except IndexError:
            index = 0
        return self.positions[index]


    def floor(self, pos, level=0):
        """
            >>> import core.mining.spilter
            >>> stream = "\\n0\\n1x\\n2\\n3x\\n4\\n5x\\n6\\n7x\\n8\\n9x"
            >>> ms = core.mining.spilter.MarkdownStruct(stream)
            >>> info = core.mining.spilter.Info(ms, r'\\d{1}x')
            >>> info.positions
            [(1, 0), (3, 0), (5, 0), (7, 0), (9, 0)]
            >>> info.floor((5, 0))
            (5, 0)
            >>> info.floor((4, 0), level=1)
            (5, 0)
            >>> info.floor((4, 0), level=2)
            (7, 0)
            >>> info.floor((9, 0), level=1)
            (9, 0)
        """
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
        """
            >>> import jieba.posseg
            >>> import core.mining.spilter
            >>> pt = jieba.posseg.pair
            >>> str_list = [[pt('this', 'eng'), pt('is', 'eng')],
            ...             [pt('a', 'eng')],
            ...             [pt('test', 'eng'), pt('string', 'eng')]]
            >>> wc = core.mining.spilter.WordCatcher("[a-z]+")
            >>> wc.word_list = str_list
            >>> wc.result()
            set(['a', 'thisis', 'teststring'])
        """
        result = []
        for word in self.word_list:
            word_str = ''.join([c.word for c in word])
            for r in self.regex.findall(word_str):
                rstr = ''.join(r)
                result.append(rstr)
        return set(result)

    def reset(self):
        self.word_list = []
