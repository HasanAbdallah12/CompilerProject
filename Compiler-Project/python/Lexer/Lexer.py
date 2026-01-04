
# ----------------------------------
# Token object
# ----------------------------------
class Token:
    def __init__(self, kind, value):
        self.kind = kind     # token type: ID, INT, PLUS...
        self.value = value  # actual value: x, 5, +

    def __repr__(self):
        return f"{self.kind}({self.value})"


# ----------------------------------
# Keywords in the language
# ----------------------------------
keywords = {
    "let": "LET",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE"
}

# ----------------------------------
# Single character tokens
# ----------------------------------
symbols = {
    '+': "PLUS",
    '-': "MINUS",
    '*': "MUL",
    '/': "DIV",
    '=': "ASSIGN",
    '>': "GT",
    '<': "LT",
    '(': "LPAREN",
    ')': "RPAREN",
    '{': "LBRACE",
    '}': "RBRACE",
    ';': "SEMI"
}


# ----------------------------------
# Lexer function
# ----------------------------------
def tokenize(code):
    token_list = []
    pos = 0

    while pos < len(code):
        current = code[pos]

        # skip spaces and new lines
        if current in ' \t\n\r':
            pos += 1
            continue

        # identifier or keyword
        if current.isalpha() or current == '_':
            start = pos
            pos += 1

            while pos < len(code) and (code[pos].isalnum() or code[pos] == '_'):
                pos += 1

            word = code[start:pos]

            if word in keywords:
                token_list.append(Token(keywords[word], word))
            else:
                token_list.append(Token("ID", word))

            continue

        # number
        if current.isdigit():
            start = pos
            pos += 1

            while pos < len(code) and code[pos].isdigit():
                pos += 1

            value = int(code[start:pos])
            token_list.append(Token("INT", value))
            continue

        # single character symbol
        if current in symbols:
            token_list.append(Token(symbols[current], current))
            pos += 1
            continue

        # unknown character
        raise Exception("Lexical error: illegal character " + current)

    token_list.append(Token("EOF", "$"))
    return token_list


# ----------------------------------
# Print tokens nicely
# ----------------------------------
def show_tokens(tokens):
    print("[" + ", ".join(str(t) for t in tokens if t.kind != "EOF") + "]")


# ----------------------------------
# Simple test
# ----------------------------------
if __name__ == "__main__":
    source_code = """
    let x = 5 + 2;
    if x > 3 {
        print x;
    }
    """

    result = tokenize(source_code)
    show_tokens(result)
