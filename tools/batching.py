# -*- coding: utf-8 -*-

import os
import time
import shutil

import utils.builtin
import utils.chsname
import core.exception
import core.outputstorage
import utils.docprocessor.libreoffice
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
            filepro = utils.docprocessor.libreoffice.LibreOfficeProcessor(filename, f, temp_output)
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
            filepro = utils.docprocessor.libreoffice.LibreOfficeProcessor(root, name, temp_output)
            yamlinfo = extractor.information_explorer.catch_cvinfo(
                                        stream=filepro.markdown_stream.decode('utf8'),
                                        filename=filepro.base.base)
            filter(filepro, yamlinfo, root, name)


import yaml
import utils._yaml
import utils.builtin

yaml.SafeDumper = utils._yaml.SafeDumper


import extractor.information_explorer

def get_explorer_name(obj):
    explorer_name = 'default'
    try:
        if obj['origin'] in [u'无忧精英爬取', u'51job', u'前程无忧', u'无忧精英']:
            explorer_name = 'jingying'
        elif obj['origin'] in [u'智联卓聘爬取', u'智联卓聘', u'智联招聘']:
            explorer_name = 'zhilian'
        elif obj['origin'] in [u'中华英才爬取', u'英才网',]:
            explorer_name = 'yingcai'
        elif obj['origin'] in [u'猎聘爬取', u'猎聘网', u'猎聘']:
            explorer_name = 'liepin'
    except TypeError:
        pass
    except KeyError:
        pass
    return explorer_name

