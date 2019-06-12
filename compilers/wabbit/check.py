# check.py
#
# This file will have the type-checking/validation 
# part of the compiler.

from .errors import error
from .model import *
from .typesys import check_binop, check_unaryop, check_typecast

def check(node):
    if isinstance(node, Expression):
        check_Expression(node)
    elif isinstance(node, Statement):
        check_Statement(node)
    elif isinstance(node, Definition):
        check_Definition(node)
    elif isinstance(node, list):
        for item in node:
            check(item)
    else:
        raise RuntimeError(f"Can't check {node}")
            
def check_Expression(expr):
    # Some kind of checking...
    if isinstance(expr, Literal):
        pass
    elif isinstance(expr, BinOp):
        check_BinOp(expr)
    elif isinstance(expr, UnaryOp):
        check_UnaryOp(expr)
    elif isinstance(expr, TypeCast):
        check_TypeCast(expr)
    elif isinstance(expr, Location):
        check_Location(expr)
    elif isinstance(expr, FunctionCall):
        check_FunctionCall(expr)
    else:
        raise RuntimeError(f"Can't check {expr}")
    # Every expression has to have a type
    assert expr.type != None

def check_BinOp(expr):
    check(expr.left)
    check(expr.right)
    # Is the operator supported?
    expr.type = check_binop(expr.op, expr.left.type, expr.right.type)
    if not expr.type:
        error(f'Type error: {expr.left.type}{expr.op}{expr.right.type}')
        # An issue here.  If the operation is not supported, what do we set
        # the expr.type to?  Do we leave it None?   Note: ALL expressions
        # must be assigned a type.
        expr.type = Type('<error>')

    
def check_UnaryOp(expr):
    check(expr.operand)
    expr.type = check_unaryop(expr.op, expr.operand.type)
    if not expr.type:
        error(f'Type error: {expr.op}{expr.operand.type}')
        expr.type = Type('<error>')

def check_TypeCast(expr):
    check(expr.value)
    expr.type = check_typecast(expr.value.type, expr.to_type)
    if not expr.type:
        error(f"Type error: Can't cast {expr.value.type} -> {expr.to_type}")
        expr.type = Type('<error>')

def check_FunctionCall(expr):
    # Check all of the function arguments first
    check(expr.args)
    expr.type = expr.func.return_type
    
    # Check argument counts
    if len(expr.func.parameters) != len(expr.args):
        error(f'Expected {len(expr.func.parameters)} arguments.')
        
    # Check argument/parameter types
    for parm, arg in zip(expr.func.parameters, expr.args):
        if parm.type != arg.type:
            error(f'Type error in argument {parm.name}. {parm.type} != {arg.type}')

def check_Location(expr):
    if isinstance(expr, DefnLocation):
        check_DefnLocation(expr)
    elif isinstance(expr, PointerLocation):
        check_PointerLocation(expr)
    else:
        raise RuntimeError(f"Can't check {expr}")

def check_DefnLocation(node):
    # Propagate the type
    node.type = node.defn.type
    # What about mutability?
    if node.usage == 'store' and not node.defn.mutable:
        error(f"Can't assign to {defn.name}")

def check_PointerLocation(node):
    check(node.address)
    if node.address.type != Type('int'):
        error("Memory address must be int")
    node.type = Type('<infer>')    # Type is inferred by context
    
def check_Statement(node):
    if isinstance(node, Assignment):
        check_Assignment(node)
    elif isinstance(node, Print):
        check_Print(node)
    elif isinstance(node, Return):
        check_Return(node)
    elif isinstance(node, (Break, Continue)):
        pass
    elif isinstance(node, If):
        check_If(node)
    elif isinstance(node, While):
        check_While(node)
    else:
        raise RuntimeError(f"Can't check {node}")
    
# location = value;
def check_Assignment(node):
    check(node.location)
    check(node.value)
    if node.value.type == Type('<infer>'):
        node.value.type = node.location.type
    if node.location.type != node.value.type:
        error("Type error. {node.location.type} != {node.value.type}")

def check_Print(node):
    check(node.value)

def check_Return(node):
    check(node.value)
    if node.value.type != node.func.return_type:
        error(f"Type error. Function returned {node.value.type}. "
              f"Expected {node.func.return_type}")

def check_If(node):
    check(node.test)
    if node.test.type != Type('bool'):
        error(f"Test must evaluate to bool. Got {node.test.type}")
    check(node.consequence)
    check(node.alternative)

def check_While(node):
    check(node.test)
    if node.test.type != Type('bool'):
        error(f"While test must evaluate to bool. Got {node.test.type}")
    check(node.body)

def check_Definition(node):
    if isinstance(node, Variable):
        check_Variable(node)
    elif isinstance(node, Function):
        check_Function(node)
    else:
        raise RuntimeError(f"Can't check {node}")

def check_Variable(node):
    if node.value:
        check(node.value)
        # If the node type was unset, set it
        if not node.type:
            node.type = node.value.type
    if node.value.type != node.type:
        error(f"Type error in declaration of {node.name}. {node.type} != {node.value.type}")

def check_Function(node):
    if node.statements:
        check(node.statements)
