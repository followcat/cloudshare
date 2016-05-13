# -*- coding: utf-8 -*-
import re
import os.path
import subprocess

import dulwich.repo

import utils.builtin


class GitInterface(object):
    author = b'developer'
    encoding = b'UTF-8'

    def __init__(self, path):
        """
            >>> import shutil
            >>> import repointerface.gitinterface
            >>> repo_name = 'repointerface/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> interface.repo # doctest: +ELLIPSIS
            <Repo at ...
            >>> shutil.rmtree(repo_name)
        """
        try:
            self.repo = dulwich.repo.Repo.init(path, mkdir=True)
        except OSError:
            self.repo = dulwich.repo.Repo(path)

    def add_files(self, filenames, message=None, committer=None):
        """
            >>> import shutil
            >>> import repointerface.gitinterface
            >>> repo_name = 'repointerface/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> path = interface.repo.path
            >>> with open('repointerface/test_repo/test_file', 'w') as file:
            ...     file.write('test')
            >>> commit_id = interface.add_files(['test_file'],
            ... b'Test commit', b'test<test@test.com>')
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
        commit_id = self.repo.do_commit(message, committer=committer)
        return commit_id

    def modify_file(self, filename, stream, message=None, committer=None):
        """
            >>> import shutil
            >>> import repointerface.gitinterface
            >>> repo_name = 'repointerface/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> path = interface.repo.path
            >>> with open('repointerface/test_repo/test_file', 'w') as file:
            ...     file.write('test')
            >>> commit_id = interface.add_files(['test_file'],
            ... b'Test commit', b'test<test@test.com>')
            >>> commit_id = interface.modify_file('test_file', b'Modify test')
            >>> with open('repointerface/test_repo/test_file') as file:
            ...     data = file.read()
            >>> data
            'Modify test'
            >>> shutil.rmtree(repo_name)
        """
        if message is None:
            message = "Change %s." % filename
        if committer is None:
            committer = self.author
        with open(os.path.join(self.repo.path, filename), 'w') as f:
            f.write(stream)
        self.repo.stage([filename])
        commit_id = self.repo.do_commit(message, committer=committer)
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

    def grep_yaml(self, restrings, path):
        """
            >>> import yaml
            >>> import shutil
            >>> import repointerface.gitinterface
            >>> repo_name = 'repointerface/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> path = interface.repo.path
            >>> data = {'name': u'中文名字'}
            >>> with open('repointerface/test_repo/test_file.yaml', 'w') as file:
            ...     file.write(yaml.dump(data))
            >>> commit_id = interface.add_files(['test_file.yaml'],
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
            >>> import repointerface.gitinterface
            >>> repo_name = 'repointerface/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> path = interface.repo.path
            >>> with open('repointerface/test_repo/test_file', 'w') as file:
            ...     file.write('test')
            >>> commit_id = interface.add_files(['test_file'],
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
