from wabbit import lexer, model
from wabbit.utils.peekable import Peekable
from wabbit.utils.reprs import vars_repr


class Parser(Peekable):
    """Predictive recursive descent parser."""

    class Error(Exception):
        def __init__(self, token):
            super().__init__()
            self.token = token

        __repr__ = vars_repr

    @classmethod
    def tokenize(cls, text):
        return cls(lexer.tokenize(text))

    def accept(self, *options):
        kind, text = token = self._next
        if kind in options:
            self._advance()
            return token
        else:
            return None

    def expect(self, *options):
        kind, text = token = self._next
        if kind in options:
            return token
        else:
            raise self.Error(token)

    def parse_Expression(self):
        # expr : term { +|- term }
        left = self.parse_Term()
        while True:
            token = self.accept('plus', 'minus')
            if not token:
                break
            right = self.parse_Term()
            left = model.InfixOp(token[1], left, right)
        return left

    def parse_Term(self):
        # term : factor { *|/ factor }
        left = self.parse_Factor()
        while True:
            token = self.accept('times', 'divide')
            if not token:
                break
            right = self.parse_Factor()
            left = model.InfixOp(token[1], left, right)
        return left

    def parse_Factor(self):
        # factor : literal | lparen expr rparen | (+|-) factor
        if self.accept('lparen'):
            expr = self.parse_Expression()
            self.expect('rparen')
            return expr
        elif self.accept('plus', 'minus'):
            token = self.accept('plus', 'minus')
            factor = self.parse_Factor()
            return model.PrefixOp(token[1], factor)
        else:
            return self.parse_Literal()

    def parse_Variable(self):
        # const name = expression;
        # var name type [ = expression ] ;
        # const|var name [type] [= expression] ;
        self.expect('const', 'var')
        _, name = self.expect('word')

    def parse_Int(self):
        _, text = self.expect('int')

    def __next__(self):
        pass
