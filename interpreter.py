import time
from typing import Any
from environment import Environment
from expr import Assign, Expr, Grouping, Literal, Logical, Unary, Variable
from expr import Visitor as ExprVisitor
from lox_callable import LoxCallable
from lox_function import LoxFunction
from return_exception import Return
from runtime_error import LoxRuntimeError
from stmt import Block, Expression, If, Print, Stmt, Var, While
from stmt import Visitor as StmtVisitor
from token_type import TokenType
from token_ import Token


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call_(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self) -> None:
        self.globals = Environment()
        self.environment = self.globals

        self.globals.define("clock", Clock())

        self.locals = {}


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

    def interpret(self, statements: list[Stmt]) -> None:
        from lox import Lox
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as e:
            Lox.runtime_error(e)

    def stringify(self, value: Any) -> str:
        if value is None:
            return "nil"

        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        return str(value)

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int) -> None:
        self.locals[expr] = depth

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt: Var) -> Any:
        value = None

        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name: Token, expr: Expr) -> Any:
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)

        return self.globals.get(name)

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)

        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visit_block_stmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_if_stmt(self, stmt: If) -> None:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_logical_expr(self, expr: Logical) -> Any:
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left

        if expr.operator.type == TokenType.AND:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)


    def visit_while_stmt(self, stmt: While) -> None:
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(argument) for argument in expr.arguments]

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        if len(arguments) != callee.arity():
            raise LoxRuntimeError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}")

        return callee.call_(self, arguments)


    def visit_function_stmt(self, stmt):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def visit_return_stmt(self, stmt):
        value = None

        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)