from wabbit import model
from wabbit.typesys import WabbitType


def test_stuff():
    model.IntLiteral(0)
    model.FloatLiteral(0.0)
    model.BoolLiteral(False)
    model.CharLiteral('a')


def test_type_check():
    assert WabbitType.int(model.IntLiteral(0))
    assert WabbitType.float(model.FloatLiteral(0.0))
    assert WabbitType.bool(model.BoolLiteral(False))
    assert WabbitType.char(model.CharLiteral('a'))
