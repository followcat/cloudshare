# -*- coding: utf-8 -*-

import os
import shutil

import utils.chsname
import core.exception
import core.converterutils


def move_file(path, origin_path, filename):
    base = "/tmp/Classify"
    des_path = os.path.join(base, path)
    if not os.path.exists(des_path):
        os.makedirs(des_path)
    shutil.copy(os.path.join(origin_path, filename),
                os.path.join(des_path, filename))


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
            name = utils.chsname.name_from_51job(processer.markdown_stream)
            if name:
                path = "51jobname"
                move_file(path, origin_path, filename)
            else:
                name = utils.chsname.name_from_filename(filename)
                if name:
                    path = "name_in_filename"
                    move_file(path, origin_path, filename)
                else:
                    path = "needaddname"
                    move_file(path, origin_path, filename)
    else:
        path = "NoneConnection"
        move_file(path, origin_path, filename)


def convert_folder(path, svc_cv, projectname, temp_output, committer=None, origin=None):
    import core.basedata
    if not os.path.exists(temp_output):
        os.makedirs(temp_output)
    for root, dirs, files in os.walk(path):
        for filename in files:
            f = open(os.path.join(root, filename), 'r')
            filepro = core.converterutils.FileProcesser(filename, f,
                                                        temp_output)
            cvobj = core.basedata.DataObject(filepro.name, filepro.markdown_stream,
                                             filepro.yamlinfo)
            if origin is not None:
                cvobj.metadata['origin'] = origin
            if not cvobj.metadata['name']:
                name = '' # name_from_51job(processfile.markdown_stream)
                cvobj.metadata['name'] = name
                if not cvobj.metadata['name']:
                    cvobj.metadata['name'] = '' # name_from_filename(filename)
            try:
                result = svc_cv.add(cvobj, unique=False, projectname=projectname)
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

def get_explorer_name(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    if obj['origin'] == u'无忧精英爬取':
        explorer_name = 'jingying'
    elif obj['origin'] == u'智联卓聘爬取':
        explorer_name = 'zhilian'
    elif obj['origin'] == u'中华英才爬取':
        explorer_name = 'yingcai'
    elif obj['origin'] == u'猎聘爬取':
        explorer_name = 'liepin'
    else:
        explorer_name = svc_cv.name
    return explorer_name

def update_selected(svc_cv, yamlname, selected):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
    explorer_name = get_explorer_name(svc_cv, yamlname)

    info = extractor.information_explorer.catch_selected(svc_cv.getmd(yamlname),
                                                         selected, explorer_name)
    obj.update(info)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def update_xp(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
    explorer_name = get_explorer_name(svc_cv, yamlname)

    extracted_data = extractor.information_explorer.get_experience(svc_cv.getmd(yamlname),
                                                                   explorer_name)
    obj.update(extracted_data)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def safeyaml(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def originid(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
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



def tracking_and_command(SVC_CV_REPO, attribute, fix=False, filltime=False):
    def fix_same(l):
        new = list()
        for each in l:
            if each not in new:
                new.append(each)
        return tuple(new)

    import re
    import yaml
    import collections
    REPO_DB = SVC_CV_REPO.interface
    save_dict = collections.defaultdict(list)
    for each in  REPO_DB.history():
        filenames = (re.findall('File ([a-z0-9]{8}\.yaml)\:  Add %s\.'%attribute,
                               each['message']) or
                    re.findall('Add %s in ([a-z0-9]{8}\.yaml)\.'%attribute,
                               each['message']))
        if filenames:
            save_dict[filenames[0]].append([each['author'], each['time']])

    for each in save_dict:
        if each:
            try:
                yaml_info = SVC_CV_REPO.getyaml(each)
                infos = yaml_info[attribute]
            except IOError:
                print(each)
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
                path_filename = os.path.join(REPO_DB.path, SVC_CV_REPO.path, each)
                with open(path_filename, 'w') as fp:
                    fp.write(yaml.safe_dump(yaml_info, allow_unicode=True))


def company_knowledge(SVC_CV, knowledge):
    for y in SVC_CV.yamls():
        info = SVC_CV.getyaml(y)
        try:
            for c in info['experience']['company']:
                try:
                    knowledge[c['name']].append(c['business'])
                except KeyError:
                    continue
        except KeyError:
            continue
        except TypeError:
            pass
    del knowledge['']
    
def initclassify(SVC_CV, knowledge=None):
    import collections
    import utils.builtin

    if knowledge is None:
        knowledge = collections.defaultdict(list)
        
    for y in SVC_CV.yamls():
        info = SVC_CV.getyaml(y)
        info['classify'] = extractor.information_explorer.get_classify(info['experience'], knowledge)
        utils.builtin.save_yaml(info, SVC_CV.path , y)


def inituniqueid(SVC_CV, with_report=False, with_diff=False):
    import difflib
    import utils.builtin
    import extractor.unique_id

    path_prefix = lambda x: os.path.join(SVC_CV.repo_path, x)
    unique_ids = {}
    for y in SVC_CV.yamls():
        info = SVC_CV.getyaml(y)
        info = extractor.unique_id.unique_id(info)
        try:
            assert info['unique_id'] not in unique_ids
            unique_ids[info['unique_id']] = y
        except KeyError:
            pass
        except AssertionError:
            if with_report:
                print(info['unique_id'], path_prefix(y) + ' ' + path_prefix(unique_ids[info['unique_id']]))
                if with_diff:
                    print('++++\n')
                    old = path_prefix(unique_ids[info['unique_id']])
                    new = path_prefix(y)
                    for l in difflib.unified_diff(file(old).readlines(), file(new).readlines(), old, new):
                        print(l.rstrip())
                    print('\n++++\n')
        utils.builtin.save_yaml(info, SVC_CV.repo_path , y)



def initproject(SVC_CV_REPO, SVC_PRJ):
    import utils.builtin
    for y in SVC_CV_REPO.yamls():
        info = SVC_CV_REPO.getyaml(y)
        convert_info = dict()
        convert_info['tag'] = info.pop('tag')
        convert_info['comment'] = info.pop('comment')
        convert_info['tracking'] = info.pop('tracking')
        convert_info['committer'] = info['committer']
        SVC_PRJ._add(y)
        utils.builtin.save_yaml(info, SVC_CV_REPO.path , y)
        utils.builtin.save_yaml(convert_info, SVC_PRJ.cvpath , y)
        SVC_PRJ.save()
