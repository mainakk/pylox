from interpreter import Interpreter
from parser import Parser
from runtime_error import LoxRuntimeError
from scanner import Scanner
from stmt import Stmt
from token_type import TokenType
from token_ import Token


class Lox:
    interpreter = None
    had_error = False
    had_runtime_error = False

    @staticmethod
    def get_interpreter():
        if Lox.interpreter is None:
            Lox.interpreter = Interpreter()
        return Lox.interpreter

    @staticmethod
    def run_file(path: str):
        with open(path) as f:
            Lox.run(f.read())

        if Lox.had_error:
            exit(65)

        if Lox.had_runtime_error:
            exit(70)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            Lox.run(line)
            Lox.had_error = False

    @staticmethod
    def run(source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        statements = parser.parse()
        if Lox.had_error:
            return

        Lox.get_interpreter().interpret(statements)

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line!s}] Error {where}: {message}")
        Lox.had_error = True

    @staticmethod
    def parse_error(token: Token, message: str):
        if token.type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error: LoxRuntimeError):
        print(f"{error}\n[line {error.token.line}]")
        Lox.had_runtime_error = True
