# -*- coding: utf-8 -*-
import re
import os.path
import subprocess

import dulwich.repo

import utils.builtin
import interface.base


class GitInterface(interface.base.Interface):
    author = 'developer'
    encoding = 'UTF-8'

    def __init__(self, path):
        """
            >>> import shutil
            >>> import interface.gitinterface
            >>> repo_name = 'interface/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> interface.repo # doctest: +ELLIPSIS
            <Repo at ...
            >>> shutil.rmtree(repo_name)
        """
        super(GitInterface, self).__init__(path)
        try:
            self.repo = dulwich.repo.Repo.init(path, mkdir=True)
        except OSError:
            self.repo = dulwich.repo.Repo(path)

    def exists(self, filename):
        result = True
        data = self.repo.get_named_file(os.path.join('../', filename))
        if data is None:
            result = False
        return result

    def get(self, filename):
        """
            >>> import shutil
            >>> import interface.gitinterface
            >>> repo_name = 'interface/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> commit_id = interface.add('test_file', 'text',
            ... 'Test commit', 'test<test@test.com>')
            >>> interface.get('test_file')
            'text'
        """
        data = None
        result = self.repo.get_named_file(os.path.join('../', filename))
        if result is not None:
            data = result.read()
        return data

    def add(self, filename, filedata, message=None, committer=None):
        """
            >>> import shutil
            >>> import interface.gitinterface
            >>> repo_name = 'interface/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> commit_id = interface.add('test_file', 'text',
            ... 'Test commit', 'test<test@test.com>')
            >>> commit_id == interface.repo.head()
            True
            >>> shutil.rmtree(repo_name)
        """
        full_path = os.path.join(self.path, filename)
        path, name = os.path.split(full_path)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(full_path, 'w') as fp:
            fp.write(filedata)
        self.repo.stage(filename)
        if committer is None:
            committer = self.author
        if message is None:
            message = "Add file: " + filename + ".\n"
        commit_id = self.repo.do_commit(bytes(message), committer=bytes(committer))
        return commit_id

    def add_files(self, filenames, message=None, committer=None):
        """
            >>> import shutil
            >>> import interface.gitinterface
            >>> repo_name = 'interface/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> with open('interface/test_repo/test_file', 'w') as file:
            ...     file.write('test')
            >>> commit_id = interface.add_files(['test_file'],
            ... 'Test commit', 'test<test@test.com>')
            >>> commit_id == interface.repo.head()
            True
            >>> shutil.rmtree(repo_name)
        """
        self.repo.stage(filenames)
        if committer is None:
            committer = self.author
        if message is None:
            message = ""
            for each in filenames:
                message += "Add file: " + each + ".\n"
        commit_id = self.repo.do_commit(bytes(message), committer=bytes(committer))
        return commit_id

    def modify(self, filename, stream, message=None, committer=None):
        """
            >>> import shutil
            >>> import interface.gitinterface
            >>> repo_name = 'interface/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> commit_id = interface.add('test_file', 'test',
            ... b'Test commit', b'test<test@test.com>')
            >>> commit_id = interface.modify('test_file', b'Modify test')
            >>> with open('interface/test_repo/test_file') as file:
            ...     data = file.read()
            >>> data
            'Modify test'
            >>> shutil.rmtree(repo_name)
        """
        if not self.exists(filename):
            raise Exception('Not exists file:', filename)
        if message is None:
            message = "Change %s." % filename
        if committer is None:
            committer = self.author
        with open(os.path.join(self.repo.path, filename), 'w') as f:
            f.write(stream)
        self.repo.stage([bytes(filename)])
        commit_id = self.repo.do_commit(message, committer=bytes(committer))
        return commit_id

    def grep(self, restrings, path):
        grep_list = []
        keywords = restrings.split()
        if keywords:
            command = ['git', 'grep', '-l', '--all-match']
            for each in keywords:
                command.append('-e')
                command.append(each.encode('utf-8'))
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=os.path.join(self.repo.path, path))
            returncode = p.communicate()[0]
            for each in returncode.split('\n'):
                if each:
                    grep_list.append(each)
        return grep_list

    def lsfiles(self, prefix, filtefile):
        lsfiles = []
        selected = os.path.join(prefix, filtefile)
        command = ['git', 'ls-files', '--with-tree=HEAD', selected]
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             cwd=self.repo.path)
        returncode = p.communicate()[0]
        for each in returncode.split('\n'):
            if each:
                lsfiles.append(each)
        if 'not found' in lsfiles[0]:
            lsfiles = []
        return lsfiles

    def grep_yaml(self, restrings, path):
        """
            >>> import yaml
            >>> import shutil
            >>> import interface.gitinterface
            >>> repo_name = 'interface/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> data = {'name': u'中文名字'}
            >>> commit_id = interface.add('test_file.yaml', yaml.safe_dump(data),
            ... b'Test commit', b'test<test@test.com>')
            >>> interface.grep_yaml('name', '.')
            ['test_file.yaml']
            >>> shutil.rmtree(repo_name)
        """
        grep_list = []
        keywords = restrings.split()
        if keywords:
            command = ['git', 'grep', '-l', '--all-match']
            for each in keywords:
                command.append('-e')
                unicode_str = re.sub(r'\\u[a-z0-9]{4}',
                                     lambda a: a.group().upper(),
                                     each.__repr__()[2:-1]).replace('\\U',
                                                                    '\\\\\\u')
                command.append(unicode_str)
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=os.path.join(self.repo.path, path))
            returncode = p.communicate()[0]
            for each in returncode.split('\n'):
                if each:
                    grep_list.append(each)
        return grep_list

    def get_file_create_info(self, filename):
        """
            >>> import shutil
            >>> import interface.gitinterface
            >>> repo_name = 'interface/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> commit_id = interface.add('test_file', 'test',
            ... b'Test commit', b'test<test@test.com>')
            >>> info = interface.get_file_create_info('test_file')
            >>> info['author']
            'test<test@test.com>'
            >>> shutil.rmtree(repo_name)
        """
        info = {}
        w = self.repo.get_walker(paths=[filename], reverse=True)
        try:
            commit = next(iter(w)).commit
        except StopIteration:
            pass
        else:
            info['author'] = commit.author
            info['time'] = utils.builtin.strftime(commit.author_time)
        return info

    def history(self, author, max_commits=None, skip=0):
        cmd = ['git', 'log', '--format=%H']
        cmd.append('--author=%s' % author)
        if skip:
            cmd.append('--skip=%d' % skip)
        if max_commits:
            cmd.append('--max-count=%d' % max_commits)
        try:
            output = utils.builtin.check_output(cmd, cwd=os.path.abspath(self.repo.path))
        except subprocess.CalledProcessError:
            return []
        sha1_sums = output.strip().split(b'\n')
        return [self.commit_info(self.repo[sha1]) for sha1 in sha1_sums]

    def commit_info(self, commit):
        info_dict = {}
        info_dict['author'] = commit.author
        info_dict['message'] = commit.message
        info_dict['time'] = utils.builtin.strftime(commit.author_time)
        info_dict['id'] = commit.id
        info_dict['filenames'] = dict()
        for name in re.findall(ur' ([a-z0-9]{8}).[yaml|md]', commit.message):
            info_dict['filenames'][name] = None
        return info_dict
