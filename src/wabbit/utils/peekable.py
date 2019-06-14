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
    >>> next(p, None)
    >>> next(p)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(p)
    []
    >>> list(Peekable(range(3)))
    [0, 1, 2]
    """
    _sentinel = object()

    def __init__(self, it):
        self._it = iter(it)
        self._advance()

    def _advance(self):
        self._next = next(self._it, self._sentinel)

    def peek(self, default=_sentinel):
        """Return the next item without advancing the iterator.

        Raises StopIteration if the iterator is empty, unless a default
        value is provided as a kwarg.
        """
        if not self:
            if default is not self._sentinel:
                return default
            else:
                raise StopIteration
        else:
            return self._next

    def __next__(self, default=_sentinel):
        if not self:
            if default is not self._sentinel:
                return default
            else:
                raise StopIteration
        else:
            val = self._next
            self._advance()
            return val

    def __bool__(self):
        return self._next is not self._sentinel
