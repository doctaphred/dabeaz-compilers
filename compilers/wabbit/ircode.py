# ircode.py
'''
A Intermediate "Virtual" Machine
================================
An actual CPU typically consists of registers and a small set of basic
opcodes for performing mathematical calculations, loading/storing
values from memory, and basic control flow (branches, jumps, etc.).
Although you can make a compiler generate instructions directly for a
CPU, it is often simpler to target a higher-level of abstraction
instead.  One such abstraction is that of a stack machine. 

For example, suppose you want to evaluate an operation like this:

    a = 2 + 3 * 4 - 5

To evaluate the above expression, you could generate
pseudo-instructions like this instead:

    CONSTI 2      ; stack = [2]
    CONSTI 3      ; stack = [2, 3]
    CONSTI 4      ; stack = [2, 3, 4]
    MULI          ; stack = [2, 12]
    ADDI          ; stack = [14]
    CONSTI 5      ; stack = [14, 5]
    SUBI          ; stack = [9]
    STORE "a"     ; stack = []

Notice how there are no details about CPU registers or anything like
that here. It's much simpler (a lower-level module can figure out the
hardware mapping later if it needs to).

CPUs usually have a small set of code datatypes such as integers and
floats.  There are dedicated instructions for each type.  The IR code
will follow the same principle by supporting integer and floating
point operations. For example:

    ADDI   ; Integer add
    ADDF   ; Float add

Although the input language might have other types such as 'bool' and
'char', those types need to be mapped down to integers or floats. For
example, a bool can be represented by an integer with values {0, 1}. A
char can be represented by an integer whose value is the same as
the character code value (i.e., an ASCII code or a Unicode code-point).

With that in mind, here is a basic instruction set for our IR Code:

    ; Integer operations
    CONSTI  value            ; Push a integer literal on the stack
    GLOBALI name             ; Declare an integer global variable 
    LOCALI name              ; Declare an integer local variable
    ADDI                     ; Add top two items on stack
    SUBI                     ; Substract top two items on stack
    MULI                     ; Multiply top two items on stack
    DIVI                     ; Divide top two items on stack
    ANDI                     ; Bitwise AND
    ORI                      ; Bitwise OR
    LTI                      : <
    LEI                      : <=
    GTI                      : >
    GEI                      : >=
    EQI                      : ==
    NEI                      : !=
    PRINTI                   ; Print top item on stack
    PEEKI                    ; Get integer from memory (address on stack)
    POKEI                    ; Put integer in memory (value, address) on stack.
    ITOF                     ; Convert integer to float

    ; Floating point operations
    CONSTF value             ; Push a float literal
    GLOBALF name             ; Declare a float global variable 
    LOCALF name              ; Declare a float local variable
    ADDF                     ; Add top two items on stack
    SUBF                     ; Substract top two items on stack
    MULF                     ; Multiply top two items on stack
    DIVF                     ; Divide top two items on stack
    LTF                      : <
    LEF                      : <=
    GTF                      : >
    GEF                      : >=
    EQF                      : ==
    NEF                      : !=
    PRINTF                   ; Print top item on stack
    PEEKF                    ; Get float from memory (address on stack)
    POKEF                    ; Put float in memory (value, address on stack) 
    FTOI                     ; Convert float to integer
    CMPF op                  ; Compare the top two items on stack

    ; Byte-oriented operations (values are presented as integers)    
    PRINTB                   ; Print top item on stack
    PEEKB                    ; Get byte from memory (address on stack)
    POKEB                    ; Put byte in memory (value, address on stack)

    ; Variable load/store
    LOAD name                ; Load variable on stack (must be declared already)
    STORE name               ; Save variable from stack (must be declared already)

    ; Function call and return
    CALL name                ; Call function. All arguments must be on stack
    RET                      ; Return from a function. Value must be on stack

    ; Structured control flow
    IF                       ; Start consequence part of an "if". Test on stack
    ELSE                     ; Start alternative part of an "if".
    ENDIF                    ; End of an "if" statement.

    LOOP                     ; Start of a loop
    CBREAK                   ; Conditional break. Test on stack.
    CONTINUE                 ; Go back to loop start
    ENDLOOP                  ; End of a loop

    ; Memory
    GROW                     ; Increment memory (size on stack) (returns new size)

One word about memory access... the PEEK and POKE instructions are
used to access raw memory addresses.  Both instructions require a
memory address to be on the stack first.  For the POKE instruction,
the value being stored is pushed after the address. The order is
important and it's easy to mess it up.  So pay careful attention to
that.

Your Task
=========
Your task is as follows: Write code that walks through the program structure
and flattens it to a sequence of instructions represented as tuples of the
form:

       (operation, operands, ...)

For example, the code at the top might end up looking like this:

    code = [
       ('CONSTI', 2),
       ('CONSTI', 3),
       ('CONSTI', 4),
       ('MULI',),
       ('ADDI',),
       ('CONSTI', 5),
       ('SUBI',),
       ('STOREI', 'a'),
    ]

Functions
=========
All generated code is associated with some kind of function.  For
example, with a user-defined function like this:

    func fact(n int) int {
        var result int = 1;
        var x int = 1;
        while x <= n {
            result = result * x;
            x = x + 1;
        }
     }

You should create a Function object that contains the name of the
function, the arguments, the return type, and a body which contains
all of the low-level instructions.  Note: at this level, the types are
going to represent low-level IR types like Integer (I) and Float (F).
They are not the same types as used in the high-level Wabbit code.

Also, all code that's defined *outside* of a Function should still
go into a function called "_init()".  For example, if you have
global declarations like this:

     const pi = 3.14159;
     const r = 2.0;
     print pi*r*r;

Your code generator should actually treat them like this:

     func _init() int {
         const pi = 3.14159;
         const r = 2.0;
         print pi*r*r;
         return 0;
     }

Bottom line: All code goes into a function.

Modules
=======
The final output of code generation is IR Code for a whole collection
of functions. To produce a final result, put all of the functions in 
some kind of Module object. 
'''
