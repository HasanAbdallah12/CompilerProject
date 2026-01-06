import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Lexer.Lexer import tokenize
from Parser.Parser import Parser, ParseError
from semantic.semantic import SemanticError


def run_test(name, code):
    print("===================================")
    print("TEST:", name)
    print("-----------------------------------")
    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ctx = parser.parse_program()

        print("Result: OK")
        print("IR:")
        for line in ctx.code:
            print("  ", line)

    except ParseError as e:
        print("Parser error:")
        print(" ", e)

    except SemanticError as e:
        print("Semantic error:")
        print(" ", e)

    except Exception as e:
        print("Lexer error:")
        print(" ", e)

    print()


test_simple_assign = """
let x = 5;
"""

test_arithmetic = """
let x = 5 + 2 * 3;
"""

test_undeclared_var = """
x = 5;
"""

test_if = """
let x = 5;
if x > 3 {
    x = x + 1;
} else {
    x = x - 1;
}
"""

test_while = """
let x = 0;
while x < 3 {
    x = x + 1;
}
"""

test_syntax_error = """
let x = 5
"""

test_full_program = """
let x = 5;
let y = 10;
let z = x + y;

if z > 10 {
    print z;
} else {
    print x;
}

while x < 10 {
    x = x + 1;
}
"""


if __name__ == "__main__":
    run_test("Simple assignment", test_simple_assign)
    run_test("Arithmetic expression", test_arithmetic)
    run_test("Undeclared variable", test_undeclared_var)
    run_test("If statement", test_if)
    run_test("While loop", test_while)
    run_t_
