# tokenizer.py
r'''
The role of a tokenizer is to turn raw text into recognized symbols 
known as tokens.

The tokenizer for Wabbit is required to recognize the following
symbols.  The suggested name of the token is on the left. The matching
text is on the right.

Reserved Keywords:
    CONST   : 'const'
    VAR     : 'var'  
    PRINT   : 'print'
    RETURN  : 'return'
    BREAK   : 'break'
    CONTINUE: 'continue'
    IF      : 'if'
    ELSE    : 'else'
    WHILE   : 'while'
    FUNC    : 'func'
    IMPORT  : 'import'
    TRUE    : 'true'
    FALSE   : 'false'

Identifiers:
    ID      : Text starting with a letter or '_', followed by any number
              number of letters, digits, or underscores.
              Examples:  'abc' 'ABC' 'abc123' '_abc' 'a_b_c'

Literals:
    INTEGER :  123   (decimal)

    FLOAT   : 1.234
              .1234
              1234.

    CHAR    : 'a'     (a single character - byte)
              '\xhh'  (byte value)
              '\n'    (newline)
              '\''    (literal single quote)

Operators:
    PLUS     : '+'
    MINUS    : '-'
    TIMES    : '*'
    DIVIDE   : '/'
    LT       : '<'
    LE       : '<='
    GT       : '>'
    GE       : '>='
    EQ       : '=='
    NE       : '!='
    LAND     : '&&'
    LOR      : '||'
    LNOT     : '!'
    GROW     : '^'
    
Miscellaneous Symbols
    ASSIGN   : '='
    SEMI     : ';'
    LPAREN   : '('
    RPAREN   : ')'
    LBRACE   : '{'
    RBRACE   : '}'
    COMMA    : ','
    DEREF    : '`'    (Backtick)

Comments:  To be ignored
     //             Skips the rest of the line
     /* ... */      Skips a block (no nesting allowed)

Errors: Your lexer may optionally recognize and report the following
error messages:

     lineno: Illegal char 'c'         
     lineno: Unterminated character constant    
     lineno: Unterminated comment

'''
            
            
        

            
    
