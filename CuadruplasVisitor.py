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

        if ctx.INHERITS():
            self.cuadruplas.agregar_cuadrupla("CLASS", ctx.TYPE()[0].getText(), ctx.TYPE()[1].getText(), None)

        else:
            self.cuadruplas.agregar_cuadrupla("CLASS", ctx.TYPE()[0].getText(), None, None)

        
        tm = self.visitChildren(ctx)

        self.cuadruplas.agregar_cuadrupla("END_CLASS", ctx.TYPE()[0].getText(), None, None)
        return 
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):

        if ctx.LPAR():
            
            params = []
            if ctx.formal():
                for por in ctx.formal():
                    string = por.getText()
                    string = string.split(":")
                    params.append((string[0], string[1]))
                    
            for tupla in params:
                self.cuadruplas.agregar_cuadrupla('PARAM', None, None, tupla[0])

        if ctx.COLON():

            variable = ctx.getChild(0).getText()
            self.cuadruplas.agregar_cuadrupla("DECLARE", variable, None, None)



            if ctx.ASSIGN():

                variable = ctx.getChild(0).getText()
                val = self.visit(ctx.getChild(4))

                if val is not None:
                    self.cuadruplas.agregar_cuadrupla("ASSING", val, None, variable)
                else:
                    self.cuadruplas.agregar_cuadrupla("ASSING", variable, None, "t")

                return None
        

        tm = self.visitChildren(ctx)

        if ctx.LPAR():
            self.cuadruplas.agregar_cuadrupla("END_FUNCTION", variable, None, None)


        return tm
    
    def visitformal(self, ctx:yaplParser.FormalContext):
        return self.visitChildren(ctx)
    
    def visitExpr(self, ctx:yaplParser.ExprContext):

        if ctx.PLUS():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('+', first_child, second_child, "t")

            return valor

        if ctx.MINUS():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('-', first_child, second_child, "t" )

            return valor

        if ctx.TIMES():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('*', first_child, second_child, "t" )

            return valor

        if ctx.DIVIDE():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('/', first_child, second_child, "t" )

            return valor

        if ctx.LT():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('<', first_child, second_child, "t" )

            return valor

        if ctx.RT():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('>', first_child, second_child, "t" )

            return valor

        if ctx.LE():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('<=', first_child, second_child, "t" )

            return valor

        if ctx.RE():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('>=', first_child, second_child, "t" )

            return valor

        if ctx.EQUALS():
            first_child = ctx.getChild(0).getText()
            second_child = ctx.getChild(2).getText()

            valor = self.cuadruplas.agregar_cuadrupla('=', first_child, second_child, "t" )

            return valor

        if ctx.NOT():
            first_child = ctx.getChild(0).getText()

            valor = self.cuadruplas.agregar_cuadrupla('NOT', first_child, None, "t" )

            return valor

        if ctx.ISVOID():
            first_child = ctx.getChild(0).getText()

            valor = self.cuadruplas.agregar_cuadrupla('ISVOID', first_child, None, "t" )

            return valor

        if ctx.DIAC():
            first_child = ctx.getChild(0).getText()

            valor = self.cuadruplas.agregar_cuadrupla('~', first_child, None, "t" )

            return valor

        if ctx.NEW():
            first_child = ctx.getChild(1).getText()

            valor = self.cuadruplas.agregar_cuadrupla('NEW', first_child, None, "t" )

            return valor

        if ctx.LET():
            first_child = ctx.getChild(1).getText()
            second_child = ctx.getChild(3).getText()

            valor = self.cuadruplas.agregar_cuadrupla('LET', first_child, second_child, "t")

            return valor

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

        if ctx.ID():

            if ctx.ASSIGN():

                first_child = ctx.getChild(0).getText()
                second_child = ctx.getChild(2)

                val = self.visit(second_child)

                first_child = "BaseIntancia + offset" + first_child

                if val is not None:

                    self.cuadruplas.agregar_cuadrupla("ASSING", val, None, first_child)
                else:
                    num = self.cuadruplas.encontrar_cuadrupla_param(second_child.getText())

                    if num is not None:
                        self.cuadruplas.agregar_cuadrupla("ASSING", second_child.getText(), None, first_child)

            if ctx.LPAR():
                    
                    argumentoss = []
                    contenido_actual = None

                    for elemento in ctx.getChildren():
                        if elemento.getText() == '(':
                            contenido_actual = []
                        elif elemento.getText() == ')':
                            if contenido_actual is not None:
                                argumentoss.append(contenido_actual)
                                contenido_actual = None
                        elif contenido_actual is not None:
                            if ',' not in elemento.getText():
                                contenido_actual.append((elemento.getText(), self.visit(elemento)))
                    argumentoss = argumentoss[0]



                    funtion = ctx.ID()[0].getText()
                    
                    
                    self.cuadruplas.agregar_cuadrupla('CALL', funtion, len(argumentoss), "t")

        if ctx.STRING():

            return ctx.getText()

        if ctx.DIGIT():

            return ctx.getText()
        
        if ctx.TRUE() or ctx.FALSE():

            return ctx.getText()


            