#!/usr/bin/python
# (c) George Shuklin, 2015
#
# This library is free software; you can redistribute it and/or
# Modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# Version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# But WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from __future__ import print_function
import sys
import time
import Queue
import decorator
import functools
import multiprocessing

from utils.timeout.exception import *


def _kill_process(process):
    if process.is_alive():
        process.terminate()


def process_exec(func, delay, queue, kill=True):
    process = multiprocessing.Process(target=func)
    process.daemon = True
    process.start()
    try:
        res = queue.get(timeout=delay)
    except Queue.Empty:
        if not kill:
            raise NotKillExecTimeout(
                "Timeout and no kill attempt")
        _kill_process(process)
        raise KilledExecTimeout(
                "Timeout and process was killed")
    return res

def parse_return(res):
    if res[0] == 'success':
        return res[1]
    if res[0] == 'exception':
        raise res[1][0], res[1][1], res[1][2]


def process_timeout_call(func, delay, kill=True, args=None, kwargs=None):
    queue = multiprocessing.Queue()

    def inner_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            queue.put(('success', result))
        except:
            e = sys.exc_info()
            queue.put(('exception', e[0:1]))

    if args is None:
        if kwargs is None:
            inner_worker = functools.partial(inner_func)
        else:
            inner_worker = functools.partial(inner_func, **kwargs)
    else:
        if kwargs is None:
            inner_worker = functools.partial(inner_func, *args)
        else:
            inner_worker = functools.partial(inner_func, *args, **kwargs)

    res = process_exec(inner_worker, delay, queue, kill=kill)
    return parse_return(res)


def process_timeout(delay, kill=True):
    @decorator.decorator
    def wrapper(wrapped, *args, **kwargs):
        queue = multiprocessing.Queue()

        def inner_worker():
            try:
                result = wrapped(*args, **kwargs)
                queue.put(('success', result))
            except:
                e = sys.exc_info()
                queue.put(('exception', e[0:1]))
        res = process_exec(inner_worker, delay, queue, kill=kill)
        return parse_return(res)
    return wrapper
