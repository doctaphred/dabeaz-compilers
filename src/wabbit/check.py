from .utils import log


class Context:
    def __init__(self):
        self.expressions = {}
        self.funcs = {}
        self.vars = {}
        self.mem = {}
        self.errors = {}

    def error(self, node, msg):
        self.errors.setdefault(node, []).append(msg)
        log(node, msg)

    @classmethod
    def eval(cls, stmts):
        self = cls()
        for stmt in stmts:
            stmt.check(self)
        return self
