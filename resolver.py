from enum import Enum
from expr import Visitor as ExprVisitor
from runtime_error import LoxRuntimeError
from stmt import Visitor as StmtVisitor


class FunctionType(Enum):
    NONE = 0
    FUNCTION = 1


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve_statements(stmt.statements)
        self.end_scope()

    def resolve_statements(self, statements):
        for statement in statements:
            self.resolve_statement(statement)

    def resolve_statement(self, statement):
        statement.accept(self)

    def resolve_expression(self, expr):
        expr.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)

        if stmt.initializer is not None:
            self.resolve_expression(stmt.initializer)

        self.define(stmt.name)

    def declare(self, name):
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]

        if name.lexeme in scope:
            raise LoxRuntimeError(name, "Already a variable with this name in this scope.")

        scope[name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def visit_variable_expr(self, expr):
        if len(self.scopes) != 0:
            scope = self.scopes[-1]
            if scope.get(expr.name.lexeme) is False:
                raise LoxRuntimeError(expr.name, "Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)

    def resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            scope = self.scopes[i]
            if name.lexeme in scope:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def visit_assign_expr(self, expr):
        self.resolve_expression(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def resolve_function(self, function, function_type):
        enclosing_function = self.current_function
        self.current_function = function_type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve_statements(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def visit_expression_stmt(self, stmt):
        self.resolve_expression(stmt.expression)

    def visit_if_stmt(self, stmt):
        self.resolve_expression(stmt.condition)
        self.resolve_statement(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_statement(stmt.else_branch)

    def visit_print_stmt(self, stmt):
        self.resolve_expression(stmt.expression)

    def visit_return_stmt(self, stmt):
        if self.current_function == FunctionType.NONE:
            raise RuntimeError(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve_expression(stmt.value)

        return None

    def visit_while_stmt(self, stmt):
        self.resolve_expression(stmt.condition)
        self.resolve_statement(stmt.body)

    def visit_binary_expr(self, expr):
        self.resolve_expression(expr.left)
        self.resolve_expression(expr.right)

    def visit_call_expr(self, expr):
        self.resolve_expression(expr.callee)
        for arg in expr.arguments:
            self.resolve_expression(arg)

    def visit_grouping_expr(self, expr):
        self.resolve_expression(expr.expression)

    def visit_literal_expr(self, expr):
        return None

    def visit_logical_expr(self, expr):
        self.resolve_expression(expr.left)
        self.resolve_expression(expr.right)

    def visit_unary_expr(self, expr):
        self.resolve_expression(expr.right)