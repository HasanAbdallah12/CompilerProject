from semantic.semantic import SemanticContext, SemanticError


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ctx = SemanticContext()

        self.val_stack = []
        self.assign_target = None

        self.table = {

            ("program", "LET"): ["stmlist", "EOF"],
            ("program", "PRINT"): ["stmlist", "EOF"],
            ("program", "IF"): ["stmlist", "EOF"],
            ("program", "WHILE"): ["stmlist", "EOF"],
            ("program", "ID"): ["stmlist", "EOF"],
            ("program", "EOF"): ["stmlist", "EOF"],

            ("stmlist", "LET"): ["stmt", "stmlist"],
            ("stmlist", "PRINT"): ["stmt", "stmlist"],
            ("stmlist", "IF"): ["stmt", "stmlist"],
            ("stmlist", "WHILE"): ["stmt", "stmlist"],
            ("stmlist", "ID"): ["stmt", "stmlist"],
            ("stmlist", "RBRACE"): [],
            ("stmlist", "EOF"): [],

            ("stmt", "LET"): ["LET", "ID", "#DECL", "ASSIGN", "expr", "#ASSIGN", "SEMI"],
            ("stmt", "ID"): ["ID", "#TARGET", "ASSIGN", "expr", "#ASSIGN", "SEMI"],
            ("stmt", "PRINT"): ["PRINT", "expr", "#PRINT", "SEMI"],

            ("stmt", "IF"): [
                "IF", "expr_rel", "LBRACE", "stmlist", "RBRACE",
                "ELSE", "LBRACE", "stmlist", "RBRACE"
            ],

            ("stmt", "WHILE"): [
                "WHILE", "expr_rel", "LBRACE", "stmlist", "RBRACE"
            ],

            ("expr_rel", "ID"): ["expr", "expr_rel_tail"],
            ("expr_rel", "INT"): ["expr", "expr_rel_tail"],
            ("expr_rel", "LPAREN"): ["expr", "expr_rel_tail"],

            ("expr_rel_tail", "GT"): ["GT", "expr", "#REL"],
            ("expr_rel_tail", "LT"): ["LT", "expr", "#REL"],
            ("expr_rel_tail", "LBRACE"): [],

            ("expr", "ID"): ["term", "expr_tail"],
            ("expr", "INT"): ["term", "expr_tail"],
            ("expr", "LPAREN"): ["term", "expr_tail"],

            ("expr_tail", "PLUS"): ["PLUS", "term", "#ADD", "expr_tail"],
            ("expr_tail", "MINUS"): ["MINUS", "term", "#SUB", "expr_tail"],
            ("expr_tail", "SEMI"): [],
            ("expr_tail", "RPAREN"): [],
            ("expr_tail", "RBRACE"): [],
            ("expr_tail", "GT"): [],
            ("expr_tail", "LT"): [],
            ("expr_tail", "LBRACE"): [],

            ("term", "ID"): ["factor", "term_tail"],
            ("term", "INT"): ["factor", "term_tail"],
            ("term", "LPAREN"): ["factor", "term_tail"],

            ("term_tail", "MUL"): ["MUL", "factor", "#MUL", "term_tail"],
            ("term_tail", "DIV"): ["DIV", "factor", "#DIV", "term_tail"],
            ("term_tail", "PLUS"): [],
            ("term_tail", "MINUS"): [],
            ("term_tail", "SEMI"): [],
            ("term_tail", "RPAREN"): [],
            ("term_tail", "RBRACE"): [],
            ("term_tail", "GT"): [],
            ("term_tail", "LT"): [],
            ("term_tail", "LBRACE"): [],

            ("factor", "ID"): ["ID", "#PUSH_ID"],
            ("factor", "INT"): ["INT", "#PUSH_INT"],
            ("factor", "LPAREN"): ["LPAREN", "expr", "RPAREN"],
        }

    def current(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def semantic_action(self, action):
        if action == "#PUSH_ID":
            name = self.tokens[self.pos - 1].value
            self.ctx.check(name)
            self.val_stack.append(name)

        elif action == "#PUSH_INT":
            self.val_stack.append(str(self.tokens[self.pos - 1].value))

        elif action in ("#ADD", "#SUB", "#MUL", "#DIV"):
            b = self.val_stack.pop()
            a = self.val_stack.pop()
            t = self.ctx.new_temp()
            op = action[1:].lower()
            self.ctx.code.append(f"{t} = {a} {op} {b}")
            self.val_stack.append(t)

        elif action == "#DECL":
            name = self.tokens[self.pos - 1].value
            self.ctx.declare(name)
            self.assign_target = name

        elif action == "#TARGET":
            self.assign_target = self.tokens[self.pos - 1].value

        elif action == "#ASSIGN":
            value = self.val_stack.pop()
            self.ctx.code.append(f"{self.assign_target} = {value}")
            self.assign_target = None

        elif action == "#PRINT":
            value = self.val_stack.pop()
            self.ctx.code.append(f"print {value}")

        elif action == "#REL":
            self.val_stack.pop()
            self.val_stack.pop()

    def parse_program(self):
        stack = ["EOF", "program"]

        while stack:
            top = stack.pop()
            lookahead = self.current().kind

            if isinstance(top, str) and top.startswith("#"):
                self.semantic_action(top)
                continue

            if top.isupper() or top == "EOF":
                if top != lookahead:
                    raise ParseError(f"Expected {top}, got {lookahead}")
                self.advance()
                continue

            key = (top, lookahead)
            if key not in self.table:
                raise ParseError(f"No rule for ({top}, {lookahead})")

            production = self.table[key]
            for sym in reversed(production):
                stack.append(sym)

        return self.ctx
