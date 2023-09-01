from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode
from SymbolTable import Symbol, SymbolTable

class SemanticR(yaplVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errores = []
        self.classes = []
        self.NOexiste= []
        self.circular = True

    def visit_program(self, ctx:yaplParser.ProgramContext):
        self.symbol_table.enter_scope2()
        return self.visitChildren(ctx)
    
    def visitClass(self, ctx:yaplParser.ClassContext):

        if ctx.INHERITS():

            hereda2 = ctx.TYPE()[1].getText()

            salmon = True

            while salmon:
                if hereda2 not in self.classes:
                    self.classes.append(hereda2)
                    current_scope = self.symbol_table.getScope()

                    respuesta1 = self.symbol_table.getSymbol(hereda2, current_scope)

                    if respuesta1 == None:
                        if hereda2 not in self.NOexiste:
                            mensaje = "Error: La clase " + hereda2 + " no existe"
                            self.NOexiste.append(hereda2)
                            self.errores.append(mensaje)
                            print(mensaje)
                        salmon = False
                    else:

                        hereda2 = respuesta1.hereda

                    if hereda2 == "Object" or hereda2 == None:
                        self.classes = []
                        salmon = False
                else:
                    if self.circular:
                        mensaje = "Error en linea " + str(self.get_line(ctx)) + ": La clase " + hereda2 + " causa un ciclo de herencia"
                        self.errores.append(mensaje)
                        print(mensaje)
                        self.circular = False
                    salmon = False
            self.classes = []
 
        #print(ctx.TYPE()[0].getText())
        self.symbol_table.enter_scope2()
        temp = self.visitChildren(ctx)
        self.symbol_table.exit_scope2()
        #self.symbol_table.exit_scope2()
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
                return "Int"
            elif first_child == "String" and second_child == "String":
                return "String"
            elif first_child == "Int" and second_child == "Bool":
                return "Int"
            elif first_child == "Bool" and second_child == "Int":
                return "Int"
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
                return "Int"
            elif first_child == "Int" and second_child == "Bool":
                return "Int"
            elif first_child == "Bool" and second_child == "Int":
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
                return "Int"
            elif first_child == "Int" and second_child == "Bool":
                return "Int"
            elif first_child == "Bool" and second_child == "Int":
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
                return "Int"
            elif first_child == "Int" and second_child == "Bool":
                return "Int"
            elif first_child == "Bool" and second_child == "Int":
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
                return "Bool"
            elif first_child == "Int" and second_child == "Bool":
                return "Bool"
            elif first_child == "Bool" and second_child == "Int":
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

            if first_child == "Bool" or first_child == "Int":
                return "Bool"
            else:
                error = "Error en linea " + str(self.get_line(ctx)) + ": No se puede negar " + first_child
                self.errores.append(error)
                print(error)
                return "Bool"
            
        elif ctx.DIAC():
            first_child = self.visit(ctx.getChild(1))

            current_scope = self.symbol_table.getScope()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(1).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]

            if first_child is None:
                first_child = "Indefinido"

            if first_child == "Bool" or first_child == "Int":
                return "Int"
            else:
                error = "Error en linea " + str(self.get_line(ctx)) + ": No se puede hacer el complemento de " + first_child
                self.errores.append(error)
                print(error)
                return "Int"

        elif ctx.ISVOID():
            first_child = self.visit(ctx.getChild(1))

            current_scope = self.symbol_table.getScope()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(1).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]

            if first_child is None:
                first_child = "Indefinido"

            if first_child == "String" or first_child == "Int":
                return "Bool"
            else:
                error = "Error en linea " + str(self.get_line(ctx)) + ": No se puede validar a nulabilidad de  " + first_child
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
        
        elif ctx.ID():

            if ctx.getChildCount() > 0:

                if ctx.ASSIGN():
                    return (self.visitChildren(ctx))
                
                if ctx.LPAR():

                    funtion = ctx.ID()[0].getText()
                    current_scope = self.symbol_table.getScope()
                    # print(current_scope)
                    # print("simon si si si s")

                    respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)

                    if respuesta1[0] == False:

                        inheri = False
                        parent_ctx = ctx

                        seaClass = True

                        while seaClass:
                            parent_ctx = parent_ctx.parentCtx
                            if isinstance(parent_ctx, yaplParser.ClassContext):
                                parent_ctx = parent_ctx.TYPE()[0].getText()

                                while not inheri:

                                    sco = self.symbol_table.getSpecific(parent_ctx)
                                    
                                    r = self.symbol_table.getSymbol(parent_ctx, sco)



                                    if r.hereda is not None:
                                        hereda = r.hereda


                                        scopeH = self.symbol_table.getSpecificScope(hereda)


                                        resp = self.symbol_table.getItem(funtion, scopeH)

                                        inheri = resp[0]

                                        
                                        if resp[0] == False:

                                            inheri = resp[0]
                                            parent_ctx = hereda

                                        else:
                                            print(resp[1])
                                            return resp[1]
                                        
                                    elif r.hereda == "Main":
                                        error = "Error en linea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + funtion
                                        self.errores.append(error)
                                        print(error)
                                        return "Int"

                                    else:

                                        inheri = True
                                        

                                seaClass = False
                            
                            


                            
                        
                    
                    if respuesta1[0] == False:
                        error = "Error en linea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + funtion
                        self.errores.append(error)
                        print(error)
                        return "Int"
                    
                    print(respuesta1[1])

                    return respuesta1[1]
            else:
                return "String"
        
        elif ctx.TRUE() or ctx.FALSE():
            return "Bool"
    
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