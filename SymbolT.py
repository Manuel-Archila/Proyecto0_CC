class Symbol:
    def __init__(self, name, line, symbol_type, scope, data_type=None):
        self.name = name  
        self.line = line  
        self.symbol_type = symbol_type  
        self.data_type = data_type  
        self.scope = scope  
    def __repr__(self):
        return str(self.name) + " " + str(self.line) + " " + str(self.symbol_type) + " " + str(self.data_type) + " " + str(self.scope)

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
        self.root = Scope("0")  # Change root name to "0"
        self.current_scope = self.root
        self.scope_counter = 1  # To generate unique scope names
    
    def enter_scope(self):
        new_scope = Scope(str(self.scope_counter), self.current_scope)
        self.current_scope.add_child(new_scope)
        self.current_scope = new_scope
        self.scope_counter += 1
    
    def exit_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def put(self, name, line, symbol_type, data_type=None):
        symbol = Symbol(name, line, symbol_type, self.current_scope.name, data_type)
        self.current_scope.put(symbol)
    
    def __repr__(self):
        def recurse(scope, indent=0):
            result = [repr(scope)]
            for child in scope.children:
                result.append(recurse(child, indent+1))
            return '\n'.join(result)
        
        return recurse(self.root)


