import time
import os.path
import subprocess

import dulwich.repo
import dulwich.index
import dulwich.objects

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
            >>> interface.modify_file('test_file', b'Modify test')
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
        blob = dulwich.objects.Blob.from_string(stream)
        head_commit = self.repo.get_object(self.repo.refs['HEAD'])
        head_tree = dulwich.objects.Tree()
        head_tree[filename] = (0o100644, blob.id)
        self.commit(head_tree, blob, message, committer)
        self.checkout(head_tree)

    def commit(self, tree, blob, message, committer):
        commit = dulwich.objects.Commit()
        commit.tree = tree.id
        commit.parents = [self.repo.refs['HEAD']]
        commit.author = commit.committer = committer
        commit.commit_time = commit.author_time = int(time.time())
        tz = dulwich.objects.parse_timezone(b'-0200')[0]
        commit.commit_timezone = commit.author_timezone = tz
        commit.encoding = self.encoding
        commit.message = message.encode()

        self.repo.object_store.add_object(blob)
        self.repo.object_store.add_object(tree)
        self.repo.object_store.add_object(commit)
        self.repo.refs['HEAD'] = commit.id

    def checkout(self, tree):
        indexfile = self.repo.index_path()
        tree = self.repo["HEAD"].tree
        dulwich.index.build_index_from_tree(self.repo.path, indexfile,
                                            self.repo.object_store, tree)

    def grep(self, restrings):
        grep_list = []
        keywords = restrings.split()
        if keywords:
            command = ['git', 'grep', '-l', '--all-match']
            for each in keywords:
                command.append('-e')
                command.append(each)
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=self.repo.path)
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
        return info_dict
