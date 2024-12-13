from environment import Environment
from lox_callable import LoxCallable


class LoxFunction(LoxCallable):
    def __init__(self, declaration):
        self.declaration = declaration

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self):
        return len(self.declaration.params)

    def call_(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for parm, arg in zip(self.declaration.params, arguments):
            environment.define(parm.lexeme, arg)
        interpreter.execute_block(self.declaration.body, environment)