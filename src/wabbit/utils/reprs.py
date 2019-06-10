def vars_repr(obj):
    """Return a repr string from the object's instance attributes."""
    return callstr(obj, **vars(obj))


def attr_repr(obj, attr_names=None):
    """Return a repr string from the specified attributes.

    If no attributes are specified, uses all "public" attributes
    (names that don't begin with an underscore).

    >>> class Thing:
    ...     a = 1
    ...     def __init__(self):
    ...         self.b = 2
    ...     @property
    ...     def c(self):
    ...         return 3
    ...     def method(self):
    ...         return 4
    ...     def __repr__(self):
    ...         return attr_repr(self, ['a', 'b', 'c'])

    >>> Thing()
    Thing(a=1, b=2, c=3)
    """
    if attr_names is None:
        attr_names = [name for name in dir(obj) if not name.startswith('_')]
    attrs = {name: getattr(obj, name) for name in attr_names}
    return callstr(obj, **attrs)


def argstr(*args, **kwargs):
    """Return a string representation of the given signature.

    Lists kwargs in sorted order.

    >>> argstr(1, 2, 3)
    '(1, 2, 3)'
    >>> argstr()
    '()'
    >>> argstr(a=1)
    '(a=1)'
    >>> argstr(1, 2, c=3)
    '(1, 2, c=3)'
    >>> argstr(a=1, c=3, b=2)
    '(a=1, b=2, c=3)'
    """
    if not args and not kwargs:
        return '()'

    args_str = ', '.join(repr(arg) for arg in args)
    kwargs_str = ', '.join('{}={!r}'.format(k, v)
                           for k, v in sorted(kwargs.items()))

    if not args:
        return f'({kwargs_str})'
    if not kwargs:
        return f'({args_str})'
    return f'({args_str}, {kwargs_str})'


def callstr(*args, **kwargs):
    """Return a string representation of a call to the given object.

    >>> def ayy(): pass
    >>> callstr(ayy, 'lm', a='o')
    "ayy('lm', a='o')"

    >>> class ayy: pass
    >>> callstr(ayy, 'lm', a='o')
    "ayy('lm', a='o')"

    >>> class ayy: pass
    >>> callstr(ayy(), 'lm', a='o')
    "ayy('lm', a='o')"
    """
    first, *rest = args
    try:
        name = first.__name__
    except AttributeError:
        name = first.__class__.__name__
    return name + argstr(*rest, **kwargs)
