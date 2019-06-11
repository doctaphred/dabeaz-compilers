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
