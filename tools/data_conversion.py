# -*- coding: utf-8 -*-

import path
import json
import yaml
import shutil
import os.path
import functools
import collections

import utils._yaml
import utils.builtin


account_12 = """bookmark: !!set {}
email: ''
id: ''
member: willendare
modifytime: ''
name: ''
phone: ''"""

password_12 = """id: 
modifytime: 
password: 
"""

message_12 = """id:
invited_member: []
inviter_member: []
processed_member: []
read_chat: []
sent_chat: []
unread_chat: []
"""

member_12 = """administrator: !!set {}
limitPEO: peolimit
storageCV: cvindividual
storagePEO: peoindividual
"""

project_12 = """autosetup: false
autoupdate: false
classify: [房地产, 培训, 建筑装潢/市政建设, 医院/医疗/护理, 环保, 服装/纺织/皮革, 市场/营销, 工程/机械/能源, 生物/制药/医疗器械,
  美容/健身/体育, 餐饮/娱乐, 通信技术开发及应用, 化工, 计算机硬件, 公关/媒介, 银行, 保安/家政/其他服务, 影视/媒体, 科研人员, 金融/证券/期货/投资,
  公务员, 酒店/旅游, 其他, 贸易, 保险, 电子/电器/半导体/仪器仪表, 物业管理, 百货/连锁/零售服务, 律师/法务/合规, 汽车, 计算机软件, 交通运输服务,
  财务/审计/税务, 航空/航天, 生产/营运, IT-品管、技术支持及其它, 质量管理/安全防护, 农/林/牧/渔, 写作/出版/印刷, 广告, 互联网/电子商务/网游,
  咨询/顾问]
"""

def convert_account(current_template, next_template, version):
    if version == '1.2':
        with open(os.path.join(next_template['ACCOUNT'], 'account.yaml')) as f:
            accounts = yaml.load(f.read())
            for name in accounts:
                d = yaml.load(account_12)
                d['name'] = name
                d['id'] = utils.builtin.hash(name)
                with open(os.path.join(next_template['ACCOUNT'], d['id']+'.yaml'), 'w') as out:
                    out.write(yaml.dump(d, Dumper=utils._yaml.SafeDumper, default_flow_style=False))

def convert_message(current_template, next_template, version):
    if version == '1.2':
        with open(os.path.join(next_template['ACCOUNT'], 'account.yaml')) as f:
            accounts = yaml.load(f.read())
            for name in accounts:
                d = yaml.load(message_12)
                d['id'] = utils.builtin.hash(name)
                with open(os.path.join(next_template['MESSAGE'], d['id']+'.yaml'), 'w') as out:
                    out.write(yaml.dump(d, Dumper=utils._yaml.SafeDumper, default_flow_style=False))

