from dist.yaplVisitor import yaplVisitor
from dist.yaplParser import yaplParser
from antlr4.tree.Tree import TerminalNode
import re

class CuadruplasVisitor2(yaplVisitor):
    def __init__(self, symbol_table, cuadruplas):
        self.symbol_table = symbol_table
        self.cuadruplas = cuadruplas
        self.visited_nodes = {}

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
                self.cuadruplas.agregar_cuadrupla('PARAM', None, tupla[1], tupla[0])
            

        if ctx.COLON():

            variable = ctx.getChild(0).getText()
            tipo = ctx.getChild(2).getText()
            if not ctx.LPAR():
                self.cuadruplas.agregar_cuadrupla("DECLARE_VAR", variable, tipo, "BaseInstancia + offset" + variable)

            if ctx.LPAR():

                self.cuadruplas.agregar_cuadrupla("DECLARE", variable, None, None)
                
                if ctx.expr():

                    if ctx.expr().LPAR():
                        pass
                    else:

                        if ctx.expr().ASSIGN():
                            pass
                        else:

                            if ctx.expr().IF():
                                pass
                            
                            else:

                                for hijo in ctx.expr().getChildren():
                                    if hijo.getText() not in [';', '{', '}']:
                                        self.visit(hijo)
                                    


            if ctx.ASSIGN():

                variable = ctx.getChild(0).getText()
                val = self.visit(ctx.getChild(4))

                if val is not None:
                    
                    variable = "BaseInstancia + offset" + variable

                    self.cuadruplas.agregar_cuadrupla("ASSIGN", val, None, variable)
                else:
                    self.cuadruplas.agregar_cuadrupla("ASSIGN", variable, None, "t")

                return None
        

        tm = self.visitChildren(ctx)    
        bandera = True

        if ctx.LPAR():

            if ctx.expr():

                if ctx.expr().LPAR():
                    pass

                else:

                    if ctx.expr().ASSIGN():
                        pass
                    else:

                        if ctx.expr().IF():

                            hay = self.cuadruplas.verIf()

                            if hay == True:
                                self.cuadruplas.retIF()
                                

                            bandera = False



            
            if bandera == True:
                cua = self.cuadruplas.get_last_cuadrupla()
            
                print("La ultima cuadrupla es: ", cua)

                if "t" in cua[3] or "BaseInstancia" in cua[3]:
                    print("entro al if con", cua[3])
                    resultado = cua[3]
                else:
                    print("entro al else con", cua[3])
                    resultado = self.cuadruplas.get_last_call()
                self.cuadruplas.agregar_cuadrupla("RETURN_FUNCTION", resultado, None, None)
            self.cuadruplas.agregar_cuadrupla("END_FUNCTION", variable, None, None)


        return tm
    
    def visitformal(self, ctx:yaplParser.FormalContext):
        return self.visitChildren(ctx)
    
    def visitExpr(self, ctx:yaplParser.ExprContext):

        if ctx in self.visited_nodes:
            return self.visited_nodes[ctx]

        if ctx.PLUS():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)

            valor = self.cuadruplas.agregar_cuadrupla('+', first_child, second_child, "t")

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.MINUS():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)

            valor = self.cuadruplas.agregar_cuadrupla('-', first_child, second_child, "t" )

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.TIMES():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)


            valor = self.cuadruplas.agregar_cuadrupla('*', first_child, second_child, "t" )

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.DIVIDE():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)

            valor = self.cuadruplas.agregar_cuadrupla('/', first_child, second_child, "t" )

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.LT():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)

            valor = self.cuadruplas.agregar_cuadrupla('<', first_child, second_child, "t" )

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.RT():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)

            valor = self.cuadruplas.agregar_cuadrupla('>', first_child, second_child, "t" )

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.LE():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)

            valor = self.cuadruplas.agregar_cuadrupla('<=', first_child, second_child, "t" )

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.RE():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)


            valor = self.cuadruplas.agregar_cuadrupla('>=', first_child, second_child, "t" )

            self.visited_nodes[ctx] = valor

            return valor

        if ctx.EQUALS():
            resultado_ant1 = self.visit(ctx.getChild(0))
            resultado_ant = self.visit(ctx.getChild(2))


            if isinstance(resultado_ant1, str):
                first_child = resultado_ant1
            else:
                print("ENTRO")
                print(resultado_ant1)

            if isinstance(resultado_ant, str):
                second_child = resultado_ant
            else:
                print("ENTRO")
                print(resultado_ant)

            valor = self.cuadruplas.agregar_cuadrupla('=', first_child, second_child, "t" )
            
            self.visited_nodes[ctx] = valor

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


            try:
                valor = self.cuadruplas.agregar_cuadrupla('LET', ctx.getChild(5).getText(), second_child, first_child)
            except:
                valor = self.cuadruplas.agregar_cuadrupla('LET', "t", second_child, first_child)

            try:
               self.visit(ctx.getChild(7))

            except:
                pass

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

            self.cuadruplas.eliminarUltima()
            self.cuadruplas.eliminarUltima()


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

                first_child = "BaseInstancia + offset" + first_child

                if val is not None:

                    self.cuadruplas.agregar_cuadrupla("ASSIGN", val, None, first_child)
                else:
                    num = self.cuadruplas.encontrar_cuadrupla_param(second_child.getText())

                    if num is not None:
                        self.cuadruplas.agregar_cuadrupla("ASSIGN", second_child.getText(), None, first_child)

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

                    tipo = ctx.getChild(2).getText()


                    
                    
                    # self.cuadruplas.agregar_cuadrupla('CALL', funtion, len(argumentoss), "t")
                    print(funtion)
                    print(tipo)
                    parametroos = self.cuadruplas.get_function_params(funtion)
                    parametroos = parametroos[::-1]

                    # for argumento in argumentoss:
                    #     self.cuadruplas.agregar_cuadrupla('ASSIGN_PARAM', argumento[1], None, argumento[0])
                    
                    for argumento, parametro in zip(argumentoss, parametroos):

                        tempo = self.cuadruplas.get_cuadrupla_put(argumento[0])

                        if parametro in ['inty']:
                            self.cuadruplas.agregar_cuadrupla('ASSIGN_PARAM', tipo, None, parametro)

                        else:

                            self.cuadruplas.agregar_cuadrupla('ASSIGN_PARAM', tempo, None, parametro)
                    
                    if funtion in ['in_int', 'out_int', 'out_string', 'in_string']:
                        tipo = 'IO'

                    
                    self.cuadruplas.agregar_cuadrupla('CALL', funtion, tipo, "t")

            return ctx.getText()
        
        if ctx.STRING():

            return ctx.getText()

        if ctx.DIGIT():

            valor = self.cuadruplas.agregar_cuadrupla('PUT', ctx.getText(), None, "t")

            self.visited_nodes[ctx] = valor

            return ctx.getText()
        
        if ctx.TRUE() or ctx.FALSE():

            return ctx.getText()

        if ctx.LPAR():
            for hijo in ctx.getChildren():
                if hijo.getText() != '(' and hijo.getText() != ')':
                    self.visit(hijo)

            return 0

            