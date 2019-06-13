import itertools

from . import encode


# TODO: use integers and a bytearray intead of bytes.


i32 = b'\x7f'
f64 = b'\x7c'


class WasmEncoder:
    def __init__(self):
        # List of function objects created
        self.functions = []
        self.typesigs = []
        self.functypes = []
        self.exports = []

    def encode_function(self, name, argtypes, rettypes, code):

        # Create a type signature
        typesig = b'\x60' + encode.vector(argtypes) + encode.vector(rettypes)
        self.typesigs.append(typesig)
        typeidx = len(self.typesigs) - 1

        # Add the typeidx to the functypes list
        self.functypes.append(encode.unsigned(typeidx))
        funcidx = len(self.functypes) - 1

        # Add the funcidx to the exports list
        self.exports.append(
            encode.name(name) + b'\x00' + encode.unsigned(funcidx)
        )

        # Now make the function instructions
        self.wcode = b''
        self.vars = {}
        self.vartypes = []

        for op, *opargs in code:
            getattr(self, f'encode_{op}')(*opargs)
        self.wcode += b'\x0b'

        # Create the proper encoding of the entire function
        groups = []
        for ty, items in itertools.groupby(self.vartypes):
            groups.append((len(list(items)), ty))

        parts = [encode.unsigned(count) + ty for count, ty in groups]
        enc_locals = encode.vector(parts)
        func = enc_locals + self.wcode
        self.functions.append(encode.unsigned(len(func)) + func)

    def encode_GLOBALI(self, name):
        self.vars[name] = len(self.vars)
        self.vartypes.append(b'\x7f')

    def encode_CONSTI(self, value):
        self.wcode += b'\x41' + encode.signed(value)

    def encode_STORE(self, name):
        self.wcode += b'\x21' + encode.unsigned(self.vars[name])

    def encode_LOAD(self, name):
        self.wcode += b'\x20' + encode.unsigned(self.vars[name])

    def encode_ADDI(self):
        self.wcode += b'\x6a'

    def encode_MULI(self):
        self.wcode += b'\x6c'

    def encode_PRINTI(self):
        # Not sure what to do here yet
        pass


if __name__ == '__main__':
    code = [
       ('GLOBALI', 'x'),
       ('CONSTI', 4),
       ('STORE', 'x'),
       ('GLOBALI', 'y'),
       ('CONSTI', 5),
       ('STORE', 'y'),
       ('GLOBALI', 'd'),
       ('LOAD', 'x'),
       ('LOAD', 'x'),
       ('MULI',),
       ('LOAD', 'y'),
       ('LOAD', 'y'),
       ('MULI',),
       ('ADDI',),
       ('STORE', 'd'),
       ('LOAD', 'd'),
       ('PRINTI',),
    ]

    encoder = WasmEncoder()
    encoder.encode_function("main", [], [i32], code)
    # print(encoder.wcode.hex())

    print('wcode:', encoder.wcode)
    print('typesigs:', encoder.typesigs)
    print('functypes:', encoder.functypes)
    print('exports:', encoder.exports)
    print('functions:', encoder.functions)

    assert encoder.typesigs == [b'`\x00\x01\x7f']
    assert encoder.functypes == [b'\x00']
    assert encoder.exports == [b'\x04main\x00\x00']
    assert encoder.functions == [b'\x1b\x01\x03\x7fA\x04!\x00A\x05!\x01 \x00 \x00l \x01 \x01lj!\x02 \x02\x0b']  # noqa
