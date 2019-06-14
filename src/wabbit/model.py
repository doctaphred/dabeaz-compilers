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

from textwrap import indent

from .typesys import WabbitType
from .utils.reprs import vars_repr


class AttrValidator:

    def __init__(self, **kwargs):
        vars(self).update(kwargs)
        self.validate()

    def validate(self):
        for name, ann in self.__init__.__annotations__.items():
            value = getattr(self, name)

            try:
                constraints = iter(ann)
            except TypeError:
                constraints = [ann]

            for constraint in constraints:
                if isinstance(constraint, type):
                    if not isinstance(value, constraint):
                        raise TypeError(
                            "expected {}, got {}".format(
                                constraint.__name__,
                                value.__class__.__name__,
                            )
                        )
                else:
                    if not constraint(value):
                        raise TypeError(
                            f"{value!r} did not satisfy {constraint!r}"
                        )

    __repr__ = vars_repr


class Node(AttrValidator):
    def check(self, ctx):
        raise NotImplementedError(self.__class__.__name__)

    def __iter__(self):
        raise NotImplementedError(self.__class__.__name__)


class Expression(Node):
    # Every expression must have a type.
    type = None


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

    def check(self, ctx):
        pass


class IntLiteral(Literal):
    """
    >>> IntLiteral(0)
    IntLiteral(value=0)

    >>> str(IntLiteral(0))
    '0'

    >>> IntLiteral('a')
    Traceback (most recent call last):
      ...
    TypeError: expected <class 'int'>, got <class 'str'>
    """
    python_type = int
    type = WabbitType.int

    def __iter__(self):
        yield 'consti', self.value


class FloatLiteral(Literal):
    """
    >>> FloatLiteral(0.0)
    FloatLiteral(value=0.0)
    """
    python_type = float
    type = WabbitType.float

    def __iter__(self):
        yield 'constf', self.value


class BoolLiteral(Literal):
    """
    >>> BoolLiteral(False)
    BoolLiteral(value=False)
    """
    python_type = bool
    type = WabbitType.bool

    def __iter__(self):
        yield 'consti', int(self.value)

    def __str__(self):
        return 'true' if self else 'false'


class CharLiteral(Literal):
    """
    >>> CharLiteral('a')
    CharLiteral(value='a')
    """
    python_type = str
    type = WabbitType.char

    def validate(self):
        super().validate()
        assert len(self.value) == 1

    def __iter__(self):
        yield 'consti', ord(self.value)


class PrefixOp(Expression):
    """
    >>> PrefixOp('+', IntLiteral(0))
    PrefixOp(symbol='+', operand=IntLiteral(value=0))
    >>> str(PrefixOp('+', IntLiteral(0)))
    '+0'

    >>> PrefixOp('?', IntLiteral(0))
    Traceback (most recent call last):
      ...
    ValueError: invalid PrefixOp symbol: '?'

    >>> stmt = VarSet('x', IntLiteral(2))
    >>> PrefixOp('-', stmt)
    Traceback (most recent call last):
      ...
    TypeError: expected Expression, got VarSet
    """
    # 1.3 Unary Operators
    #        +operand       (Positive)
    #        -operand       (Negation)
    #        !operand       (logical not)
    #        ^operand       (Grow memory)
    symbols = {
        '+': {'int': 'int', 'float': 'float'},
        '-': {'int': 'int', 'float': 'float'},
        '!': {'bool': 'bool'},
        '^': {'int': 'int'},
    }

    def __init__(self, symbol: str, operand: Expression):
        super().__init__(symbol=symbol, operand=operand)

    def validate(self):
        super().validate()
        if self.symbol not in self.symbols:
            raise ValueError(
                f"invalid {self.__class__.__name__} symbol: {self.symbol!r}"
            )

    def check(self, ctx):
        self.operand.check(ctx)

        transitions = self.symbols[self.symbol]

        name = self.operand.type.name

        if name not in transitions:
            self.type = WabbitType.error
            ctx.error(self, f"{self!r} ({self}): unsupported type: {name}")
            return
        else:
            self.type = WabbitType(transitions[name])

    def __iter__(self):
        if self.symbol == '+':
            # '+' is a no-op: just push the operand on the stack.
            yield from self.operand
        elif self.symbol == '-':
            if self.type is WabbitType.float:
                # TODO: is this order correct?
                yield 'constf', 0.0
                yield from self.operand
                yield ('subf',)
            else:
                yield 'consti', 0
                yield from self.operand
                yield ('subi',)
        elif self.symbol == '!':
            # 1 - 1 == 0; 1 - 0 == 1
            yield 'consti', 1
            yield from self.operand
            yield ('subi',)
        else:
            assert False  # TODO

    def __str__(self):
        return f"{self.symbol}{self.operand}"


