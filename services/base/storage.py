import os
import yaml

import utils.issue
import utils._yaml
import core.outputstorage
import services.base.service


class BaseStorage(services.base.service.Service):

    commitinfo = 'BaseData'

    def __init__(self, path, name=None, iotype=None):
        self.path = path
        super(BaseStorage, self).__init__(self.path, name, iotype)
        self.unique_checker = None
        self.info = ""
        self._nums = 0

    def exists(self, id):
        """
            >>> import services.base.storage
            >>> DIR = 'repo/CV'
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DIR)
            >>> assert SVC_BSSTO.exists('blr6dter')
        """
        return id in self.ids

    def unique(self, id):
        """
            >>> import shutil
            >>> import core.basedata
            >>> import services.base.storage
            >>> import extractor.information_explorer
            >>> repo_name = 'core/test_repo'
            >>> test_path = 'core/test_output'
            >>> f1 = open('core/test/cv_1.doc', 'r')
            >>> fp1 = core.docprocessor.Processor(f1, 'cv_1.doc', test_path)
            >>> yamlinfo = extractor.information_explorer.catch_cvinfo(
            ...     stream=fp1.markdown_stream.decode('utf8'), filename=fp1.base.base)
            >>> cv1 = core.basedata.DataObject(data=fp1.markdown_stream, metadata=yamlinfo)
            >>> svc_cv = services.base.storage.BaseStorage(repo_name)
            >>> fp1.result
            True
            >>> svc_cv.unique(cv1.name)
            True
            >>> svc_cv.add(cv1)
            True
            >>> svc_cv.unique(cv1.name)
            False
            >>> svc_cv.add(cv1)
            False
            >>> f1.close()
            >>> shutil.rmtree(repo_name)
            >>> shutil.rmtree(test_path)
        """
        return not self.exists(id)

    def modify(self, filename, stream, message=None, committer=None, do_commit=True):
        self.interface.modify(filename, stream, message, committer, do_commit=do_commit)
        return True

    def add(self, bsobj, committer=None, unique=True, yamlfile=True, mdfile=True, do_commit=True):
        if unique is True and self.unique(bsobj.name) is False:
            self.info = "Exists File"
            return False
        name = core.outputstorage.ConvertName(bsobj.name)
        if mdfile is True:
            message = "Add %s: %s data." % (self.commitinfo, name)
            self.interface.add(name.md, bsobj.data, message=message,
                               committer=committer, do_commit=do_commit)
        if yamlfile is True:
            if committer is not None:
                bsobj.metadata['committer'] = committer
            message = "Add %s: %s metadata." % (self.commitinfo, name)
            self.interface.add(name.yaml, yaml.safe_dump(bsobj.metadata, allow_unicode=True),
                               message=message, committer=committer, do_commit=do_commit)
        self._nums += 1
        return True

    def getyaml(self, id):
        """
        Expects an IOError exception if file not found.
            >>> import services.base.storage
            >>> DIR = 'services/test_repo'
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DIR)
            >>> SVC_BSSTO.getyaml('CV') # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            IOError...
        """
        name = core.outputstorage.ConvertName(id).yaml
        yaml_str = self.interface.get(name)
        return yaml.load(yaml_str, Loader=utils._yaml.SafeLoader)

    def getmd(self, name):
        """
            >>> import services.base.storage
            >>> DIR = 'repo/CV'
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DIR)
            >>> assert SVC_BSSTO.getmd('blr6dter.yaml')
        """
        result = unicode()
        md = core.outputstorage.ConvertName(name).md
        markdown = self.interface.get(md)
        if markdown is None:
            result = None
        elif isinstance(markdown, unicode):
            result = markdown
        else:
            result = unicode(str(markdown), 'utf-8')
        return result

    def search(self, keyword):
        results = set()
        allfile = self.interface.grep(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def search_yaml(self, keyword):
        results = set()
        allfile = self.interface.grep_yaml(keyword)
        for filename in allfile:
            id = core.outputstorage.ConvertName(filename).base
            results.add(id)
        return results

    def names(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).md

    def yamls(self):
        for id in self.ids:
            yield core.outputstorage.ConvertName(id).yaml

    def datas(self):
        for id in self.ids:
            name = core.outputstorage.ConvertName(id).md
            text = self.getmd(id)
            yield name, text

    def history(self, author=None, entries=10, skip=0):
        return self.interface.history(author=author, max_commits=entries, skip=skip)

    @property
    def ids(self):
        """
            >>> import services.base.storage
            >>> DIR = 'repo/CV'
            >>> SVC_BSSTO = services.base.storage.BaseStorage(DIR)
            >>> assert SVC_BSSTO.interface.lsfiles('.', 'blr6dter.yaml')
        """
        return [os.path.splitext(f)[0]
                for f in self.interface.lsfiles('.', '*.yaml')]

    @property
    def NUMS(self):
        if not self._nums:
            self._nums = len(self.ids)
        return self._nums

