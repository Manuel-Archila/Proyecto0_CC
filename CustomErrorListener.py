from antlr4.error.ErrorListener import ErrorListener
from dist.yaplLexer import yaplLexer
from colorama import init, Fore, Back, Style

class CustomErrorListener(ErrorListener):
    def __init__(self, tipo):
        super().__init__()
        self.type = tipo
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if offendingSymbol.type == yaplLexer.ERROR:
            received = offendingSymbol.text
            expected = recognizer.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
            error_message = f"Error {self.type} en la línea {line}."
            error_message += f"\nRecibido: {received}"
            error_message += f"\nEsperado: {expected}"
            print(Fore.RED + " \n **ALERTA** \n" + error_message)