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
    def __init__(self, name):
        self.name = name
        self.symbols = {}
    
    def put(self, symbol):
        self.symbols[symbol.name] = symbol
    
    def get(self, name):
        return self.symbols.get(name, None)
    
    def __repr__(self):
        symbols_repr = []
        symbols_repr.append(f"Scope: {self.name}")
        symbols_repr.extend([str(symbol) for symbol in self.symbols.values()])
        symbols_repr.append("")  # Add an empty line between scopes
        return "\n".join(symbols_repr)

class SymbolTable:
    def __init__(self):
        self.scopes = []
        self.full_scopes = []

    
    def enter_scope(self):

        self.scopes.append(Scope(len(self.full_scopes)))
        self.full_scopes.append(Scope(len(self.full_scopes)))

    
    def exit_scope(self):
        self.scopes.pop()
    
    def put(self, name, line, symbol_type, data_type=None):
        current_scope = self.scopes[-1].name

        symbol = Symbol(name, line, symbol_type, current_scope, data_type)

        self.full_scopes[current_scope].put(symbol)
    
    # def get(self, name):
    #     for scope_index in range(self.current_scope_index, -1, -1):
    #         if name in self.scopes[scope_index]:
    #             return self.scopes[scope_index][name]
    #     return None
        
    def print_table(self):
        table_repr = []
        for index, scope in enumerate(self.full_scopes):
            table_repr.append(f"Scope {index}:")
            table_repr.extend([str(symbol) for symbol in scope.symbols.values()])
            table_repr.append("")  # Add an empty line between scopes

        print("\n".join(table_repr))
    
    def __repr__(self):
        symbols_repr = []
        for scope_index, scope_symbols in enumerate(self.scopes):
            symbols_repr.append(f"Scope: {scope_index}")
            symbols_repr.extend([str(symbol) for symbol in scope_symbols.values()])
            symbols_repr.append("")  # Add an empty line between scopes
        return "\n".join(symbols_repr)
    

symbo = SymbolTable()

symbo.enter_scope()
symbo.put("Main", 1, "CLASS", "int")
symbo.enter_scope()
symbo.put("main", 1, "function", "int")
symbo.enter_scope()
symbo.put("x", 1, "variable", "int")
symbo.enter_scope()
symbo.put("while", 1, "while", "int")
symbo.exit_scope()
symbo.exit_scope()
symbo.put("contador", 1, "function", "int")
symbo.enter_scope()
symbo.put("inicio", 1, "variable", "int")
symbo.exit_scope()
symbo.put("count", 1, "function", "int")
symbo.enter_scope()
symbo.put("initial", 1, "variable", "int")
symbo.exit_scope()

symbo.print_table()