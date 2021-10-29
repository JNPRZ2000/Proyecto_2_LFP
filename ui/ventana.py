from tkinter import Scrollbar, Tk, Text, Frame, Button, StringVar, OptionMenu
from PIL import Image, ImageTk
from metodos.file import openFile
from analizador.sintax import Sintax
from analizador.lexico import Lexico
import webbrowser

class Ventana(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Proyecto 2')
        self.state('zoomed')
        self.update()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        self.geometry('{}x{}+0+0'.format(ancho,alto))
        self.resizable(1, 1)
        self.entradaTexto = None

        self.addItems()
    
    def addItems(self):
        ancho = self.winfo_width()
        alto = self.winfo_height()
        ancho2 = ancho//2-(60)
        alto2 = alto-170

        fondo = Frame(self)
        fondo.config(width = ancho, height = alto, bg = '#082032',)
        fondo.place(x= 0, y = 0)
        #ENTRADA DE TEXTO
        scrl1 = Scrollbar(self)
        self.entradaTexto = Text(fondo, yscrollcommand= scrl1.set, bg = '#2C394B', fg = 'yellow', 
                                insertbackground = 'yellow', font= ('Consolas',13))
        scrl1.config(command = self.entradaTexto.yview, background= 'black')
        scrl1.place(x = 20+ancho2, y = 100, height = alto2)
        scrl1.update()
        self.entradaTexto.place(x = 20, y = 100, width = ancho2, height = alto2)
        #SALIDA DE TEXTO
        scrl2 = Scrollbar(self)
        self.salidaTexto = Text(fondo, yscrollcommand= scrl2.set, bg = '#2C394B', fg = 'yellow', 
                                insertbackground = 'yellow', font= ('Consolas',11), state = 'disabled')
        scrl2.config(command = self.salidaTexto.yview, background= '#999')
        scrl2.place(x = ancho-37, y = 100, height = alto2)
        self.salidaTexto.place(x = ancho-37-ancho2, y = 100, width = ancho2, height = alto2)

        #AGREGAR MENU
        cinta = Frame(fondo, bg = 'black')
        cinta.place(x = 0, y = 0, width = ancho, height = 34)
        self.img1 = Image.open('source\Archivo.png')
        self.img1 = self.img1.resize((30,30), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.img2 = Image.open('source\Compilar.png')
        self.img2 = self.img2.resize((30,30), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.img3 = Image.open('source\Reporte.png')
        self.img3 = self.img3.resize((30,30), Image.ANTIALIAS)
        self.img3 = ImageTk.PhotoImage(self.img3)

        self.btnCargar = Button(cinta , image = self.img1, command = self.Cargar, bg = 'black')
        self.btnCargar.place(x = 10, y = 2 , width = 30, height = 30)
        self.btnCompilar = Button(cinta, image = self.img2, command = self.Compilar, bg = 'black')
        self.btnCompilar.place(x = 40, y = 2, width = 30, height = 30)
        self.btnBorrar = Button(cinta, text = 'CLR', command = self.borrar, bg = 'black', fg = 'white')
        self.btnBorrar.place(x= 70, y = 2, width = 30, height = 30)
        self.btnDelete = Button(cinta, text = 'DLT', command = self.delete, bg = 'black', fg = 'white')
        self.btnDelete.place(x= 100, y = 2, width = 30, height = 30)

        #AGREGAR MENU LIST DE REPORTES
        self.variable = StringVar(cinta)
        optionList = ["Reporte de A. Léxico", "R. de A. Sintáctico", "Árbol de derivación"]
        opt = OptionMenu(cinta, self.variable, *optionList)
        opt.config(activebackground = "#E3FDFD", background = "#393E46", fg = "white")
        opt.place(x = 130, y = 2, width = 150, height = 30)
        self.variable.trace('w', self.callback)
    
    def callback(self, *args):
        selected = self.variable.get()
        if selected == 'Reporte de A. Léxico':
            file = open("{}.html".format(selected), "w")
            file.write(self.reporteTokens())
            file.close()
            webbrowser.open_new_tab('{}.html'.format(selected))

    def borrar(self):
        self.salidaTexto.config(state = 'normal')
        self.salidaTexto.delete('1.0', 'end')
        self.salidaTexto.config(state = 'disabled')

    def delete(self):
        self.salidaTexto.config(state = 'normal')
        self.salidaTexto.delete('1.0', 'end')
        self.salidaTexto.config(state = 'disabled')
        self.entradaTexto.delete('1.0', 'end')

    def Cargar(self):
        openFile(self.entradaTexto)
    
    def Compilar(self):
        self.analizadorL = Lexico(self.entradaTexto.get('1.0', 'end'))
        self.listToken = self.analizadorL.analyze()
        self.analizadorS = Sintax(self.listToken, self.salidaTexto)
        self.analizadorS.analyze()
        print("{}".format(self.analizadorS.printError()))
        print("Analisis exitoso")


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