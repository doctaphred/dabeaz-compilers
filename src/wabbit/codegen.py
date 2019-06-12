import itertools

from .utils import leb


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


class Interpreter:
    def __init__(self):
        self.store = {}
        self.stack = []
        self.pc = 0

    def run(self, code):
        self.pc = 0
        while self.pc < len(code):
            op, *opargs = code[self.pc]
            getattr(self, f'run_{op}')(*opargs)
            self.pc += 1

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def run_GLOBALI(self, name):
        self.store[name] = None

    def run_CONSTI(self, value):
        self.push(value)

    def run_STORE(self, name):
        self.store[name] = self.pop()

    def run_LOAD(self, name):
        self.push(self.store[name])

    def run_ADDI(self):
        self.push(self.pop() + self.pop())

    def run_MULI(self):
        self.push(self.pop() * self.pop())

    def run_PRINTI(self):
        print(self.pop())


class PythonTranspiler:
    def __init__(self):
        self.stack = []
        self.lines = []

    def translate(self, code):
        self.emit('def main():')
        for op, *args in code:
            getattr(self, f'translate_{op}')(*args)
        self.emit('main()')
        return '\n'.join(self.lines)

    def push(self, fragment):
        self.stack.append(fragment)

    def pop(self):
        return self.stack.pop()

    def emit(self, line):
        self.lines.append(line)

    def translate_GLOBALI(self, name):
        pass

    def translate_CONSTI(self, value):
        self.push(repr(value))

    def translate_STORE(self, name):
        self.emit(f'    {name} = {self.pop()}')

    def translate_LOAD(self, name):
        self.push(name)

    def translate_ADDI(self):
        self.push(f'({self.pop()} + {self.pop()})')

    def translate_MULI(self):
        self.push(f'({self.pop()} * {self.pop()})')

    def translate_PRINTI(self):
        self.emit(f'    print({self.pop()})')


class CTranspiler:
    def __init__(self):
        self.stack = []
        self.lines = []

    def translate(self, code):
        self.emit('#include <stdio.h>')
        self.emit('int main() {')
        for op, *args in code:
            getattr(self, f'translate_{op}')(*args)
        self.emit('}')
        return '\n'.join(self.lines)

    def push(self, fragment):
        self.stack.append(fragment)

    def pop(self):
        return self.stack.pop()

    def emit(self, line):
        self.lines.append(line)

    def translate_GLOBALI(self, name):
        self.emit(f'    int {name};')

    def translate_CONSTI(self, value):
        self.push(repr(value))

    def translate_STORE(self, name):
        self.emit(f'    {name} = {self.pop()};')

    def translate_LOAD(self, name):
        self.push(name)

    def translate_ADDI(self):
        self.push(f'({self.pop()} + {self.pop()})')

    def translate_MULI(self):
        self.push(f'({self.pop()} * {self.pop()})')

    def translate_PRINTI(self):
        self.emit(fr'    printf("%i\n", {self.pop()});')


class WasmEncoder:
    def __init__(self):
        # List of function objects created
        self.functions = []

    def encode(self, code):
        self.wcode = bytearray()
        self.vars = {}
        self.vartypes = []

        for op, *opargs in code:
            getattr(self, f'encode_{op}')(*opargs)

        # Put a block terminator on the code
        self.wcode.append(0x0b)

        # Create the proper encoding of the entire function
        groups = []
        for ty, items in itertools.groupby(self.vartypes):
            groups.append((len(list(items)), ty))

        parts = [leb.unsigned(count) + ty for count, ty in groups]
        enc_locals = leb.vector(parts)
        func = enc_locals + self.wcode
        self.functions.append(leb.unsigned(len(func)))
        self.functions += func

    def encode_GLOBALI(self, name):
        self.vars[name] = len(self.vars)
        # TODO: make this an int
        self.vartypes.append(b'7f')

    def encode_CONSTI(self, value):
        self.wcode.append(0x41)
        self.wcode += leb.signed(value)

    def encode_STORE(self, name):
        self.wcode.append(0x21)
        self.wcode += leb.unsigned(self.vars[name])

    def encode_LOAD(self, name):
        self.wcode.append(0x20)
        self.wcode += leb.unsigned(self.vars[name])

    def encode_ADDI(self):
        self.wcode.append(0x6a)

    def encode_MULI(self):
        self.wcode.append(0x6c)

    def encode_PRINTI(self):
        # Not sure what to do here yet
        pass


if __name__ == '__main__':
    interp = Interpreter()
    interp.run(code)

    py_transp = PythonTranspiler()
    python = py_transp.translate(code)
    print(python)
    exec(python)

    c_transp = CTranspiler()
    c = c_transp.translate(code)
    print(c)
    with open('ayy.c', 'w') as f:
        print(c, file=f)

    encoder = WasmEncoder()
    encoder.encode(code)
    print(encoder.wcode)
    print(encoder.wcode.hex())
