from antlr4 import *
from dist.yaplLexer import yaplLexer
from dist.yaplParser import yaplParser

input_stream = FileStream('prueba.txt')

lexer = yaplLexer(input_stream)
token_stream = CommonTokenStream(lexer)

token = lexer.nextToken()

list_tokens = []

while token.type != Token.EOF:

    if token.type == token.INVALID_TYPE:
    ##if token.type == lexer.ERROR:
        print("Error léxico en línea", token.line, ": ", token.text)
        break

    else:
        token_pair = [lexer.symbolicNames[token.type], token.text, token.line]
        list_tokens.append(token_pair)

    token = lexer.nextToken()

print(list_tokens)

parser = yaplParser(token_stream)
tree = parser.program()
