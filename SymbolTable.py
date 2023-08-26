class Symbol:
    def __init__(self, name, line, symbol_type, scope, data_type=None):
        self.name = name  
        self.line = line  
        self.symbol_type = symbol_type  
        self.data_type = data_type  
        self.scope = scope  
    def __repr__(self):
        return str(self.name) + " " + str(self.line) + " " + str(self.symbol_type) + " " + str(self.data_type) + " " + str(self.scope)

class SymbolTable:
    def __init__(self):
        self.scopes = []
        self.current_scope_index = 0
        self.scope_counter = 0
    
    def enter_scope(self):
        self.scope_counter += 1
        scope_name = f"scope_{self.scope_counter}"
        self.scopes.append({})  # Agregar un nuevo ámbito vacío
        self.current_scope_index = len(self.scopes) - 1
    
    def exit_scope(self):
        if self.current_scope_index > 0:
            self.current_scope_index -= 1
    
    def put(self, name, line, symbol_type, data_type=None):
        current_scope = self.scopes[self.current_scope_index]
        symbol = Symbol(name, line, symbol_type, self.current_scope_index, data_type)
        current_scope[name] = symbol
    
    def get(self, name):
        for scope_index in range(self.current_scope_index, -1, -1):
            if name in self.scopes[scope_index]:
                return self.scopes[scope_index][name]
        return None
    
    def __repr__(self):
        symbols_repr = []
        for scope_index, scope_symbols in enumerate(self.scopes):
            symbols_repr.append(f"Scope: {scope_index}")
            symbols_repr.extend([str(symbol) for symbol in scope_symbols.values()])
            symbols_repr.append("")  # Add an empty line between scopes
        return "\n".join(symbols_repr)