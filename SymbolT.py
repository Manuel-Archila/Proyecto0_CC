class Symbol:
    def __init__(self, name, line, symbol_type, scope, data_type=None, hereda=None, params=None, memoria = None):
        self.name = name  
        self.line = line  
        self.symbol_type = symbol_type  
        self.data_type = data_type  
        self.scope = scope  
        self.hereda = hereda
        self.params = params
        self.memoria = memoria
    def __repr__(self):
        return str(self.name) + " " + str(self.line) + " " + str(self.symbol_type) + " " + str(self.data_type) + " " + str(self.scope) + " " + str(self.hereda) + " " + str(self.params) + " " + str(self.memoria) 

class Scope:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []  
        self.symbols = {}
    
    def put(self, symbol):
        self.symbols[symbol.name] = symbol
    
    def get(self, name):
        return self.symbols.get(name, None)
    
    def add_child(self, child_scope):
        self.children.append(child_scope)
    
    def __repr__(self):
        symbols_repr = []
        symbols_repr.append(f"Scope: {self.name}")
        symbols_repr.extend([str(symbol) for symbol in self.symbols.values()])
        symbols_repr.append("")  # Add an empty line between scopes
        return "\n".join(symbols_repr)

class SymbolT:
    def __init__(self):
        self.current_scope = None
        self.scope_counter = 0
        self.root = None

        self.current_scope2 = None
        self.scope_counter2 = 0

        self.current_scope3 = None
        self.scope_counter3 = 0
    
    def enter_scope(self):
        if self.scope_counter == 0:
            self.root = Scope(str(self.scope_counter))
            self.current_scope = self.root
            self.scope_counter += 1
        else:
            new_scope = Scope(str(self.scope_counter), self.current_scope)
            self.current_scope.add_child(new_scope)
            self.current_scope = new_scope
            self.scope_counter += 1
        #print("Entrando al scope", self.current_scope.name)    
    def exit_scope(self):
        if self.current_scope.parent:
            #print("Saliendo del scope", self.current_scope.name)
            self.current_scope = self.current_scope.parent
    
    def put(self, name, line, symbol_type, data_type=None, hereda=None, params=None, memoria = None):
        symbol = Symbol(name, line, symbol_type, self.current_scope.name, data_type, hereda, params, memoria)
        self.current_scope.put(symbol)
    
    def enter_scope2(self):
        if self.scope_counter2 == 0:
            self.root2 = Scope(str(self.scope_counter2))
            self.current_scope2 = self.root2
            self.scope_counter2 += 1
        else:
            new_scope = Scope(str(self.scope_counter2), self.current_scope2)
            self.current_scope2.add_child(new_scope)
            self.current_scope2 = new_scope
            self.scope_counter2 += 1
    
    def exit_scope2(self):
        if self.current_scope2.parent:
            self.current_scope2 = self.current_scope2.parent

    
    def enter_scope3(self):
        if self.scope_counter3 == 0:
            self.root3 = Scope(str(self.scope_counter3))
            self.current_scope3 = self.root3
            self.scope_counter3 += 1
        else:
            new_scope = Scope(str(self.scope_counter3), self.current_scope3)
            self.current_scope3.add_child(new_scope)
            self.current_scope3 = new_scope
            self.scope_counter3 += 1
    
    def exit_scope3(self):
        if self.current_scope3.parent:
            self.current_scope3 = self.current_scope3.parent
    
    
    def visit_elements(self, scope, name):
    # Check if the current scope has the desired name
        if scope.name == name:
            return scope
        for child in scope.children:
            result = self.visit_elements(child, name)
            if result:
                return result
        return None

        
    def getScope(self):
        name = self.current_scope2.name
        scope = self.visit_elements(self.root, name)
        return scope

    def getScope2(self):
        name = self.current_scope3.name
        scope = self.visit_elements(self.root, name)
        return scope
    
    def getScopE(self):
        name = self.current_scope.name
        scope = self.visit_elements(self.root, name)
        return scope

    # def getSpecificScope(self, name):
    #     current_scope = self.current_scope
    #     while current_scope:
    #         if name in current_scope.symbols:
    #             return current_scope

    #         current_scope = current_scope.parent
    #     return None
    
    #Retorna el scope donde se encuentra el simbolo
    def getSpecific(self, name):
        current_scope = self.current_scope
        while current_scope:
            if name in current_scope.symbols:
                return current_scope

            current_scope = current_scope.parent
        return None
    
    def getSpecific2(self, name):
        current_scope = self.current_scope
        while current_scope:
            if name in current_scope.symbols:
                return current_scope

            for child in current_scope.children:
                result = self.recurs(child, name)
                if result:
                    return result 
        return None
    
    def recurs(self, scope, name):
        if name in scope.symbols:
            return scope
        
        for child in scope.children:
            result = self.recurs(child, name)
            if result:
                return result
        return None

    # Retorna el scope del simbolo
    def getSpecificScope(self, name):
        current_scope = self.current_scope
        while current_scope:
            if name in current_scope.symbols:
                contador = 0
                for scope in current_scope.symbols:
                    if scope != name:
                        contador += 1
                    if scope == name:
                        break
                return current_scope.children[contador]
            current_scope = current_scope.parent
        return None

    def getItem(self, name, scope):
        current_scope = scope
        while current_scope:
            if name in current_scope.symbols:
                return True, current_scope.symbols[name].data_type
            current_scope = current_scope.parent
        return False, None
    
    def getSymbol(self, name, scope):
        current_scope = scope
        while current_scope:
            if name in current_scope.symbols:
                return current_scope.symbols[name]
            current_scope = current_scope.parent
        return None
    
    def verificarPeso(self, scope):
        contador = 0
        for sim in scope.symbols:
            if scope.symbols[sim].symbol_type == "atribute":
                contador += scope.symbols[sim].memoria
        return contador

    def cambiarPeso(self, name, scope, peso):
        current_scope = scope
        while current_scope:
            if name in current_scope.symbols:
                current_scope.symbols[name].memoria = peso
                return True
            current_scope = current_scope.parent
        

    def __repr__(self):
        def recurse(scope, indent=0):
            result = [repr(scope)]
            for child in scope.children:
                result.append(recurse(child, indent+1))
            return '\n'.join(result)
        
        return recurse(self.root)
    
    def get_params(self, name, scope):
        current_scope = scope
        while current_scope:
            if name in current_scope.symbols:
                return current_scope.symbols[name].params
            current_scope = current_scope.parent
        return None
    
    def build_natives(self):
        # Scope 0
        self.enter_scope()
        self.enter_scope2()
        self.put("Object", 0, "class", None, None)
        self.put("String", 0, "class", None, "Object")
        self.put("Int", 0, "class", None, "Object")
        self.put("Bool", 0, "class", None, "Object")
        self.put("IO", 0, "class", None, "Object")
        # Scope 1
        self.enter_scope()
        self.enter_scope2()
        self.put("abort", 0, "function", "Object", None, [])
        self.enter_scope()
        self.enter_scope2()
        # Scope 2
        self.exit_scope()
        self.exit_scope2()
        # Scope 1
        self.put("type_name", 0, "function", "String", None, [])
        self.enter_scope()
        self.enter_scope2()
        # Scope 3
        self.exit_scope()
        self.exit_scope2()
        # Scope 1
        self.put("copy", 0, "function", "Object", None, [])
        self.enter_scope()
        self.enter_scope2()
        # Scope 4
        self.exit_scope()
        self.exit_scope2()
        # Scope 1
        self.exit_scope2()
        self.exit_scope()
        
        
        # Scope 5
        self.enter_scope()
        self.enter_scope2()
        self.put("length", 0, "function", "Int", None, [])
        self.enter_scope()
        self.enter_scope2()
        # Scope 6
        self.exit_scope()
        self.exit_scope2()
        
        self.put("concat", 0, "function", "String", None, [("str", "String")])
        self.enter_scope()
        self.enter_scope2()
        # Scope 7
        self.put("str", 0, "formal", "String", None, None)
        
        self.exit_scope()
        self.exit_scope2()

        self.put("substr", 0, "function", "Int", None, [("index1", "Int"), ("index2", "Int")])

        self.enter_scope()
        self.enter_scope2()
        # Scope 8
        self.put("i", 0, "formal", "Int", None, None)
        self.put("one", 0, "formal", "Int", None, None)

        self.exit_scope()
        self.exit_scope2()

        self.exit_scope()
        self.exit_scope2()



        # Scope 9
        self.enter_scope()
        self.enter_scope2()

        self.exit_scope()
        self.exit_scope2()
        # Scope 10
        self.enter_scope()
        self.enter_scope2()

        self.exit_scope()
        self.exit_scope2()
        # Scope 11
        self.enter_scope()
        self.enter_scope2()
        self.put("out_string", 0, "function", "String", None, [("str", "String")])
        self.enter_scope()
        self.enter_scope2()
        # Scope 12
        self.put("str", 0, "formal", "String", None, None)
        self.exit_scope()
        self.exit_scope2()

        self.put("out_int", 0, "function", "Int", None, [("i", "Int")])
        # Scope 13
        self.enter_scope()
        self.enter_scope2()
        self.put("i", 0, "formal", "Int", None, None)
        self.exit_scope()
        self.exit_scope2()

        self.put("in_string", 0, "function", "String", None, [])
        # Scope 14
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()

        self.put("in_int", 0, "function", "Int", None, [])
        # Scope 15
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()

        self.exit_scope()
        self.exit_scope2()
        
        
        
        