def update_selected(svc_cv, yamlname, selected, as_date=None, timing=False):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, core.outputstorage.ConvertName(yamlname).yaml)
    explorer_name = get_explorer_name(obj)

    info = extractor.information_explorer.catch_selected(svc_cv.getmd(yamlname),
                                                         selected,
                                                         fix_func=explorer_name,
                                                         as_date=as_date,
                                                         timing=timing)
    if obj is None:
        obj = dict()
    result = utils.builtin.merge(obj, info, update=True)
    yamlstream = yaml.safe_dump(result, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def update_uniqueid(svc_cv, yamlname):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
    extractor.unique_id.unique_id(obj)
    yamlstream = yaml.safe_dump(obj, allow_unicode=True)
    with open(yamlpathfile, 'w') as fp:
        fp.write(yamlstream)

def update_xp(svc_cv, yamlname, as_date=None):
    obj = svc_cv.getyaml(yamlname)
    yamlpathfile = os.path.join(svc_cv.path, yamlname)
    explorer_name = get_explorer_name(svc_cv, yamlname)
    extracted_data = extractor.information_explorer.get_experience(svc_cv.getmd(yamlname),
                                                                   explorer_name, as_date)
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

def timeout_process_action(svc_cv, action, timeout, *args, **kwargs):
    import utils.timeout.process
    import utils.timeout.exception
    i = 0
    t1 = time.time()
    for yamlname in svc_cv.yamls():
        i += 1
        try:
            utils.timeout.process.timeout_call(action, timeout,
                                    args=tuple([svc_cv, yamlname]+list(args)),
                                    kwargs=kwargs)
        except utils.timeout.exception.ExecTimeout as e:
            print(yamlname, action, e)
        except Exception as e:
            print(yamlname, action, e)
        if i % 100 == 0:
            usetime = time.time() - t1
            t1 = time.time()
            print("100 Action use %s."%(str(usetime)))
            print i

def timeout_thread_action(svc_cv, action, timeout, *args, **kwargs):
    import utils.timeout.thread
    import utils.timeout.exception
    i = 0
    t1 = time.time()
    for yamlname in svc_cv.yamls():
        i += 1
        try:
            utils.timeout.thread.timeout_call(action, timeout,
                                    args=tuple([svc_cv, yamlname]+list(args)),
                                    kwargs=kwargs)
        except utils.timeout.exception.ExecTimeout as e:
            print(yamlname, action, e)
        except utils.timeout.exception.FailedKillExecTimeout as e:
            print(yamlname, action, e)
        except Exception as e:
            print(yamlname, action, e)
        if i % 100 == 0:
            usetime = time.time() - t1
            t1 = time.time()
            print("100 Action use %s."%(str(usetime)))
            print i

def timeout_action(svc_cv, action, timeout, *args, **kwargs):
    import utils.timeout.inprocess
    import utils.timeout.exception
    i = 0
    t1 = time.time()
    for yamlname in svc_cv.yamls():
        i += 1
        try:
            utils.timeout.inprocess.timeout_call(action, timeout,
                                    args=tuple([svc_cv, yamlname]+list(args)),
                                    kwargs=kwargs)
        except utils.timeout.exception.ExecTimeout as e:
            print(yamlname, action, e)
        except Exception as e:
            print(yamlname, action, e)
        if i % 100 == 0:
            usetime = time.time() - t1
            t1 = time.time()
            print("100 Action use %s."%(str(usetime)))
            print i

def yamlaction(svc_cv, action, *args, **kwargs):
    i = 0
    t1 = time.time()
    for yamlname in svc_cv.yamls():
        i += 1
        try:
            action(svc_cv, yamlname, *args, **kwargs)
        except Exception as e:
            print(yamlname, action, e)
        if i % 100 == 0:
            usetime = time.time() - t1
            t1 = time.time()
            print("100 Action use %s."%(str(usetime)))
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
                company = extractor.information_explorer.catch_coinfo(stream=c)
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
        metadata = extractor.information_explorer.catch_coinfo(stream=args)
        coobj = core.basedata.DataObject(metadata, data=args['introduction'].encode('utf-8'))
        SVC_CO_REPO.add(coobj)


def update_jd_co_id(SVC_JD, SVC_CO):
    import yaml
    co_dict = {}
    for id in SVC_CO.ids:
        co_info = SVC_CO.getyaml(id)
        co_dict[co_info['name']] = co_info

    for jd_id, jd in SVC_JD.datas():
        jd_company = jd['company']
        if jd_company in co_dict:
            jd['company'] = co_dict[jd_company]['id']
            dump_data = yaml.safe_dump(jd, allow_unicode=True)
            filename = SVC_JD.filename(jd_id)
            with open(os.path.join(SVC_JD.path, filename), 'w') as f:
                f.write(dump_data)


def update_jd_commentary(SVC_JD, comments_dict):
    import yaml
    for jd_id, jd in SVC_JD.datas():
        if 'commentary' in jd:
            continue
        if jd_id in comments_dict:
            jd['commentary'] = comments_dict[jd_id]
        else:
            jd['commentary'] = ''
        dump_data = yaml.safe_dump(jd, allow_unicode=True)
        filename = SVC_JD.filename(jd_id)
        with open(os.path.join(SVC_JD.path, filename), 'w') as f:
            f.write(dump_data)


def add_jd_followup(SVC_PRJ):
    import yaml
    SVC_JD = SVC_PRJ.jobdescription
    for jd_id, jd in SVC_JD.datas():
        if 'followup' in jd:
            continue
        jd['followup'] = ''
        if '\n' in jd['commentary']:
            jd['followup'] = jd['commentary']
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

def init_esindex_mem(SVC_INDEX, SVC_MEMBERS):
    for memname, mem in SVC_MEMBERS.members.items():
        for prjname, prj in mem.projects.items():
            SVC_INDEX.updatesvc(SVC_INDEX.config['CO_MEM'], prj.id,
                                prj.company, numbers=1000)
            SVC_INDEX.updatesvc(SVC_INDEX.config['JD_MEM'], prj.id,
                                prj.jobdescription, numbers=1000)
            SVC_INDEX.updatesvc(SVC_INDEX.config['CV_MEM'], prj.id,
                                prj.curriculumvitae, numbers=1000)

def init_esindex_cvsto(SVC_INDEX, SVC_CV_STO, content=True):
    SVC_INDEX.updatesvc(SVC_INDEX.config['CV_STO'], SVC_CV_STO.id,
                        SVC_CV_STO, content=content, numbers=5000)
