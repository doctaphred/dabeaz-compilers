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


class AttrValidator:

    def __init__(self, **kwargs):
        vars(self).update(kwargs)
        self.validate()

    def validate(self):
        for name, ann in self.__init__.__annotations__.items():
            value = getattr(self, name)
            if not isinstance(value, ann):
                raise TypeError(
                    f"expected {ann.__name__}, got {value.__class__.__name__}"
                )

    __repr__ = vars_repr


class Expression(AttrValidator):
    pass

    # TODO: global registry?
    # def __init_subclass__(cls, **kwargs):
    #     kind = cls.kind()
    #     if kind in cls.kinds:
    #         raise TypeError(f"{kind} is already {cls.kinds[kind]}")
    #     cls.kinds[kind] = cls


class Literal(Expression):
    # 1.1 Literals
    #        23            (Integer literal)
    #        4.5           (Float literal)
    #        true,false    (Bool literal)
    #        'c'           (Character literal - A single character)
    #

    def __init__(self, value):
        super().__init__(value=value)

    def __str__(self):
        return repr(self.value)

    def validate(self):
        super().validate()
        if type(self.value) != self.python_type:
            raise TypeError(
                f"expected {self.python_type}, got {type(self.value)}"
            )


class Integer(Literal):
    """
    >>> Integer(0)
    Integer(value=0)

    >>> str(Integer(0))
    '0'

    >>> Integer('a')
    Traceback (most recent call last):
      ...
    TypeError: expected <class 'int'>, got <class 'str'>
    """
    python_type = int


class Float(Literal):
    """
    >>> Float(0.0)
    Float(value=0.0)
    """
    python_type = float


class Bool(Literal):
    """
    >>> Bool(False)
    Bool(value=False)
    """
    python_type = bool


class Character(Literal):
    """
    >>> Character('a')
    Character(value='a')
    """
    python_type = str

    def validate(self):
        super().validate()
        assert len(self.value) == 1


class PrefixOp(Expression):
    """
    >>> PrefixOp('+', Integer(0))
    PrefixOp(symbol='+', operand=Integer(value=0))
    >>> str(PrefixOp('+', Integer(0)))
    '+0'

    >>> PrefixOp('?', Integer(0))
    Traceback (most recent call last):
      ...
    ValueError: invalid PrefixOp symbol: '?'

    >>> stmt = AssignVar('x', Integer(2))
    >>> PrefixOp('-', stmt)
    Traceback (most recent call last):
      ...
    TypeError: expected Expression, got AssignVar
    """
    # 1.3 Unary Operators
    #        +operand       (Positive)
    #        -operand       (Negation)
    #        !operand       (logical not)
    #        ^operand       (Grow memory)
    symbols = set('+-!^')

    def __init__(self, symbol: str, operand: Expression):
        super().__init__(symbol=symbol, operand=operand)

    def validate(self):
        super().validate()
        if self.symbol not in self.symbols:
            raise ValueError(
                f"invalid {self.__class__.__name__} symbol: {self.symbol!r}"
            )

    def __str__(self):
        return f"{self.symbol}{self.operand}"


class InfixOp(Expression):
    """
    >>> InfixOp('+', Integer(1), Integer(2))
    InfixOp(symbol='+', left=Integer(value=1), right=Integer(value=2))
    >>> str(InfixOp('+', Integer(1), Integer(2)))
    '1 + 2'
    """
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

    symbols = {
        '+',
        '-',
        '*',
        '/',
        '<',
        '<=',
        '> ',
        '>=',
        '==',
        '!=',
        '&&',
        '||',
    }

    def __init__(self, symbol, left: Expression, right: Expression):
        super().__init__(symbol=symbol, left=left, right=right)

    def validate(self):
        super().validate()
        if self.symbol not in self.symbols:
            raise ValueError(
                f"invalid {self.__class__.__name__} symbol: {self.symbol!r}"
            )

    def __str__(self):
        return f"{self.left} {self.symbol} {self.right}"


