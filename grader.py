#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import StringIO
import sys, os, signal, unittest, hashlib

# Import the student program and optionally the reference program here.
# import reference_program as my
# import student_program as your

# The score of each testcase. Should be equal to (100 / number of tests).
EACH_SCORE = 10

# Write the log to stdout if True, otherwise write to file `LOG_FILE`.
# This value should be set to False if deployed to a server!
LOG_STDOUT = False

# The log file pathname.
LOG_FILE = 'result.txt'

class TestTimeoutError(Exception):
    pass

# The timeout decorator.
def timeout(sec=1):
    def decorator(func):
        def _handle_timeout(a, b):
            raise TestTimeoutError('{}s'.format(sec))

        def wrapper(self):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(sec)
            try:
                func(self)
            finally:
                signal.alarm(0)

        return wrapper
    return decorator

# SHA1 checksum.
def checksum_sha1(filename):
    h = hashlib.sha1()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

# Testcases.
class MyTest(unittest.TestCase):
    def get_name(self):
        return self._testMethodName[5:]

    # Should succeed.
    @timeout(1)
    def test_0_valid(self):
        self.assertEqual(1 + 1, 2)
        self.assertTrue(isinstance(1, int))
        self.assertRaises(ZeroDivisionError, lambda: 1 / 0)

    # Should fail.
    @timeout(1)
    def test_1_invalid(self):
        self.assertEqual(1 + 1, 3)

    # Should timeout.
    @timeout(1)
    def test_2_loop(self):
        while True:
            pass

    # Should runtime error.
    @timeout(1)
    def test_3_exception(self):
        raise Exception

class MyTestResult(unittest._TextTestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.num_succ = 0
        self.num_tests = 0

    def startTest(self, test):
        self.num_tests += 1

    def addSuccess(self, test):
        self.num_succ += 1
        log.write('Test {test} succeeded.\n'.format(test=test.get_name()))

    def addFailure(self, test, err):
        log.write('Test {test} failed.\n'.format(test=test.get_name()))

    def addError(self, test, err):
        if err[0] is TestTimeoutError:
            log.write('Test {test} timeout ({err}).\n'.format(
                test=test.get_name(), err=err[1]))
        else:
            log.write('Test {test} runtime error.\n'.format(
                test=test.get_name()))

class MyTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return MyTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        result = self._makeResult()
        test(result)
        return result

def test():
    global log
    if LOG_STDOUT:
        log = sys.stdout
    else:
        log = StringIO()

    ret = unittest.main(exit=False, testRunner=MyTestRunner)
    result = ret.result
    your_score = EACH_SCORE * result.num_succ
    full_score = EACH_SCORE * result.num_tests

    log.write('\n')
    log.write('Each test is worth {} points.\n'.format(EACH_SCORE))
    log.write('You passed {}/{} tests, score: {}/{}.\n'.format(
        result.num_succ, result.num_tests, your_score, full_score))

    if not LOG_STDOUT:
        with open(LOG_FILE, 'w') as f:
            f.write(log.getvalue())
        print('log written to {}'.format(LOG_FILE))

    os._exit(0)

if __name__ == '__main__':
    test()
