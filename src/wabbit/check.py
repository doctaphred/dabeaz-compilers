from .utils import log


def compile(nodes, ctx=None):
    if ctx is None:
        ctx = Context()
    for node in nodes:
        ctx.append(node)
    return ctx


class Context:
    def __init__(self):
        self.nodes = []
        self.funcs = {}
        self.vars = {}
        self.mem = {}
        self.errors = {}

    def error(self, node, msg):
        self.errors.setdefault(node, []).append(msg)
        log(node, msg)

    def append(self, node):
        self.nodes.append(node)
        node.check(self)

    def __str__(self):
        return '\n'.join(str(node) for node in self.nodes)

    def dis(self):
        return '\n'.join(node.dis() for node in self.nodes)
