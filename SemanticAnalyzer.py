from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode
from SymbolTable import Symbol, SymbolTable

class SemanticAnalyzerMio(yaplVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def visit_program(self, ctx:yaplParser.ProgramContext):
        return self.visitChildren(ctx)
    
    def visitClass(self, ctx:yaplParser.ClassContext):
        self.symbol_table.put(ctx.TYPE()[0].getText(), ctx.start.line, "class")
        self.symbol_table.push_scope()
        temp = self.visitChildren(ctx)
        self.symbol_table.pop_scope()
        return temp
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):

        if ctx.LPAR():
            self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "function", ctx.TYPE().getText())

            self.symbol_table.push_scope()
            temp = self.visitChildren(ctx)
            self.symbol_table.pop_scope()

            return temp

        else:
            self.symbol_table.put(ctx.ID().getText(), self.get_line(ctx), "atribute")

            return self.visitChildren(ctx)
    
    def visitFormal(self, ctx:yaplParser.FormalContext):
        self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "variableT", ctx.TYPE().getText())

        return None
    
    def visitExpr(self, ctx:yaplParser.ExprContext):

        print(ctx.getText())
        
        if ctx.IF():
            self.symbol_table.push_scope()
            temp = self.visitChildren(ctx)
            self.symbol_table.pop_scope()
            return temp

        if ctx.ELSE():
            self.symbol_table.push_scope()
            temp = self.visitChildren(ctx)
            self.symbol_table.pop_scope()
            return temp

        if ctx.WHILE():
            self.symbol_table.push_scope()
            temp = self.visitChildren(ctx)
            self.symbol_table.pop_scope()
            return temp

        if ctx.LET():
            for i in range(len(ctx.ID())):
                self.symbol_table.put(ctx.ID()[i], self.get_line(ctx), "variable",ctx.TYPE()[i].getText())
                for chil in ctx.getChildren():
                    print(chil.getText())
                return self.visitChildren(ctx)

        else:
            return self.visitChildren(ctx)
    # # Para declaraciones de clases
    # def visitClass(self, ctx:yaplParser.ClassContext):
    #     class_name = ctx.TYPE()[0].getText()
    #     line = self.get_line(ctx.TYPE()[0])
    #     self.symbol_table.put(class_name, line, "class")
    #     self.symbol_table.push_scope()
    #     ret = self.visitChildren(ctx)
    #     self.symbol_table.pop_scope()

    #     return ret

    # def visitFeature(self, ctx:yaplParser.FeatureContext):
    #     if ctx.LPAR():
    #         self.visitMethod(ctx)
    #     else:
    #         self.visitAttribute(ctx)


    # def visitMethod(self, ctx:yaplParser.FeatureContext):
    #         if ctx.ID() and ctx.TYPE():
    #             var_name = ctx.ID().getText()
    #             var_type = ctx.TYPE().getText()
    #             line = self.get_line(ctx.ID())
    #             self.symbol_table.put(var_name, line, "function", var_type)


    #             for formal in ctx.formal():
    #                 self.symbol_table.push_scope()
    #                 self.visitFormal(formal)
    #                 self.symbol_table.pop_scope()

    #             if ctx.expr():
    #                 self.symbol_table.push_scope()
    #                 self.visitExpr(ctx.expr())
    #                 self.symbol_table.pop_scope()

    #             return self.visitChildren(ctx)
    #         else:
    #             print("Error en la declaracion de metodos")

    # def visitAttribute(self, ctx:yaplParser.FeatureContext):
    #     self.symbol_table.put(ctx.ID().getText(), self.get_line(ctx.ID()), "attribute", ctx.TYPE().getText())


    # def visit_Expr(self, ctx:yaplParser.ExprContext):

    #     if ctx.IF():
    #         node_type = ctx.getText()
    #         line = self.get_line(ctx)

    #         for hijo in ctx.getChildren():
    #             if not isinstance(hijo, TerminalNode):
    #                 self.visit_Expr(hijo)
    #             else:
    #                 self.visitExpr(hijo)

    #         # print("Anadi un una expresion a la tabla")
    #         self.symbol_table.put(node_type, line, ctx, "if")

    #     for hijo in ctx.getChildren():
    #         if not isinstance(hijo, TerminalNode):
    #             self.visitExpr(hijo)
    #         else:
    #             self.verify_expr(hijo)
    #     # if ctx.ASSIGN():
    #     #     var_name = ctx.ID()[0].getText()
    #     #     self.symbol_table.put(var_name, self.get_line(ctx.ID()[0]), "variable", self.get_expr_type(ctx.expr()))
    #     #     # if var_name in self.symbol_table.get_table():
    #     #     #     raise Exception(f"Variable {var_name} not declared at line {ctx.start.line}")

    #     #     # # Suponiendo que tienes un método get_expr_type
    #     #     # right_expr_type = self.get_expr_type(ctx.expr())
    #     #     # if symbol.data_type != right_expr_type:
    #     #     #     raise Exception(f"Type mismatch for variable {var_name} at line {ctx.start.line}. Expected {symbol.data_type} but got {right_expr_type}")

    #     # elif ctx.DOT():
    #     #     method_name = ctx.ID()[0].getText()
    #     #     symbol = self.symbol_table.get_symbol(method_name)
    #     #     if not symbol or symbol.symbol_type != "method":
    #     #         raise Exception(f"Method {method_name} not declared or used incorrectly at line {ctx.start.line}")

    #     #     # Suponiendo que el símbolo para un método tiene un atributo 'arguments'
    #     #     passed_args = ctx.expr()  
    #     #     if len(passed_args) != len(symbol.arguments):
    #     #         raise Exception(f"Incorrect number of arguments for method {method_name} at line {ctx.start.line}")

    #     #     for idx, arg in enumerate(passed_args):
    #     #         arg_type = self.get_expr_type(arg)
    #     #         if arg_type != symbol.arguments[idx].data_type:
    #     #             raise Exception(f"Type mismatch for argument {idx+1} of method {method_name} at line {ctx.start.line}. Expected {symbol.arguments[idx].data_type} but got {arg_type}")

    #     # elif ctx.ID():
    #     #     var_name = ctx.ID().getText()
    #     #     symbol = self.symbol_table.get_symbol(var_name)
    #     #     if not symbol:
    #     #         raise Exception(f"Variable {var_name} not declared at line {ctx.start.line}")

    # def visitExpr(self, ctx:yaplParser.ExprContext):

        

    #     node_type = ctx.getText()
    #     line = self.get_line(ctx)

    #     # print("Anadi un una expresion a la tabla")
    #     self.symbol_table.put(node_type, line, ctx)



    # def visitFormal(self, ctx:yaplParser.FormalContext):
    #     arg_name = ctx.ID().getText()
    #     arg_type = ctx.TYPE().getText()
        
    #     existing_symbol = self.symbol_table.get_symbol(arg_name)
    #     if existing_symbol and existing_symbol.scope == self.symbol_table.current_scope():
    #         raise Exception(f"Argument {arg_name} already declared at line {ctx.start.line}")
        
    #     symbol = Symbol(name=arg_name, line=ctx.start.line, symbol_type="argument", data_type=arg_type, scope=self.symbol_table.current_scope())
    #     self.symbol_table.add_symbol(symbol)

    # # Este es un esqueleto para get_expr_type. Deberías expandir esto según las necesidades de tu lenguaje.
    # def get_expr_type(self, ctx):
    #     if ctx[0].ID():
    #         symbol = self.symbol_table.get_symbol(ctx.ID().getText())
    #         if symbol:
    #             return symbol.data_type
    #     # ... agregar más lógica para otros tipos de expresiones
    #     return None  # Devuelve None si no se puede determinar el tipo

    def get_line(self, node):
        # Si el nodo es un TerminalNode, se puede obtener la línea directamente.
        if isinstance(node, TerminalNode):
            return node.symbol.line
        # De lo contrario, si es un nodo de una regla, se utiliza `start`.
        elif hasattr(node, 'start'):
            return node.start.line
        # Si el nodo no tiene información de línea, devuelve None o cualquier valor por defecto.
        else:
            return None