from environment import Environment
from lox_callable import LoxCallable
from return_exception import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self):
        return len(self.declaration.params)

    def call_(self, interpreter, arguments):
        environment = Environment(self.closure)
        for parm, arg in zip(self.declaration.params, arguments):
            environment.define(parm.lexeme, arg)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as r:
            return r.value
