# programs.py
#
# *** Note: Only work on this file *AFTER* you have defined the data
# model in wabbit/model.py. ***
#
# Within the bowels of your compiler, you need to represent programs
# as data structures.   In this file, you need to manually encode
# some simple Wabbit programs using the data model you've developed.
#
# The purpose of these programs is two-fold:
#
#   1. Make sure you understand the data model of your compiler.
#   2. Have some program structures that you can use for later testing
#      and experimentation.
#
# This file is broken into sections. Follow the instructions for
# each part.  Parts of this file might be referenced in later
# parts of the project.  Plan to have a lot of discussion.
#
# You need to play defense with all of your coding. In the
# wabbit/model.py file you should actively place assertions and other
# checks that prevent the creation of a bad model.  Those assertions
# will help you here if you screw things up.

from wabbit.model import (
    Block,
    Conditional,
    FloatLiteral,
    FuncCall,
    FuncDef,
    InfixOp,
    IntLiteral,
    Loop,
    MemGet,
    MemSet,
    Parameter,
    PrefixOp,
    Print,
    Return,
    VarDef,
    VarDefSet,
    VarGet,
    VarSet,
)

from .typesys import WabbitType


# ----------------------------------------------------------------------
# Simple Expressions:
#
# Encode:   int_expr      -> 2 + 3 * 4
# Encode:   float_expr    -> 2.0 + 3.0 * 4.0
#
# This one is given to you as an example.

int_expr = InfixOp('+', IntLiteral(2),
                   InfixOp('*', IntLiteral(3), IntLiteral(4)))

float_expr = InfixOp('+', FloatLiteral(2.0),
                     InfixOp('*', FloatLiteral(3.0), FloatLiteral(4.0)))

# ----------------------------------------------------------------------
# Program 1: Printing
#
# Encode the following program which tests printing and simple expresions.
#
#    print 2 + 3 * -4;
#    print 2.0 - 3.0 / -4.0;
#

program1 = [
    Print(
        InfixOp(
            '+',
            IntLiteral(2),
            InfixOp(
                '*',
                IntLiteral(3),
                PrefixOp(
                    '-',
                    IntLiteral(4),
                ),
            ),
        ),
    ),
    Print(
        InfixOp(
            '-',
            FloatLiteral(2.0),
            InfixOp(
                '/',
                FloatLiteral(3.0),
                PrefixOp(
                    '-',
                    FloatLiteral(4.0),
                ),
            ),
        ),
    ),
]

# ----------------------------------------------------------------------
# Program 2: Variable and constant declarations.
#            Expressions and assignment.
#
# Encode the following statements.
#
#    const pi = 3.14159;
#    var tau FloatLiteral;
#    tau = 2.0 * pi;
#    print(tau);

program2 = [
    VarDefSet(
        name='pi',
        type=WabbitType.float,
        value=FloatLiteral(
            value=3.14159,
        ),
        const=True,
    ),
    VarDef(
        name='tau',
        type=WabbitType.float,
    ),
    VarSet(
        name='tau',
        value=InfixOp(
            symbol='*',
            left=FloatLiteral(
                value=2.0,
            ),
            right=VarGet(
                name='pi',
            ),
        ),
    ),
    Print(
        VarGet(
            name='tau',
        ),
    ),
]

# ----------------------------------------------------------------------
# Program 3: Conditionals.  This program prints out the minimum of
# two values.
#
#    var a int = 2;
#    var b int = 3;
#    if a < b {
#        print a;
#    } else {
#        print b;
#    }
#

program3 = [
    VarDefSet(
        name='a',
        type=WabbitType.int,
        value=IntLiteral(
            value=2,
        ),
        const=False,
    ),
    VarDefSet(
        name='b',
        type=WabbitType.int,
        value=IntLiteral(
            value=3,
        ),
        const=False,
    ),
    Conditional(
        test=InfixOp(
            symbol='<',
            left=VarGet(
                name='a',
            ),
            right=VarGet(
                name='b',
            ),
        ),
        then=Block(
            statements=(
                Print(value=VarGet(name='a')),
            ),
        ),
        otherwise=Block(
            statements=(
                Print(value=VarGet(name='b')),
            ),
        ),
    ),
]