def convert_member(current_template, next_template, version):
    if version == '1.1':
        # This is a backward conversion (from 1.2)
        for member in ('willendare',):
            for subdir in ('accounts', 'companies', 'curriculumvitaes', 'projects'):
                if subdir in ('projects',):
                    for project in [os.path.basename(_) for _ in path.Path(os.path.join(current_template['MEMBERS'], member, subdir)).dirs()]:
                        try:
                            os.makedirs(os.path.join(next_template['PROJECT'], project))
                        except OSError:
                            pass
                        for data in ('CO', 'CV', 'PEO', 'JD'):
                            try:
                                os.makedirs(os.path.join(next_template['PROJECT'], project, data))
                            except OSError:
                                pass
                            if data in ('CO', 'CV', 'PEO'):
                                files = path.Path(current_template['_'.join((data, 'REPO'))]).files()
                                with open(os.path.join(current_template['MEMBERS'], member, subdir, project, data, 'names.json')) as f:
                                    names = [_+'.yaml' for _ in json.loads(f.read())]
                                    for name in [_ for _ in files if os.path.basename(_) in names]:
                                        shutil.copy(name, os.path.join(next_template['PROJECT'], project, data, os.path.basename(name)))
                            elif data in ('JD',):
                                files = path.Path(os.path.join(current_template['MEMBERS'], member, subdir, project, data)).files()
                                for name in files:
                                    shutil.copy(name, os.path.join(next_template['PROJECT'], project, data, os.path.basename(name)))
    elif version == '1.2':
        for member in ('default', 'willendare'):
            os.makedirs(os.path.join(next_template['MEMBERS'], member))
            d = yaml.load(member_12)
            if member == 'willendare':
                d['storageCV'] = 'cloudshare'
                d['storagePEO'] = 'peostorage'
                d['administrator'] = {}
                d['max_project_nums'] = 100
                admin = ['root', 'WLJ', 'DYL']
                for f in path.Path(next_template['ACCOUNT']).files():
                    if f.endswith('account.yaml'):
                        continue
                    account = yaml.load(f.text())
                    if account['name'] in admin:
                        d['administrator'][account['id']] = None
            with open(os.path.join(next_template['MEMBERS'], member, 'config.yaml'), 'w') as out:
                out.write(yaml.dump(d, Dumper=utils._yaml.SafeDumper, default_flow_style=False))
            for subdir in ('accounts', 'companies', 'curriculumvitaes', 'projects'):
                os.makedirs(os.path.join(next_template['MEMBERS'], member, subdir))
                if subdir in ('accounts', 'curriculumvitaes'):
                    d = []
                    if member == 'willendare':
                        if subdir == 'accounts':
                            for f in path.Path(next_template['ACCOUNT']).files():
                                d.append(os.path.basename(f).split(os.path.extsep)[0])
                        elif subdir == 'curriculumvitaes':
                            for f in path.Path(current_template['CV_REPO']).files():
                                d.append(os.path.basename(f).split(os.path.extsep)[0])
                    with open(os.path.join(next_template['MEMBERS'], member, subdir, 'names.json'), 'w') as out:
                        json.dump(d, out)
                elif subdir in ('companies',):
                    d = []
                    if member == 'willendare':
                        for f in path.Path(current_template['CO_REPO']).files():
                            d.append(os.path.basename(f).split(os.path.extsep)[0])
                            shutil.copy(f, os.path.join(next_template['MEMBERS'], member, subdir, os.path.basename(f)))
                    with open(os.path.join(next_template['MEMBERS'], member, subdir, 'names.json'), 'w') as out:
                        json.dump(d, out)
                elif subdir in ('projects',):
                    if member == 'willendare':
                        for project in [os.path.basename(_) for _ in path.Path(current_template['PROJECT']).dirs()]:
                            os.makedirs(os.path.join(next_template['MEMBERS'], member, subdir, project))
                            try:
                                shutil.copy(os.path.join(current_template['PROJECT'], project, 'config.yaml'),
                                            os.path.join(next_template['MEMBERS'], member, subdir, project, 'config.yaml'))
                            except IOError:
                                pass
                            for data in ('CO', 'CV', 'PEO', 'JD'):
                                if data in ('CO', 'CV', 'PEO'):
                                    os.makedirs(os.path.join(next_template['MEMBERS'], member, subdir, project, data))
                                    files = [os.path.basename(_) for _ in path.Path(os.path.join(current_template['PROJECT'], project, data)).files()]
                                    with open(os.path.join(next_template['MEMBERS'], member, subdir, project, data, 'names.json'), 'w') as out:
                                        json.dump([_.split(os.extsep)[0] for _ in files], out)
                                else:
                                    os.renames(os.path.join(current_template['PROJECT'], project, data), os.path.join(next_template['MEMBERS'], member, subdir, project, data))
                    else:
                        os.makedirs(os.path.join(next_template['MEMBERS'], member, subdir, 'default'))
                        with open(os.path.join(next_template['MEMBERS'], member, subdir, 'default', 'config.yaml'), 'w') as out:
                            d = yaml.load(member_12)
                            del d['administrator']
                            d.update(yaml.load(project_12))
                            out.write(yaml.dump(d, Dumper=utils._yaml.SafeDumper, allow_unicode=True, default_flow_style=False))
                        for data in ('CO', 'CV', 'PEO', 'JD'):
                            os.makedirs(os.path.join(next_template['MEMBERS'], member, subdir, 'default', data))
                            if data in ('CO', 'CV', 'PEO'):
                                with open(os.path.join(next_template['MEMBERS'], member, subdir, 'default', data, 'names.json'), 'w') as out:
                                    json.dump([], out)
    elif version == '1.5':
        for member in path.Path(os.path.join(next_template['MEMBERS'])).dirs():
            if member:
                for subdir in ('projects', 'companies'):
                    if subdir in ('projects',):
                        for data in ('CO', 'CV', 'PEO', 'JD'):
                            if data in ('JD', ):
                                try:
                                    os.makedirs(next_template['_'.join((data, 'REPO'))])
                                except OSError:
                                    pass
                                for project in path.Path(os.path.join(next_template['MEMBERS'], member, subdir)).dirs():
                                    files = [os.path.basename(_) for _ in path.Path(os.path.join(project, data)).files()]
                                    with open(os.path.join(project, data, 'names.json'), 'w') as out:
                                        json.dump([_.split(os.extsep)[0] for _ in files], out)
                                    for f in path.Path(os.path.join(project, data)).files():
                                        if os.path.basename(f) == 'names.json':
                                            continue
                                        try:
                                            os.renames(f, os.path.join(next_template['_'.join((data, 'REPO'))], os.path.basename(f)))
                                        except IOError:
                                            pass
                    elif subdir in ('companies',):
                        for data in ('CO', 'CV', 'PEO', 'JD'):
                            if data in ('CO', ):
                                try:
                                    os.makedirs(next_template['_'.join((data, 'REPO'))])
                                except OSError:
                                    pass
                                files = [os.path.basename(_) for _ in path.Path(os.path.join(next_template['MEMBERS'], member, subdir)).files()]
                                with open(os.path.join(project, data, 'names.json'), 'w') as out:
                                    json.dump([_.split(os.extsep)[0] for _ in files], out)
                                for f in path.Path(os.path.join(next_template['MEMBERS'], member, subdir)).files():
                                        if os.path.basename(f) == 'names.json':
                                            continue
                                        try:
                                            os.renames(f, os.path.join(next_template['_'.join((data, 'REPO'))], os.path.basename(f)))
                                        except IOError:
                                            pass