class InfixOp(Expression):
    """
    >>> InfixOp('+', IntLiteral(1), IntLiteral(2))
    InfixOp(symbol='+', left=IntLiteral(value=1), right=IntLiteral(value=2))
    >>> str(InfixOp('+', IntLiteral(1), IntLiteral(2)))
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
        '+':  {'int': 'int', 'float': 'float'},
        '-':  {'int': 'int', 'float': 'float'},
        '*':  {'int': 'int', 'float': 'float'},
        '/':  {'int': 'int', 'float': 'float'},
        '<':  {'int': 'bool', 'float': 'bool', 'char': 'bool'},
        '<=': {'int': 'bool', 'float': 'bool', 'char': 'bool'},
        '>':  {'int': 'bool', 'float': 'bool', 'char': 'bool'},
        '>=': {'int': 'bool', 'float': 'bool', 'char': 'bool'},
        '==': {'int': 'bool', 'float': 'bool', 'char': 'bool', 'bool': 'bool'},
        '!=': {'int': 'bool', 'float': 'bool', 'char': 'bool', 'bool': 'bool'},
        '&&': {'bool': 'bool'},
        '||': {'bool': 'bool'},
    }

    def __init__(self, symbol, left: Expression, right: Expression):
        super().__init__(symbol=symbol, left=left, right=right)

    def validate(self):
        super().validate()
        if self.symbol not in self.symbols:
            raise ValueError(
                f"invalid {self.__class__.__name__} symbol: {self.symbol!r}"
            )

    def check(self, ctx):
        self.left.check(ctx)
        self.right.check(ctx)

        transitions = self.symbols[self.symbol]

        t1, t2 = self.left.type, self.right.type
        if t1 is WabbitType.infer:
            name = t2.name
        elif t2 is WabbitType.infer:
            name = t1.name
        elif t1 is not t2:
            self.type = WabbitType.error
            ctx.error(self, f"{self!r} ({self}): mismatched types: {t1}, {t2}")
            return
        else:
            assert t1 is t2
            name = t1.name

        if name not in transitions:
            self.type = WabbitType.error
            ctx.error(self, f"{self!r} ({self}): unsupported type: {name}")
        else:
            self.type = WabbitType(transitions[name])

    symbol_names = {
        '+':  'add',
        '-':  'sub',
        '*':  'mul',
        '/':  'div',
        '<':  'lt',
        '<=': 'le',
        '>':  'gt',
        '>=': 'ge',
        '==': 'eq',
        '!=': 'ne',
        '&&': 'and',
        '||': 'or',
    }

    def __iter__(self):
        yield from self.left
        yield from self.right
        name = self.symbol_names[self.symbol]
        if self.type is WabbitType.float:
            yield (name + 'f',)
        else:
            # ints, chars, and bools are all implemented as ints.
            yield (name + 'i',)

    def __str__(self):
        return f"{self.left} {self.symbol} {self.right}"


class VarGet(Expression):
    """
    >>> VarGet('ayy')
    VarGet(name='ayy')

    >>> VarGet(IntLiteral(0))
    Traceback (most recent call last):
      ...
    TypeError: expected str, got IntLiteral
    """
    # 1.4 Loading from a location
    #        xyz           (The value of variable xyz)
    #        `expr         (The contents of memory location expr)
    def __init__(self, name: str):
        super().__init__(name=name)

    def __str__(self):
        return self.name

    def check(self, ctx):
        if self.name not in ctx.vars:
            self.type = WabbitType.error
            ctx.error(self, f"undefined variable {self.name}")
        else:
            self.type = ctx.vars[self.name].type

    def __iter__(self):
        yield ('load', self.name)


class MemGet(Expression):
    """
    >>> MemGet(IntLiteral(0))
    MemGet(loc=IntLiteral(value=0))

    >>> MemGet('ayy')
    Traceback (most recent call last):
      ...
    TypeError: expected Expression, got str

    >>> stmt = VarSet('x', IntLiteral(2))
    >>> MemGet(stmt)
    Traceback (most recent call last):
      ...
    TypeError: expected Expression, got VarSet
    """
    # 1.4 Loading from a location
    #        xyz           (The value of variable xyz)
    #        `expr         (The contents of memory location expr)
    # TODO: is this just a PrefixOp?
    def __init__(self, loc: Expression):
        super().__init__(loc=loc)

    def __str__(self):
        return f"`{self.loc}"

    def check(self, ctx):
        self.loc.check(ctx)
        if self.loc.type is not WabbitType.int:
            self.type = WabbitType.error
            ctx.error(self, f"can't access non-int memory location {self.loc}")
        else:
            self.type = WabbitType.infer

    def __iter__(self):
        yield from self.loc
        # TODO: which type to load from memory?


class TypeCast(Expression):
    # 1.5 Type-casts
    #         int(expr)
    #         float(expr)

    casts = {
        'int': 'float',
        'float': 'int',
    }

    def __init__(self, type, value: Expression):
        super().__init__(type=type, value=value)

    def check(self, ctx):
        self.value.check(ctx)

        name = self.type.name
        if name not in self.casts:
            self.type = WabbitType.error
            ctx.error(self, f"can't cast to type {name}")
            return

        cast_result = self.casts[name]
        if self.value.type.name is not cast_result:
            ctx.error(
                self,
                f"can't cast from {self.value.type} to {self.type}"
            )

    def __iter__(self):
        yield from self.value
        # If types already match, assume no conversion is needed.
        if self.type is WabbitType.float:
            if self.value.type is WabbitType.int:
                yield 'itof'
        elif self.type is WabbitType.int:
            if self.value.type is WabbitType.float:
                yield 'itof'


class FuncCall(Expression):
    # 1.6 Function/Procedure Call
    #        func(arg1, arg2, ..., argn)
    def __init__(self, name: str, args):
        super().__init__(name=name, args=args)

    def validate(self):
        super().validate()
        for arg in self.args:
            assert isinstance(arg, Expression)

    def check(self, ctx):
        for arg in self.args:
            arg.check(ctx)
        if self.name not in ctx.funcs:
            self.type = WabbitType.error
            ctx.error(self, f"undefined function {self.name}")
        else:
            self.type = ctx.funcs[self.name].return_type
        # TODO: validate number of args?

    def __str__(self):
        args = ', '.join(str(arg) for arg in self.args)
        return f"{self.name}({args})"

    def __iter__(self):
        for arg in self.args:
            yield from arg
        yield 'call', self.name


class Parameter(Expression):
    # 2.2 Function Parameters
    #
    #       func square(x int) int { return x*x; }
    #
    # A function parameter is a special kind of local variable.  It
    # has a name and a type like a local variable.  However, it
    # is declared as part of the function definition itself, not as
    # a separate "var" declaration.
    def __init__(self, name, type: WabbitType):
        super().__init__(name=name, type=type)

    def check(self, ctx):
        pass

    def __str__(self):
        return f"{self.name} {self.type}"

    def __iter__(self):
        pass  # TODO


class Statement(Node):
    pass


class VarDef(Statement):
    """
    >>> VarDef('x', WabbitType.int)
    VarDef(name='x', type=WabbitType('int'))

    >>> VarDef(1, IntLiteral(2))
    Traceback (most recent call last):
      ...
    TypeError: expected str, got int

    >>> VarDef(CharLiteral('x'), IntLiteral(2))
    Traceback (most recent call last):
      ...
    TypeError: expected str, got CharLiteral
    """
    # 2.1 Variables.  Variables can be declared in a few different forms.
    #
    #    var name type [= value];
    #    var name [type] = value;
    def __init__(self, name: str, type: WabbitType):
        super().__init__(name=name, type=type)

    def __str__(self):
        return f"var {self.name} {self.type};"

    def check(self, ctx):
        assert self.name not in ctx.vars, self.name
        ctx.vars[self.name] = self

    def __iter__(self):
        # TODO: global vars?
        if self.type is WabbitType.float:
            yield 'localf', self.name
        else:
            yield 'locali', self.name


class VarSet(Statement):
    """
    >>> VarSet('x', IntLiteral(2))
    VarSet(name='x', value=IntLiteral(value=2))

    >>> VarSet(1, IntLiteral(2))
    Traceback (most recent call last):
      ...
    TypeError: expected str, got int

    >>> VarSet(CharLiteral('x'), IntLiteral(2))
    Traceback (most recent call last):
      ...
    TypeError: expected str, got CharLiteral
    """
    # 3.1 Assignment
    #
    #     location = expression ;
    def __init__(self, name: str, value: Expression):
        super().__init__(name=name, value=value)

    def __str__(self):
        return f"{self.name} = {self.value};"

    def check(self, ctx):
        self.value.check(ctx)
        if self.name not in ctx.vars:
            ctx.error(self, f"undefined variable {self.name}")
            return
        var = ctx.vars[self.name]
        if self.value.type is not var.type:
            ctx.error(self, f"expected {var.type}, got {self.value.type}")

    def __iter__(self):
        yield from self.value
        yield 'store', self.name


class VarDefSet(Statement):
    #    var name type [= value];
    #    const name = value;
    def __init__(
        self,
        name: str,
        type: WabbitType,  # TODO: make this optional.
        value: Expression,
        const: bool,
    ):
        super().__init__(name=name, type=type, value=value, const=const)

    def __str__(self):
        if self.const:
            prefix = 'const'
        else:
            prefix = 'var'
        return f"{prefix} {self.name} {self.type} = {self.value};"

    def check(self, ctx):
        self.value.check(ctx)
        ctx.vars[self.name] = self
        if self.value.type is not self.type:
            ctx.error(self, f"expected {self.type}, got {self.value.type}")

    def __iter__(self):
        if self.type is WabbitType.float:
            yield 'localf', self.name
        else:
            yield 'locali', self.name
        yield from self.value
        yield 'store', self.name


class MemSet(Statement):
    # `location = expression ;
    def __init__(self, loc: Expression, value: Expression):
        super().__init__(loc=loc, value=value)

    def __str__(self):
        return f"`{self.loc} = {self.value};"

    def check(self, ctx):
        ctx.mem[self.loc] = self


class Block:
    def __init__(self, statements):
        for statement in statements:
            if not isinstance(statement, Statement):
                raise TypeError(f"{type(statement)}: {statement}")
        self.statements = statements

    def __str__(self):
        return '\n'.join([
            '{',
            *[indent(str(stmt), '    ') for stmt in self.statements],
            '}',
        ])

    def check(self, ctx):
        for statement in self.statements:
            statement.check(ctx)

    def __iter__(self):
        for statement in self.statements:
            yield from statement


class FuncDef(Statement):
    # 2.3 Function definitions.
    #
    #    func name(parameters) return_type { statements }
    def __init__(self, name, params, return_type, body: Block):
        super().__init__(
            name=name,
            params=params,
            return_type=return_type,
            body=body,
        )

    def validate(self):
        super().validate()
        for param in self.params:
            assert isinstance(param, Parameter), param

    def check(self, ctx):
        for param in self.params:
            param.check(ctx)
        assert self.name not in ctx.funcs, self.name
        ctx.funcs[self.name] = self

    def __str__(self):
        params = ', '.join(str(param) for param in self.params)
        return "func {}({}) {} {}".format(
            self.name,
            params,
            self.return_type,
            self.body,
        )


class ImportFunc(FuncDef):
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

    def __str__(self):
        return f"print {self.value};"

    def check(self, ctx):
        self.value.check(ctx)

    def __iter__(self):
        yield from self.value
        if self.value.type is WabbitType.float:
            yield ('printf',)
        elif self.value.type is WabbitType.char:
            yield ('printb',)
        else:
            yield ('printi',)


class If(Statement):
    #
    # 3.3 Conditional
    #
    #     if test { consequence} else { alternative }
    def __init__(self, test: Expression, then: Block, otherwise: Block):
        super().__init__(test=test, then=then, otherwise=otherwise)

    def __str__(self):
        return f"if {self.test} {self.then} else {self.otherwise}"

    def check(self, ctx):
        self.test.check(ctx)
        if self.test.type is not WabbitType.bool:
            ctx.error(self, f"non-bool test {self.test} ({self.test.type})")
        self.then.check(ctx)
        self.otherwise.check(ctx)

    def __iter__(self):
        yield from self.test
        yield ('if',)
        yield from self.then
        yield ('else',)
        yield from self.otherwise
        yield ('endif',)


class While(Statement):
    # 3.4 Loop
    #
    #  while test { body }
    def __init__(self, test: Expression, body: Block):
        super().__init__(test=test, body=body)

    def __str__(self):
        return f"while {self.test} {self.body}"

    def check(self, ctx):
        self.test.check(ctx)
        if self.test.type is not WabbitType.bool:
            ctx.error(self, f"non-bool test {self.test} ({self.test.type})")
        self.body.check(ctx)


class Break(Statement):
    # 3.5 Break and Continue
    #
    #   while test {
    #       ...
    #       break;
    #   }
    def __init__(self):
        pass

    def check(self, ctx):
        # TODO: check if in a While Block?
        pass


class Continue(Statement):
    #   while test {
    #       ...
    #       continue;
    #   }
    def __init__(self):
        pass

    def check(self, ctx):
        # TODO: check if in a While Block?
        pass


class Return(Statement):
    # 3.6 Function Return
    #
    #  return expression ;
    #
    # Does it need a reference to its enclosing function?
    def __init__(self, value: Expression):
        super().__init__(value=value)

    def __str__(self):
        return f"return {self.value};"

    def check(self, ctx):
        self.value.check(ctx)
