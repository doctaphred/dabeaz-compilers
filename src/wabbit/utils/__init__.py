import sys


def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)
