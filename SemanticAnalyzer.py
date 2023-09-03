from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode
from SymbolTable import Symbol, SymbolTable

class SemanticAnalyzerMio(yaplVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.mmain = False
        self.mmain2 = False
        self.errores = []

    def visit_program(self, ctx:yaplParser.ProgramContext):
        self.symbol_table.enter_scope()
        return self.visitChildren(ctx)
    
    def visitClass(self, ctx:yaplParser.ClassContext):
        ## print("Llamada a class")
        hereda = None
        
        if ctx.INHERITS():

            hereda = ctx.TYPE()[1].getText()

            if ctx.TYPE()[0].getText() == ctx.TYPE()[1].getText():
                self.errores.append("Error: Herencia circular")
                # print("Error: Herencia circular")
                
            if ctx.TYPE()[0].getText() == "Main":
                self.errores.append("Error: Herencia de Main")
                # print("Error: Herencia de Main")

            if ctx.TYPE()[1].getText() == "String" or ctx.TYPE()[1].getText() == "Int" or ctx.TYPE()[1].getText() == "Bool":
                self.errores.append("Error: No se puede heredar de clases nativas")
                # print("Error: No se puede heredar de clases nativas")
        
        if ctx.TYPE()[0].getText() == "SELF_TYPE":
            self.errores.append("Error: La clase no se puede llamar SELF_TYPE")
            # print("Error: La clase no se puede llamar SELF_TYPE")
        
        
        if ctx.TYPE()[0].getText() == "Main":
            self.mmain = True

        
        if hereda is None:
            if ctx.TYPE()[0].getText() == "Main" or ctx.TYPE()[0].getText() == "Object":
                hereda = None
            else:
                hereda = "Object"

        current = self.symbol_table.getScopE()

        resp = self.symbol_table.getItem(ctx.TYPE()[0].getText(), current)

        if resp[0] == True:
            self.errores.append("Error: La clase " + ctx.TYPE()[0].getText() + " ya existe")
            # print("Error: La clase " + ctx.TYPE()[0].getText() + " ya existe")

        else:
        
            self.symbol_table.put(ctx.TYPE()[0].getText(), ctx.start.line, "class", None , hereda)
        self.symbol_table.enter_scope()
        temp = self.visitChildren(ctx)
        self.symbol_table.exit_scope()
        #self.symbol_table.exit_scope()
        return temp
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):
        ## print("Llamada a feature")

        if ctx.LPAR():
            
            params = []
            if ctx.formal():
                for por in ctx.formal():
                    string = por.getText()
                    string = string.split(":")
                    params.append((string[0], string[1]))
                    
            valores_vistos = set()
            repetidos = False
            for tupla in params:
                if tupla[0] in valores_vistos:
                    repetidos = True  
                valores_vistos.add(tupla[0])

            if repetidos:
                self.errores.append("Error en la línea " + str(self.get_line(ctx)) +": La función " + ctx.ID().getText() + " tiene parametros repetidos")
                # print("Error en la línea " + str(self.get_line(ctx)) +": La función " + ctx.ID().getText() + " tiene parametros repetidos")

            if ctx.ID().getText() == "main":
                self.mmain2 = True
                
            

                if ctx.formal():
                    self.errores.append("Error: La función main no debe poseer parametros")
                    # print("Error: La función main no debe poseer parametros")
            
            if ctx.ID().getText() == "self":
                self.errores.append("Error: La función no puede llamarse self")
                # print("Error: La función no puede llamarse self")

            
            current = self.symbol_table.getScopE()

            resp = self.symbol_table.getItem(ctx.ID().getText(), current)

            if resp[0] == True:
                self.errores.append("Error: La función " + ctx.ID().getText() + " ya existe")
                # print("Error: La función " + ctx.ID().getText() + " ya existe")

            else:
                self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "function", ctx.TYPE().getText(), None, params)

            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx)
            self.symbol_table.exit_scope()
            return temp

        else:
            name = ctx.ID().getText()

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



                        if r.name != "Main" and r.hereda is not None:
                            hereda = r.hereda


                            scopeH = self.symbol_table.getSpecificScope(hereda)


                            resp = self.symbol_table.getItem(name, scopeH)

                            inheri = resp[0]

                            if resp[0] == False:
                                inheri = resp[0]
                                parent_ctx = hereda

                            else:
                                self.errores.append("Error: El atributo " + name + " ya existe en clase padre")
                                # print("Error: El atributo " + name + " ya existe en clase padre")
                                inheri = True

                        else:
                            inheri = True

                    seaClass = False

            current = self.symbol_table.getScopE()
            
            resp = self.symbol_table.getItem(ctx.ID().getText(), current)

            if resp[0] == True:
                self.errores.append("Error: El atribute " + ctx.ID().getText() + " ya existe")
                # print("Error: El atribute " + ctx.ID().getText() + " ya existe")

            else:

                if ctx.ID().getText() == "self":
                    self.errores.append("Error: El atributo no puede llamarse self")
                    # print("Error: El atributo no puede llamarse self")

                else:
                    self.symbol_table.put(ctx.ID().getText(), self.get_line(ctx), "atribute", ctx.TYPE().getText())

            return None
    
    def visitFormal(self, ctx:yaplParser.FormalContext):
        self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "formal", ctx.TYPE().getText())
        # ## print("Exit")
        # self.symbol_table.exit_scope()
        return None
    
    def visitExpr(self, ctx:yaplParser.ExprContext):
        # # print("Llamada a Expr")

        # ARREGLAR IF Y ELSE DESPUES DE HACER EL RESTO
        if ctx.IF():

            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx.expr()[0])
            self.symbol_table.exit_scope()

            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx.expr()[1])
            self.symbol_table.exit_scope()

            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx.expr()[2])
            self.symbol_table.exit_scope()


            return temp


        elif ctx.WHILE():
            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx.expr()[0])
            self.symbol_table.exit_scope()

            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx.expr()[1])
            self.symbol_table.exit_scope()
            return temp


        elif ctx.LET():

            identificadores = ctx.ID()

            for i in range(len(identificadores)):
                for j in range(i + 1, len(identificadores)):  # Compara con los identificadores restantes
                    if identificadores[i].getText() == identificadores[j].getText():
                        self.errores.append("Error: La variable " + identificadores[i].getText() + " se está definiendo dos veces en el mismo bloque")
                        # print("Error: La variable " + identificadores[i].getText() + " se esta definiendo dos veces en el mismo bloque")

            for i in range(len(ctx.ID())):

                current = self.symbol_table.getScopE()

                resp = self.symbol_table.getItem(ctx.ID()[i].getText(), current)

                if resp[0] == True:
                    self.errores.append("Error: La variable " + ctx.ID()[i].getText() + " ya existe")
                    # print("Error: La variable " + ctx.ID()[i].getText() + " ya existe")

                else:
                    
                    if ctx.ID()[i].getText() == "self":
                        self.errores.append("Error: La variable no puede llamarse self")
                        # print("Error: La variable no puede llamarse self")
                        
                    else:
                        
                        self.symbol_table.put(ctx.ID()[i].getText(), self.get_line(ctx), "variable",ctx.TYPE()[i].getText())

                self.symbol_table.enter_scope()
                temp = self.visitChildren(ctx)
                self.symbol_table.exit_scope()

                return temp

            #self.symbol_table.exit_scope()
        else:
            #self.symbol_table.put("ctx.ID()[i]", self.get_line(ctx), "variable","ctx.TYPE()[i].getText()")
            temp = self.visitChildren(ctx)
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
        
    def error_mmain(self):
        if self.mmain == False:
            self.errores.append("Error: No hay clase Main")
            # print("Error: No hay clase Main")
            
    def error_mmain2(self):
        if self.mmain2 == False:
            self.errores.append("Error: No hay metodo main")
            # print("Error: No hay metodo main")