# ----------------------------------------------------------------------
# Program 4: Loops.  This program prints out the first 10 factorials.
#
#    const n = 10;
#    var x int = 1;
#    var fact int = 1;
#
#    while x < n {
#        fact = fact * x;
#        print fact;
#        x = x + 1;
#    }
#

program4 = [
    VarDefSet(
        name='n',
        type=WabbitType.int,
        value=IntLiteral(10),
        const=True,
    ),
    VarDefSet(
        name='x',
        type=WabbitType.int,
        value=IntLiteral(1),
        const=False,
    ),
    VarDefSet(
        name='fact',
        type=WabbitType.int,
        value=IntLiteral(1),
        const=False,
    ),
    Loop(
        test=InfixOp(
            symbol='<',
            left=VarGet(name='x'),
            right=VarGet(name='n'),
        ),
        body=Block(
            statements=(
                VarSet(
                    name='fact',
                    value=InfixOp(
                        symbol='*',
                        left=VarGet(name='fact'),
                        right=VarGet(name='x'),
                    ),
                ),
                Print(VarGet(name='fact')),
                VarSet(
                    name='x',
                    value=InfixOp(
                        symbol='+',
                        left=VarGet(name='x'),
                        right=IntLiteral(1),
                    ),
                ),
            ),
        ),
    ),
]

# ----------------------------------------------------------------------
# Program 5: Functions (simple)
#
#    func square(x int) int {
#        return x*x;
#    }
#
#    print square(4);
#    print square(10);
#

program5 = [
    FuncDef(
        name='square',
        params=[
            Parameter(
                name='x',
                type=WabbitType.int,
            ),
        ],
        return_type=WabbitType.int,
        body=Block([
            Return(InfixOp('*', VarGet('x'), VarGet('x'))),
        ]),
    ),
    Print(
        FuncCall(
            name='square',
            args=[IntLiteral(4)],
        ),
    ),
    Print(
        FuncCall(
            name='square',
            args=[IntLiteral(10)],
        ),
    ),
]

# ----------------------------------------------------------------------
# Program 6: Functions (complex)
#
#    func fact(n int) int {
#        var x int = 1;
#        var result int = 1;
#        while x < n {
#            result = result * x;
#            x = x + 1;
#        }
#        return result;
#    }
#
#    print(fact(10))

program6 = [
    FuncDef(
        name='fact',
        params=[Parameter('n', WabbitType.int)],
        return_type=WabbitType.int,
        body=Block([
            VarDefSet(
                'x',
                WabbitType.int,
                IntLiteral(1),
                const=False,
            ),
            VarDefSet(
                'result',
                WabbitType.int,
                IntLiteral(1),
                const=False,
            ),
            Loop(
                test=InfixOp('<', VarGet('x'), VarGet('n')),
                body=Block([
                    VarSet(
                        'result',
                        InfixOp('*', VarGet('result'), VarGet('x')),
                    ),
                    VarSet('x', InfixOp('+', VarGet('x'), IntLiteral(1))),
                ]),
            ),
            Return(VarGet('result')),
        ]),
    ),
    Print(FuncCall('fact', [IntLiteral(10)])),
]

# ----------------------------------------------------------------------
# Program 7: Memory
#
#    var memsize int = ^1000;
#    const addr = 500;
#    `addr = 1234;          // Stores 1234 at memory address addr
#    print(`addr + 10000);  // Reads 1234 from memory address addr
#

program7 = [
    VarDefSet(
        'memsize',
        WabbitType.int,
        PrefixOp('^', IntLiteral(1000)),
        const=False,
    ),
    VarDefSet(
        'addr',
        WabbitType.int,
        IntLiteral(500),
        const=True,
    ),
    MemSet(VarGet('addr'), IntLiteral(1234)),
    Print(
        InfixOp(
            '+',
            MemGet(VarGet('addr')),
            IntLiteral(10000),
        ),
    ),
]
