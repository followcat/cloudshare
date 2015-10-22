import os.path
import hashlib

import yaml
import flask.ext.login

import webapp.core
import webapp.core.views
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
        >>> RepoAccount.add('admin', 'password')
        >>> RepoAccount.USERS['admin']
        u'5f4dcc3b5aa765d61d8327deb882cf99'
        >>> RepoAccount.add('admin', 'password') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ExistsUser: admin
        >>> RepoAccount.delete('admin')
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
    def add(cls, id, password):
        m = hashlib.md5()
        data = cls.USERS
        uid = unicode(id)
        if uid in data:
            raise webapp.core.exception.ExistsUser(uid)
        m.update(password)
        data[uid] = unicode(m.hexdigest())
        dump_data = yaml.dump(data)
        cls.repo.modify_file(cls.account_filename, dump_data)

    @classmethod
    def delete(cls, id):
        data = cls.USERS
        data.pop(unicode(id))
        dump_data = yaml.dump(data)
        cls.repo.modify_file(cls.account_filename, dump_data)

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


class User(flask.ext.login.UserMixin):

    def __init__(self, id, account_dict):
        self.id = unicode(id)
        if id not in account_dict:
            raise webapp.core.exception.UserNotFoundError()
        self.password = account_dict[self.id]

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
            u'root'
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
