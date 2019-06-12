# hellollvm.py

from llvmlite.ir import (
    Constant,
    Function,
    FunctionType,
    IntType,
    IRBuilder,
    Module,
)

mod = Module('hello')
int_type = IntType(32)
hello_func = Function(mod, FunctionType(int_type, []), name='hello')
block = hello_func.append_basic_block('entry')
builder = IRBuilder(block)
builder.ret(Constant(IntType(32), 37))
print(mod)

with open('hello.ll', 'w') as f:
    print(mod, file=f)
