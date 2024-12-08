from scanner import Scanner
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

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line!s}] Error {where}: {message}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: lox.py [script]")
        exit(64)

    if len(sys.argv) == 2:
        script = sys.argv[1]
        Lox.run_file(script)
    else:
        Lox.run_prompt()