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
        #print("Llamada a class")
        hereda = None
        
        if ctx.INHERITS():

            hereda = ctx.TYPE()[1].getText()

            if ctx.TYPE()[0].getText() == ctx.TYPE()[1].getText():
                self.errores.append("Error: Herencia circular")
                print("Error: Herencia circular")
                
            if ctx.TYPE()[0].getText() == "Main":
                self.errores.append("Error: Herencia de Main")
                print("Error: Herencia de Main")

            if ctx.TYPE()[1].getText() == "String" or ctx.TYPE()[1].getText() == "Int" or ctx.TYPE()[1].getText() == "Bool":
                self.errores.append("Error: No se puede heredar de clases nativas")
                print("Error: No se puede heredar de clases nativas")
            
                
        
        
        if ctx.TYPE()[0].getText() == "Main":
            self.mmain = True

        
        if hereda is None:
            print("No hereda")
            if ctx.TYPE()[0].getText() == "Main" or ctx.TYPE()[0].getText() == "Object":
                hereda = None
            else:
                hereda = "Object"

        current = self.symbol_table.getScopE()

        resp = self.symbol_table.getItem(ctx.TYPE()[0].getText(), current)

        if resp[0] == True:
            self.errores.append("Error: La clase " + ctx.TYPE()[0].getText() + " ya existe")
            print("Error: La clase " + ctx.TYPE()[0].getText() + " ya existe")

        else:
        
            self.symbol_table.put(ctx.TYPE()[0].getText(), ctx.start.line, "class", None , hereda)
        self.symbol_table.enter_scope()
        temp = self.visitChildren(ctx)
        self.symbol_table.exit_scope()
        #self.symbol_table.exit_scope()
        return temp
    
    def visitFeature(self, ctx:yaplParser.FeatureContext):
        #print("Llamada a feature")

        if ctx.LPAR():

            if ctx.ID().getText() == "main":
                self.mmain2 = True

                if ctx.formal():
                    self.errores.append("Error: La funcion main no debe poseer parametros")
                    print("Error: La funcion main no debe poseer parametros")

            
            current = self.symbol_table.getScopE()

            resp = self.symbol_table.getItem(ctx.ID().getText(), current)

            if resp[0] == True:
                self.errores.append("Error: La función " + ctx.ID().getText() + " ya existe")
                print("Error: La función " + ctx.ID().getText() + " ya existe")

            else:
                self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "function", ctx.TYPE().getText())

            self.symbol_table.enter_scope()
            temp = self.visitChildren(ctx)
            self.symbol_table.exit_scope()
            return temp

        else:
            current = self.symbol_table.getScopE()

            resp = self.symbol_table.getItem(ctx.ID().getText(), current)

            if resp[0] == True:
                self.errores.append("Error: La función " + ctx.ID().getText() + " ya existe")
                print("Error: La función " + ctx.ID().getText() + " ya existe")

            else:

                self.symbol_table.put(ctx.ID().getText(), self.get_line(ctx), "atribute", ctx.TYPE().getText())

            return None
    
    def visitFormal(self, ctx:yaplParser.FormalContext):
        self.symbol_table.put(ctx.ID().getText(), ctx.start.line, "formal", ctx.TYPE().getText())
        # #print("Exit")
        # self.symbol_table.exit_scope()
        return None
    
    def visitExpr(self, ctx:yaplParser.ExprContext):
        # print("Llamada a Expr")
        new_scope_required = ctx.IF()

        if new_scope_required:
            #print("Enter")
            self.symbol_table.enter_scope()
        # ARREGLAR IF Y ELSE DESPUES DE HACER EL RESTO
        if ctx.IF():
            #print("Enter")
            self.symbol_table.enter_scope()
            self.symbol_table.put(ctx.getText(), ctx.start.line, "if")

            if ctx.ELSE():
                # print("ctx trae un else")
                # self.symbol_table.exit_scope()
                # print("Entro al else")
                #print("Enter")
                self.symbol_table.enter_scope()
                self.symbol_table.put(ctx.getText(), ctx.start.line, "else")
                # temp = self.visitChildren(ctx)
                #print("Exit")
                self.symbol_table.exit_scope()
            # else:
            #     temp = self.visitChildren(ctx)

            temp = self.visitChildren(ctx)
            #print("Exit")
            self.symbol_table.exit_scope()
            # self.symbol_table.exit_scope()

            return temp


        elif ctx.WHILE():
            #print("entre a while")
            #print("Enter")
            self.symbol_table.enter_scope()
            self.symbol_table.put('ctx.getText()', ctx.start.line, "while")
            temp = self.visitChildren(ctx)
            #print("Exit")
            self.symbol_table.exit_scope()
            return temp


        elif ctx.LET():
            for i in range(len(ctx.ID())):

                current = self.symbol_table.getScopE()

                resp = self.symbol_table.getItem(ctx.ID()[i].getText(), current)

                if resp[0] == True:
                    self.errores.append("Error: La variable " + ctx.ID()[i].getText() + " ya existe")
                    print("Error: La variable " + ctx.ID()[i].getText() + " ya existe")

                else:

                    self.symbol_table.put(ctx.ID()[i].getText(), self.get_line(ctx), "variable",ctx.TYPE()[i].getText())


                return self.visitChildren(ctx)
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
            print("Error: No hay clase Main")
            
    def error_mmain2(self):
        if self.mmain2 == False:
            self.errores.append("Error: No hay metodo main")
            print("Error: No hay metodo main")