import flask.ext.login

import services.exception


class User(flask.ext.login.UserMixin):

    def __init__(self, id, account_ser):
        self.id = id
        self.account_ser = account_ser
        if id not in account_ser.USERS:
            raise services.exception.UserNotFoundError()
        self.password = account_ser.USERS[unicode(id)]

    def changepassword(self, password):
        self.account_ser.modify(self.id, password)

    @classmethod
    def get(self_class, id, account_ser):
        """
            >>> import shutil
            >>> import services.account
            >>> import webapp.views.account
            >>> import interface.gitinterface
            >>> repo_name = 'webapp/views/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> account_ser = services.account.Account(interface)
            >>> user = webapp.views.account.User.get('root', account_ser)
            >>> user.id
            'root'
            >>> user.password
            u'5f4dcc3b5aa765d61d8327deb882cf99'
            >>> type(webapp.views.account.User.get('None', account_ser))
            <type 'NoneType'>
            >>> shutil.rmtree(repo_name)
        """
        try:
            return self_class(id, account_ser)
        except services.exception.UserNotFoundError:
            return None
