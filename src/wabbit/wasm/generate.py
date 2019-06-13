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
        self.imports = []
        # Import built-in runtime functions
        self._printi = self.import_function('runtime', '_printi', [i32], [])

    def import_function(self, module, name, argtypes, rettypes):
        # Make a type signature
        typesig = b'\x60' + encode.vector(argtypes) + encode.vector(rettypes)
        self.typesigs.append(typesig)
        typeidx = len(self.typesigs) - 1

        # Make an import record
        enc = (
            encode.name(module)
            + encode.name(name)
            + b'\x00'
            + encode.unsigned(typeidx)
        )
        self.imports.append(enc)
        funcidx = len(self.imports) - 1
        return funcidx

    def encode_function(self, name, argtypes, rettypes, code):

        # Create a type signature
        typesig = b'\x60' + encode.vector(argtypes) + encode.vector(rettypes)
        self.typesigs.append(typesig)
        typeidx = len(self.typesigs) - 1

        # Add the typeidx to the functypes list
        self.functypes.append(encode.unsigned(typeidx))
        funcidx = len(self.imports) + len(self.functypes) - 1

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

    def encode_module(self):
        module = b'\x00asm\x01\x00\x00\x00'
        module += encode.section(1, encode.vector(self.typesigs))
        module += encode.section(2, encode.vector(self.imports))
        module += encode.section(3, encode.vector(self.functypes))
        module += encode.section(7, encode.vector(self.exports))
        module += encode.section(10, encode.vector(self.functions))
        return module

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
        self.wcode += b'\x10' + encode.unsigned(self._printi)


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
    encoder.encode_function("main", [], [], code)
    # print(encoder.wcode.hex())

    print('wcode:', encoder.wcode)
    print('typesigs:', encoder.typesigs)
    print('functypes:', encoder.functypes)
    print('exports:', encoder.exports)
    print('functions:', encoder.functions)

    module = encoder.encode_module()
    print('module:', module)
    with open('out.wasm', 'wb') as file:
        file.write(module)
