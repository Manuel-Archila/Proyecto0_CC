from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode
from SymbolTable import Symbol, SymbolTable

class SemanticR(yaplVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def visit_program(self, ctx:yaplParser.ProgramContext):
        return self.visitChildren(ctx)
    
    def visitClass(self, ctx:yaplParser.ClassContext):
        
        self.symbol_table.enter_scope2()
        print(ctx.TYPE()[0].getText())
        self.symbol_table.enter_scope2()
        temp = self.visitChildren(ctx)
        self.symbol_table.exit_scope2()
        self.symbol_table.exit_scope2()
        return temp
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):

        if ctx.LPAR():
            #print("Enter")
            self.symbol_table.enter_scope2()
            temp = self.visitChildren(ctx)
            #print("Exit")
            self.symbol_table.exit_scope2()
            # #print("Exit")
            # self.symbol_table.exit_scope2()
            # self.symbol_table.exit_scope2()
            return temp

        else:
            #print("Enter")
            self.symbol_table.enter_scope2()
            temp = self.visitChildren(ctx)
            #print("Exit")
            self.symbol_table.exit_scope2()
            return temp
    
    def visitFormal(self, ctx:yaplParser.FormalContext):
        pass
        # #print("Exit")
        # self.symbol_table.exit_scope2()

        return None
    
    def visitExpr(self, ctx:yaplParser.ExprContext):
        # print("Llamada a Expr")
        new_scope_required = ctx.IF()

        if new_scope_required:
            #print("Enter")
            self.symbol_table.enter_scope2()
        # ARREGLAR IF Y ELSE DESPUES DE HACER EL RESTO
        if ctx.IF():
            #print("Enter")
            self.symbol_table.enter_scope2()
            self.symbol_table.put2(ctx.getText(), ctx.start.line, "if")

            if ctx.ELSE():
                # print("ctx trae un else")
                # self.symbol_table.exit_scope2()
                # print("Entro al else")
                #print("Enter")
                self.symbol_table.enter_scope2()
                self.symbol_table.put2(ctx.getText(), ctx.start.line, "else")
                # temp = self.visitChildren(ctx)
                #print("Exit")
                self.symbol_table.exit_scope2()
            # else:
            #     temp = self.visitChildren(ctx)

            temp = self.visitChildren(ctx)
            #print("Exit")
            self.symbol_table.exit_scope2()
            # self.symbol_table.exit_scope2()

            return temp

        if ctx.PLUS():
            print(ctx.DIGIT())
            print(ctx.getText())

        elif ctx.WHILE():
            #print("entre a while")
            #print("Enter")
            self.symbol_table.enter_scope2()
            self.symbol_table.put2('ctx.getText()', ctx.start.line, "while")
            temp = self.visitChildren(ctx)
            #print("Exit")
            self.symbol_table.exit_scope2()
            return temp

        elif ctx.LET():
            for i in range(len(ctx.ID())):
                self.symbol_table.put2(ctx.ID()[i], self.get_line(ctx), "variable",ctx.TYPE()[i].getText())
                # for chil in ctx.getChildren():
                #     print(chil.getText())

                return self.visitChildren(ctx)
        else:
            temp = self.visitChildren(ctx)
            return temp

    def get_line(self, node):
        if isinstance(node, TerminalNode):
            return node.symbol.line
        elif hasattr(node, 'start'):
            return node.start.line
        else:
            return None