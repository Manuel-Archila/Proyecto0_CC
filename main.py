from antlr4 import *
from dist.yaplParser import yaplParser
from CustomErrorListener import CustomErrorListener
from MyLexer import MyLexer
from TreeBuildingVisitor import TreeBuildingVisitor
from SymbolT import *
from SemanticVisitor import SemanticR
from SemanticAnalyzer import SemanticAnalyzerMio
from SemanticVisitor2 import SemanticV2
from CuadruplasVisitor import *
from CuadruplasVisitor2 import *
from Cuadruplas import *
from traductor import *

import tempfile

import tkinter as tk
from tkinter import filedialog, messagebox

archivo_temporal = None
archi = None

palabras_reservadas = ["IF", "ELSE", "WHILE", "LOOP", "RETURN", "Int", "String", "Bool", "class", "if", "while", "else"]
delimitador_inicio = "(*"
delimitador_fin = "*)"

color1 = "#404040"
letra1 = "#CCFFFF"
color2 = "#FFFFFF"
letra2 = "black"
color_actual = color1
color_letra = letra1

def on_text_change(event=None):
    resaltar_palabras_reservadas()
    resaltar_delimitadores()

def resaltar_delimitadores():
    contenido = contenido_texto.get("1.0", tk.END)
    inicio = "1.0"
    while True:
        inicio = contenido_texto.search(delimitador_inicio, inicio, stopindex=tk.END)
        if not inicio:
            break
        fin = contenido_texto.search(delimitador_fin, inicio, stopindex=tk.END)
        if not fin:
            break
        fin = f"{fin}+{len(delimitador_fin)}c"
        contenido_texto.tag_add("delimitador", inicio, fin)
        inicio = fin

def resaltar_palabras_reservadas():
    contenido = contenido_texto.get("1.0", tk.END)
    for palabra in palabras_reservadas:
        inicio = "1.0"
        while True:
            inicio = contenido_texto.search(palabra, inicio, stopindex=tk.END)
            if not inicio:
                break
            fin = f"{inicio}+{len(palabra)}c"
            contenido_texto.tag_add("reservada", inicio, fin)
            inicio = fin

def cargar_archivo():
    global archi

    global color_actual

    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            archi = archivo
            contenido_texto.delete("1.0", tk.END)
            contenido_texto.insert(tk.END, f.read()) 

            contenido_texto.tag_configure("reservada", foreground="#CE8E0F")  
            contenido_texto.tag_configure("delimitador", foreground="green")  
            resaltar_palabras_reservadas()  
            resaltar_delimitadores()

            contenido_texto.tag_configure("color_texto_tag", foreground=color_letra)
            contenido_texto.tag_add("color_texto_tag", "1.0", tk.END)

            actualizar_numeros_de_linea()

def guardar_archivo():
    global archivo_temporal
    contenido = contenido_texto.get("1.0", tk.END)
    
    if not archivo_temporal:
        archivo_temporal = tempfile.NamedTemporaryFile(delete=False)
    
    with open(archivo_temporal.name, 'wb') as archivo:
        archivo.write(contenido.encode())
    
    archivo_temporal.close()  

def cerrar_ventana():
    guardar_archivo()
    



    if archivo_temporal:
        input_stream = FileStream(archivo_temporal.name)

        lexer = MyLexer(input_stream)
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
            #semantic_visitor.error_mmain2()

            print(semantic_visitor.errores)
        except:
            pass
        

        print(symbol_table)
        print("=============================")

        semanticR = SemanticR(symbol_table)

        semanticR.visit_program(tree)
        semanticR.error_mmain2()

        print("=============================")

        semanticV = SemanticV2(semanticR.symbol_table)
        semanticV.visit_program(tree)


        if len(semantic_visitor.errores) > 0 or len(semanticR.errores) > 0 or len(semanticV.errores) > 0:

            mensaje = "Se encontraron errores semánticos:\n\n"
            for error in list(set(semantic_visitor.errores)):
                mensaje += f"- {error}\n"
            for error in list(set(semanticR.errores)):
                mensaje += f"- {error}\n"
            for error in list(set(semanticV.errores)):
                mensaje += f"- {error}\n"

            messagebox.showerror("Errores Semánticos", mensaje)
        
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

            print(semanticV.symbol_table)

            dot_graph = visitor.getDotGraph()
            dot_graph.render(filename='output.gv', view=True, format='png')

            #Aqui

            print("============ CUADRUPLAS ==============\n\n")

            cuadruplas = Cuadruplas()

            genCuadruplas = CuadruplasVisitor2(semanticV.symbol_table, cuadruplas)

            genCuadruplas.visit_program(tree)


            cuadruplas.imprimir_cuadruplas()

            cuadruplas.escribir_cuadruplas_en_archivo("Cuadruplas.txt")

            print("============ MIPS ==============\n\n")

            traductor = Traductor(cuadruplas.cuadruplas)

            lis = traductor.buscar_operadores_aritmeticos()

            trad = traductor.generar_codigo_mips(lis)

            traductor.escribir_cuadruplaTrad_en_archivo("MIPS.txt", trad)

            for el in trad:
                print(el)
                          

def cambiar_color_fondo():
    global color_actual
    global color_letra

    if color_actual == color1:
        color_actual = color2
        color_letra = letra2
    else:
        color_actual = color1
        color_letra = letra1
    
    contenido_texto.configure(bg=color_actual)
    numeros_linea_widget.configure(bg=color_actual)

    contenido_texto.tag_configure("color_texto_tag", foreground=color_letra)
    contenido_texto.tag_add("color_texto_tag", "1.0", tk.END)

    numeros_linea_widget.tag_configure("color_texto_tag", foreground=color_letra)
    numeros_linea_widget.tag_add("color_texto_tag", "1.0", tk.END)

