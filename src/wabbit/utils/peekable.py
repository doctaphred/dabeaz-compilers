from collections.abc import Iterator


class Peekable(Iterator):
    """
    >>> p = Peekable(range(3))
    >>> next(p)
    0
    >>> next(p)
    1
    >>> p.peek()
    2
    >>> p.peek(default=None)
    2
    >>> bool(p)
    True
    >>> next(p)
    2
    >>> bool(p)
    False
    >>> p.peek()
    Traceback (most recent call last):
      ...
    StopIteration
    >>> p.peek(default=None)
    >>> next(p)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(Peekable(range(3)))
    [0, 1, 2]
    """
    sentinel = object()

    def __init__(self, it):
        self.__it = iter(it)
        self.__advance()

    def __advance(self):
        try:
            self.__next_val = next(self.__it)
        except StopIteration:
            self.__empty = True
        else:
            self.__empty = False

    def peek(self, *, default=sentinel):
        """Return the next item without advancing the iterator.

        Raises StopIteration if the iterator is empty, unless a default
        value is provided as a kwarg.
        """
        if self.__empty:
            if default is self.sentinel:
                raise StopIteration
            else:
                return default
        return self.__next_val

    def __next__(self):
        if self.__empty:
            raise StopIteration
        val = self.__next_val
        self.__advance()
        return val

    def __bool__(self):
        return not self.__empty
