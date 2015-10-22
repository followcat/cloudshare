import os
import codecs

import yaml
import pypandoc

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
        core.outputstorage.save_stream(self.tmp_path, self.convertname,
                                       fileobject.read())
        self.storage = core.converterutils.FileProcesser(self.tmp_path,
                                                         self.convertname,
                                                         self.tmp_path)
        self.result = self.storage.convert()
        if self.result is False:
            self.information = 'Can not Convert'
        else:
            self.information = 'Sucess'

    def preview_yaml(self):
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
            >>> yaml_data = up.preview_yaml()
            >>> yaml_data['filename']
            u'cv_1'
            >>> up.remove()
            >>> shutil.rmtree(test_path)
        """
        filename = os.path.join(self.storage.yaml_path, self.storage.name.yaml)
        with open(filename, 'r') as yf:
            stream = yf.read()
        yaml_data = yaml.load(stream)
        return yaml_data

    def preview_markdown(self):
        filename = os.path.join(self.storage.markdown_path,
                                self.storage.name.md)
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
        output = pypandoc.convert(data, 'html', format='markdown')
        return output

    def confirm(self, repo):
        """
            >>> import glob
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
            self.storage.storage(repo)
            result = True
        except core.exception.DuplicateException:
            self.information = 'Exists File'
        return result

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
