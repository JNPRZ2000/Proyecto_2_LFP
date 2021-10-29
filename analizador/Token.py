class Token:
    def __init__(self, lexeme, type, line, column):
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.column = column
    
    def __str__(self):
        return "Lexema: {}  Tipo: {}    L: {}    C: {}\n".format(self.lexeme, self.type, self.line, self.column)