from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode
from SymbolTable import Symbol, SymbolTable

class SemanticR(yaplVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errores = []

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

        elif ctx.PLUS():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)
            respuesta2 = self.symbol_table.getItem(ctx.getChild(2).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]
            if respuesta2[0] == True:
                second_child = respuesta2[1]

            if second_child is None:
                second_child = "Indefinido"
            if first_child is None:
                first_child = "Indefinido"


            if first_child == "Int" and second_child == "Int":
                print("No hay errores")
                return "Int"
            elif first_child == "String" and second_child == "String":
                print("No hay errores")
                return "String"
            else:
                mensaje ="Error en linea" + str(self.get_line(ctx)) + ": No se puede sumar " + first_child + " con " + second_child
                self.errores.append(mensaje)
                print(mensaje)
                return "Int"

        elif ctx.MINUS():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)
            respuesta2 = self.symbol_table.getItem(ctx.getChild(2).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]
            if respuesta2[0] == True:
                second_child = respuesta2[1]

            if second_child is None:
                second_child = "Indefinido"
            if first_child is None:
                first_child = "Indefinido"


            if first_child == "Int" and second_child == "Int":
                print("No hay errores")
                return "Int"
            else:
                mensaje ="Error en linea " + str(self.get_line(ctx)) + ": No se puede restar " + first_child + " con " + second_child
                self.errores.append(mensaje)
                print(mensaje)
                return "Int"

        elif ctx.TIMES():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)
            respuesta2 = self.symbol_table.getItem(ctx.getChild(2).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]
            if respuesta2[0] == True:
                second_child = respuesta2[1]

            if second_child is None:
                second_child = "Indefinido"
            if first_child is None:
                first_child = "Indefinido"


            if first_child == "Int" and second_child == "Int":
                print("No hay errores")
                return "Int"
            else:
                mensaje ="Error en linea " + str(self.get_line(ctx)) + ": No se puede multiplicar " + first_child + " con " + second_child
                self.errores.append(mensaje)
                print(mensaje)
                return "Int"

        elif ctx.DIVIDE():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)
            respuesta2 = self.symbol_table.getItem(ctx.getChild(2).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]
            if respuesta2[0] == True:
                second_child = respuesta2[1]

            if second_child is None:
                second_child = "Indefinido"
            if first_child is None:
                first_child = "Indefinido"


            if first_child == "Int" and second_child == "Int":
                print("No hay errores")
                return "Int"
            else:
                mensaje ="Error en linea " + str(self.get_line(ctx)) + ": No se puede dividir " + first_child + " con " + second_child
                self.errores.append(mensaje)
                print(mensaje)
                return "Int"

        elif ctx.LT() or ctx.RT() or ctx.RE() or ctx.LE() or ctx.EQUALS():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope()
            print(current_scope)

            respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)
            respuesta2 = self.symbol_table.getItem(ctx.getChild(2).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]
            if respuesta2[0] == True:
                second_child = respuesta2[1]

            if second_child is None:
                second_child = "Indefinido"
            if first_child is None:
                first_child = "Indefinido"


            if first_child == "Int" and second_child == "Int":
                print("No hay errores")
                return "Bool"

            else:
                error = "Error en linea " + str(self.get_line(ctx)) + ": No se puede comparar " + first_child + " con " + second_child
                self.errores.append(error)
                print(error)
                return "Bool"
        
        elif ctx.NOT():
            first_child = self.visit(ctx.getChild(1))

            current_scope = self.symbol_table.getScope()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(1).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]

            if first_child is None:
                first_child = "Indefinido"

            if first_child == "Bool":
                print("No hay errores")
                return "Bool"
            else:
                error = "Error en linea " + str(self.get_line(ctx)) + ": No se puede negar " + first_child
                self.errores.append(error)
                print(error)
                return "Bool"
            
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
        
        elif ctx.DIGIT():
            return "Int"

        elif ctx.STRING():
            return "String"
        
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