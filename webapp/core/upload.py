import codecs
import os.path

import core.exception
import core.outputstorage
import core.converterutils


class UploadObject(object):

    def __init__(self, filename, fileobject, path):
        """
            >>> import os
            >>> import shutil
            >>> import os.path
            >>> import webapp.core.upload
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> obj = open(os.path.join(root, name))
            >>> test_path = "webapp/core/test_output"
            >>> os.makedirs(test_path)
            >>> up = webapp.core.upload.UploadObject(name, obj, test_path)
            >>> up.result
            True
            >>> up.remove()
            >>> shutil.rmtree(test_path)
        """
        self.result = False
        self.tmp_path = path
        self.convertname = core.outputstorage.ConvertName(
            filename.encode('utf-8'))
        self.storage = core.converterutils.FileProcesser(fileobject,
                                                         self.convertname,
                                                         self.tmp_path)
        self.result = self.storage.result
        if self.result is False:
            self.information = 'Can not Convert'
        else:
            self.information = 'Sucess'

    def preview_markdown(self):
        output = core.converterutils.md_to_html(self.storage.markdown_stream)
        return output

    def confirm(self, repo, committer=None):
        """
            >>> import shutil
            >>> import os.path
            >>> import webapp.core.upload
            >>> import repointerface.gitinterface
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> repo_name = 'webapp/core/test_repo'
            >>> test_path = "webapp/core/test_output"
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> up = webapp.core.upload.UploadObject(name, obj, test_path)
            >>> up.confirm(interface)
            True
            >>> up.confirm(interface)
            False
            >>> up.information
            'Exists File'
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        result = False
        try:
            self.storage.storage(repo, committer=committer)
            result = True
        except core.exception.DuplicateException:
            self.information = 'Exists File'
        return result

    def confirm_md(self, repo, committer=None):
        """
            >>> import shutil
            >>> import os.path
            >>> import webapp.core.upload
            >>> import repointerface.gitinterface
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> repo_name = 'webapp/core/test_repo'
            >>> test_path = "webapp/core/test_output"
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> obj = open(os.path.join(root, name))
            >>> os.makedirs(test_path)
            >>> up = webapp.core.upload.UploadObject(name, obj, test_path)
            >>> up.confirm(interface)
            True
            >>> up.confirm_md(interface)
            True
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        self.storage.storage_md(repo, committer=committer)
        return True

    def remove(self):
        """
            >>> import os
            >>> import shutil
            >>> import os.path
            >>> import webapp.core.upload
            >>> root = "core/test"
            >>> name = "cv_1.doc"
            >>> obj = open(os.path.join(root, name))
            >>> test_path = "webapp/core/test_output"
            >>> os.makedirs(test_path)
            >>> up = webapp.core.upload.UploadObject(name, obj, test_path)
            >>> fn = os.path.join(up.storage.markdown_path, up.storage.name.md)
            >>> os.path.exists(fn)
            True
            >>> up.remove()
            >>> os.path.exists(fn)
            False
            >>> shutil.rmtree(test_path)
        """
        self.storage.deleteconvert()
