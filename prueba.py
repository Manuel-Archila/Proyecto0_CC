from antlr4 import *
from dist.yaplLexer import yalpLexer

def scanner(input_file):
    # Leer el archivo de entrada
    with open(input_file, 'r') as file:
        input_text = file.read()

    input_stream = InputStream(input_text)
    lexer = yalpLexer(input_stream)

    # Obtener los tokens
    token = lexer.nextToken()
    reconocidos = []

    # Imprimir los tokens
    while token.type != Token.EOF:
        
        if token.type == Token.INVALID_TYPE:
            print("Error léxico: ", token.text)
            break

        else:
            reconocidos.append(token.text)

        token = lexer.nextToken()
    print(reconocidos)

# Archivo de entrada a analizar
archivo_entrada = "entrada.txt"

# Llamar a la función para analizar los errores léxicos
scanner(archivo_entrada)