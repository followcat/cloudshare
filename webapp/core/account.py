import os.path

import yaml
import flask.ext.login

import utils.builtin
import webapp.core.exception


class RepoAccount(object):
    """
        >>> import shutil
        >>> import webapp.core.account
        >>> import repointerface.gitinterface
        >>> repo_name = 'webapp/core/test_repo'
        >>> interface = repointerface.gitinterface.GitInterface(repo_name)
        >>> repoaccount = webapp.core.account.RepoAccount(interface)
        >>> repoaccount.USERS
        {u'root': u'5f4dcc3b5aa765d61d8327deb882cf99'}
        >>> repoaccount.add('root', 'admin', 'password')
        True
        >>> repoaccount.USERS['admin']
        u'5f4dcc3b5aa765d61d8327deb882cf99'
        >>> repoaccount.get_user_list()
        [u'admin']
        >>> repoaccount.add('root', 'admin', 'password') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ExistsUser: admin
        >>> repoaccount.delete('root', 'admin')
        True
        >>> repoaccount.USERS
        {u'root': u'5f4dcc3b5aa765d61d8327deb882cf99'}
        >>> shutil.rmtree(repo_name)
    """
    default_root_name = u'root'
    default_root_password = 'password'
    account_filename = 'account.yaml'

    def __init__(self, repo):
        self.repo = repo

    def create(self):
        upassword = utils.builtin.md5(self.default_root_password)
        empty_dict = {self.default_root_name: upassword}
        with open(os.path.join(self.repo.repo.path, self.account_filename),
                  'w') as f:
            f.write(yaml.dump(empty_dict))
        self.repo.add_files(self.account_filename, "Add account file.")

    def add(self, mender, id, password):
        if mender != u'root':
            return False
        data = self.USERS
        uid = unicode(id)
        upw = utils.builtin.md5(password)
        if uid in data:
            raise webapp.core.exception.ExistsUser(uid)
        data[uid] = upw
        dump_data = yaml.dump(data)
        self.repo.modify_file(self.account_filename, dump_data)
        return True

    def modify(self, id, password):
        data = self.USERS
        uid = unicode(id)
        upw = utils.builtin.md5(password)
        data[uid] = upw
        dump_data = yaml.dump(data)
        self.repo.modify_file(self.account_filename, dump_data)

    def delete(self, mender, id):
        if mender != u'root':
            return False
        data = self.USERS
        data.pop(unicode(id))
        dump_data = yaml.dump(data)
        self.repo.modify_file(self.account_filename, dump_data)
        return True

    @property
    def USERS(self):
        account_file = self.repo.repo.get_named_file(
            os.path.join('..', self.account_filename))
        if account_file is None:
            self.create()
            account_file = self.repo.repo.get_named_file(
                os.path.join('..', self.account_filename))
        data = yaml.load(account_file.read())
        account_file.close()
        return data

    def get_user_list(self):
        account_list = self.USERS.keys()
        account_list.remove(self.default_root_name)
        user_list = account_list
        return user_list


class User(flask.ext.login.UserMixin):

    def __init__(self, id, repoaccount):
        self.id = id
        self.repoaccount = repoaccount
        if id not in repoaccount.USERS:
            raise webapp.core.exception.UserNotFoundError()
        self.password = repoaccount.USERS[unicode(id)]

    def changepassword(self, password):
        self.repoaccount.modify(self.id, password)

    @classmethod
    def get(self_class, id, repoaccount):
        """
            >>> import shutil
            >>> import webapp.core.account
            >>> import repointerface.gitinterface
            >>> repo_name = 'webapp/core/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> repoaccount = webapp.core.account.RepoAccount(interface)
            >>> user = webapp.core.account.User.get('root', repoaccount)
            >>> user.id
            'root'
            >>> user.password
            u'5f4dcc3b5aa765d61d8327deb882cf99'
            >>> type(webapp.core.account.User.get('None', repoaccount))
            <type 'NoneType'>
            >>> shutil.rmtree(repo_name)
        """
        try:
            return self_class(id, repoaccount)
        except webapp.core.exception.UserNotFoundError:
            return None


def init_login(app):
    login_manager = flask.ext.login.LoginManager()
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.get(id, app.config['REPO_ACCOUNT'])
