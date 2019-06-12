# errors.py
#
# Compiler error handling support.
#
# One of the most important (and annoying) parts of writing a compiler
# is reliable reporting of error messages back to the user.  This file
# should consolidate some basic error handling functionality in one
# place.  Make it easy to report errors.  Make it easy to find out
# if errors have occurred.
#
# You might also want to think about errors in the context of testing.

from pathlib import Path

from .utils import log


@type.__call__
class error:

    def __init__(self, path='errors.txt'):
        self.list = []
        self.path = Path(path)

    def __call__(self, msg):
        self.list.append(msg)
        log(msg)
        with open(self.path, 'a') as f:
            print(msg, file=f)
        return msg
