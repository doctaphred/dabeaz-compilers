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


class NamedSingleton(type):
    __cache = {}

    def __call__(cls, name):
        try:
            return cls.__cache[name]
        except KeyError:
            cls.__cache[name] = obj = super().__call__(name)
            return obj

    def bogus(cls, name):
        return (
            name == 'pytest_mock_example_attribute_that_shouldnt_exist'
            or name.startswith('_')
        )

    def __getattr__(cls, name):
        if cls.bogus(name):
            raise AttributeError(name)
        return cls(name)


class WabbitType(metaclass=NamedSingleton):
    """
    >>> WabbitType.int is WabbitType('int') is WabbitType(name='int')
    True

    >>> WabbitType('int')
    WabbitType('int')

    >>> WabbitType.int
    WabbitType('int')
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"
