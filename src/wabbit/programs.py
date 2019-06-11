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
    InfixOp,
    Float,
    Integer,
    PrefixOp,
    Print,
    DeclareAssignVar,
    DeclareVar,
    AssignVar,
    LoadVar,
)

from .typesys import WabbitType


# ----------------------------------------------------------------------
# Simple Expressions:
#
# Encode:   int_expr      -> 2 + 3 * 4
# Encode:   float_expr    -> 2.0 + 3.0 * 4.0
#
# This one is given to you as an example.

int_expr = InfixOp('+', Integer(2),
                   InfixOp('*', Integer(3), Integer(4)))

float_expr = InfixOp('+', Float(2.0),
                     InfixOp('*', Float(3.0), Float(4.0)))

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
            Integer(2),
            InfixOp(
                '*',
                Integer(3),
                PrefixOp(
                    '-',
                    Integer(4),
                ),
            ),
        ),
    ),
    Print(
        InfixOp(
            '-',
            Float(2.0),
            InfixOp(
                '/',
                Float(3.0),
                PrefixOp(
                    '-',
                    Float(4.0),
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
#    var tau float;
#    tau = 2.0 * pi;
#    print(tau);

program2 = [
    DeclareAssignVar(
        name='pi',
        type=WabbitType.float,
        value=Float(
            value=3.14159
        ),
        const=True,
    ),
    DeclareVar(
        name='tau',
        type=WabbitType.float,
    ),
    AssignVar(
        name='tau',
        value=InfixOp(
            symbol='*',
            left=Float(
                value=2.0,
            ),
            right=LoadVar(
                name='pi',
            ),
        ),
    ),
    Print(
        LoadVar(
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

program3 = []

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

program4 = []

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

program5 = []

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

program6 = []

# ----------------------------------------------------------------------
# Program 7: Memory
#
#    var memsize int = ^1000;
#    const addr = 500;
#    `addr = 1234;          // Stores 1234 at memory address addr
#    print(`addr + 10000);  // Reads 1234 from memory address addr
#

program7 = []
