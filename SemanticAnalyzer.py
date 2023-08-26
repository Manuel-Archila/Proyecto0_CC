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
        print("Llamada a class")
        
        print("Enter")
        self.symbol_table.enter_scope() 
        self.symbol_table.put(ctx.TYPE()[0].getText(), ctx.start.line, "class")
        print("Enter")
        self.symbol_table.enter_scope()
        temp = self.visitChildren(ctx)
        print("Exit")
        self.symbol_table.exit_scope()
        print("Exit")
        self.symbol_table.exit_scope()
        return temp
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):
        print("Llamada a feature")

        if ctx.LPAR():
            self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "function", ctx.TYPE().getText())
            print("Enter")
            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx)
            print("Exit")
            self.symbol_table.exit_scope()
            # print("Exit")
            # self.symbol_table.exit_scope()
            # self.symbol_table.exit_scope()
            return temp

        else:
            self.symbol_table.put(ctx.ID().getText(), self.get_line(ctx), "atribute")
            print("Enter")
            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx)
            print("Exit")
            self.symbol_table.exit_scope()
            return temp
    
    def visitFormal(self, ctx:yaplParser.FormalContext):
        self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "variableT", ctx.TYPE().getText())
        # print("Exit")
        # self.symbol_table.exit_scope()

        return None
    
    def visitExpr(self, ctx:yaplParser.ExprContext):
        # print("Llamada a Expr")
        new_scope_required = ctx.IF()

        if new_scope_required:
            print("Enter")
            self.symbol_table.enter_scope()
        
        if ctx.IF():
            print("Enter")
            self.symbol_table.enter_scope()
            self.symbol_table.put(ctx.getText(), ctx.start.line, "if")

            if ctx.ELSE():
                # print("ctx trae un else")
                # self.symbol_table.exit_scope()
                # print("Entro al else")
                print("Enter")
                self.symbol_table.enter_scope()
                self.symbol_table.put(ctx.getText(), ctx.start.line, "else")
                # temp = self.visitChildren(ctx)
                print("Exit")
                self.symbol_table.exit_scope()
            # else:
            #     temp = self.visitChildren(ctx)


            temp = self.visitChildren(ctx)
            print("Exit")
            self.symbol_table.exit_scope()
            # self.symbol_table.exit_scope()

            return temp


        elif ctx.WHILE():
            #print("entre a while")
            print("Enter")
            self.symbol_table.enter_scope()
            self.symbol_table.put('ctx.getText()', ctx.start.line, "while")
            temp = self.visitChildren(ctx)
            print("Exit")
            self.symbol_table.exit_scope()
            return temp

        elif ctx.LET():
            for i in range(len(ctx.ID())):
                self.symbol_table.put(ctx.ID()[i], self.get_line(ctx), "variable",ctx.TYPE()[i].getText())
                # for chil in ctx.getChildren():
                #     print(chil.getText())
                return self.visitChildren(ctx)
            #self.symbol_table.exit_scope()

        else:
            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx)
            self.symbol_table.exit_scope()
            return temp

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