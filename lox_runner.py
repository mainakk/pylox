import sys
from lox import Lox


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: lox.py [script]")
        exit(64)

    if len(sys.argv) == 2:
        script = sys.argv[1]
        Lox.run_file(script)
    else:
        Lox.run_prompt()