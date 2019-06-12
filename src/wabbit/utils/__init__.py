import sys


def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def pprog(prog, dis=False):
    for stmt in prog:
        print(stmt)
        if dis:
            for inst in stmt:
                print('>', inst)


def dis(prog):
    pprog(prog, dis=True)
