    >>> from wabbit.programs import *
    >>> from wabbit.utils import dis, pprog

    >>> print(int_expr)
    2 + 3 * 4

    >>> print(float_expr)
    2.0 + 3.0 * 4.0

    >>> pprog(program1)
    print 2 + 3 * -4;
    print 2.0 - 3.0 / -4.0;

    >>> dis(program1)
    print 2 + 3 * -4;
    > ('consti', 2)
    > ('consti', 3)
    > ('consti', 4)
    > ('muli',)
    > ('addi',)
    > ('printi',)
    print 2.0 - 3.0 / -4.0;
    > ('constf', 2.0)
    > ('constf', 3.0)
    > ('constf', 4.0)
    > ('divf',)
    > ('subf',)
    > ('printf',)

    - TODO: change 'const pi float' to 'const pi'
    - TODO: add parens to print statement

    >>> pprog(program2)
    const pi float = 3.14159;
    var tau float;
    tau = 2.0 * pi;
    print tau;

    >>> pprog(program3)
    var a int = 2;
    var b int = 3;
    if a < b {
        print a;
    } else {
        print b;
    }

    TODO: 
        - 'const n int' -> 'const n'

    >>> pprog(program4)
    const n int = 10;
    var x int = 1;
    var fact int = 1;
    while x < n {
        fact = fact * x;
        print fact;
        x = x + 1;
    }


    >>> pprog(program5)
    func square(x int) int {
        return x * x;
    }
    print square(4);
    print square(10);

    TODO:
        - parentheses for print
        - no semicolon after print(??)

    >>> pprog(program6)
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

    >>> pprog(program7)
    var memsize int = ^1000;
    const addr int = 500;
    `addr = 1234;
    print `addr + 10000;
