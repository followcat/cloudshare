# -*- coding: utf-8 -*-
import re
import os.path
import subprocess

import yaml
import pypandoc

import core.information_explorer
import utils.builtin
import interface.base

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
        'origin': '',
        'phone': "",
        'position': "",
        'school': "",
        'tag': [],
        'tracking': [],
        }
    return template


def extract_details(uploaded_details):
    DATE = '(([0-9]{4,4}[\./][0-9]{2,2})|(\\\\u81F3\\\\u4ECA))'
    WORKXP = ur"(\d{4}[/.\\年 ]+\d{1,2}[月]*)[-– —]*(\d{4}[/.\\年 ]+\d{1,2}[月]*|至今)[：: ]*([^\n,，.。（（:]*)"
    STUDIES = u'\s*'+DATE+' - '+DATE+'(?P<expe>[^\(].+?)(?='+DATE+'|$)'

    details = cloudshare_yaml_template()

    details['date'] = 0
    details['id'] = uploaded_details['id']
    details['company'] = uploaded_details['peo'][7]
    details['position'] = uploaded_details['peo'][6]
    details['filename'] = uploaded_details['href']
    details['age']= re.compile('[0-9]*').match(uploaded_details['peo'][2]).group()
    try:
        education = re.compile(STUDIES, re.M).search(uploaded_details['info'][0]).group('expe')
    except:
        education = ''
    details['school'] = education.split('|')[0]
    details['education'] = education.split('|')[-1]
    for expe in uploaded_details['info']:
        work = re.compile(WORKXP).findall(expe)
        for w in work:
            details['experience'].append(list(w))
    return details

class PredatorInterface(interface.base.Interface):

    extension = '.html'
    
    def __init__(self, yamlpath, yamlfile, path):
        super(PredatorInterface, self).__init__(path)
        self.path = path
        self.yamlpath = yamlpath
        self.yamlfile = yamlfile
        self._yamldata = None
        self.yamlstat = None

    @property
    def yamldata(self):
        result = {}
        if self.yamlstat == os.stat(os.path.join(self.yamlpath, self.yamlfile)):
            result = self._yamldata
        else:
            mdpath = os.path.join(self.path, 'CV')
            self._yamldata = {}
            for name, data in utils.builtin.load_yaml(self.yamlpath, self.yamlfile).iteritems():
                if os.path.exists(os.path.join(mdpath, name+self.extension)):
                    self._yamldata[name] = data
            self.yamlstat = os.stat(os.path.join(self.yamlpath, self.yamlfile))
            result = self._yamldata
        return self._yamldata

    def get(self, filename):
        name, extension = os.path.splitext(filename)
        if extension == '.yaml':
            return self._get_yaml(name)
        elif extension == '.md':
            input_file = os.path.join(self.path, name+self.extension)
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
