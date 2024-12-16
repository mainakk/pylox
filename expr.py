from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from token_ import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor") -> Any:
        pass

@dataclass(unsafe_hash=True)
class Assign(Expr):
    name: Token
    value: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_assign_expr(self)

@dataclass(unsafe_hash=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_binary_expr(self)

@dataclass(unsafe_hash=True)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_call_expr(self)

@dataclass(unsafe_hash=True)
class Grouping(Expr):
    expression: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_grouping_expr(self)

@dataclass(unsafe_hash=True)
class Literal(Expr):
    value: Any
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_literal_expr(self)

@dataclass(unsafe_hash=True)
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_logical_expr(self)

@dataclass(unsafe_hash=True)
class Unary(Expr):
    operator: Token
    right: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_unary_expr(self)

@dataclass(unsafe_hash=True)
class Variable(Expr):
    name: Token
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_variable_expr(self)

class Visitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: Assign) -> Any:
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> Any:
        pass

    @abstractmethod
    def visit_call_expr(self, expr: Call) -> Any:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping) -> Any:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal) -> Any:
        pass

    @abstractmethod
    def visit_logical_expr(self, expr: Logical) -> Any:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> Any:
        pass

    @abstractmethod
    def visit_variable_expr(self, expr: Variable) -> Any:
        pass

