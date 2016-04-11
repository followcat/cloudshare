#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals



import unittest
import requests

class Test(unittest.TestCase):
    def test_api_init(self):
        jsond = requests.get('http://127.0.0.1:4888/api/test').json()
        self.assertEqual(jsond,{'message':'api ready'})






if __name__ == '__main__':
    unittest.main()
