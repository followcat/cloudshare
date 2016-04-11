#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.web
from tornado.web import FallbackHandler
from tornado.wsgi import WSGIContainer


import webapp.server
app = webapp.server.app
flask_app = WSGIContainer(app)


from api import TestHandler

class Application(tornado.web.Application):
    def __init__(self,debug=False):
        handlers = [
            (r'/api/test[/]?', TestHandler),
            (r'.*',FallbackHandler,dict(fallback=flask_app)),
            ]

        settings = dict(
            cooike_secret = "you secret key",
            template_path = os.path.join(os.path.dirname(__file__),"webapp/templates"),
            static_path = os.path.join(os.path.dirname(__file__),"webapp/static"),
            debug = debug,
            )
        print(handlers)

        super(Application, self).__init__(handlers,**settings)







if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    AsyncIOMainLoop().install()

    application = Application(debug=True)

    application.listen(4888)

    print('http://127.0.0.1:4888')

    import trollius as asyncio##for python2
    loop = asyncio.get_event_loop()
    loop.set_debug('enabled')
    loop.run_forever()



