# grader-py

The automatic grader for Python modules, based on `unittest`.

## License

This is free and unencumbered software released into the public domain.

## Usage

Run this script with Python 3.

## Introduction

This script is an automatic grader that runs testcases on a Python module, based
on `unittest`.

An example of tests is given in the class `MyTest`. A test is roughly a method
of a class that inherits from `unittest.TestCase`, and the method name must
starts with `test`.

There are 4 types of results for a test: success, failure, timeout, and runtime
error. One example is given for each type of results.

- The test is **success** if all the code in the test method runs, and the grader
is able to return from the method normally. In other words, if `print('hello')`
is added to the end of a test method, the `hello` should appear if the test
succeeds.
- The test is **failure** if a special assert statement (provided by `unittest`)
fails. These should be straightforward. Just like the `AssertionError`, the code
after the failed assertion will not be run. In addition, `self.assertRaises` is
able to assert if a specific exception is raised during the execution of a
function - you may find lambda functions useful.
- The test **timeouts** if the test method cannot finish in a given amount of time.
Simply use the decorator `@timeout(sec)`. Note that `sec` must be a positive
integer. The timeout functionality depends on `signal`, so it may only work in
UNIX(-like) environments.
- The test encounters a **runtime error** if an unexpected exception is raised, or
an unexpected exit (e.g. calls `exit()`) happens. Note that the `unittest`
framework is NOT able to catch some types of exits like `os._exit(0)` or
segmentation faults.

## Security Notes (PLEASE READ)

This script does NOT sandbox the module to be tested, and it tests the module in
the current process. Take care of the potential vulnerabilities. In addition,
you might need to run this script in a sandbox as a user with restricted
permissions, and properly set the permissions of other relevant files.

In case that the student program overwrites some Python files, it is recommended
to import standard modules and the reference program BEFORE importing the
student program. In case that the names under the student program overwrites
some names in this script, it is NOT recommended to `import *` from the student
program.

Since a student program may write anything to stdout or stderr, it is NOT
recommended to log the results to the two standard streams. Instead, log the
results directly to a file in the filesystem. Since the student program may also
write to the log file, a simple solution is to temporarily log to a `StringIO`
object, and then write to the log file after the execution of all testcases. In
case that a student program uses `atexit` to register some malicious functions
at a normal exit, manually exit the script using `os._exit(0)`.
