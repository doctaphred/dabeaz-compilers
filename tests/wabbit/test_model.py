from wabbit import model
from wabbit.typesys import WabbitType


def test_stuff():
    model.Integer(0)
    model.Float(0.0)
    model.Bool(False)
    model.Character('a')


def test_type_check():
    assert WabbitType.int(model.Integer(0))
    assert WabbitType.float(model.Float(0.0))
    assert WabbitType.bool(model.Bool(False))
    assert WabbitType.char(model.Character('a'))
