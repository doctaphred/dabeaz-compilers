# typesys.py
'''
Type System
===========
This file implements basic features of the type system.  There is a
lot of flexibility possible here, but the best strategy might be to
not overthink the problem.  At least not at first.  Here are the
minimal basic requirements:

1. Types have identity (e.g., minimally a name such as 'int', 'float', 'char')
2. Types have to be comparable. (e.g., int != float).
3. Types support different operators (e.g., +, -, *, /, etc.)

One way to achieve all of these goals is to start off with some kind
of table-driven approach.  It's not the most sophisticated thing, but
it will work as a starting point.  You can come back and refactor the
type system later.
'''
from .utils.reprs import vars_repr


class WabbitType:
    """
    >>> WabbitType['int']
    WabbitType(name='int')
    """
    names = {}

    def __init__(self, name):
        assert name not in self.names, name
        self.name = name
        self.names[name] = self

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    __repr__ = vars_repr

    def __class_getitem__(cls, name):
        return cls.names[name]


IntType = WabbitType('int')
FloatType = WabbitType('float')
BoolType = WabbitType('bool')
CharType = WabbitType('char')