def resetear_todo():
    global archivo_temporal
    archivo_temporal = None  # Reiniciar el archivo temporal
    contenido_texto.delete("1.0", tk.END)  # Borrar el contenido del área de edición
    actualizar_numeros_de_linea()  # Actualizar los números de línea si es necesario

def update_line_numbers_view(nose = None):
    text_yview = contenido_texto.yview()
    numeros_linea_widget.yview_moveto(text_yview[0])

    numeros_linea_widget.tag_configure("color_texto_tag", foreground=color_letra)
    numeros_linea_widget.tag_add("color_texto_tag", "1.0", tk.END)

def actualizar_numeros_de_linea(event=None):
    numeros_linea = "\n".join(str(i) for i in range(1, int(contenido_texto.index(tk.END).split('.')[0])))
    numeros_linea_widget.config(state=tk.NORMAL)
    numeros_linea_widget.delete("1.0", tk.END)
    numeros_linea_widget.insert("1.0", numeros_linea)
    numeros_linea_widget.config(state=tk.DISABLED)
    update_line_numbers_view()

def mostrar_cuadruplas():
    ventana_cuadruplas = tk.Toplevel(ventana)
    ventana_cuadruplas.title("Cuádruplas")
    
    with open("Cuadruplas.txt", "r") as archivo_cuadruplas:
        contenido = archivo_cuadruplas.read()

    cuadruplas_texto = tk.Text(ventana_cuadruplas, wrap=tk.WORD, height=50, width=120, bg=color1, fg=letra1)
    cuadruplas_texto.pack(padx=10, pady=10)
    cuadruplas_texto.insert(tk.END, contenido)
    cuadruplas_texto.config(state=tk.DISABLED)

def mostrar_mips():
    with open("MIPS.txt", "r") as f:
            
            contenido_texto.delete("1.0", tk.END)
            contenido_texto.insert(tk.END, f.read()) 

            contenido_texto.tag_configure("reservada", foreground="#CE8E0F")  
            contenido_texto.tag_configure("delimitador", foreground="green")  
            resaltar_palabras_reservadas()  
            resaltar_delimitadores()

            contenido_texto.tag_configure("color_texto_tag", foreground=color_letra)
            contenido_texto.tag_add("color_texto_tag", "1.0", tk.END)

            actualizar_numeros_de_linea()


ventana = tk.Tk()
ventana.title("Editor de Archivos")

boton_frame = tk.Frame(ventana)
boton_frame.pack()

boton_cargar = tk.Button(boton_frame, text="Cargar Archivo", command=cargar_archivo, bg="#c7eaf2")
boton_cargar.pack(side=tk.LEFT, padx=5, pady=5)

boton_cerrar = tk.Button(boton_frame, text="Analizar Codigo", command=cerrar_ventana, bg="#c7eaf2")
boton_cerrar.pack(side=tk.LEFT, padx=5, pady=5)

boton_resetear = tk.Button(boton_frame, text="Resetear Todo", command=resetear_todo, bg="#c7eaf2")
boton_resetear.pack(side=tk.LEFT, padx=5, pady=5)

boton_cambiar_color_fondo = tk.Button(boton_frame, text="Cambiar Tema", command=cambiar_color_fondo, bg="#c7eaf2")
boton_cambiar_color_fondo.pack(side=tk.LEFT, padx=2.5, pady=2.5)

boton_mostrar_cuadruplas = tk.Button(boton_frame, text="Mostrar Cuádruplas", command=mostrar_cuadruplas, bg="#c7eaf2")
boton_mostrar_cuadruplas.pack(side=tk.LEFT, padx=5, pady=5)

boton_mostrar_cuadruplas = tk.Button(boton_frame, text="Mostrar MIPS", command=mostrar_mips, bg="#c7eaf2")
boton_mostrar_cuadruplas.pack(side=tk.LEFT, padx=5, pady=5)

contenido_frame = tk.Frame(ventana)
contenido_frame.pack(fill=tk.BOTH, expand=True)

numeros_linea_widget = tk.Text(contenido_frame, width=4, bg=color_actual, state=tk.DISABLED)
numeros_linea_widget.pack(side=tk.LEFT, fill=tk.Y)
numeros_linea_widget.tag_configure("color_texto_tag", foreground=color_letra)
numeros_linea_widget.tag_add("color_texto_tag", "1.0", tk.END)
contenido_texto = tk.Text(contenido_frame, wrap=tk.NONE, bg=color_actual)
contenido_texto.pack(side=tk.LEFT, fill=tk.Y)
contenido_texto.tag_configure("color_texto_tag", foreground=color_letra)
contenido_texto.tag_add("color_texto_tag", "1.0", tk.END)

cambiar_color_fondo()

contenido_texto.bind("<Return>", actualizar_numeros_de_linea)
contenido_texto.bind("<BackSpace>", actualizar_numeros_de_linea)
contenido_texto.bind("<MouseWheel>", actualizar_numeros_de_linea)
contenido_texto.bind("<Configure>", update_line_numbers_view)
contenido_texto.bind("<KeyRelease>", on_text_change)
contenido_texto.bind("<KeyRelease>", actualizar_numeros_de_linea)
ventana.mainloop()