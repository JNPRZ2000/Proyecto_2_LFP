class Error:
    
    def __init__(self, descripcion, linea, columna):
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna
    
    def __str__(self):
        return "Error: {}   L: {}   C: {}\n".format(self.descripcion, self.linea, self.columna)