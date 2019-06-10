# model.py
#
# This file defines a data model for Wabbit programs.  Basically,
# the data model is a large data structure that represents the
# contents of a program as objects, not text.  To do this, you
# need to identify the different "elements" that make up a program
# and encode them into classes.  You also need to think about
# defensive programming.   Can you add appropriate assertions
# and checks that prevent someone from creating a badly formed model?
#
# This file is broken up into parts that describe parts of the
# Wabbit language specification.

# ----------------------------------------------------------------------
# Part 1: Expressions.
#
# Expressions represent things that evaluate to a concrete value.
#
# Wabbit defines the following expressions and operators
#
# 1.1 Literals
#        23            (Integer literal)
#        4.5           (Float literal)
#        true,false    (Bool literal)
#        'c'           (Character literal - A single character)
#
# 1.2 Binary Operators
#        left + right        (Addition)
#        left - right        (Subtraction)
#        left * right        (Multiplication)
#        left / right        (Division)
#        left < right        (Less than)
#        left <= right       (Less than or equal)
#        left > right        (Greater than)
#        left >= right       (Greater than or equal)
#        left == right       (Equal to)
#        left != right       (Not equal)
#        left && right       (Logical and)
#        left || right       (Logical or)
#
# 1.3 Unary Operators
#        +operand       (Positive)
#        -operand       (Negation)
#        !operand       (logical not)
#        ^operand       (Grow memory)
#
# 1.4 Loading from a location
#        xyz           (The value of variable xyz)
#        `expr         (The contents of memory location expr)
#
# 1.5 Type-casts
#         int(expr)
#         float(expr)
#
# 1.6 Function/Procedure Call
#        func(arg1, arg2, ..., argn)
#

# ----------------------------------------------------------------------
# Part 2. Definitions
#
# Wabbit requires variables and functions to be declared in advance.
#
# 2.1 Variables.  Variables can be declared in a few different forms.
#
#    const name = value;
#    var name type [= value];
#    var name [type] = value;
#
# Variables can exist as globals or as local variables to a function.
# Constants are immutable.  The type of a constant is later inferred from
# its value.
#
# 2.2 Function Parameters
#
#       func square(x int) int { return x*x; }
#
# A function parameter is a special kind of local variable.  It
# has a name and a type like a local variable.  However, it
# is declared as part of the function definition itself, not as
# a separate "var" declaration.
#
# 2.3 Function definitions.
#
#    func name(parameters) return_type { statements }
#
# Functions can be imported from external libraries using
# the special statement
#
#    import func name(parms) type;
#

# ----------------------------------------------------------------------
# Part 3. Statements.
#
# Wabbit programs consist of sequences of statements.  Statements
# are mainly related to mutating state (assignment), I/O (printing), and
# control-flow.
#
# 3.1 Assignment
#
#     location = expression ;
#
#
# 3.2 Printing
#
#     print expression ;
#
# 3.3 Conditional
#
#     if test { consequence} else { alternative }
#
# 3.4 Loop
#
#  while test { body }
#
# 3.5 Break and Continue
#
#   while test {
#       ...
#       break;
#   }
#
# 3.6 Function Return
#
#  return expression ;
#
# Does it need a reference to its enclosing function?


from .utils.reprs import vars_repr


class Expression:
    def __init__(self, **kwargs):
        vars(self).update(kwargs)
        self.validate()

    @classmethod
    def validate(self, *args, **kwargs):
        assert False, f"{self.__class__.__name__} cannot be instantiated"

    __repr__ = vars_repr


class Literal(Expression):
    kinds = {}

    def __init_subclass__(cls, **kwargs):
        key = cls.__name__
        if key in cls.kinds:
            raise ValueError(f"{key} is already {cls.kinds[key]}")
        cls.kinds[key] = cls

    def __init__(self, value):
        super().__init__(value=value)

    def literal(self):
        return repr(self.value)


class Integer(Literal):
    """
    >>> Integer(0)
    Integer(value=0)
    """
    def validate(self):
        assert isinstance(self.value, int)


class Float(Literal):
    """
    >>> Float(0.0)
    Float(value=0.0)
    """
    def validate(self):
        assert isinstance(self.value, float)


class Bool(Literal):
    """
    >>> Bool(False)
    Bool(value=False)
    """
    def validate(self):
        assert isinstance(self.value, bool)


class Character(Literal):
    """
    >>> Character('a')
    Character(value='a')
    """
    def validate(self):
        assert isinstance(self.value, str)
        assert len(self.value) == 1
