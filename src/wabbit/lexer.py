text = (
    "123 abc23 4.5 /* Comment 67 */ 'x' '\\n' '\\'' + - * def 73"
    "+ - * / < > <= >= && || == != ! ^ ` , ; ="
    "if while var const func return break continue else true false"
    " print import"
)


def tokenize(text):
    '''
    Find all numbers and words and print them out.
    Find INTEGER vs FLOAT.    123 vs. 1.234.
    Ignore block comments /* ... */
    Find quoted CHAR. Examples:  'x', '\'' '\n'
    Modify words to allow trailing digits.
    How to identify special keywords like "if", "while", "var", "const",
    "print"

       if   -> ('IF', 'if')
       while -> ('WHILE', 'while')
       var -> ('VAR', 'var')
       const -> ('CONST', 'const')
       print -> ('PRINT', 'print')
       func -> ('FUNC', 'func')
       return -> ('RETURN', 'return')
       break -> ('BREAK', 'break')
       continue -> ('CONTINUE', 'continue')
       import -> ('IMPORT', 'import')
       true -> ('TRUE', 'true'),
       false -> ('FALSE', 'false')
       else -> ('ELSE', 'else')

    Find symbols:
        +   -> ('PLUS', '+')
        -   -> ('MINUS', '-')
        *   -> ('TIMES', '*')
        /   -> ('DIVIDE', '/')
        <   -> ('LT', '<')
        >   -> ('GT', '>')
        ,   -> ('COMMA', ',')
        ;   -> ('SEMI', ';')
        (   -> ('LPAREN', '(')
        )   -> ('RIGHT', ')')
        `   -> ('BACKTICK', '`')
        ^   -> ('HAT', '^')
        =   -> ('ASSIGN', '=')
        !   -> ('NOT', '!')

        <=  -> ('LE', '<=')
        >=  -> ('GE', '>=')
        ==  -> ('EQ', '==')
        !=  -> ('NE', '!=')
        &&  -> ('AND', '&&')
        ||  -> ('OR', '||')

    Example:

        INT: 123
        WORD: abc
        FLOAT: 4.5
        WORD: def
        INT: 73

    Ignore all other characters.
    '''

    symbols_1 = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'TIMES',
        '/': 'DIVIDE',
        '<': 'LT',
        '>': 'GT',
        ',': 'COMMA',
        ';': 'SEMI',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '`': 'BACKTICK',
        '^': 'HAT',
        '=': 'ASSIGN',
        '!': 'NOT',
    }

    symbols_2 = {
        '<=': 'LE',
        '>=': 'GE',
        '==': 'EQ',
        '!=': 'NE',
        '&&': 'AND',
        '||': 'OR'
    }

    keywords = {
        'if',
        'else',
        'while',
        'var',
        'const',
        'print',
        'return',
        'break',
        'continue',
        'true',
        'false',
        'import',
        'func',
    }

    text += ' '
    index = 0
    while index < len(text):
        ch = text[index]
        # Problem: How do you know when you start/end a word or number?
        # Number is one or more digits.
        # Word is one or more letters.
        if ch >= '0' and ch <= '9':
            start = index
            while ch >= '0' and ch <= '9':
                index += 1
                ch = text[index]
            if ch == '.':
                index += 1
                ch = text[index]
                while ch >= '0' and ch <= '9':
                    index += 1
                    ch = text[index]
                yield ('FLOAT', text[start:index])
            else:
                yield ('INT', text[start:index])

        elif (ch >= 'a' and ch <= 'z'
                or ch >= 'A' and ch <= 'Z'):
            start = index
            while (ch >= 'a' and ch <= 'z'
                    or ch >= 'A' and ch <= 'Z'
                    or ch >= '0' and ch <= '9'):
                index += 1
                ch = text[index]
            word = text[start:index]
            if word in keywords:
                yield (word.upper(), word)
            else:
                yield ('WORD', text[start:index])

        # Ignore comments (just skip over it)
        elif text[index:index+2] == '/*':
            index += 2
            while index < len(text) and text[index:index+2] != '*/':
                index += 1
            index += 2

        elif ch == "'":
            start = index
            index += 1
            ch = text[index]
            while ch != "'":
                if ch == '\\':
                    index += 1
                index += 1
                ch = text[index]
            index += 1
            yield ('CHAR', text[start:index])

        # Two character symbols
        elif text[index:index+2] in symbols_2:
            t = text[index:index+2]
            yield (symbols_2[t], t)
            index += 2

        # Single character symbols
        elif ch in symbols_1:
            yield (symbols_1[ch], ch)
            index += 1

        elif ch in ' \t':
            # Whitespace (ignore)
            index += 1
        else:
            # Oh well.  Ignore the character.
            print("Unknown character:", repr(ch))
            index += 1


if __name__ == '__main__':
    for match in tokenize(text):
        print(match)