class LoadVar(Expression):
    """
    >>> LoadVar('ayy')
    LoadVar(name='ayy')
    """
    # 1.4 Loading from a location
    #        xyz           (The value of variable xyz)
    #        `expr         (The contents of memory location expr)
    def __init__(self, name: str):
        super().__init__(name=name)


class LoadMem(Expression):
    # 1.4 Loading from a location
    #        xyz           (The value of variable xyz)
    #        `expr         (The contents of memory location expr)
    def __init__(self, loc: Expression):
        super().__init__(loc=loc)


class TypeCast(Expression):
    # 1.5 Type-casts
    #         int(expr)
    #         float(expr)
    def __init__(self, type, value: Expression):
        super().__init__(type=type, value=value)


class Call(Expression):
    # 1.6 Function/Procedure Call
    #        func(arg1, arg2, ..., argn)
    def __init__(self, func, args):
        super().__init__(func=func, args=args)


class FuncParam(Expression):
    # 2.2 Function Parameters
    #
    #       func square(x int) int { return x*x; }
    #
    # A function parameter is a special kind of local variable.  It
    # has a name and a type like a local variable.  However, it
    # is declared as part of the function definition itself, not as
    # a separate "var" declaration.
    def __init__(self, name, type):
        super().__init__(name=name, type=type)


class Statement(AttrValidator):
    pass


class DeclareVar(Statement):
    # 2.1 Variables.  Variables can be declared in a few different forms.
    #
    #    var name type [= value];
    #    var name [type] = value;
    def __init__(self, name, type):
        super().__init__(name=name, type=type)


class AssignVar(Statement):
    # 3.1 Assignment
    #
    #     location = expression ;
    def __init__(self, name, value: Expression):
        super().__init__(name=name, value=value)


class DeclareAssignVar(Statement):
    #    var name type [= value];
    #    const name = value;
    def __init__(self, name, type, value, const):
        super().__init__(name=name, type=type, value=value, const=const)


class AssignMem(Statement):
    # `location = expression ;
    def __init__(self, loc: Expression, value: Expression):
        super().__init__(loc=loc, value=value)


class Block:
    def __init__(self, statements):
        for statement in statements:
            if not isinstance(statement, Statement):
                raise TypeError(f"{type(statement)}: {statement}")
        self.statements = statements


class DefineFunc(Statement):
    # 2.3 Function definitions.
    #
    #    func name(parameters) return_type { statements }
    def __init__(self, name, params, return_type, block: Block):
        super().__init__(
            self,
            name=name,
            params=params,
            return_type=return_type,
            block=block,
        )


class ImportFunc(DefineFunc):
    # Functions can be imported from external libraries using
    # the special statement
    #
    #    import func name(parms) type;
    pass


class Print(Statement):
    # 3.2 Printing
    #
    #     print expression ;
    def __init__(self, value: Expression):
        super().__init__(value=value)


class Conditional(Statement):
    #
    # 3.3 Conditional
    #
    #     if test { consequence} else { alternative }
    def __init__(self, test: Expression, then: Block, otherwise: Block):
        super().__init__(test=test, then=then, otherwise=otherwise)


class Loop(Statement):
    # 3.4 Loop
    #
    #  while test { body }
    def __init__(self, test: Expression, body: Block):
        super().__init__(test=test, body=body)


class Break(Statement):
    # 3.5 Break and Continue
    #
    #   while test {
    #       ...
    #       break;
    #   }
    def __init__(self):
        pass


class Continue(Statement):
    #   while test {
    #       ...
    #       continue;
    #   }
    def __init__(self):
        pass


class Return(Statement):
    # 3.6 Function Return
    #
    #  return expression ;
    #
    # Does it need a reference to its enclosing function?
    def __init__(self, value: Expression):
        super().__init__(value=value)
