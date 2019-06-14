    >>> from wabbit.programs import *

    >>> print(int_expr)
    2 + 3 * 4

    >>> print(float_expr)
    2.0 + 3.0 * 4.0

    >>> print(program1)
    print 2 + 3 * -4;
    print 2.0 - 3.0 / -4.0;

    >>> print(program1.dis())
    print 2 + 3 * -4;
    > ('consti', 2)
    > ('consti', 3)
    > ('consti', 0)
    > ('consti', 4)
    > ('subi',)
    > ('muli',)
    > ('addi',)
    > ('printi',)
    print 2.0 - 3.0 / -4.0;
    > ('constf', 2.0)
    > ('constf', 3.0)
    > ('constf', 0.0)
    > ('constf', 4.0)
    > ('subf',)
    > ('divf',)
    > ('subf',)
    > ('printf',)

    - TODO: change 'const pi float' to 'const pi'
    - TODO: add parens to print statement

    >>> print(program2)
    const pi float = 3.14159;
    var tau float;
    tau = 2.0 * pi;
    print tau;

    >>> print(program2.dis())
    const pi float = 3.14159;
    > ('localf', 'pi')
    > ('constf', 3.14159)
    > ('store', 'pi')
    var tau float;
    > ('localf', 'tau')
    tau = 2.0 * pi;
    > ('constf', 2.0)
    > ('load', 'pi')
    > ('mulf',)
    > ('store', 'tau')
    print tau;
    > ('load', 'tau')
    > ('printf',)

    >>> print(program3)
    var a int = 2;
    var b int = 3;
    if a < b {
        print a;
    } else {
        print b;
    }

    >>> print(program3.dis())
    var a int = 2;
    > ('locali', 'a')
    > ('consti', 2)
    > ('store', 'a')
    var b int = 3;
    > ('locali', 'b')
    > ('consti', 3)
    > ('store', 'b')
    if a < b {
        print a;
    } else {
        print b;
    }
    > ('load', 'a')
    > ('load', 'b')
    > ('lti',)
    > ('if',)
    > ('load', 'a')
    > ('printi',)
    > ('else',)
    > ('load', 'b')
    > ('printi',)
    > ('endif',)

    TODO: 
        - 'const n int' -> 'const n'

    >>> print(program4)
    const n int = 10;
    var x int = 1;
    var fact int = 1;
    while x < n {
        fact = fact * x;
        print fact;
        x = x + 1;
    }

    >>> print(program4.dis())
    const n int = 10;
    > ('locali', 'n')
    > ('consti', 10)
    > ('store', 'n')
    var x int = 1;
    > ('locali', 'x')
    > ('consti', 1)
    > ('store', 'x')
    var fact int = 1;
    > ('locali', 'fact')
    > ('consti', 1)
    > ('store', 'fact')
    while x < n {
        fact = fact * x;
        print fact;
        x = x + 1;
    }
    > ('loop',)
    > ('consti', 1)
    > ('load', 'x')
    > ('load', 'n')
    > ('lti',)
    > ('subi',)
    > ('cbreak',)
    > ('load', 'fact')
    > ('load', 'x')
    > ('muli',)
    > ('store', 'fact')
    > ('load', 'fact')
    > ('printi',)
    > ('load', 'x')
    > ('consti', 1)
    > ('addi',)
    > ('store', 'x')
    > ('endloop',)

    >>> print(program5)
    func square(x int) int {
        return x * x;
    }
    print square(4);
    print square(10);

    >>> print(program5.dis())
    func square(x int) int {
        return x * x;
    }
    > ('load', 'x')
    > ('load', 'x')
    > ('muli',)
    > ret
    print square(4);
    > ('consti', 4)
    > ('call', 'square')
    > ('printi',)
    print square(10);
    > ('consti', 10)
    > ('call', 'square')
    > ('printi',)

    TODO:
        - parentheses for print
        - no semicolon after print(??)

    >>> print(program6)
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

    >>> print(program7)
    var memsize int = ^1000;
    const addr int = 500;
    `addr = 1234;
    print `addr + 10000;
