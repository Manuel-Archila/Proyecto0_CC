from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode
from SymbolTable import Symbol, SymbolTable
import re

class SemanticV2(yaplVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errores = []
        self.classes = []
        self.NOexiste= []
        self.circular = True
        self.mmain2 = False
        self.originales = ["Int", "String", "Bool", "IO", "Object"]

    def visit_program(self, ctx:yaplParser.ProgramContext):
        self.symbol_table.enter_scope3()
        return self.visitChildren(ctx)
    
    def visitClass(self, ctx:yaplParser.ClassContext):

        if ctx.INHERITS():

            hereda2 = ctx.TYPE()[1].getText()

            salmon = True

            while salmon:
                if hereda2 not in self.classes:
                    self.classes.append(hereda2)
                    current_scope = self.symbol_table.getScope2()

                    respuesta1 = self.symbol_table.getSymbol(hereda2, current_scope)

                    if respuesta1 == None:
                        if hereda2 not in self.NOexiste:
                            mensaje = "Error: La clase " + hereda2 + " no existe"
                            self.NOexiste.append(hereda2)
                            #self.errores.append(mensaje)
                            # #print(mensaje)
                        salmon = False
                    else:

                        hereda2 = respuesta1.hereda

                    if hereda2 == "Object" or hereda2 == None:
                        self.classes = []
                        salmon = False
                else:
                    if self.circular:
                        mensaje = "Error en línea " + str(self.get_line(ctx)) + ": La clase " + hereda2 + " causa un ciclo de herencia"
                        #self.errores.append(mensaje)
                        # #print(mensaje)
                        self.circular = False
                    salmon = False
            self.classes = []
 
        ## #print(ctx.TYPE()[0].getText())
        self.symbol_table.enter_scope3()
        temp = self.visitChildren(ctx)
        self.symbol_table.exit_scope3()
        #self.symbol_table.exit_scope3()
        return temp
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):

        tipo = ctx.TYPE().getText()

        if ctx.LPAR():

            if ctx.ID().getText() == "main":
                parent_ctx = ctx.parentCtx
                if parent_ctx.TYPE()[0].getText() == "Main":
                    self.mmain2 = True

               
            self.symbol_table.enter_scope3()
            temp = self.visitChildren(ctx)
            self.symbol_table.exit_scope3()

            if ctx.expr():

                if ctx.expr().DOT():

                    if ctx.expr().AT():

                        padre = ctx.expr().TYPE()[0].getText()

                        fun2 = ctx.expr().ID()[0].getText()

                        scopeH = self.symbol_table.getSpecificScope(padre)

                        resp = self.symbol_table.getItem(fun2, scopeH)

                        if resp[0] == False:
                            error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + fun2
                            self.errores.append(error)
                            return "Indefinido"
                        
                        else:

                            type2 = resp[1]

                            if tipo != type2:
                                mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + str(type2) + " no coincide con el retorno " + str(tipo)
                                self.errores.append(mensaje)


                            return type2

                    else:

                        fun2 = ctx.expr().ID()[0].getText()

                        current = self.symbol_table.getSpecific2(fun2)

                        resp = self.symbol_table.getItem(fun2, current)

                        if resp[0] == False:
                            
                            inheri = False
                            parent_ctx = ctx

                            seaClass = True

                            while seaClass:
                                #print("Chequeo si existe y argumentos 2")
                                parent_ctx = parent_ctx.parentCtx
                                if isinstance(parent_ctx, yaplParser.ClassContext):
                                    parent_ctx = parent_ctx.TYPE()[0].getText()

                                    while not inheri:
                                        #print("Inheri de Chequeo si existe y argumentos 2")

                                        sco = self.symbol_table.getSpecific(parent_ctx)
                                        
                                        r = self.symbol_table.getSymbol(parent_ctx, sco)


                                        if r.hereda is not None:
                                            hereda = r.hereda


                                            scopeH = self.symbol_table.getSpecificScope(hereda)


                                            resp = self.symbol_table.getItem(fun2, scopeH)


                                            
                                            if resp[0] == False:

                                                inheri = resp[0]
                                                parent_ctx = hereda

                                            else:
                                                

                                                type2 = resp[1]

                                                if tipo != type2:
                                                    mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + str(type2) + " no coincide con el retorno " + str(tipo)
                                                    self.errores.append(mensaje)

                                                    inheri = True


                                        else:

                                            inheri = True
                                        

                                    seaClass = False
                        
                        else:

                            type2 = resp[1]

                            if tipo != type2:
                                mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + str(type2) + " no coincide con el retorno " + str(tipo)
                                self.errores.append(mensaje)
                        



                if ctx.expr().LPAR():

                    fun = ctx.ID().getText()

                    current = self.symbol_table.getSpecific2(fun)

                    fun2 = ctx.expr().getChild(0).getText()

                    resp = self.symbol_table.getItem(fun2, current)


                    if resp[0] == False:
                        
                        inheri = False
                        parent_ctx = ctx

                        seaClass = True

                        while seaClass:
                            #print("Chequeo si existe y argumentos 2")
                            parent_ctx = parent_ctx.parentCtx
                            if isinstance(parent_ctx, yaplParser.ClassContext):
                                parent_ctx = parent_ctx.TYPE()[0].getText()

                                while not inheri:
                                    #print("Inheri de Chequeo si existe y argumentos 2")

                                    sco = self.symbol_table.getSpecific(parent_ctx)
                                    
                                    r = self.symbol_table.getSymbol(parent_ctx, sco)


                                    if r.hereda is not None:
                                        hereda = r.hereda


                                        scopeH = self.symbol_table.getSpecificScope(hereda)


                                        resp = self.symbol_table.getItem(fun2, scopeH)


                                        
                                        if resp[0] == False:

                                            inheri = resp[0]
                                            parent_ctx = hereda

                                        else:
                                            

                                            type2 = resp[1]

                                            if tipo != type2:
                                                mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + str(type2) + " no coincide con el retorno " + str(tipo)
                                                self.errores.append(mensaje)

                                                inheri = True

                                            inheri = True

                                    else:
                                        inheri = True
                                    

                                seaClass = False
                    
                    else:

                        type2 = resp[1]

                        if tipo != type2:
                            mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + str(type2) + " no coincide con el retorno " + str(tipo)
                            self.errores.append(mensaje)
                   
                else:

                    type2 = self.visit(ctx.expr())

                    ty = ctx.TYPE().getText()

                    if ty != type2:
                        mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + str(type2) + " no coincide con el retorno " + str(ty)
                        self.errores.append(mensaje)

            return temp

        else:

            if ctx.ASSIGN():

                tipo2 = ctx.getChild(4).getText()

                indice = tipo2.find("new")  # Encuentra la posición de "new" en la cadena
                if indice != -1:
                    tipo2 = tipo2[indice + len("new"):]

                if tipo != tipo2:
                    mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + tipo + " no coincide con el tipo " + tipo2
                    #self.errores.append(mensaje)
                    # #print(mensaje)


            parent_ctx = ctx

            seaClass = True

            while seaClass:
                parent_ctx = parent_ctx.parentCtx
                if isinstance(parent_ctx, yaplParser.ClassContext):
                    parent_ctx = parent_ctx.TYPE()[0].getText()

                    sco = self.symbol_table.getSpecific(parent_ctx)

                    r = self.symbol_table.getItem(tipo, sco)

                    if r[0] == False:
                        if tipo not in self.originales:
                            mensaje = "Error en línea " + str(self.get_line(ctx)) + ": El tipo " + tipo + " no existe"
                            #self.errores.append(mensaje)
                            # #print(mensaje)

                    seaClass = False
           
            temp = self.visitChildren(ctx)
            return temp
    
    def visitFormal(self, ctx:yaplParser.FormalContext):
        pass
        # ## #print("Exit")
        # self.symbol_table.exit_scope3()

        return None
    
    def visitExpr(self, ctx:yaplParser.ExprContext):
        # # #print("Llamada a Expr")
        # ARREGLAR IF Y ELSE DESPUES DE HACER EL RESTO
        if ctx.IF():
            ## #print("Enter")

            #print(ctx.expr()[0].getText())
            #print(ctx.expr()[1].getText())
            #print(ctx.expr()[2].getText())

            self.symbol_table.enter_scope3()
            temp = self.visit(ctx.expr()[0])
            self.symbol_table.exit_scope3()

            if temp != "Bool":
                mensaje = "Error en línea " + str(self.get_line(ctx)) + ": La condición del if no es de tipo Bool"
                #self.errores.append(mensaje)

            self.symbol_table.enter_scope3()
            temp1 = self.visit(ctx.expr()[1])
            self.symbol_table.exit_scope3()

            self.symbol_table.enter_scope3()
            temp2 = self.visit(ctx.expr()[2])
            self.symbol_table.exit_scope3()


            if temp1 != temp2:
                if temp1 in self.originales and temp2 in self.originales:
                    return "Object"
                else:
                    mensaje = "Error en línea " + str(self.get_line(ctx)) + ": Los tipos de retorno del if no coinciden"
                    #self.errores.append(mensaje)
                    return "Object"
                
            else:
                return temp1

        elif ctx.PLUS():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope2()

            #print(ctx.getChild(0).getText())
            #print(ctx.getChild(2).getText())

            #print(first_child)
            #print(second_child)

            if first_child != "String" or first_child != "Boolean" or first_child != "Int":
                respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)
            else:
                respuesta1 = (True, first_child)
            if second_child != "String" or second_child != "Bool" or second_child != "Int":
                respuesta2 = self.symbol_table.getItem(ctx.getChild(2).getText(), current_scope)
            else:
                respuesta2 = (True, second_child)

            #print(respuesta1)
            #print(respuesta2)

            if respuesta1[0] == True:
                first_child = respuesta1[1]
            if respuesta2[0] == True:
                second_child = respuesta2[1]

            #print(first_child)
            #print(second_child)

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
                mensaje ="Error en línea " + str(self.get_line(ctx)) + ": No se puede sumar " + first_child + " con " + second_child
                #self.errores.append(mensaje)
                # #print(mensaje)
                return "Int"

        elif ctx.MINUS():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope2()

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
                mensaje ="Error en línea " + str(self.get_line(ctx)) + ": No se puede restar " + first_child + " con " + second_child
                #self.errores.append(mensaje)
                # #print(mensaje)
                return "Int"

        elif ctx.TIMES():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope2()

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
                mensaje ="Error en línea " + str(self.get_line(ctx)) + ": No se puede multiplicar " + first_child + " con " + second_child
                #self.errores.append(mensaje)
                # #print(mensaje)
                return "Int"

        elif ctx.DIVIDE():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope2()

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
                mensaje ="Error en línea " + str(self.get_line(ctx)) + ": No se puede dividir " + first_child + " con " + second_child
                #self.errores.append(mensaje)
                # #print(mensaje)
                return "Int"

        elif ctx.LT() or ctx.RT() or ctx.RE() or ctx.LE() or ctx.EQUALS():
            first_child = self.visit(ctx.getChild(0))
            second_child = self.visit(ctx.getChild(2))

            current_scope = self.symbol_table.getScope2()
            # #print(current_scope)

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
                error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede comparar " + first_child + " con " + second_child
                #self.errores.append(error)
                # #print(error)
                return "Bool"
        
        elif ctx.NOT():
            first_child = self.visit(ctx.getChild(1))

            current_scope = self.symbol_table.getScope2()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(1).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]

            if first_child is None:
                first_child = "Indefinido"

            if first_child == "Bool" or first_child == "Int":
                return "Bool"
            else:
                error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede negar " + first_child
                #self.errores.append(error)
                # #print(error)
                return "Bool"
            
        elif ctx.DIAC():
            first_child = self.visit(ctx.getChild(1))

            current_scope = self.symbol_table.getScope2()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(1).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]

            if first_child is None:
                first_child = "Indefinido"

            if first_child == "Bool" or first_child == "Int":
                return "Int"
            else:
                error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede hacer el complemento de " + first_child
                #self.errores.append(error)
                # #print(error)
                return "Int"

        elif ctx.ISVOID():
            first_child = self.visit(ctx.getChild(1))

            current_scope = self.symbol_table.getScope2()

            respuesta1 = self.symbol_table.getItem(ctx.getChild(1).getText(), current_scope)

            if respuesta1[0] == True:
                first_child = respuesta1[1]

            if first_child is None:
                first_child = "Indefinido"

            if first_child == "String" or first_child == "Int":
                return "Bool"
            else:
                error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede validar a nulabilidad de  " + first_child
                #self.errores.append(error)
                # #print(error)
                return "Bool"

        elif ctx.WHILE():

            self.symbol_table.enter_scope3()
            temp = self.visit(ctx.expr()[0])
            self.symbol_table.exit_scope3()

            self.symbol_table.enter_scope3()
            temp1 = self.visit(ctx.expr()[1])
            self.symbol_table.exit_scope3()


            return temp1

        elif ctx.LET():


            self.symbol_table.enter_scope3()
            temp = self.visitChildren(ctx)
            self.symbol_table.exit_scope3()

            return temp

        elif ctx.STRING():
            return "String"

        elif ctx.DOT():

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

            if ctx.AT():
                
                padre = ctx.TYPE()[0].getText()

                funtion = ctx.ID()[0].getText()

                scopeH = self.symbol_table.getSpecificScope(padre)


                resp = self.symbol_table.getItem(funtion, scopeH)

                argumentTemp = self.symbol_table.getSymbol(funtion, scopeH)

                if argumentTemp is not None:
                    argument = argumentTemp.params


                if resp[0] == False:
                    error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + funtion
                    #self.errores.append(error)
                    return "Indefinido"
                else:

                    if len(argument) != len(argumentoss):
                        error = "Error en línea " + str(self.get_line(ctx)) + ": se esperan  " + str(len(argument)) + " argumentos, pero se recibieron " + str(len(argumentoss))
                        #self.errores.append(error)
                        # #print(error)
                        return "Indefinido"
                    else:
                        for argumento, parametro in zip(argumentoss, argument):
                            if argumento[1] != parametro[1]:
                                error = "Error en línea " + str(self.get_line(ctx)) + ": El argumento  " + str(argumento[0]) + " no es de tipo " + str(parametro[1])
                                #self.errores.append(error)
                                # #print(error)
                                return "Indefinido"
                            
                    
                    return resp[1]


            else:
                # #print(argumentoss)

                funtion = ctx.ID()[0].getText()
                # #print(funtion)
                current_scope = self.symbol_table.getScope2()

                respuesta1 = self.symbol_table.getItem(funtion, current_scope)

                argumentTemp = self.symbol_table.getSymbol(funtion, current_scope)

                if argumentTemp is not None:
                    argument = argumentTemp.params

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

                                    argumentTemp = self.symbol_table.getSymbol(funtion, scopeH)

                                    if argumentTemp is not None:
                                        argument = argumentTemp.params

                                    inheri = resp[0]

                                    
                                    if resp[0] == False:

                                        inheri = resp[0]
                                        parent_ctx = hereda

                                    else:

                                        # #print(argument)
                                        # #print(argumentoss)

                                        if len(argument) != len(argumentoss):
                                            error = "Error en línea " + str(self.get_line(ctx)) + ": se esperan  " + str(len(argument)) + " argumentos, pero se recibieron " + str(len(argumentoss))
                                            #self.errores.append(error)
                                            # #print(error)
                                            return "Indefinido"
                                        else:
                                            for argumento, parametro in zip(argumentoss, argument):
                                                if argumento[1] != parametro[1]:
                                                    error = "Error en línea " + str(self.get_line(ctx)) + ": El argumento  " + str(argumento[0]) + " no es de tipo " + str(parametro[1])
                                                    #self.errores.append(error)
                                                    # #print(error)
                                                    return "Indefinido"
                                        
                                        return resp[1]
                                    
                                elif r.hereda == "Main":
                                    error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + funtion
                                    #self.errores.append(error)
                                    # #print(error)
                                    return "Indefinido"

                                else:

                                    inheri = True
                                    

                            seaClass = False
                        
                if respuesta1[0] == False:
                    error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + funtion
                    #self.errores.append(error)
                    # #print(error)
                    return "Indefinido"

                if len(argument) != len(argumentoss):
                    error = "Error en línea " + str(self.get_line(ctx)) + ": se esperan  " + str(len(argument)) + " argumentos, pero se recibieron " + str(len(argumentoss))
                    #self.errores.append(error)
                    # #print(error)
                    return "Indefinido"
                else:
                    for argumento, parametro in zip(argumentoss, argument):
                        if argumento[1] != parametro[1]:
                            error = "Error en línea " + str(self.get_line(ctx)) + ": El argumento " + str(argumento[0])+ " no es de tipo " + str(parametro[1])
                            #self.errores.append(error)
                            # #print(error)
                            return "Indefinido"

                return respuesta1[1]
        
        elif ctx.ID():
            if ctx.ID()[0].getText() == "self":
                if ctx.DOT():
                    error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede usar self en una llamada a metodo"
                    #self.errores.append(error)

            if ctx.getChildCount() > 0:

                if ctx.ASSIGN():
                    return (self.visitChildren(ctx))
                
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
                    current_scope = self.symbol_table.getScope2()

                    respuesta1 = self.symbol_table.getItem(ctx.getChild(0).getText(), current_scope)

                    argumentTemp = self.symbol_table.getSymbol(ctx.getChild(0).getText(), current_scope)

                    if argumentTemp is not None:
                        argument = argumentTemp.params

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

                                        argumentTemp = self.symbol_table.getSymbol(funtion, scopeH)

                                        if argumentTemp is not None:
                                            argument = argumentTemp.params

                                        inheri = resp[0]

                                        
                                        if resp[0] == False:

                                            inheri = resp[0]
                                            parent_ctx = hereda

                                        else:

                                            # #print(argument)
                                            # #print(argumentoss)

                                            if len(argument) != len(argumentoss):
                                                error = "Error en línea " + str(self.get_line(ctx)) + ": se esperan  " + str(len(argument)) + " argumentos, pero se recibieron " + str(len(argumentoss))
                                                #self.errores.append(error)
                                                # #print(error)
                                                return "Indefinido"
                                            else:
                                                for argumento, parametro in zip(argumentoss, argument):
                                                    if argumento[1] != parametro[1]:
                                                        error = "Error en línea " + str(self.get_line(ctx)) + ": El argumento  " + str(argumento[0]) + " no es de tipo " + str(parametro[1])
                                                        #self.errores.append(error)
                                                        # #print(error)
                                                        return "Indefinido"
                                            
                                            return resp[1]
                                        
                                    elif r.hereda == "Main":
                                        error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + funtion
                                        #self.errores.append(error)
                                        # #print(error)
                                        return "Indefinido"

                                    else:

                                        inheri = True
                                        

                                seaClass = False
                            
                    if respuesta1[0] == False:
                        error = "Error en línea " + str(self.get_line(ctx)) + ": No se puede reconocer  " + funtion
                        #self.errores.append(error)
                        # #print(error)
                        return "Indefinido"

                    if len(argument) != len(argumentoss):
                        error = "Error en línea " + str(self.get_line(ctx)) + ": se esperan  " + str(len(argument)) + " argumentos, pero se recibieron " + str(len(argumentoss))
                        #self.errores.append(error)
                        # #print(error)
                        return "Indefinido"
                    else:
                        for argumento, parametro in zip(argumentoss, argument):
                            if argumento[1] != parametro[1]:
                                error = "Error en línea " + str(self.get_line(ctx)) + ": El argumento " + str(argumento[0])+ " no es de tipo " + str(parametro[1])
                                #self.errores.append(error)
                                # #print(error)
                                return "Indefinido"

                    return respuesta1[1]
            else:
                return "String"
        
        elif ctx.TRUE() or ctx.FALSE():
            return "Bool"

        elif ctx.DIGIT():
            return "Int"

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
        