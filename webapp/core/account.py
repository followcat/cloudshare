import os.path
import hashlib

import yaml
import flask.ext.login

import webapp.core
import utils.classproperty
import webapp.core.exception


class RepoAccount(object):
    """
        >>> import shutil
        >>> import webapp.core.account
        >>> import utils.classproperty
        >>> import repointerface.gitinterface
        >>> repo_name = 'webapp/core/test_repo'
        >>> interface = repointerface.gitinterface.GitInterface(repo_name)
        >>> RepoAccount = webapp.core.account.RepoAccount
        >>> save_repo = RepoAccount.repo
        >>> RepoAccount.repo = interface
        >>> RepoAccount.USERS
        {u'root': u'5f4dcc3b5aa765d61d8327deb882cf99'}
        >>> RepoAccount.add('root', 'admin', 'password')
        True
        >>> RepoAccount.USERS['admin']
        u'5f4dcc3b5aa765d61d8327deb882cf99'
        >>> RepoAccount.get_user_list()
        [u'admin']
        >>> RepoAccount.add('root', 'admin', 'password') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ExistsUser: admin
        >>> RepoAccount.delete('root', 'admin')
        True
        >>> RepoAccount.USERS
        {u'root': u'5f4dcc3b5aa765d61d8327deb882cf99'}
        >>> RepoAccount.repo = save_repo
        >>> shutil.rmtree(repo_name)
    """
    default_root_name = u'root'
    default_root_password = 'password'
    account_filename = 'account.yaml'

    repo = webapp.core.repo

    @classmethod
    def create(cls):
        m = hashlib.md5()
        m.update(cls.default_root_password)
        empty_dict = {cls.default_root_name: unicode(m.hexdigest())}
        with open(os.path.join(cls.repo.repo.path, cls.account_filename),
                  'w') as f:
            f.write(yaml.dump(empty_dict))
        cls.repo.add_files(cls.account_filename, "Add account file.")

    @classmethod
    def unicodemd5(cls, password):
        m = hashlib.md5()
        m.update(password)
        return unicode(m.hexdigest())

    @classmethod
    def add(cls, mender, id, password):
        if mender != u'root':
            return False
        data = cls.USERS
        uid = unicode(id)
        upw = cls.unicodemd5(password)
        if uid in data:
            raise webapp.core.exception.ExistsUser(uid)
        data[uid] = upw
        dump_data = yaml.dump(data)
        cls.repo.modify_file(cls.account_filename, dump_data)
        return True

    @classmethod
    def modify(cls, id, password):
        data = cls.USERS
        uid = unicode(id)
        upw = cls.unicodemd5(password)
        data[uid] = upw
        dump_data = yaml.dump(data)
        cls.repo.modify_file(cls.account_filename, dump_data)

    @classmethod
    def delete(cls, mender, id):
        if mender != u'root':
            return False
        data = cls.USERS
        data.pop(unicode(id))
        dump_data = yaml.dump(data)
        cls.repo.modify_file(cls.account_filename, dump_data)
        return True

    @utils.classproperty.ClassProperty
    def USERS(cls):
        account_file = cls.repo.repo.get_named_file(
            os.path.join('..', cls.account_filename))
        if account_file is None:
            cls.create()
            account_file = cls.repo.repo.get_named_file(
                os.path.join('..', cls.account_filename))
        data = yaml.load(account_file.read())
        account_file.close()
        return data

    @classmethod
    def get_user_list(cls):
        account_list = cls.USERS.keys()
        account_list.remove(cls.default_root_name)
        user_list = account_list
        return user_list


class User(flask.ext.login.UserMixin):

    def __init__(self, id, account_dict):
        self.id = id
        if id not in account_dict:
            raise webapp.core.exception.UserNotFoundError()
        self.password = account_dict[unicode(id)]

    def changepassword(self, password):
        RepoAccount.modify(self.id, password)

    @classmethod
    def get(self_class, id, account_dict=None):
        """
            >>> import shutil
            >>> import webapp.core.account
            >>> import repointerface.gitinterface
            >>> repo_name = 'webapp/core/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> RepoAccount = webapp.core.account.RepoAccount
            >>> save_repo = RepoAccount.repo
            >>> RepoAccount.repo = interface
            >>> user = webapp.core.account.User.get('root')
            >>> user.id
            'root'
            >>> user.password
            u'5f4dcc3b5aa765d61d8327deb882cf99'
            >>> type(webapp.core.account.User.get('None'))
            <type 'NoneType'>
            >>> RepoAccount.repo = save_repo
            >>> shutil.rmtree(repo_name)
        """
        if account_dict is None:
            account_dict = RepoAccount.USERS
        try:
            return self_class(id, account_dict)
        except webapp.core.exception.UserNotFoundError:
            return None


def init_login(app):
    login_manager = flask.ext.login.LoginManager()
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.get(id)
