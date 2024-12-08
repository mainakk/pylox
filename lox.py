from ast_printer import AstPrinter
from parser import Parser
from scanner import Scanner
from token_type import TokenType
from token_ import Token
import sys


class Lox:
    had_error = False

    @staticmethod
    def run_file(path: str):
        with open(path) as f:
            Lox.run(f.read())

        if Lox.had_error:
            exit(65)

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
        expr = parser.parse()
        if Lox.had_error:
            return

        print(AstPrinter().print(expr))

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


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: lox.py [script]")
        exit(64)

    if len(sys.argv) == 2:
        script = sys.argv[1]
        Lox.run_file(script)
    else:
        Lox.run_prompt()