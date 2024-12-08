from typing import Any
from expr import Expr, Grouping, Literal, Unary, Visitor
from runtime_error import LoxRuntimeError
from token_type import TokenType
from token_ import Token


class Interpreter(Visitor):
    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self.is_truthy(right)
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right

        return None

    def check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def is_truthy(self, value: Any) -> bool:
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        return True

    def visit_binary_expr(self, expr: Expr) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case TokenType.PLUS:
                if (isinstance(left, float) and isinstance(right, float)) or (isinstance(left, str) and isinstance(right, str)):
                    return left + right

                raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right

        return None

    def is_equal(self, left: Any, right: Any) -> bool:
        if left is None and right is None:
            return True

        if left is None:
            return False

        return left == right

    def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return

        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def interpret(self, expr: Expr) -> None:
        from lox import Lox
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except LoxRuntimeError as e:
            Lox.runtime_error(e)

    def stringify(self, value: Any) -> str:
        if value is None:
            return "nil"

        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        return str(value)