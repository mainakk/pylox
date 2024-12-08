import sys

class AstGenerator:
    @staticmethod
    def generate(output_dir: str):
        AstGenerator.define_ast(output_dir, "Expr", [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Any value",
            "Unary    : Token operator, Expr right",
            "Variable : Token name",
        ])
        AstGenerator.define_ast(output_dir, "Stmt", [
            "Expression : Expr expression",
            "Print      : Expr expression",
            "Var        : Token name, Expr initializer",
        ])
    @staticmethod
    def define_ast(output_dir: str, base_name: str, types: list[str]):
        path = output_dir + "/" + base_name.lower() + ".py"
        with open(path, "w") as f:
            f.write("from abc import ABC, abstractmethod\n")
            f.write("from dataclasses import dataclass\n")
            f.write("from typing import Any\n")
            if base_name.lower() != "expr":
                f.write("from expr import Expr\n")
            f.write("from token_ import Token\n\n\n")
            f.write(f"class {base_name}(ABC):\n")
            f.write("    @abstractmethod\n")
            f.write('    def accept(self, visitor: "Visitor") -> Any:\n')
            f.write("        pass\n\n")
            for type_ in types:
                name, fields = [x.strip() for x in type_.split(":")]
                AstGenerator.define_type(f, base_name, name, fields)

            AstGenerator.define_visitor(f, base_name, types)

    @staticmethod
    def define_type(f, base_name: str, name: str, fields: str):
        f.write("@dataclass\n")
        f.write(f"class {name}({base_name}):\n")
        for field in fields.split(", "):
            type_, filed_name = field.split(" ")
            f.write(f"    {filed_name}: {type_}\n")
        f.write(f"    def accept(self, visitor: 'Visitor') -> Any:\n")
        f.write(f"        return visitor.visit_{name.lower()}_{base_name.lower()}(self)\n\n")

    @staticmethod
    def define_visitor(f, base_name: str, types: list[str]):

        f.write(f"class Visitor(ABC):\n")
        for type_ in types:
            name = type_.split(":")[0].strip()
            f.write(f"    @abstractmethod\n")
            f.write(f"    def visit_{name.lower()}_{base_name.lower()}(self, {base_name.lower()}: {name}) -> Any:\n")
            f.write(f"        pass\n\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast.py <output directory>")
        exit(64)

    output_dir = sys.argv[1]
    AstGenerator.generate(output_dir)