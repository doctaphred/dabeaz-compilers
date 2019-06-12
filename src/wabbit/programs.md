    >>> from wabbit.programs import *

    >>> print(int_expr)
    2 + 3 * 4

    >>> print(float_expr)
    2.0 + 3.0 * 4.0

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

    TODO: 
        - 'const n int' -> 'const n'

    >>> for stmt in program4:
    ...     print(stmt)
    const n int = 10;
    var x int = 1;
    var fact int = 1;
    while x < n {
        fact = fact * x;
        print fact;
        x = x + 1;
    }


    >>> for stmt in program5:
    ...     print(stmt)
    func square(x int) int {
        return x * x;
    }
    print square(4);
    print square(10);

    TODO:
        - parentheses for print
        - no semicolon after print(??)

    >>> for stmt in program6:
    ...     print(stmt)
    func fact(n int) int {
        var x int = 1;
        var result int = 1;
        while x < n {
            result = result * x;
            x = x + 1;
        }
        return result;
    }
    print fact(10);

    TODO:
        - 'const addr int' -> 'const addr'
        - add parens to print

    >>> for stmt in program7:
    ...     print(stmt)
    var memsize int = ^1000;
    const addr int = 500;
    `addr = 1234;
    print `addr + 10000;
