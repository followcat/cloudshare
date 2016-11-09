# This code is part of the checkmate project.
# Copyright (C) 2014-2016 The checkmate project contributors
#
# This program is free software under the terms of the GNU GPL, either
# version 3 of the License, or (at your option) any later version.

import os
import doctest
import functools


__all__ = ['report_issue', 'fix_issue', 'runtest']


class Runner(doctest.DocTestRunner):
     def report_unexpected_exception(self, *args, **kwargs):
         """Remove junk from failure output"""
         pass
     def report_failure(self, *args, **kwargs):
         pass

def runtest(filename, runner=doctest.DocTestRunner()):
    if os.path.isfile(filename):
        _f = open(filename)
    else:
        _f = open(os.path.sep.join([filename]))
    test = _f.read()
    _f.close()
    return runner.run(doctest.DocTestParser().get_doctest(test, locals(),
                        filename, None, None))

def runtest_silent(filename):
    return runtest(filename, Runner(verbose=False))

def _issue_record(filename, failed):
    result = runtest_silent(filename)
    if result.failed != failed:
        print(runtest(filename))
        if failed == 0:
            print("Expected: success, got: %d failures" % result.failed)
        else:
            print("Expected: %d failures, got: %d" % (failed, result.failed))

def _add_issue_doctest(filename, failed=0):
    def append_docstring(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        if wrapper.__doc__ is None:
            wrapper.__doc__ = ""
        wrapper.__doc__ += """
            \n            >>> %s._issue_record('%s', failed=%d)
            """ % (__name__, filename, failed)
        return wrapper
    return append_docstring

def report_issue(filename, failed=1):
    """
        >>> import os
        >>> import doctest
        >>> import utils.issue
        >>> filename = 'dt1.rst'
        >>> filepath = os.path.join('tests', filename)

    Hardcoded failed doctest:
        >>> with open(filepath, 'w') as f:
        ...     n = f.write(\">>> print(False)\\nFalse\")
        ... 
        >>> @utils.issue.report_issue(filepath)
        ... def func():
        ...     pass
        >>> _r = utils.issue.Runner(verbose=False)
        >>> test = doctest.DocTestParser().get_doctest(func.__doc__,
        ...             locals(), func.__name__, None, None)
        >>> _r.run(test) # doctest: +ELLIPSIS
        TestResults(failed=1, ...

    Hardcoded successful doctest:
        >>> with open(filepath, 'w') as f:
        ...     n = f.write(\">>> print(True)\\nFalse\")
        ... 
        >>> @utils.issue.report_issue(filepath)
        ... def func():
        ...     pass
        ... 
        >>> doctest.run_docstring_examples(func, locals())
        >>> os.remove(filepath)
    """
    return _add_issue_doctest(filename, failed)

def fix_issue(filename):
    """
        >>> import os
        >>> import doctest
        >>> import utils.issue
        >>> filename = 'dt1.rst'
        >>> filepath = os.path.join('tests', filename)

    Hardcoded successful doctest:
        >>> with open(filepath, 'w') as f:
        ...     n = f.write(\">>> print(False)\\nFalse\")
        ... 
        >>> @utils.issue.fix_issue(filepath)
        ... def func():
        ...     pass
        ... 
        >>> doctest.run_docstring_examples(func, locals())

    Hardcoded failed doctest:
        >>> with open(filepath, 'w') as f:
        ...     n = f.write(\">>> print(True)\\nFalse\")
        ... 
        >>> @utils.issue.fix_issue(filepath)
        ... def func():
        ...     pass
        >>> _r = utils.issue.Runner(verbose=False)
        >>> test = doctest.DocTestParser().get_doctest(func.__doc__,
        ...             locals(), func.__name__, None, None)
        >>> _r.run(test) # doctest: +ELLIPSIS
        TestResults(failed=1, ...
        >>> os.remove(filepath)
    """
    return _add_issue_doctest(filename)

