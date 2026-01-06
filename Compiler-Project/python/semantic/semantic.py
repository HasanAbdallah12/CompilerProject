# semantic/semantic.py

class SemanticError(Exception):
    pass


class SemanticContext:
    def __init__(self):
        self.symbols = set()
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return "t" + str(self.temp_counter)

    def new_label(self):
        self.label_counter += 1
        return "L" + str(self.label_counter)

    def declare(self, name):
        self.symbols.add(name)

    def check(self, name):
        if name not in self.symbols:
            raise SemanticError("Semantic error: variable not defined -> " + name)

    def emit(self, line):
        self.code.append(line)
