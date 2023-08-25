from dist.yaplVisitor import yaplVisitor
from SymbolTable import SymbolTable, Symbol
from dist.yaplParser import yaplParser

class SemanticAnalyzerMio(yaplVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def visit_program(self, ctx:yaplParser.ProgramContext):
        self.visitChildren(ctx)
        
        return

    # Para declaraciones de clases
    def visitClass(self, ctx:yaplParser.ClassContext):
        class_name = ctx.TYPE()[0].getText()
        symbol = Symbol(name=class_name, line=ctx.start.line, symbol_type="class", scope=self.symbol_table.current_scope())
        self.symbol_table.add_symbol(symbol)
        
        # Entrar a un nuevo ámbito para el cuerpo de la clase
        self.symbol_table.enter_scope(class_name)
        
        # Visitar las características de la clase (métodos/variables)
        self.visitChildren(ctx)
        
        # Salir del ámbito de la clase después de visitar su cuerpo
        self.symbol_table.exit_scope()
        return

    # Para declaraciones de variables
    def visitFeature(self, ctx:yaplParser.FeatureContext):
        if ctx.ID() and ctx.TYPE():
            var_name = ctx.ID().getText()
            var_type = ctx.TYPE().getText()
            symbol = Symbol(name=var_name, line=ctx.start.line, symbol_type="variable", data_type=var_type, scope=self.symbol_table.current_scope())
            self.symbol_table.add_symbol(symbol)

    def visitExpr(self, ctx:yaplParser.ExprContext):
        if ctx.ASSIGN():
            var_name = ctx.ID().getText()
            symbol = self.symbol_table.get_symbol(var_name)
            if not symbol:
                raise Exception(f"Variable {var_name} not declared at line {ctx.start.line}")

            # Suponiendo que tienes un método get_expr_type
            right_expr_type = self.get_expr_type(ctx.expr())
            if symbol.data_type != right_expr_type:
                raise Exception(f"Type mismatch for variable {var_name} at line {ctx.start.line}. Expected {symbol.data_type} but got {right_expr_type}")

        elif ctx.DOT():
            method_name = ctx.ID().getText()
            symbol = self.symbol_table.get_symbol(method_name)
            if not symbol or symbol.symbol_type != "method":
                raise Exception(f"Method {method_name} not declared or used incorrectly at line {ctx.start.line}")

            # Suponiendo que el símbolo para un método tiene un atributo 'arguments'
            passed_args = ctx.expr()  
            if len(passed_args) != len(symbol.arguments):
                raise Exception(f"Incorrect number of arguments for method {method_name} at line {ctx.start.line}")

            for idx, arg in enumerate(passed_args):
                arg_type = self.get_expr_type(arg)
                if arg_type != symbol.arguments[idx].data_type:
                    raise Exception(f"Type mismatch for argument {idx+1} of method {method_name} at line {ctx.start.line}. Expected {symbol.arguments[idx].data_type} but got {arg_type}")

    def visitFormal(self, ctx:yaplParser.FormalContext):
        arg_name = ctx.ID().getText()
        arg_type = ctx.TYPE().getText()
        
        existing_symbol = self.symbol_table.get_symbol(arg_name)
        if existing_symbol and existing_symbol.scope == self.symbol_table.current_scope():
            raise Exception(f"Argument {arg_name} already declared at line {ctx.start.line}")
        
        symbol = Symbol(name=arg_name, line=ctx.start.line, symbol_type="argument", data_type=arg_type, scope=self.symbol_table.current_scope())
        self.symbol_table.add_symbol(symbol)

    # Este es un esqueleto para get_expr_type. Deberías expandir esto según las necesidades de tu lenguaje.
    def get_expr_type(self, ctx):
        if ctx.ID():
            symbol = self.symbol_table.get_symbol(ctx.ID().getText())
            if symbol:
                return symbol.data_type
        # ... agregar más lógica para otros tipos de expresiones
        return None  # Devuelve None si no se puede determinar el tipo