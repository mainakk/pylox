from io import StringIO
from Expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from lox import Token, TokenType


class AstPrinter(Visitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value == None:
            return "nil"

        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *arg) -> str:
        output = StringIO()
        output.write("(" + name)
        for expr in arg:
            output.write(" " + expr.accept(self))
        output.write(")")
        return output.getvalue()


if __name__ == "__main__":
    expr = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123),
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
    print(AstPrinter().print(expr))
