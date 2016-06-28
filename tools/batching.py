# -*- coding: utf-8 -*-
import os
import shutil

import core.exception
import core.converterutils
import extractor.information_explorer


def move_file(path, origin_path, filename):
    base = "/tmp/Classify"
    des_path = os.path.join(base, path)
    if not os.path.exists(des_path):
        os.makedirs(des_path)
    shutil.copy(os.path.join(origin_path, filename),
                os.path.join(des_path, filename))


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
    firstname_list = u"李,王,张,刘,陈,杨,黄,赵,周,吴,徐,孙,朱,马,胡,郭,林,何,高,梁,郑,罗,宋,谢,唐,韩,曹,许,邓,萧,冯,曾,程,蔡,彭,潘,袁,於,董,余,苏,叶,吕,魏,蒋,田,杜,丁,沈,姜,范,江,傅,钟,卢,汪,戴,崔,任,陆,廖,姚,方,金,邱,夏,谭,韦,贾,邹,石,熊,孟,秦,阎,薛,侯,雷,白,龙,段,郝,孔,邵,史,毛,常,万,顾,赖,武,康,贺,严,尹,钱,施,牛,洪,龚,翟,由,樊,戚,季,岑,付,占,肖,舒,闫,麦,黎,童,欧".split(u',')
    splits = extractor.information_explorer.get_tagfromstring(filename, ur'[\u4e00-\u9fa5]+')
    name = ''
    for each in splits:
        if each[0] in firstname_list:
            name = each
            break
    return name


def filter(processer, origin_path, filename):
    def mustjudge(d):
        return (d['email'] or d['phone'])

    if processer.result is False:
        path = "NotConvert"
        move_file(path, origin_path, filename)
        return
    info = processer.yamlinfo
    if mustjudge(info):
        if info['name']:
            path = "OK"
            move_file(path, origin_path, filename)
        else:
            name = name_from_51job(processer.markdown_stream)
            if name:
                path = "51jobname"
                move_file(path, origin_path, filename)
            else:
                name = name_from_filename(filename)
                if name:
                    path = "name_in_filename"
                    move_file(path, origin_path, filename)
                else:
                    path = "needaddname"
                    move_file(path, origin_path, filename)
    else:
        path = "NoneConnection"
        move_file(path, origin_path, filename)


def convert_folder(path, repo, temp_output, committer=None, origin=None):
    if not os.path.exists(temp_output):
        os.makedirs(temp_output)
    for root, dirs, files in os.walk(path):
        for filename in files:
            f = open(os.path.join(root, filename), 'r')
            processfile = core.converterutils.FileProcesser(f, filename, temp_output)
            if origin is not None:
                processfile.yamlinfo['origin'] = origin
            if not processfile.yamlinfo['name']:
                name = name_from_51job(processfile.markdown_stream)
                processfile.yamlinfo['name'] = name
                if not processfile.yamlinfo['name']:
                    processfile.yamlinfo['name'] = name_from_filename(filename)
            try:
                processfile.storage(repo, committer=committer)
            except core.exception.DuplicateException as error:
                continue


def classify(path, temp_output):
    if not os.path.exists(temp_output):
        os.makedirs(temp_output)
    for root, dirs, files in os.walk(path):
        for name in files:
            processfile = core.converterutils.FileProcesser(root, name, temp_output)
            filter(processfile, root, name)


import yaml
import utils._yaml
import utils.builtin

yaml.SafeDumper = utils._yaml.SafeDumper

import re
import extractor.extract_experience
RE = re.compile(extractor.extract_experience.DURATION)

def update_xp(svc_cv, yamlname):
    yamlpath = os.path.join(svc_cv.interface.path, svc_cv.path)
    yamlpathfile = os.path.join(svc_cv.interface.path, svc_cv.path, yamlname)
    extracted_data = extractor.extract_experience.fix(svc_cv.getmd(yamlname))
    if not extracted_data[1]:
        (company, position) = extracted_data[0]
        obj = utils.builtin.load_yaml(yamlpath, yamlname)
        obj['experience'] = []
        for (i,c) in enumerate(company):
            current_positions = [p for p in position if p[4] == i]
            for p in current_positions:
                if c[3] and len(current_positions) == 1 and not RE.search(p[2]):
                    obj['experience'].append((p[0], p[1], c[2]+'|'+p[2]+'('+c[3]+')'))
                elif c[3]:
                    obj['experience'].append((p[0], p[1], c[2]+'('+c[3]+')'+'|'+p[2]))
                else:
                    obj['experience'].append((p[0], p[1], c[2]+'|'+p[2]))
            else:
                if not len(current_positions):
                    obj['experience'].append((c[0], c[1], c[2]))
        yamlstream = yaml.safe_dump(obj, allow_unicode=True)
        with open(yamlpathfile, 'w') as fp:
            fp.write(yamlstream)

def safeyaml(svc_cv, yamlname):
    yamlpath = os.path.join(svc_cv.interface.path, svc_cv.path)
    yamlpathfile = os.path.join(svc_cv.interface.path, svc_cv.path, yamlname)
    obj = utils.builtin.load_yaml(yamlpath, yamlname)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def originid(svc_cv, yamlname):
    yamlpath = os.path.join(svc_cv.interface.path, svc_cv.path)
    yamlpathfile = os.path.join(svc_cv.interface.path, svc_cv.path, yamlname)
    obj = utils.builtin.load_yaml(yamlpath, yamlname)
    if 'originid' not in obj:
        id_str, suffix = os.path.splitext(yamlname)
        obj['originid'] = obj['id']
        obj['id'] = id_str

    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def yamlaction(svc_cv, action):
    for yamlname in svc_cv.yamls():
        action(svc_cv, yamlname)
