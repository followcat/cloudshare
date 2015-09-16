import time
import logging
import os.path

import dulwich.repo
import dulwich.index
import dulwich.objects


class GitInterface(object):
    author = b'user<user@git.com>'
    encoding = b"UTF-8"

    def __init__(self, path):
        """
            >>> import shutil
            >>> import gitinterface
            >>> repo_name = 'test_repo'
            >>> interface = gitinterface.GitInterface(repo_name)
            >>> interface.repo # doctest: +ELLIPSIS
            <Repo at ...
            >>> shutil.rmtree(repo_name)
        """
        try:
            self.repo = dulwich.repo.Repo.init(path, mkdir=True)
        except OSError:
            self.repo = dulwich.repo.Repo(path)

    def add_file(self, path, filename, message=None, committer=None):
        """
            >>> import shutil
            >>> import gitinterface
            >>> repo_name = 'test_repo'
            >>> interface = gitinterface.GitInterface(repo_name)
            >>> path = interface.repo.path
            >>> with open('test_repo/test_file', 'w') as file:
            ...     file.write('test')
            >>> commit_id = interface.add_file(path, 'test_file',
            ... b'Test commit', b'test<test@test.com>')
            >>> commit_id == interface.repo.head()
            True
            >>> shutil.rmtree(repo_name)
        """
        self.repo.stage([filename])
        if committer is None:
            committer = self.author
        if message is None:
            message = "Add file: " + filename + "."
        commit_id = self.repo.do_commit(message, committer=committer)
        return commit_id

    def modify_file(self, filename, stream):
        """
            >>> import shutil
            >>> import gitinterface
            >>> repo_name = 'test_repo'
            >>> interface = gitinterface.GitInterface(repo_name)
            >>> path = interface.repo.path
            >>> with open('test_repo/test_file', 'w') as file:
            ...     file.write('test')
            >>> commit_id = interface.add_file(path, 'test_file',
            ... b'Test commit', b'test<test@test.com>')
            >>> interface.modify_file('test_file', b'Modify test')
            >>> with open('test_repo/test_file') as file:
            ...     data = file.read()
            >>> data
            'Modify test'
            >>> shutil.rmtree(repo_name)
        """
        blob = dulwich.objects.Blob.from_string(stream)
        head_commit = self.repo.get_object(self.repo.refs['HEAD'])
        head_tree = dulwich.objects.Tree()
        head_tree[filename] = (0o100644, blob.id)
        self.commit(head_tree, blob, "Change %s" % filename)
        self.checkout(head_tree)

    def commit(self, tree, blob, message):
        commit = dulwich.objects.Commit()
        commit.tree = tree.id
        author = self.author
        commit.parents = [self.repo.refs['HEAD']]
        commit.author = commit.committer = author
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
