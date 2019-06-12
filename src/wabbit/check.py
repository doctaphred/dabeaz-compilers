from .utils import log


class Context:
    def __init__(self):
        self.expressions = {}
        self.funcs = {}
        self.vars = {}
        self.errors = {}

    def error(self, node, msg):
        self.errors.setdefault(node, []).append(msg)
        log(node, msg)
