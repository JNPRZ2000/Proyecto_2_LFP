from tkinter import INSERT
from lista.lista import Lista
class Sintax:
    def __init__(self, tokens, outputText):
        self.tokens = tokens
        self.errores = []
        self.tokens.reverse()
        self.output = outputText
        self.keys = Lista()
        self.flag = bool
        self.flag2 = bool
        self.data = list()
        self.reserved = ['PR_imprimir', 'PR_imprimirln', 'PR_Claves', 'PR_Registros', 'PR_conteo',
        'PR_promedio', 'PR_contarsi', 'PR_datos', 'PR_sumar', 'PR_max', 'PR_min', 'PR_exportar']
    
    def addError(self, token, expected):
        self.errores.append(
            "<ERROR SINTÁCTICO> Se obtuvo {}, se esperaba {}. Fila: {}, Columna: {}".format(
                token.type,expected,token.line,token.column))
        if token.type in self.reserved:
            self.tokens.append(token)
        else:
            self.delete()  
    def delete(self):
        if len(self.tokens) > 0:
            temp = self.tokens[-1]
            if temp.type in self.reserved:
                pass
            else:
                self.tokens.pop()
                self.delete()
    
    def analyze(self):
        self.inicio()
    def inicio(self):
        try:
            if len(self.tokens) > 0:
                temp = self.tokens.pop()
                if temp.type == 'PR_imprimir':
                    self.imprimir()
                    self.inicio()
                elif temp.type == 'PR_imprimirln':
                    self.imprimirln()
                    self.inicio()
                elif temp.type == 'PR_conteo':
                    self.conteo()
                    self.inicio()
                elif temp.type == 'PR_promedio':
                    self.promedio()
                    self.inicio()
                elif temp.type == 'PR_contarsi':
                    self.contarsi()
                    self.inicio()
                elif temp.type == 'PR_sumar':
                    self.sumar()
                    self.inicio()
                elif temp.type == 'PR_max':
                    self.max()
                    self.inicio()
                elif temp.type == 'PR_min':
                    self.min()
                    self.inicio()
                elif temp.type == 'PR_exportar':
                    self.exportar()
                    self.inicio()
                elif temp.type == 'PR_Claves':
                    self.claves()
                    self.inicio()
                elif temp.type == 'PR_Registros':
                    self.registros()
                    self.inicio()
                elif temp.type == 'PR_datos':
                    self.datosi()
                    self.inicio()
                else:
                    self.addError(temp, 'instruccion')
        except IndexError:
            pass
    
    def registros(self):
        temp = self.tokens.pop()
        if temp.type == 'igual':
            temp = self.tokens.pop()
            if temp.type == 'corcheteI':
                self.registro()
                if self.flag == True:
                    temp = self.tokens.pop()
                    if temp.type == 'corcheteD':
                        i = 0
                        j =0
                        while i < len(self.data):
                                self.keys.addById(j,self.data[i])
                                j += 1
                                i += 1
                                if j == self.keys.size:
                                    j = 0
                        print("Registro exitoso")
                    else:
                        self.data = list()
                        self.addError(temp, ']')
                else:
                    self.data = list()
            else:
                self.addError(temp, '[')
        else:
            self.addError(temp, '=')
        self.flag = False
    def registro(self):
        self.flag2 = False
        temp = self.tokens.pop()
        if temp.type == 'llaveI':
            self.datos()
            if self.flag2 == True:
                temp = self.tokens.pop()
                if temp.type == 'llaveD':
                    temp = self.tokens[-1]
                    if temp.type == 'llaveI':
                        self.registro()
                    elif temp.type == 'corcheteD':
                        self.flag = True
                    else:
                        self.tokens.pop()
                        self.addError(temp, '{ | ]')
                        self.flag = False
                else:
                    self.addError(temp, '}')
            else:
                pass
        else:
            self.addError(temp,'{')
    def datos(self):
        temp = self.tokens.pop()
        if temp.type == 'comilla':
            temp = self.tokens.pop()
            if temp.type == 'cadena':
                self.data.append(temp.lexeme)
                temp = self.tokens.pop()
                if temp.type == 'comilla':
                    aux = self.tokens[-1]
                    if aux.type == 'coma':
                        self.tokens.pop()
                        self.datos()
                    elif aux.type == 'llaveD':
                        self.flag2 = True
                    else:
                        self.tokens.pop()
                        self.addError(aux, ', | }')
                else:
                    self.addError(temp, '\"')
            else:
                self.addError(temp, 'cadena')
        elif temp.type == 'numero':
            self.data.append(float(temp.lexeme))
            aux = self.tokens[-1]
            if aux.type == 'coma':
                self.tokens.pop()
                self.datos()
            elif aux.type == 'llaveD':
                self.flag2 = True
            else:
                self.tokens.pop()
                self.addError(aux, ', | }')
        else:
            self.addError(temp, '\" | numero')

    def claves(self):
        self.flag = False
        temp = self.tokens.pop()
        if temp.type == 'igual':
            temp = self.tokens.pop()
            if temp.type == 'corcheteI':
                self.clave()
                if self.flag == True:
                    temp = self.tokens.pop()
                    if temp.type == 'corcheteD':
                        print("Claves: exito")
                    else:
                        self.keys = Lista()
                        self.addError(temp, ']')
                else:
                    self.keys = Lista()
            else:
                self.addError(temp, '[')
        else:
            self.addError(temp, '=')
        self.flag = False
    def clave(self):
        temp = self.tokens.pop()
        if temp.type == 'comilla':
            temp = self.tokens.pop()
            if temp.type == 'cadena':
                self.keys.insert(temp.lexeme)
                temp = self.tokens.pop()
                if temp.type == 'comilla':
                    aux = self.tokens[-1]
                    if aux.type == 'coma':
                        self.tokens.pop()
                        self.clave()
                    elif aux.type == 'corcheteD':
                        self.flag = True
                    else:
                        self.tokens.pop()
                        self.addError(temp, ', | ]')
                else:
                    self.addError(temp, '\"')
            else:
                self.addError(temp, 'cadena')
        else:
            self.addError(temp, '\"')

    def imprimir(self):
        cadena = ''
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena += temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'parentesisD':
                            temp = self.tokens.pop()
                            if temp.type == 'puntocoma':
                                self.output.config(state = 'normal')
                                self.output.insert(INSERT, cadena)
                                self.output.config(state = 'disabled')
                            else:
                                self.addError(temp, ';')
                        else:
                            self.addError(temp, ')')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else: 
            self.addError(temp, '(')
    def imprimirln(self):
        cadena = '\n'
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena += temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'parentesisD':
                            temp = self.tokens.pop()
                            if temp.type == 'puntocoma':
                                self.output.config(state = 'normal')
                                self.output.insert(INSERT, cadena)
                                self.output.config(state = 'disabled')
                            else:
                                self.addError(temp, ';')
                        else:
                            self.addError(temp, ')')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else: 
            self.addError(temp, '(')

    def conteo(self):
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'parentesisD':
                temp = self.tokens.pop()
                if temp.type == 'puntocoma':
                    conteo = '\n>> Conteo: {}'.format(len(self.data))
                    self.output.config(state = 'normal')
                    self.output.insert(INSERT, conteo)
                    self.output.config(state = 'disabled')
                else:
                    self.addError(temp, ';')
            else:
                self.addError(temp, ')')
        else:
            self.addError(temp, '(')

    def promedio(self):
        cadena = ''
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena += temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'parentesisD':
                            temp = self.tokens.pop()
                            if temp.type == 'puntocoma':
                                promedio = self.keys.promedio(cadena)
                                self.output.config(state = 'normal')
                                self.output.insert(INSERT, promedio)
                                self.output.config(state = 'disabled')
                            else:
                                self.addError(temp, ';')
                        else:
                            self.addError(temp, ')')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else:
            self.addError(temp, '(')

    def contarsi(self): 
        cadena = ''
        numero = 0
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena += temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'coma':
                            temp = self.tokens.pop()
                            if temp.type == 'numero':
                                numero += float(temp.lexeme)
                                temp = self.tokens.pop()
                                if temp.type == 'parentesisD':
                                    temp = self.tokens.pop()
                                    if temp.type == 'puntocoma':
                                        contarsi = self.keys.contarsi(cadena, numero)
                                        self.output.config(state = 'normal')
                                        self.output.insert(INSERT, contarsi)
                                        self.output.config(state = 'disabled')
                                    else:
                                        self.addError(temp, ';')
                                else:
                                    self.addError(temp, ')')
                            else:
                                self.addError(temp, 'numero')
                        else:
                            self.addError(temp, ',')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else:
            self.addError(temp, '(')

    def sumar(self):
        cadena = ''
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena+=temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'parentesisD':
                            temp = self.tokens.pop()
                            if temp.type == 'puntocoma':
                                sumar = self.keys.sumar(cadena)
                                self.output.config(state = 'normal')
                                self.output.insert(INSERT, sumar)
                                self.output.config(state = 'disabled')
                            else:
                                self.patch(temp)
                                self.addError(temp, ';')
                        else:
                            self.patch(temp)
                            self.addError(temp, ')')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else:
            self.addError(temp, '(')

    def max(self):
        cadena = ''
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena += temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'parentesisD':
                            temp = self.tokens.pop()
                            if temp.type == 'puntocoma':
                                max = self.keys.max(cadena)
                                self.output.config(state = 'normal')
                                self.output.insert(INSERT, max)
                                self.output.config(state  = 'disabled')
                            else:
                                self.addError(temp, ';')
                        else:
                            self.addError(temp, ')')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else:
            self.addError(temp, '(')

    def min(self):
        cadena = ''
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena += temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'parentesisD':
                            temp = self.tokens.pop()
                            if temp.type == 'puntocoma':
                                min = self.keys.min(cadena)
                                self.output.config(state = 'normal')
                                self.output.insert(INSERT, min)
                                self.output.config(state  = 'disabled')
                            else:
                                self.addError(temp, ';')
                        else:
                            self.addError(temp, ')')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else:
            self.addError(temp, '(')

    def exportar(self):
        cadena = ''
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'comilla':
                temp = self.tokens.pop()
                if temp.type == 'cadena':
                    cadena += temp.lexeme
                    temp = self.tokens.pop()
                    if temp.type == 'comilla':
                        temp = self.tokens.pop()
                        if temp.type == 'parentesisD':
                            temp = self.tokens.pop()
                            if temp.type == 'puntocoma':
                                self.keys.exportar(cadena, self.data)
                            else:
                                self.addError(temp, ';')
                        else:
                            self.addError(temp, ')')
                    else:
                        self.addError(temp, '\"')
                else:
                    self.addError(temp, 'cadena')
            else:
                self.addError(temp, '\"')
        else:
            self.addError(temp, '(')

    def datosi(self):
        temp = self.tokens.pop()
        if temp.type == 'parentesisI':
            temp = self.tokens.pop()
            if temp.type == 'parentesisD':
                temp = self.tokens.pop()
                if temp.type == 'puntocoma':
                    datos = self.keys.datos(self.data)
                    self.output.config(state = 'normal')
                    self.output.insert(INSERT, datos)
                    self.output.config(state = 'disabled')
                else:
                    self.addError(temp, ';')
            else:
                self.addError(temp, ')')
        else:
            self.addError(temp, '(')

    def printError(self):
        self.s = 'Errores:\n'
        for error in self.errores:
            self.s += '\n{}'.format(error)
        return self.s
