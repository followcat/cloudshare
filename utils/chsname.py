# -*- coding: utf-8 -*-
import extractor.information_explorer


def name_from_51job(stream):
    name = extractor.information_explorer.get_tagfromstring(stream,
                u'Script简历关键字：[\u4E00-\u9FA5|\w|\S ]+[\n]+([\u4E00-\u9FA5]+)')
    if name:
        return name[0]
    else:
        name = extractor.information_explorer.get_tagfromstring(stream,
                    u'Script([\u4E00-\u9FA5]+)\W')
        if name and len(name) < 4:
            return name[0]
        else:
            return ''


def name_from_filename(filename):
    firstname_list = u"李,王,张,刘,陈,杨,黄,赵,周,吴,徐,孙,朱,马,胡,郭,\
                       林,何,高,梁,郑,罗,宋,谢,唐,韩,曹,许,邓,萧,冯,曾,\
                       程,蔡,彭,潘,袁,於,董,余,苏,叶,吕,魏,蒋,田,杜,丁,\
                       沈,姜,范,江,傅,钟,卢,汪,戴,崔,任,陆,廖,姚,方,金,\
                       邱,夏,谭,韦,贾,邹,石,熊,孟,秦,阎,薛,侯,雷,白,龙,\
                       段,郝,孔,邵,史,毛,常,万,顾,赖,武,康,贺,严,尹,钱,\
                       施,牛,洪,龚,翟,由,樊,戚,季,岑,付,占,肖,舒,闫,麦,\
                       黎,童,欧".split(u',')
    splits = extractor.information_explorer.get_tagfromstring(filename, ur'[\u4e00-\u9fa5]+')
    name = ''
    for each in splits:
        if each[0] in firstname_list:
            name = each
            break
    return name
