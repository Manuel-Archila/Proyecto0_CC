from antlr4 import *
from dist.yaplParser import yaplParser
from CustomErrorListener import CustomErrorListener
from MyLexer import MyLexer
from TreeBuildingVisitor import TreeBuildingVisitor
from TS import TS


tabla_simbolos = TS()

input_stream = FileStream('prueba.txt')

lexer = MyLexer(input_stream, tabla_simbolos)
token_stream = CommonTokenStream(lexer)
token_stream.fill()

print(tabla_simbolos.buscar_simbolo(';'))

print("=============================")


print(tabla_simbolos.get_table())

# for token in token_stream.tokens:
#     lexema = token.text
#     linea = token.line
#     columna = token.column
#     tipo_token = lexer.symbolicNames[token.type] if token.type != Token.EOF else "EOF"

#     # Registrar el lexema y sus atributos en la tabla de símbolos
#     agregar_simbolo(tabla_simbolos, lexema, linea, columna, tipo_token)

parser = yaplParser(token_stream)
parser.removeErrorListeners()
parserErrorListener = CustomErrorListener("sintáctico")
parser.addErrorListener(parserErrorListener)
tree = parser.program()

if parserErrorListener.getErrorCount() > 0:
    print("Se encontraron errores sintácticos. No se generará el árbol de análisis sintáctico.")
    exit()
else:
    visitor = TreeBuildingVisitor()
    visitor.visit(tree)

    dot_graph = visitor.getDotGraph()
    dot_graph.render(filename='output.gv', view=True, format='png')