def convert_password(current_template, next_template, version):
    if version == '1.1':
        # This is a backward conversion (from 1.2)
        accounts = {}
        for f in path.Path(current_template['PASSWORD']).files():
            if f.endswith('account.yaml'):
                continue
            d = yaml.load(f.text())
            with open(os.path.join(current_template['ACCOUNT'], os.path.basename(f))) as acc:
                d.update(yaml.load(acc.read()))
            accounts[d['name']] = d['password']
        with open(os.path.join(next_template['ACCOUNT'], 'account.yaml'), 'w') as out:
            out.write(yaml.dump(accounts, Dumper=utils._yaml.SafeDumper, default_flow_style=False))
    elif version == '1.2':
        with open(os.path.join(next_template['ACCOUNT'], 'account.yaml')) as f:
            accounts = yaml.load(f.read())
            for name in accounts:
                d = yaml.load(password_12)
                d['password'] = accounts[name]
                d['id'] = utils.builtin.hash(name)
                with open(os.path.join(next_template['PASSWORD'], d['id']+'.yaml'), 'w') as out:
                    out.write(yaml.dump(d, Dumper=utils._yaml.SafeDumper, default_flow_style=False))

def convert_model(current_template, next_template, version):
    if version == '1.5':
        for model in ('default', 'ArtificialIntelligence',):
            for subdir in ('all', 'model',):
                try:
                    os.makedirs(os.path.join(next_template['LSI'], model, subdir))
                except OSError:
                    pass
            if model in ('default',):
                try:
                    os.makedirs(os.path.join(next_template['LSI'], model, 'all', model))
                except OSError:
                    pass

conversion_rules = {
    # Backward conversions
    ('1.2', '1.1'): collections.OrderedDict({
        'PASSWORD': functools.partial(convert_password, version='1.1'),
        }),
    # Forward conversions
    ('1.1', '1.2'): collections.OrderedDict({
        'ACCOUNT': functools.partial(convert_account, version='1.2'),
        'PASSWORD': functools.partial(convert_password, version='1.2'),
        'MESSAGE': functools.partial(convert_message, version='1.2'),
        'MEMBERS': functools.partial(convert_member, version='1.2'),
        }),
    ('1.2', '1.5'): collections.OrderedDict({
        'MEMBERS': functools.partial(convert_member, version='1.5'),
        'LSI': functools.partial(convert_model, version='1.5'),
        }),
    }

