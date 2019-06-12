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

# This is real "sketchy" at this point.  All we know is that types
# are things (objects).  Types have to be attached to values in the data
# model.

typenames = { 'int', 'float', 'bool', 'char', '<error>', '<infer>' }

class Type:
    def __init__(self, name):
        assert name in typenames
        self.name = name
        
    def __eq__(self, other):
        if isinstance(other, Type):
            return self.name == other.name
        return False

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return f'{type(self).__name__}({self.name!r})'    

# How to encode the capabilities of each type?   What binary operators?
# What are the result types?

_bin_ops = {
    # Integer operations
    **{ ('int', op, 'int'): 'int' for op in ['+','-','*','/'] },
    **{ ('int', op, 'int'): 'bool' for op in ['<','<=','>','>=','==','!='] },
    
    # Float operations
    **{ ('float', op, 'float'): 'float' for op in ['+','-','*','/'] },
    **{ ('float', op, 'float'): 'bool' for op in ['<','<=','>','>=','==','!='] },

    # Character operations
    **{ ('char', op, 'char'): 'bool' for op in ['<','<=','>','>=','==','!='] },

    # Bool
    **{ ('bool', op, 'bool'): 'bool' for op in ['&&','||','==','!='] },
    }

# Return the result type of an operation or None (if unsupported)
def check_binop(op, lefttype, righttype):
    result = _bin_ops.get((str(lefttype), op, str(righttype)))
    if result:
        return Type(result)
    else:
        return None

_unary_ops = {
    **{ (op, 'int') : 'int' for op in ['+','-','^'] },
    **{ (op, 'float') : 'float' for op in ['+','-'] },
    ('!', 'bool'): 'bool'
    }

def check_unaryop(op, optype):
    result = _unary_ops.get((op, str(optype)))
    if result:
        return Type(result)
    else:
        return None

_typecasts = {
    'int': 'int',
    'int': 'float',
    'float': 'int',
    'float': 'float',
    }

def check_typecast(from_type, to_type):
    result = _typecasts.get(str(from_type))
    if result:
        return Type(result)
    else:
        return None
    
# Thought: Maybe better to not overthink it right now. Types have names.
# Types can be compared.   That's it.  

a = Type('int')
b = Type('int')
assert a == b
c = Type('float')
assert a != c
