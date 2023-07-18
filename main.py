from antlr4 import *
from dist.yaplParser import yaplParser
import graphviz as gv
from CustomErrorListener import CustomErrorListener
from MyLexer import MyLexer
from TreeBuildingVisitor import TreeBuildingVisitor

input_stream = FileStream('prueba.txt')

lexer = MyLexer(input_stream)
token_stream = CommonTokenStream(lexer)
token_stream.fill()

# for element in token_stream.tokens:
#     print(element.type)

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
