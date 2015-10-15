import flask
import flask.ext.login

import webapp.core.exception


class User(flask.ext.login.UserMixin):
    '''Simple User class'''
    USERS = {
        # username: password
        'john': 'love mary',
        'mary': 'love peter'
    }

    def __init__(self, id):
        if id not in self.USERS:
            raise webapp.core.exception.UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
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
        # validate username and password
        user = User.get(flask.request.form['username'])
        if (user and user.password == flask.request.form['password']):
            flask.ext.login.login_user(user)
        else:
            flask.flash('Username or password incorrect')

        return flask.redirect(flask.url_for('index'))


class Logout(flask.views.MethodView):
    def get(self):
        flask.ext.login.logout_user()
        return flask.redirect(flask.url_for('index'))
