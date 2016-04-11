#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals


from tornado.web import RequestHandler
from tornado import gen



class TestHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        info = {'message':'api ready'}
        self.write(info)














#if __name__ == '__main__':
