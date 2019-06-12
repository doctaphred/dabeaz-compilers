# import typing

from .reprs import vars_repr


# class attr:
#     def __init__(self, func=None, type=None):
#         self.func = func
#         self.type = type

#     def __call__(self, value):
#         if self.type is not None:
#             pass


class EZAttrs:
    # required = object()  # Sentinel object.

    def __init__(self, *args, **kwargs):
        # constraints = self.__annotations__
        unexpected = kwargs.keys() - self.attrs
        if unexpected:
            raise TypeError(f"unexpected attr(s): {unexpected}")

        it = iter(args)
        for name, value in zip(self.attrs, it):
            setattr(self, name, value)

        leftovers = set(it)
        missing = leftovers - kwargs.keys()
        if missing:
            raise TypeError(f"missing kwarg(s): {missing}")

        vars(self).update(kwargs)

        self.validate()

    def validate(self):
        pass

    __repr__ = vars_repr
