from tkinter import filedialog, messagebox, INSERT
def openFile(InputText):
    try:
        ruta = filedialog.askopenfilename(title = "Abrir Archivo", filetypes = (("LFP FILES", "*.lfp"),))
        file = open(ruta, 'r')
        InputText.insert(INSERT, file.read())
    except FileNotFoundError:
        messagebox.showerror(title = "ERROR", message = "Ruta de archivo no válida")
    except IOError:
        messagebox.showerror(title = "ERROR", message = "ERROR DESCONOCIDO")


