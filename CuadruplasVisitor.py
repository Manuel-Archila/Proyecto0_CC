from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode

class CuadruplasVisitor(yaplVisitor):
    def __init__(self, symbol_table, cuadruplas):
        self.symbol_table = symbol_table
        self.cuadruplas = cuadruplas

    def visit_program(self, ctx:yaplParser.ProgramContext):
        return self.visitChildren(ctx)
    
    def visitClass(self, ctx:yaplParser.ClassContext):
        return self.visitChildren(ctx)
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):
        return self.visitChildren(ctx)
    
    def visitformal(self, ctx:yaplParser.FormalContext):
        return self.visitChildren(ctx)
    
    def visitExpr(self, ctx:yaplParser.ExprContext):

        if ctx.PLUS():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('+', first_child, second_child, "t")

        if ctx.MINUS():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('-', first_child, second_child, "t" )

        if ctx.TIMES():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('*', first_child, second_child, "t" )
        
        if ctx.DIVIDE():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('/', first_child, second_child, "t" )
        
        # if ctx.ASSIGN():
        #     first_child = ctx.getChild(0).getText()

        #     self.cuadruplas.agregar_cuadrupla('<-', first_child, None, "t" + str(self.cuadruplas.temporal_counter))
        
        if ctx.LT():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('<', first_child, second_child, "t" )
        
        if ctx.RT():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('>', first_child, second_child, "t" )
        
        if ctx.LE():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('<=', first_child, second_child, "t" )
        
        if ctx.RE():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('>=', first_child, second_child, "t" )
        
        if ctx.EQUALS():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            self.cuadruplas.agregar_cuadrupla('=', first_child, second_child, "t" )
        
        if ctx.NOT():
            first_child = ctx.getChild(0).getText()

            self.cuadruplas.agregar_cuadrupla('NOT', first_child, None, "t" )
        
        if ctx.ISVOID():
            first_child = ctx.getChild(0).getText()

            self.cuadruplas.agregar_cuadrupla('ISVOID', first_child, None, "t" )
        
        if ctx.DIAC():
            first_child = ctx.getChild(0).getText()

            self.cuadruplas.agregar_cuadrupla('~', first_child, None, "t" )
        
        if ctx.NEW():
            first_child = ctx.getChild(1).getText()

            self.cuadruplas.agregar_cuadrupla('NEW', first_child, None, "t" )
        
        if ctx.LET():
            first_child = ctx.getChild(1).getText()
            second_child = ctx.getChild(3).getText()

            self.cuadruplas.agregar_cuadrupla('LET', first_child, second_child, "t")
        
        if ctx.IF():
            first_child = ctx.getChild(1)

            operador = first_child.getChild(1).getText()
            
            arg1 = first_child.expr()[0].getText()
            arg2 = first_child.expr()[1].getText()

            operador = "IF (" + operador + ")"

            name1 = self.cuadruplas.agregar_cuadrupla(operador, arg1, arg2, "L")
            name2 = self.cuadruplas.agregar_cuadrupla("GOTO_IFFALSE", None, None, "L")

            self.cuadruplas.agregar_cuadrupla("LABEL", name1, None, None)

            self.visit(ctx.expr(1))

            self.cuadruplas.agregar_cuadrupla("LABEL", name2, None, None)

            self.visit(ctx.expr(2))

        
        if ctx.WHILE():
            first_child = ctx.getChild(1)

            operador = first_child.getChild(1).getText()
            
            arg1 = first_child.expr()[0].getText()
            arg2 = first_child.expr()[1].getText()

            name1 = self.cuadruplas.nuevoLabel("L")

            self.cuadruplas.agregar_cuadrupla("LABEL", name1, None, None)

            name2 = self.cuadruplas.agregar_cuadrupla(operador, arg1, arg2, "L")
            self.cuadruplas.agregar_cuadrupla("GOTO_IFFALSE", None, None, "EXIT")

            self.cuadruplas.agregar_cuadrupla("LABEL", name2, None, None)

            self.visit(ctx.expr(1))

            self.cuadruplas.agregar_cuadrupla("GOTO", None, None, name1)

            first_child




            