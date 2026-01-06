import sys

from Lexer.Lexer import tokenize
from Parser.Parser import Parser, ParseError
from semantic.semantic import SemanticError


def print_tokens(tokens):
    print("=== LEXER OUTPUT (TOKENS) ===")
    print("[", end="")
    first = True
    for t in tokens:
        if t.kind == "EOF":
            continue
        if not first:
            print(", ", end="")
        print(f"{t.kind}({t.value})", end="")
        first = False
    print("]")
    print()


def print_semantic(ctx):
    print("=== SEMANTIC OUTPUT ===")
    print("Declared variables:")
    if len(ctx.symbols) == 0:
        print("  (none)")
    else:
        for name in ctx.symbols:
            print("  ", name)
    print()


def print_ir(ctx):
    print("=== INTERMEDIATE CODE (IR / GOTO) ===")
    if len(ctx.code) == 0:
        print("  (no code generated)")
    else:
        for line in ctx.code:
            print("  ", line)
    print()


if __name__ == "__main__":

    source_code = """
    let x = 5;
    let y = 10;
    let z = x + y;
    

    if z > 10 {
        print z;
    } else {
        x = x + 1;
    }

    while x < 10 {
        x = x + 1;
    }
    """

    print("====================================")
    print("SOURCE CODE")
    print("====================================")
    print(source_code.strip())
    print()

    try:
        tokens = tokenize(source_code)
        print_tokens(tokens)
    except Exception as e:
        print("LEXER ERROR:")
        print(e)
        sys.exit(1)

    try:
        parser = Parser(tokens)
        ctx = parser.parse_program()
        print("=== PARSER OUTPUT ===")
        print("Parsing completed successfully.")
        print()
    except ParseError as e:
        print("PARSER ERROR:")
        print(e)
        sys.exit(1)

    except SemanticError as e:
        print("SEMANTIC ERROR:")
        print(e)
        sys.exit(1)

    print_semantic(ctx)
    print_ir(ctx)

    print("====================================")
    print("COMPILATION FINISHED SUCCESSFULLY")
    print("====================================")
