# lexercise.py

text = "123 abc 45 + - * def 73"


def kind(c):
    if '0' <= c <= '9':
        return 'number'
    elif 'a' <= c <= 'z' or 'A' <= c <= 'Z':
        return 'word'
    else:
        return 'other'


def lex(text):
    it = iter(text)
    prev_word = next(it)
    prev_kind = kind(prev_word)

    for c in it:
        curr_kind = kind(c)
        if curr_kind != prev_kind:
            yield prev_kind, prev_word
            prev_word = c
            prev_kind = curr_kind
        else:
            prev_word += c

    yield curr_kind, prev_word


def find(text):
    '''
    Find all numbers and all words and prints them out.
    Example:

    >>> find(text)
    NUMBER: 123
    WORD: abc
    NUMBER: 45
    WORD: def
    NUMBER: 73

    Ignore all other characters.
    '''
    for k, w in lex(text):
        if k in {'number', 'word'}:
            print(f"{k.upper()}: {w}")


def is_digit(c):
    return '0' <= c <= '9'


def is_sign(c):
    return c == '+' or c == '-'


def is_decimal(c):
    return c == '.'


def is_letter(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z'


def is_separator(c):
    return c == ' '


def maybe_number(token, it):
    for c in it:
        if is_digit(c):
            token += c
        elif is_decimal(c):
            yield from maybe_float(token + c, it)
        elif is_separator(c):
            yield 'int', token
            yield 'separator', c
            return
        else:
            yield 'error', token + c
    yield 'int', token


def maybe_float(token, it):
    for c in it:
        if is_digit(c):
            token += c
        elif is_separator(c):
            yield 'float', token
            yield 'separator', c
            return
        else:
            yield 'error', token + c
    yield 'float', token


def maybe_identifier(token, it):
    for c in it:
        # Identifiers can have numbers after an initial letter.
        if is_letter(c) or is_digit(c):
            token += c
        elif is_separator(c):
            yield 'identifier', token
            yield 'separator', c
            return
        else:
            yield 'error', token + c
    yield 'identifier', token


def tokenize(text):
    """
    >>> for kind, token in tokenize("123 abc 45 + - * def 73"):
    ...     print(f"{kind}: {token!r}")
    int: '123'
    separator: ' '
    identifier: 'abc'
    separator: ' '
    int: '45'
    separator: ' '
    int: '+'
    separator: ' '
    int: '-'
    separator: ' '
    other: '*'
    other: ' '
    identifier: 'def'
    separator: ' '
    int: '73'
    """
    it = iter(text)
    for c in it:
        if is_digit(c) or is_sign(c):
            yield from maybe_number(c, it)
        elif is_decimal(c):
            yield from maybe_float(c, it)
        elif is_letter(c):
            yield from maybe_identifier(c, it)
        else:
            yield 'other', c


test_cases = [
    "123 abc 45 + - * def 73",
    "123 abc23 4.5 /* Comment 67 */ 'x' '\\n' '\\'' + - * def 73",
]


def test_tokenize():
    r"""
    >>> test_tokenize()
    Case #1:
    int: '123'
    separator: ' '
    identifier: 'abc'
    separator: ' '
    int: '45'
    separator: ' '
    int: '+'
    separator: ' '
    int: '-'
    separator: ' '
    other: '*'
    other: ' '
    identifier: 'def'
    separator: ' '
    int: '73'
    ---
    Case #2:
    int: '123'
    separator: ' '
    identifier: 'abc23'
    separator: ' '
    float: '4.5'
    separator: ' '
    error: '4/'
    error: '4*'
    int: '4'
    separator: ' '
    identifier: 'Comment'
    separator: ' '
    int: '67'
    separator: ' '
    other: '*'
    other: '/'
    other: ' '
    other: "'"
    error: "x'"
    identifier: 'x'
    separator: ' '
    other: "'"
    other: '\\'
    error: "n'"
    identifier: 'n'
    separator: ' '
    other: "'"
    other: '\\'
    other: "'"
    other: "'"
    other: ' '
    int: '+'
    separator: ' '
    int: '-'
    separator: ' '
    other: '*'
    other: ' '
    identifier: 'def'
    separator: ' '
    int: '73'
    ---
    """
    for i, case in enumerate(test_cases, start=1):
        print(f"Case #{i}:")
        for kind, token in tokenize(case):
            print(f"{kind}: {token!r}")
        print("---")
