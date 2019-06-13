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
