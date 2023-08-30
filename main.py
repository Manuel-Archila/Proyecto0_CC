from antlr4 import *
from dist.yaplParser import yaplParser
from CustomErrorListener import CustomErrorListener
from MyLexer import MyLexer
from TreeBuildingVisitor import TreeBuildingVisitor
from TS import TS 
from SymbolTable import *
from SymbolT import *
from SemanticVisitor import SemanticR
from SemanticAnalyzer import SemanticAnalyzerMio
import tempfile

import tkinter as tk
from tkinter import filedialog, messagebox

archivo_temporal = None
archi = None


def cargar_archivo():
    global archi
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            archi = archivo
            contenido_texto.delete("1.0", tk.END)
            contenido_texto.insert(tk.END, f.read()) 

def guardar_archivo():
    global archivo_temporal
    contenido = contenido_texto.get("1.0", tk.END)
    
    if not archivo_temporal:
        archivo_temporal = tempfile.NamedTemporaryFile(delete=False)
    
    with open(archivo_temporal.name, 'wb') as archivo:
        archivo.write(contenido.encode())
    
    archivo_temporal.close()  # Cerrar el archivo después de escribir en él

# def guardar_archivo():
#     global archivo_temporal
    
#     # Read the content of fijos.txt
#     with open("fijas.txt", "r") as fijos_file:
#         fijos_content = fijos_file.read()
    
#     contenido = contenido_texto.get("1.0", tk.END)
    
#     if not archivo_temporal:
#         archivo_temporal = tempfile.NamedTemporaryFile(delete=False)
    
#     # Combine fijos_content and contenido
#     combined_content = fijos_content + "\n" + contenido
    
#     with open(archivo_temporal.name, 'wb') as archivo:
#         archivo.write(combined_content.encode())
    
#     archivo_temporal.close()  # Cerrar el archivo después de escribir en él


def cerrar_ventana():
    guardar_archivo()
    
    tabla_simbolos = TS()


    
    if archivo_temporal:
        input_stream = FileStream(archivo_temporal.name)

        lexer = MyLexer(input_stream, tabla_simbolos)
        token_stream = CommonTokenStream(lexer)
        token_stream.fill()


        print("=============================")




        parser = yaplParser(token_stream)
        parser.removeErrorListeners()
        parserErrorListener = CustomErrorListener("sintáctico")
        parser.addErrorListener(parserErrorListener)
        tree = parser.program()
        symbol_table = SymbolT()
        symbol_table.build_natives()
        semantic_visitor = SemanticAnalyzerMio(symbol_table)
        
        
        try:
            semantic_visitor.visit_program(tree)
            semantic_visitor.error_mmain()
            semantic_visitor.error_mmain2()

            print(semantic_visitor.errores)
        except:
            pass
        

        print(symbol_table)
        print("=============================")

        semanticR = SemanticR(symbol_table)

        semanticR.visit_program(tree)

        
        errores_sintacticos = parserErrorListener.errores
        errores_lexicos = lexer.errors  
        if parserErrorListener.getErrorCount() > 0:

            mensaje = "Se encontraron errores sintácticos:\n\n"
            mensaje += "Errores sintácticos:\n"
            for error in errores_sintacticos:
                mensaje += f"- {error}\n"
            mensaje += "\nErrores léxicos:\n"
            for error in errores_lexicos:
                mensaje += f"- {error}\n"

            messagebox.showerror("Errores Sintácticos", mensaje)

        else:
            visitor = TreeBuildingVisitor()
            visitor.visitar(tree)

            dot_graph = visitor.getDotGraph()
            dot_graph.render(filename='output.gv', view=True, format='png')

def resetear_todo():
    global archivo_temporal
    archivo_temporal = None  # Reiniciar el archivo temporal
    contenido_texto.delete("1.0", tk.END)  # Borrar el contenido del área de edición
    actualizar_numeros_de_linea()  # Actualizar los números de línea si es necesario

def actualizar_numeros_de_linea(event=None):
    contenido = contenido_texto.get("1.0", tk.END).splitlines()
    numeros_linea = "\n".join(str(i) for i in range(1, len(contenido) + 1))
    numeros_linea_widget.config(state=tk.NORMAL)
    numeros_linea_widget.delete("1.0", tk.END)
    numeros_linea_widget.insert(tk.END, numeros_linea)
    numeros_linea_widget.config(state=tk.DISABLED)

ventana = tk.Tk()
ventana.title("Editor de Archivos")

boton_frame = tk.Frame(ventana)
boton_frame.pack()

boton_cargar = tk.Button(boton_frame, text="Cargar Archivo", command=cargar_archivo)
boton_cargar.pack(side=tk.LEFT, padx=5, pady=5)

boton_cerrar = tk.Button(boton_frame, text="Analizar Codigo", command=cerrar_ventana)
boton_cerrar.pack(side=tk.LEFT, padx=5, pady=5)

boton_resetear = tk.Button(boton_frame, text="Resetear Todo", command=resetear_todo)
boton_resetear.pack(side=tk.LEFT, padx=5, pady=5)

contenido_frame = tk.Frame(ventana)
contenido_frame.pack(fill=tk.BOTH, expand=True)

numeros_linea_widget = tk.Text(contenido_frame, width=4, padx=4, takefocus=0, border=0, background="#f0f0f0", state=tk.DISABLED)
numeros_linea_widget.pack(side=tk.LEFT, fill=tk.Y)
contenido_texto = tk.Text(contenido_frame, wrap=tk.NONE)
contenido_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
contenido_texto.bind("<Configure>", actualizar_numeros_de_linea)
contenido_texto.bind("<Key>", actualizar_numeros_de_linea)

ventana.mainloop()