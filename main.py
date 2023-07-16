from antlr4 import *
from dist.yaplLexer import yaplLexer
from dist.yaplParser import yaplParser

input_stream = FileStream('prueba.txt')

lexer = yaplLexer(input_stream)
token_stream = CommonTokenStream(lexer)

token = lexer.nextToken()

list_tokens = []

MAX_STRING_LENGTH = 25

while token.type != Token.EOF:

    #if token.type == token.ERROR:
    if token.type == lexer.ERROR:
        print("Error léxico en línea", token.line, ": ", token.text)

        token_pair = [lexer.symbolicNames[lexer.ERROR], token.text, token.line]
        list_tokens.append(token_pair)
    
    elif token.type == lexer.STRING:
        if len(token.text) > MAX_STRING_LENGTH:
            print("Error: Tamaño de lexema excedido en linea", token.line, ": ", token.text)
            token_pair = [lexer.symbolicNames[lexer.ERROR], token.text, token.line]
            list_tokens.append(token_pair)
        elif '\n' in token.text:
            print("Error: Nueva linea detectado dentro del String en linea ", token.line, ": ", token.text)
            token_pair = [lexer.symbolicNames[lexer.ERROR], token.text, token.line]
            list_tokens.append(token_pair)
        else:
            token_pair = [lexer.symbolicNames[token.type], token.text, token.line]
            list_tokens.append(token_pair)        

    else:
        token_pair = [lexer.symbolicNames[token.type], token.text, token.line]
        list_tokens.append(token_pair)

    token = lexer.nextToken()

#print(list_tokens)

parser = yaplParser(token_stream)
tree = parser.program()
