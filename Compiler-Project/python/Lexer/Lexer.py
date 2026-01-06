class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"{self.kind}({self.value})"


keywords = {
    "let": "LET",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE"
}

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


def tokenize(code):
    tokens = []
    pos = 0

    while pos < len(code):
        ch = code[pos]

        if ch in ' \t\n\r':
            pos += 1
            continue

        if ch.isalpha() or ch == '_':
            start = pos
            pos += 1
            while pos < len(code) and (code[pos].isalnum() or code[pos] == '_'):
                pos += 1
            word = code[start:pos]
            kind = keywords.get(word, "ID")
            tokens.append(Token(kind, word))
            continue

        if ch.isdigit():
            start = pos
            pos += 1
            while pos < len(code) and code[pos].isdigit():
                pos += 1
            tokens.append(Token("INT", int(code[start:pos])))
            continue

        if ch in symbols:
            tokens.append(Token(symbols[ch], ch))
            pos += 1
            continue

        raise Exception("Lexical error: illegal character " + ch)

    tokens.append(Token("EOF", "$"))
    return tokens
