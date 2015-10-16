import os.path
import hashlib

import yaml
import flask
import flask.views
import flask.ext.login

import webapp.core.exception
import repointerface.gitinterface


class RepoAccount(object):
    """
        >>> import shutil
        >>> import repointerface.gitinterface
        >>> import webapp.core.account
        >>> repo_name = 'webapp/core/test_repo'
        >>> interface = repointerface.gitinterface.GitInterface(repo_name)
        >>> account = webapp.core.account.RepoAccount(interface)
        >>> account.get_account_date()
        {u'root': u'63a9f0ea7bb98050796b649e85481845'}
        >>> account.USERS
        {u'root': u'63a9f0ea7bb98050796b649e85481845'}
        >>> account.add('admin', 'password')
        >>> account.USERS['admin']
        u'5f4dcc3b5aa765d61d8327deb882cf99'
        >>> account.add('admin', 'password') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ExistsUser: admin
        >>> account.delete('admin')
        >>> account.USERS
        {u'root': u'63a9f0ea7bb98050796b649e85481845'}
        >>> shutil.rmtree(repo_name)
    """
    default_root_name = u'root'
    default_root_password = 'root'
    account_filename = 'account.yaml'

    def __init__(self, repo):
        self.repo = repo
        account_file = repo.repo.get_named_file(
            os.path.join('..', self.account_filename))
        if account_file is None:
            self.create()

    def create(self):
        m = hashlib.md5()
        m.update(self.default_root_password)
        empty_dict = {self.default_root_name: unicode(m.hexdigest())}
        with open(os.path.join(self.repo.repo.path, self.account_filename),
                  'w') as f:
            f.write(yaml.dump(empty_dict))
        self.repo.add_files(self.account_filename, "Add account file.")

    def get_account_date(self):
        account_file = self.repo.repo.get_named_file(
            os.path.join('..', self.account_filename))
        data = yaml.load(account_file.read())
        account_file.close()
        return data

    def add(self, id, password):
        m = hashlib.md5()
        data = self.get_account_date()
        uid = unicode(id)
        if uid in data:
            raise webapp.core.exception.ExistsUser(uid)
        m.update(password)
        data[uid] = unicode(m.hexdigest())
        dump_data = yaml.dump(data)
        self.repo.modify_file(self.account_filename, dump_data)

    def delete(self, id):
        data = self.get_account_date()
        data.pop(unicode(id))
        dump_data = yaml.dump(data)
        self.repo.modify_file(self.account_filename, dump_data)

    @property
    def USERS(self):
        return self.get_account_date()

repo = repointerface.gitinterface.GitInterface("repo")
accounts = RepoAccount(repo)


class User(flask.ext.login.UserMixin):
    USERS = accounts.USERS

    def __init__(self, id):
        self.id = unicode(id)
        if id not in self.USERS:
            raise webapp.core.exception.UserNotFoundError()
        self.password = self.USERS[self.id]

    @classmethod
    def get(self_class, id):
        """
            >>> import shutil
            >>> import webapp.core.account
            >>> import repointerface.gitinterface
            >>> repo_name = 'webapp/core/test_repo'
            >>> interface = repointerface.gitinterface.GitInterface(repo_name)
            >>> account = webapp.core.account.RepoAccount(interface)
            >>> webapp.core.account.User.USERS = account.USERS
            >>> user = webapp.core.account.User('root')
            >>> user.id
            u'root'
            >>> user.password
            u'63a9f0ea7bb98050796b649e85481845'
            >>> type(webapp.core.account.User.get('None'))
            <type 'NoneType'>
            >>> webapp.core.account.User.USERS = webapp.core.account.accounts
            >>> shutil.rmtree(repo_name)
        """
        try:
            return self_class(id)
        except webapp.core.exception.UserNotFoundError:
            return None


def init_login(app):
    login_manager = flask.ext.login.LoginManager()
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.get(id)


class Index(flask.views.MethodView):

    def get(self):
        return (
            '''
                <h1>Hello {1}</h1>
                <p style="color: #f00;">{0}</p>
                <p>{2}</p>
            '''.format(
                # flash message
                ', '.join([str(m) for m in flask.get_flashed_messages()]),
                flask.ext.login.current_user.get_id() or 'Guest',
                ('<a href="/logout">Logout</a>' if flask.ext.login.current_user.is_authenticated
                    else '<a href="/login">Login</a>')
            )
        )


class Login(flask.views.MethodView):

    def get(self):
        return '''
            <form action="/login/check" method="post">
                <p>Username: <input name="username" type="text"></p>
                <p>Password: <input name="password" type="password"></p>
                <input type="submit">
            </form>
        '''


class LoginCheck(flask.views.MethodView):

    def post(self):
        user = User.get(flask.request.form['username'])
        password = flask.request.form['password']
        m = hashlib.md5()
        m.update(password)
        upassword = unicode(m.hexdigest())
        if (user and user.password == upassword):
            flask.ext.login.login_user(user)
        else:
            flask.flash('Username or password incorrect.')

        return flask.redirect(flask.url_for('index'))


class Logout(flask.views.MethodView):

    def get(self):
        flask.ext.login.logout_user()
        return flask.redirect(flask.url_for('index'))
