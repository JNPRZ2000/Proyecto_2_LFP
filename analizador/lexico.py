from analizador.Token import Token
from analizador.Error import Error

class Lexico:
    def __init__(self, text):
        self.text = text
        self.listToken = []
        self.listError = []
        self.column = 1
        self.line = 1
        self.i = 0
        self.buffer = ''
        self.estado = 'e0'
        self.anterior = 'void'
            
    def addToken(self, type):
        if self.anterior == 'numero':
            self.buffer == float(self.buffer)
            self.anterior == 'void'
        self.listToken.append(Token(self.buffer,type,self.line, self.column))
        self.buffer = ''
        self.estado = 'e0'

    def addError(self, error):
        self.listError.append(Error(error,self.line, self.column))
        self.estado = 'e0'
        self.anterior = 'void'
    
    def analyze(self):
        text = self.text
        self.text = None
        while self.i < len(text):
            if self.estado == 'e0':
                self.e0(text[self.i])
            elif self.estado == 'palabra':
                self.palabra(text[self.i])
            elif self.estado == 'numero':
                self.numero(text[self.i])
            elif self.estado == 'bloque0':
                self.bloque0(text[self.i])
            elif self.estado == 'bloque1':
                self.bloque1(text[self.i])
            elif self.estado == 'bloque2':
                self.bloque2(text[self.i])
            elif self.estado == 'bloque3':
                self.bloque3(text[self.i])
            elif self.estado == 'comentario':
                self.comentario(text[self.i])
            elif self.estado == 'cadena':
                self.cadena(text[self.i])
            
            self.i += 1
        return self.listToken
    
    def e0(self, caracter):
        if caracter.isalpha() and self.anterior == 'void':
            self.estado = 'palabra'
            self.i -= 1 
        elif caracter.isdigit():
            self.estado = 'numero'
            self.i -= 1
        elif caracter == '\'': 
            self.estado = 'bloque0'
            self.i -= 1
        elif caracter == '#':
            self.estado = 'comentario'
        elif caracter == '\"':
            self.column += 1
            self.buffer += caracter
            self.addToken('comilla')
            if self.anterior == 'void':
                self.estado = 'cadena'
            elif self.anterior == 'cadena':
                self.anterior = 'void'
        elif caracter == ';':
            self.column += 1
            self.buffer += caracter
            self.addToken('puntocoma')
        elif caracter == '=':
            self.column += 1
            self.buffer += caracter
            self.addToken('igual')
        elif caracter == ',':
            self.column += 1
            self.buffer += caracter
            self.addToken('coma')
        elif caracter == '(':
            self.column += 1
            self.buffer += caracter
            self.addToken('parentesisI')
        elif caracter == ')':
            self.column += 1
            self.buffer += caracter
            self.addToken('parentesisD')
        elif caracter == '{':
            self.column += 1
            self.buffer += caracter
            self.addToken('llaveI')
        elif caracter == '}':
            self.column += 1
            self.buffer += caracter
            self.addToken('llaveD')
        elif caracter == '[':
            self.column += 1
            self.buffer += caracter
            self.addToken('corcheteI')
        elif caracter == ']':
            self.column += 1
            self.buffer += caracter
            self.addToken('corcheteD')  
        else:
            self.comprobar(caracter)

    def comentario(self, caracter):
        if caracter == '\n':
            self.columm = 1
            self.line += 1
            self.estado = 'e0'
        else:
            pass

    def bloque0(self, caracter):
        if caracter == "\'":
            self.column += 1
            self.estado = 'bloque1'
        else:
            self.i-= 1
            self.addError(self.buffer)
    def bloque1(self, caracter):
        if caracter == "\'":
            self.column += 1
            self.estado = 'bloque2'
        else:
            self.i-= 1
            self.addError(self.buffer)
    def bloque2(self, caracter):
        if caracter == "\'":
            self.column+=1
            if self.anterior == 'void':
                self.estado = 'bloque3'
            elif self.anterior == 'bloque3':
                self.estado = 'e0'
                self.anterior = 'void'
        else:
            self.comprobar(caracter)
    def bloque3(self,caracter):
        if caracter != "\'":
            if caracter == '\n':
                self.line += 1
                self.column = 0
            elif caracter in ['\t',' ']:
                if caracter == "\t":
                    self.column += 4
                else:
                    self.column += 1      
            elif caracter == '\r':
                pass
            else:
                self.column += 1
        else:
            self.i -= 1
            self.estado = 'bloque0'
            self.anterior = 'bloque3'
  
    def comprobar(self, caracter):
        if caracter == '\n':
            self.line += 1
            self.column = 0
        elif caracter in ['\t',' ']:
            if caracter == "\t":
                self.column += 4
            else:
                self.column += 1      
        elif caracter == '\r':
            pass
        else:
            self.addError(caracter)
            self.column += 1
        self.estado = 'e0' 

    def numero(self, caracter):
        if caracter.isdigit() or caracter == '.':
            self.buffer += caracter
            self.column += 1
        else:
            self.anterior == 'numero'
            self.addToken('numero')
            self.estado = 'e0'
            self.i -= 1
        
    def palabra(self, caracter):
        if caracter.isalpha():
            self.buffer += caracter
            self.column += 1
        else:
            if self.buffer == 'imprimir':
                self.addToken('PR_imprimir')
            elif self.buffer == 'imprimirln':
                self.addToken('PR_imprimirln')
            elif self.buffer == 'Registros':
                self.addToken('PR_Registros')
            elif self.buffer == 'Claves':
                self.addToken('PR_Claves')
            elif self.buffer == 'conteo':
                self.addToken('PR_conteo')
            elif self.buffer == 'promedio':
                self.addToken('PR_promedio')
            elif self.buffer == 'contarsi':
                self.addToken('PR_contarsi')
            elif self.buffer == 'datos':
                self.addToken('PR_datos')
            elif self.buffer == 'sumar':
                self.addToken('PR_sumar')
            elif self.buffer == 'max':
                self.addToken('PR_max')
            elif self.buffer == 'min':
                self.addToken('PR_min')
            elif self.buffer == 'exportarReporte':
                self.addToken('PR_exportar')
            else:
                self.addError(self.buffer)
            self.i -= 1

    def cadena(self, caracter):
        if caracter != '\"':
            self.anterior = 'cadena'
            self.buffer += caracter
            self.column += 1
        elif caracter == '\"':
            self.addToken('cadena')
            self.anterior = 'cadena'
            self.estado = 'e0'
            self.i -= 1
    

    def reporteTokens(self):
        re = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset='utf-8'>
                <meta http-equiv='X-UA-Compatible' content='IE=edge'>
                <title>REPORTE DE TOKENS</title>
                <meta name='viewport' content='width=device-width, initial-scale=1'>
                <link rel='stylesheet' type='text/css' media='screen' href='reporte.css'>
            </head>
        <body>
            <h1>REPORTE DE TOKENS</h1>
            <table>
                </thead>
                <tr><th>&nbsp;&nbsp;LEXEMA&nbsp;&nbsp;</th><th>&nbsp;&nbsp;TOKEN&nbsp;&nbsp;</th><th>&nbsp;&nbsp;LINEA&nbsp;&nbsp;</th><th>&nbsp;&nbsp;COLUMNA&nbsp;&nbsp;</th></tr>\n
                </thead>
            <tbody>
        """
        print("tamaño de tokens {}".format(len(self.listToken)))
        for i in range(len(self.listToken)):
            re += "\t\t<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n".format(
                    self.listToken[i].lexeme,
                    self.listToken[i].type,
                    self.listToken[i].line,
                    self.listToken[i].column)
        re += """
                </tbody>
                </table>
            </body>
            </html>
        """
        return re

    def printError(self):
        for error in self.listError:
            print(error)