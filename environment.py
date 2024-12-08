from runtime_error import LoxRuntimeError


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")