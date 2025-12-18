#LEXER__
#Terminals = {let, print, if, while, id, num, +, -, *, /, (, ), =, {, }}
#decraling terminals:
LET = "LET"#let
PRINT = "PRINT"#print
IF = "IF"#if
WHILE = "WHILE"#while
ELSE = "ELSE"#else
ID = "ID"#id
NUM = "NUM"#num
PLUS = "PLUS"#+
MINUS = "MINUS"#-
MULTIPLY = "MULTIPLY"#*
DIVIDE = "DIVIDE"#/
ASSIGN = "ASSIGN"#=
SEMICOLON = "SEMICOLON"#;
LEFTPAREN = "LEFTPAREN"#(
RIGHTPAREN = "RIGHTPAREN"#)
LEFTBRACE = "LEFTBRACE"#{
RIGHTBRACE = "RIGHTBRACE"#}

# keywords in our language
KEYWORDS = {
    "let": LET,
    "print": PRINT,
    "if": IF,
    "while": WHILE,
    "else": ELSE
}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.currentIndex = 0
        if text is not None:
            self.currentChar = text[0]  # point to first char
        else:
            self.currentChar = None

    def nextChar(self):  # move to next char
        if self.currentIndex + 1 >= len(self.text):
            self.currentChar = None
        else:
            self.currentIndex += 1
            self.currentChar = self.text[self.currentIndex]  # fix typo

    def skip_space(self):
        while self.currentChar is not None and self.currentChar == ' ':
            self.nextChar()

    def printcurrent(self):
        print(self.currentChar)


example = Lexer("hello my name is hassan")
while example.currentChar is not None:
    example.skip_space()
    example.printcurrent()
    example.nextChar()