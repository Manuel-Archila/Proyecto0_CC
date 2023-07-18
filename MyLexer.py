from dist.yaplLexer import yaplLexer

class MyLexer(yaplLexer):
    def __init__(self, input_stream):
        super().__init__(input_stream)
        

    def nextToken(self):
        MAX_STRING_LENGTH = 25
        
        token = super().nextToken()
        
        if token.type == yaplLexer.STRING:
            if len(token.text) > MAX_STRING_LENGTH:
                print("Error: Tamaño de lexema excedido en linea", token.line, ": ", token.text)
                token.type = yaplLexer.ERROR
                #return
            elif '\n' in token.text:
                print("Error: Nueva linea detectado dentro del String en linea ", token.line, ": ", token.text)
                token.type = yaplLexer.ERROR
                #return
            
        elif token.type == yaplLexer.ERROR:
            print("Error léxico en línea", token.line, ": ", token.text)
        
        return token