from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from expr import Expr
from token_ import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor") -> Any:
        pass

@dataclass
class Block(Stmt):
    statements: list[Stmt]
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_block_stmt(self)

@dataclass
class Expression(Stmt):
    expression: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_expression_stmt(self)

@dataclass
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_function_stmt(self)

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_if_stmt(self)

@dataclass
class Print(Stmt):
    expression: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_print_stmt(self)

@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_var_stmt(self)

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt
    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit_while_stmt(self)

class Visitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: Block) -> Any:
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression) -> Any:
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt: Function) -> Any:
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: If) -> Any:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: Print) -> Any:
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: Var) -> Any:
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt: While) -> Any:
        pass

