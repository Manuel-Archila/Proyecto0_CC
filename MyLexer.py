from dist.yaplLexer import yaplLexer

class MyLexer(yaplLexer):
    def __init__(self, input_stream, ts):
        super().__init__(input_stream)
        self.ts = ts
        self.errors = []
        

    def nextToken(self):
        MAX_STRING_LENGTH = 25
        
        token = super().nextToken()
        
        if token.type == yaplLexer.STRING:
            if len(token.text) > MAX_STRING_LENGTH:
                error = "Error: Tamaño de lexema excedido en linea " + str(token.line) + ": " + str(token.text)
                self.errors.append(error)
                token.type = yaplLexer.ERROR
                #ts.agregar_simbolo(token.text, token.line, token.column, token.type)
                #return
            elif '\n' in token.text:
                error = "Error: Nueva linea detectado dentro del String en linea " + str(token.line), ": " + str(token.text)
                self.errors.append(error)
                token.type = yaplLexer.ERROR
                #ts.agregar_simbolo(token.text, token.line, token.column, token.type)
                #return
            
        elif token.type == yaplLexer.ERROR:
            error = "Error léxico en línea " + str(token.line) + ": " + str(token.text)
            self.errors.append(error)
        
        if token.type != yaplLexer.ERROR:
            self.ts.agregar_simbolo(token.text, token.line, token.column, token.type)
        
        return token