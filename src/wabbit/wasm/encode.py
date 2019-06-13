r"""WebAssembly encoding helpers.

See https://en.wikipedia.org/wiki/LEB128

>>> unsigned(1234).hex()
'd209'
>>> signed(-1234).hex()
'ae76'
>>> f64(123.45).hex()
'cdccccccccdc5e40'
>>> name('spam').hex()
'047370616d'

"""
import struct


def unsigned(value):
    """Produce an LEB128 encoded unsigned integer."""
    parts = []
    while value:
        parts.append((value & 0x7f) | 0x80)
        value >>= 7
    if not parts:
        parts.append(0)
    parts[-1] &= 0x7f
    return bytes(parts)


def signed(value):
    """Produce a LEB128 encoded signed integer."""
    parts = []
    if value < 0:
        # Sign extend the value up to a multiple of 7 bits
        value += (1 << (value.bit_length() + (7 - value.bit_length() % 7)))
        negative = True
    else:
        negative = False
    while value:
        parts.append((value & 0x7f) | 0x80)
        value >>= 7
    if not parts or (not negative and parts[-1] & 0x40):
        parts.append(0)
    parts[-1] &= 0x7f
    return bytes(parts)


def f64(value):
    """Encode a 64-bit float point as little endian."""
    return struct.pack('<d', value)


def vector(items):
    """
    A size-prefixed collection of objects.  If items is already
    bytes, it is prepended by a length and returned.  If items
    is a list of byte-strings, the length of the list is prepended
    to byte-string formed by concatenating all of the items.
    """
    if isinstance(items, bytes):
        return unsigned(len(items)) + items
    else:
        return unsigned(len(items)) + b''.join(items)


def name(name):
    """Encode a text name as a UTF-8 vector."""
    return vector(name.encode('utf-8'))


def signature(argtypes, rettypes):
    return b'\x60' + vector(argtypes) + vector(rettypes)


def section(sectnum, contents):
    return bytes([sectnum]) + unsigned(len(contents)) + contents


assert unsigned(624485) == bytes([0xe5, 0x8e, 0x26])
assert unsigned(127) == bytes([0x7f])
assert signed(-624485) == bytes([0x9b, 0xf1, 0x59])
assert signed(127) == bytes([0xff, 0x00])
