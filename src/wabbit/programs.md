    >>> from wabbit.programs import *

    >>> int_expr
    InfixOp(symbol='+', left=Integer(value=2), right=InfixOp(symbol='*', left=Integer(value=3), right=Integer(value=4)))

    >>> float_expr
    InfixOp(symbol='+', left=Float(value=2.0), right=InfixOp(symbol='*', left=Float(value=3.0), right=Float(value=4.0)))

    >>> program1
    [Print(value=InfixOp(symbol='+', left=Integer(value=2), right=InfixOp(symbol='*', left=Integer(value=3), right=PrefixOp(symbol='-', operand=Integer(value=4))))), Print(value=InfixOp(symbol='-', left=Float(value=2.0), right=InfixOp(symbol='/', left=Float(value=3.0), right=PrefixOp(symbol='-', operand=Float(value=4.0)))))]

    >>> for stmt in program1:
    ...     print(stmt)
    print 2 + 3 * -4;
    print 2.0 - 3.0 / -4.0;

    - TODO: change 'const pi float' to 'const pi'
    - TODO: add parens to print statement

    >>> for stmt in program2:
    ...     print(stmt)
    const pi float = 3.14159;
    var tau float;
    tau = 2.0 * pi;
    print tau;

    >>> for stmt in program3:
    ...     print(stmt)
    var a int = 2;
    var b int = 3;
    if a < b {
        print a;
    } else {
        print b;
    }
