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


def convert_folder(path, svc_cv, temp_output, committer=None, origin=None):
    import services.curriculumvitae
    if not os.path.exists(temp_output):
        os.makedirs(temp_output)
    for root, dirs, files in os.walk(path):
        for filename in files:
            f = open(os.path.join(root, filename), 'r')
            upobj = services.curriculumvitae.CurriculumVitaeObject(filename,
                                                                   f, temp_output)
            if origin is not None:
                upobj.filepro.yamlinfo['origin'] = origin
            if not upobj.filepro.yamlinfo['name']:
                name = '' # name_from_51job(processfile.markdown_stream)
                upobj.filepro.yamlinfo['name'] = name
                if not upobj.filepro.yamlinfo['name']:
                    upobj.filepro.yamlinfo['name'] = '' # name_from_filename(filename)
            try:
                result = svc_cv.add(upobj, unique=False)
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


import extractor.information_explorer

def update_selected(svc_cv, yamlname, selected):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.repo_path, yamlname)
    info = extractor.information_explorer.catch_selected(svc_cv.getmd(yamlname),
                                                         selected, svc_cv.name)
    obj.update(info)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def update_xp(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.repo_path, yamlname)
    extracted_data = extractor.information_explorer.get_experience(svc_cv.getmd(yamlname),
                                                                   svc_cv.name)
    obj.update(extracted_data)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def safeyaml(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.repo_path, yamlname)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def originid(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.repo_path, yamlname)
    if 'originid' not in obj:
        id_str, suffix = os.path.splitext(yamlname)
        obj['originid'] = obj['id']
        obj['id'] = id_str
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def yamlaction(svc_cv, action, *args, **kwargs):
    for yamlname in svc_cv.yamls():
        action(svc_cv, yamlname, *args, **kwargs)



def tracking_and_command(DEF_SVC_CV, attribute, fix=False, filltime=False):
    def fix_same(l):
        new = list()
        for each in l:
            if each not in new:
                new.append(each)
        return tuple(new)

    import re
    import yaml
    import collections
    DATA_DB = DEF_SVC_CV.interface
    save_dict = collections.defaultdict(list)
    for each in  DATA_DB.history():
        filenames = (re.findall('File ([a-z0-9]{8}\.yaml)\:  Add %s\.'%attribute,
                               each['message']) or
                    re.findall('Add %s in ([a-z0-9]{8}\.yaml)\.'%attribute,
                               each['message']))
        if filenames:
            save_dict[filenames[0]].append([each['author'], each['time']])

    for each in save_dict:
        if each:
            try:
                yaml_info = DEF_SVC_CV.getyaml(each)
                infos = yaml_info[attribute]
            except IOError:
                print each
                continue
            try:
                assert len(save_dict[each]) == len(infos)
            except:
                if fix:
                    yaml_info[attribute] = fix_same(infos)
                    infos = yaml_info[attribute]
                assert len(save_dict[each]) == len(infos)
            if filltime:
                for index in range(len(infos)):
                    assert save_dict[each][index][0].startswith(infos[index]['author'])
                    if 'date' not in infos[index]:
                        yaml_info[attribute][index]['date'] = save_dict[each][index][1]
            if fix or filltime:
                path_filename = os.path.join(DATA_DB.path, DEF_SVC_CV.path, each)
                with open(path_filename, 'w') as fp:
                    fp.write(yaml.safe_dump(yaml_info, allow_unicode=True))
