# -*- coding: utf-8 -*-
import re
import glob
import os.path
import subprocess

import yaml
import pypandoc

import core.information_explorer
import utils.builtin
import interface.base

from interface.utils_parsing import *



def cloudshare_yaml_template():
    template = {
        'age': 0,
        'comment': [],
        'committer': "SCRAPPY",
        'company': "",
        'date': 0.,
        'education': "",
        'email': '',
        'experience': [],
        'filename': "",
        'id': '',
        'name': "",
        'origin': u'猎聘爬取',
        'phone': "",
        'position': "",
        'school': "",
        'tag': [],
        'tracking': [],
        }
    return template


def extract_details(uploaded_details):
    details = cloudshare_yaml_template()

    details['date'] = 0
    details['name'] = uploaded_details['name']
    details['id'] = uploaded_details['data-id']
    details['company'] = uploaded_details['peo'][7]
    details['position'] = uploaded_details['peo'][6]
    details['filename'] = uploaded_details['href']
    details['age']= re.compile('[0-9]*').match(uploaded_details['peo'][2]).group()
    add_cr = lambda x:'\n'+x.group()
    for education in re.compile(STUDIES, re.M).finditer(re.compile(PERIOD).sub(add_cr, uploaded_details['info'][0])):
        details['school'] = education.group('school')
        details['major'] = education.group('major')
        details['education'] = education.group('education')

    for expe in uploaded_details['info']:
        for w in re.compile(WORKXP, re.M).finditer(re.compile(PERIOD).sub(add_cr, expe)):
            details['experience'].append((fix_date(w.group('from')), fix_date(w.group('to')),
                fix_name(w.group('company'))+'|'+fix_name(w.group('position'))+'('+fix_duration(w.group('duration'))+')'))
    if u'…' in details['company']:
        no_braket = lambda x:x.replace('(','').replace(')','')
        escape_star = lambda x:x.replace('*','\*')
        RE = re.compile(escape_star(no_braket(details['company'])[:-1]))
        for xp in details['experience']:
            if RE.match(no_braket(xp[2])):
                details['company'] = xp[2].split('|')[0]
                break
    return details


class PredatorLiteInterface(interface.base.Interface):
    
    def __init__(self, yamlpath):
        self.path = os.path.split(yamlpath)[0]
        super(PredatorLiteInterface, self).__init__(self.path)
        self.yamlpath = yamlpath
        self.yamlfile = list()
        self.yamlstat = dict()
        self._yamldata = dict()
        self.yamlfiles = glob.glob(os.path.join(self.yamlpath, '*.yaml'))

    @property
    def yamldata(self):
        for yamlfile in self.yamlfiles:
            if (yamlfile in self.yamlstat and
                self.yamlstat[yamlfile] == os.stat(yamlfile)):
                continue
            else:
                path, file = os.path.split(yamlfile)
                for name, data in utils.builtin.load_yaml(path, file).iteritems():
                    self._yamldata[name] = data
                self.yamlstat[yamlfile] = os.stat(yamlfile)
        return self._yamldata

    def exists(self, filename):
        return filename in self.lsfiles()

    def get(self, filename):
        name, extension = os.path.splitext(filename)
        if extension == '.yaml':
            return self._get_yaml(name)
        else:
            return None

    def _get_yaml(self, name):
        data = None
        path, id_str = os.path.split(name)
        if id_str in self.yamldata:
            data = extract_details(self.yamldata[id_str])
        return utils.builtin.dump_yaml(data)

    def lsfiles(self, *args, **kwargs):
        return [name+'.yaml' for name in self.yamldata]

    def grep(self, restrings, path):
        grep_list = []
        keywords = restrings.split()
        if keywords:
            command = 'grep -l '
            command += keywords[0].encode('utf-8')
            command += ' *'
            for each in keywords[1:]:
                command += ' | grep '
                command += each.encode('utf-8')
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=os.path.join(self.path, path), shell=True)
            returncode = p.communicate()[0]
            for each in returncode.split('\n'):
                if each:
                    grep_list.append(each)
        return grep_list

    def grep_yaml(self, restrings, path):
        return []


class PredatorInterface(PredatorLiteInterface):

    extension = '.html'

    def __init__(self, yamlpath, htmlpath):
        super(PredatorInterface, self).__init__(yamlpath)
        self.htmlpath = htmlpath

    @property
    def yamldata(self):
        for yamlfile in self.yamlfiles:
            if (yamlfile in self.yamlstat and
                self.yamlstat[yamlfile] == os.stat(yamlfile)):
                continue
            else:
                path, file = os.path.split(yamlfile)
                for name, data in utils.builtin.load_yaml(path, file).iteritems():
                    if os.path.exists(os.path.join(self.htmlpath, name+self.extension)):
                        self._yamldata[name] = data
                self.yamlstat[yamlfile] = os.stat(yamlfile)
        return self._yamldata

    def exists(self, filename):
        result = False
        name, extension = os.path.splitext(filename)
        filename = filename.replace(extension, self.extension)
        path_file = os.path.join(self.htmlpath, filename)
        if os.path.exists(path_file):
            result = True
        return result

    def get(self, filename):
        name, extension = os.path.splitext(filename)
        if extension == '.yaml':
            return self._get_yaml(name)
        elif extension == '.md':
            cv_path, cv_name = os.path.split(name)
            input_file = os.path.join(self.htmlpath, cv_name+self.extension)
            return pypandoc.convert(input_file, 'markdown', format='docbook')
        else:
            return self._get_file(filename)

    def _get_file(self, filename):
        data = None
        path_file = os.path.join(self.path, filename)
        if os.path.exists(path_file):
            with open(path_file) as fp:
                data = fp.read()
        return data
