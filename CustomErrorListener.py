from antlr4.error.ErrorListener import ErrorListener
from dist.yaplLexer import yaplLexer

class CustomErrorListener(ErrorListener):
    def __init__(self, tipo):
        super().__init__()
        self.type = tipo
        self.errores = []
        self.error_counter = 0
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if offendingSymbol.type == yaplLexer.ERROR:
            self.error_counter += 1
            received = offendingSymbol.text
            expected = recognizer.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
            error_message = f"Error {self.type} en la línea {line}."
            error_message += f"\nRecibido: {received}"
            error_message += f"\nEsperado: {expected}"
            self.errores.append(" \n **ALERTA** \n" + error_message)
        elif recognizer.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames) != offendingSymbol.text:
            self.error_counter += 1
            received = offendingSymbol.text
            expected = recognizer.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
            error_message = f"Error {self.type} en la línea {line}."
            error_message += f"\nRecibido: {received}"
            error_message += f"\nEsperado: {expected}"
            self.errores.append(" \n **ALERTA** \n" + error_message)
            
        
    def getErrorCount(self):
        return self.error_counter