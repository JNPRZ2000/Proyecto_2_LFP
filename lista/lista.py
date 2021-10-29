from lista.nodo import Nodo

class Lista:
    def __init__(self):
        self.size = 0
        self.cabeza = None
        self.cola = None
    
    def insert(self, key):
        new = Nodo(key)
        if self.cabeza == None:
            new.id = 0
            self.cabeza = new
            self.cola = self.cabeza
        else:
            new.back = self.cola
            new.id = self.cola.id +1
            self.cola.next = new
            self.cola = new
        self.size += 1

    def addById(self, id, value):
        if id >= 0 and id < self.size:
            actual = self.cabeza
            while actual.id != id:
                actual = actual.next
            actual.content.append(value)

    def get(self, id):
        actual = self.cabeza
        while actual.id != id:
            actual = actual.next
        return actual.key

    def getByKeye(self,key):
        actual = self.cabeza
        while actual.key != key and actual != None:
            actual = actual.next
        if actual.key != key:
            return False
        else:
            return actual.content
    def printKeys(self):
        s = '''<thead>
            <tr>
        '''
        actual = self.cabeza
        while actual != None:
            s += "<th>{}</th>".format(actual.key)
            actual = actual.next
        s +='''
            </tr>
        </thead>
        <tbody>\n
        '''
        return s
    
    def __str__(self):
        self.string = 'keys:\n'
        actual = self.cabeza
        while actual != None:
            self.string += '{}\n'.format()
            actual = actual.next
        return self.string


    #Funciones
    def sumar(self, key):
        string = '\n>> suma ({}): '.format(key)
        self.auxlist = []
        actual = self.cabeza
        while actual != None:
            if actual.key == key:
                self.auxlist = actual.content
                break
            else:
                actual = actual.next
        if len(self.auxlist) == 0:
            string += 'La clave {} no ha sido registrada'.format(key)
        else:
            suma = 0
            for element in self.auxlist:
                suma += float(element)
            string += str(suma)
        return string
    
    def contarsi(self, key, num):
        string = '\n>> contar en {} si {}: '.format(key, num)
        self.auxlist = []
        actual = self.cabeza
        while actual != None:
            if actual.key == key:
                self.auxlist = actual.content
                break
            else:
                actual = actual.next
        if len(self.auxlist) == 0:
            string += 'La clave {} no ha sido registrada'.format(key)
        else:
            suma = 0
            for element in self.auxlist:
                if float(element) == float(num):
                    suma += 1
            string += str(suma)
        return string

    def promedio(self, key):
        string = '\n>> promedio ({}): '.format(key)
        self.auxlist = []
        actual = self.cabeza
        while actual != None:
            if actual.key == key:
                self.auxlist = actual.content
                break
            else:
                actual = actual.next
        if len(self.auxlist) == 0:
            string += 'La clave {} no ha sido registrada'.format(key)
        else:
            suma = 0
            for element in self.auxlist:
                suma += float(element)
            promedio = float(suma/len(self.auxlist))
            string += str(promedio)
        return string 

    def max(self, key):  
        string = '\n>> Max ({}): '.format(key)
        self.auxlist = []
        actual = self.cabeza
        while actual != None:
            if actual.key == key:
                self.auxlist = actual.content
                break
            else:
                actual = actual.next
        if len(self.auxlist) == 0:
            string += 'La clave {} no ha sido registrada'.format(key)
        else:
            max = self.auxlist[0]
            for element in self.auxlist:
                if float(element) > max:
                    max = element
            string += str(max)
        return string
            
    def min(self, key):  
        string = '\n>> Min ({}): '.format(key)
        self.auxlist = []
        actual = self.cabeza
        while actual != None:
            if actual.key == key:
                self.auxlist = actual.content
                break
            else:
                actual = actual.next
        if len(self.auxlist) == 0:
            string += 'La clave {} no ha sido registrada'.format(key)
        else:
            min = self.auxlist[0]
            for element in self.auxlist:
                if float(element) < min:
                    min = element
            string += str(min)
        return string

    def datos(self, data):
        claves = []
        listas = []
        j = 0
        aux = []
        for i in range(len(data)):
            if j < self.size:
                aux.append(data[i])
                j += 1
                if j == self.size:
                    j = 0
                    listas.append(aux)
                    aux = []
        actual = self.cabeza
        while actual != None:
            claves.append(actual.key)
            actual = actual.next
        string = '\nDatos:\n'
        for clave in claves:
            string += '{:<15}'.format(clave)
        for lista in listas:
            string += "\n"
            for elemento in lista:
                string += "{:<15}".format(elemento)
        string += "\n"
        return string

    def exportar(self, name, data):
        re = '''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset='utf-8'>
                <meta http-equiv='X-UA-Compatible' content='IE=edge'>
                <title>{}</title>
                <meta name='viewport' content='width=device-width, initial-scale=1'>
                <link rel='stylesheet' type='text/css' media='screen' href='reporte.css'>
            </head>
        <body>
            <h1>REPORTE DE REGISTROS</h1>
            <table>'''.format(name)
        re += self.printKeys()
        re += '''

        '''
        i = 0
        j =0
        while i < len(data):
                if j == 0:
                    re += "\t<tr>"
                re += "<td>{}</td>".format(data[i])
                j += 1
                i += 1
                if j == self.size:
                    re += "\t</tr>\n"
                    j = 0
        re += '''\t</tbody>
        </table>
        </body>
        </html>
        '''
        file = open("{}.html".format(name), "w")
        file.write(re)
        file.close()
