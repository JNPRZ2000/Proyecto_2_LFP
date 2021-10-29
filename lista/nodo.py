class Nodo:
    def __init__(self, key):
        self.key = key
        self.back = None
        self.next = None
        self.id = None
        self.content = list()
    
    def __str__(self):
        return "Clave: {}   Contenido: {}".format(self.key, self.content)