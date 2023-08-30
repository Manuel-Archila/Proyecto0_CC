class Symbol:
    def __init__(self, name, line, symbol_type, scope, data_type=None, hereda=None):
        self.name = name  
        self.line = line  
        self.symbol_type = symbol_type  
        self.data_type = data_type  
        self.scope = scope  
        self.hereda = hereda
    def __repr__(self):
        return str(self.name) + " " + str(self.line) + " " + str(self.symbol_type) + " " + str(self.data_type) + " " + str(self.scope) + " " + str(self.hereda)

class Scope:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []  # List to store child scopes
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
    
    def put(self, name, line, symbol_type, data_type=None, hereda=None):
        symbol = Symbol(name, line, symbol_type, self.current_scope.name, data_type, hereda)
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
    
    def put2(self, name, line, symbol_type, data_type=None):
        symbol = Symbol(name, line, symbol_type, self.current_scope2.name, data_type)
        self.current_scope2.put(symbol)
    
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
          
    def __repr__(self):
        def recurse(scope, indent=0):
            result = [repr(scope)]
            for child in scope.children:
                result.append(recurse(child, indent+1))
            return '\n'.join(result)
        
        return recurse(self.root)
    
    def build_natives(self):
        print("Building natives")
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
        self.put("abort", 0, "function", "Object", None)
        self.put("type_name", 0, "function", "String", None)
        self.put("copy", 0, "function", "Object", None)
        self.exit_scope2()
        self.exit_scope()
        # Scope 2
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()
        # Scope 3
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()
        # Scope 4
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()
        # Scope 5
        self.enter_scope()
        self.enter_scope2()
        self.put("length", 0, "function", "Int", None)
        self.put("concat", 0, "function", "String", None)
        self.put("substr", 0, "function", "Int", None)
        self.exit_scope()
        self.exit_scope2()
        # Scope 6
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()
        # Scope 7
        self.enter_scope()
        self.enter_scope2()
        self.put("str", 0, "formal", "String", None)
        self.exit_scope()
        self.exit_scope2()
        # Scope 8
        self.enter_scope()
        self.enter_scope2()
        self.put("i", 0, "formal", "Int", None)
        self.put("one", 0, "formal", "Int", None)
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
        self.put("out_string", 0, "function", "String", None)
        self.put("out_int", 0, "function", "Int", None)
        self.put("in_string", 0, "function", "String", None)
        self.put("in_int", 0, "function", "Int", None)
        self.exit_scope()
        self.exit_scope2()
        # Scope 12
        self.enter_scope()
        self.enter_scope2()
        self.put("str", 0, "formal", "String", None)
        self.exit_scope()
        self.exit_scope2()
        # Scope 13
        self.enter_scope()
        self.enter_scope2()
        self.put("i", 0, "formal", "Int", None)
        self.exit_scope()
        self.exit_scope2()
        # Scope 14
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()
        # Scope 15
        self.enter_scope()
        self.enter_scope2()
        self.exit_scope()
        self.exit_scope2()



