from antlr4 import FileStream, CommonTokenStream
from dist.yaplLexer import yaplLexer
from dist.yaplParser import yaplParser

input_stream = FileStream('prueba.txt')

lexer = yaplLexer(input_stream)
token_stream = CommonTokenStream(lexer)

token = lexer.nextToken()
while token.type == yaplLexer.EOF:
    print(token.text)
    token = lexer.nextToken()

parser = yaplParser(token_stream)
tree = parser.program()