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


def run_jit(module):
    import llvmlite.binding as llvm

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    compiled_mod = llvm.parse_assembly(str(module))
    engine = llvm.create_mcjit_compiler(compiled_mod, target_machine)

    # Look up the function pointer (a Python int)
    func_ptr = engine.get_function_address("hello")

    # Turn into a Python callable using ctypes
    from ctypes import CFUNCTYPE, c_int
    hello = CFUNCTYPE(c_int)(func_ptr)

    res = hello()
    print('hello() returned', res)


# Run it!
run_jit(mod)
