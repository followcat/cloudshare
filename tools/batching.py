# -*- coding: utf-8 -*-

import os
import shutil

import utils.chsname
import core.exception
import core.docprocessor
import extractor.information_explorer


def move_file(path, origin_path, filename):
    base = "/tmp/Classify"
    des_path = os.path.join(base, path)
    if not os.path.exists(des_path):
        os.makedirs(des_path)
    shutil.copy(os.path.join(origin_path, filename),
                os.path.join(des_path, filename))


def filter(processer, yamlinfo, origin_path, filename):
    def mustjudge(d):
        return (d['email'] or d['phone'])

    if processer.result is False:
        path = "NotConvert"
        move_file(path, origin_path, filename)
        return
    info = yamlinfo
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
            filepro = core.docprocessor.Processor(filename, f, temp_output)
            yamlinfo = extractor.information_explorer.catch_cvinfo(
                                        stream=filepro.markdown_stream.decode('utf8'),
                                        filename=filepro.base.base)
            cvobj = core.basedata.DataObject(data=filepro.markdown_stream,
                                             metadata=yamlinfo)
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
            filepro = core.docprocessor.Processor(root, name, temp_output)
            yamlinfo = extractor.information_explorer.catch_cvinfo(
                                        stream=filepro.markdown_stream.decode('utf8'),
                                        filename=filepro.base.base)
            filter(filepro, yamlinfo, root, name)


import yaml
import utils._yaml
import utils.builtin

yaml.SafeDumper = utils._yaml.SafeDumper


import extractor.information_explorer

def get_explorer_name(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    explorer_name = svc_cv.name
    try:
        if obj['origin'] == u'无忧精英爬取':
            explorer_name = 'jingying'
        elif obj['origin'] == u'智联卓聘爬取':
            explorer_name = 'zhilian'
        elif obj['origin'] == u'中华英才爬取':
            explorer_name = 'yingcai'
        elif obj['origin'] == u'猎聘爬取':
            explorer_name = 'liepin'
    except TypeError:
        pass
    except KeyError:
        pass
    return explorer_name

def update_selected(svc_cv, yamlname, selected):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
    explorer_name = get_explorer_name(svc_cv, yamlname)

    info = extractor.information_explorer.catch_selected(svc_cv.getmd(yamlname),
                                                         selected, explorer_name)
    try:
        obj.update(info)
    except AttributeError:
        obj = info
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def update_uniqueid(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
    extractor.unique_id.unique_id(obj)
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
    import time
    import utils.timeout.process
    i = 0
    for yamlname in svc_cv.yamls():
        i += 1
        t1 = time.time()
        try:
            utils.timeout.process.process_timeout_call(action, 120,
                                    args=tuple([svc_cv, yamlname]+list(args)),
                                    kwargs=kwargs)
        except utils.timeout.process.KilledExecTimeout as e:
            print(yamlname, action, e)
        usetime = time.time() - t1
        print("CV %s use %s."%(yamlname, str(usetime)))
        if i % 100 == 0:
            print i

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


def company_knowledge(SVC_CV, SVC_CO):
    import core.basedata
    import core.outputstorage
    import services.exception

    for y in SVC_CV.yamls():
        info = SVC_CV.getyaml(y)
        try:
            for c in [c for c in info['experience']['company'] if c['name']]:
                company = extractor.information_explorer.catch_coinfo(name=c['name'], stream=c)
                coobj = core.basedata.DataObject(company, data='')
                try:
                    result = SVC_CO.add(coobj)
                except services.exception.ExistsCompany:
                    name = core.outputstorage.ConvertName(coobj.metadata['id'])
                    coinfo = SVC_CO.getyaml(name)
                    coinfo['business'] = sorted(set(coinfo['business']).union(set(coobj.metadata['business'])))
                    if 'total_employees' in coobj.metadata and coobj.metadata['total_employees']:
                        coinfo['total_employees'] = coobj.metadata['total_employees']
                    utils.builtin.save_yaml(coinfo, SVC_CO.path , name.yaml)
        except KeyError:
            continue
        except TypeError:
            pass

def initclassify(SVC_CV, SVC_CO=None):
    import collections
    import utils.builtin

    for y in SVC_CV.yamls():
        info = SVC_CV.getyaml(y)
        info['classify'] = extractor.information_explorer.get_classify(info['experience'], SVC_CO)
        if info['classify']:
            utils.builtin.save_yaml(info, SVC_CV.path , y)


def inituniqueid(SVC_CV, with_report=False, with_diff=False):
    import difflib
    import utils.builtin
    import extractor.unique_id

    path_prefix = lambda x: os.path.join(SVC_CV.path, x)
    unique_ids = {}
    for y in SVC_CV.yamls():
        info = SVC_CV.getyaml(y)
        extractor.unique_id.unique_id(info)
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
        utils.builtin.save_yaml(info, SVC_CV.path , y)



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


def convert_oldcompany(SVC_CO_REPO, filepath, filename):
    import core.basedata
    yamls = utils.builtin.load_yaml(filepath, filename)
    for y in yamls:
        args = y
        metadata = extractor.information_explorer.catch_coinfo(name=args['name'], stream=args)
        coobj = core.basedata.DataObject(metadata, data=args['introduction'].encode('utf-8'))
        SVC_CO_REPO.add(coobj)


def update_jd_co_id(SVC_JD, SVC_CO):
    import yaml
    co_dict = {}
    for id in SVC_CO.ids:
        co_info = SVC_CO.getyaml(id)
        co_dict[co_info['name']] = co_info

    for jd in SVC_JD.lists():
        jd_id = jd['id']
        jd_company = jd['company']
        if jd_company in co_dict:
            jd['company'] = co_dict[jd_company]['id']
            dump_data = yaml.safe_dump(jd, allow_unicode=True)
            filename = SVC_JD.filename(jd_id)
            with open(os.path.join(SVC_JD.path, filename), 'w') as f:
                f.write(dump_data)


def update_jd_commentary(SVC_JD, comments_dict):
    import yaml
    for jd in SVC_JD.lists():
        if 'commentary' in jd:
            continue
        jd_id = jd['id']
        if jd_id in comments_dict:
            jd['commentary'] = comments_dict[jd_id]
        else:
            jd['commentary'] = ''
        dump_data = yaml.safe_dump(jd, allow_unicode=True)
        filename = SVC_JD.filename(jd_id)
        with open(os.path.join(SVC_JD.path, filename), 'w') as f:
            f.write(dump_data)


def init_people(SVC_CV, SVC_PEO):
    import core.basedata
    for y in SVC_CV.yamls():
        info = SVC_CV.getyaml(y)
        peopmeta = extractor.information_explorer.catch_peopinfo(info)
        peopobj = core.basedata.DataObject(data='', metadata=peopmeta)
        SVC_PEO.add(peopobj)
