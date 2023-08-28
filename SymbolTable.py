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

        self.scopes2 = []
        self.full_scopes2 = []
    
    def enter_scope(self):
        self.scopes.append(Scope(len(self.full_scopes)))
        self.full_scopes.append(Scope(len(self.full_scopes)))
    
    def exit_scope(self):
       self.scopes.pop()
    
    def put(self, name, line, symbol_type, data_type=None):
        current_scope = self.scopes[-1].name
        symbol = Symbol(name, line, symbol_type, current_scope, data_type)
        self.full_scopes[current_scope].put(symbol)
    
    def getItem(self, name, scopee):
        #print("getItem")
        #for scope_index in range(len(self.full_scopes)-1, -1, -1):
            # print(self.full_scopes[scope_index].symbols.keys())
            # print(name)
        if name in self.full_scopes[scopee].symbols.keys():
            # table_repr = []
            # for index, scope in enumerate(self.full_scopes):
            #     table_repr.append(f"Scope {index}:")
            #     table_repr.extend([str(symbol) for symbol in scope.symbols.values()])
            #     table_repr.append("")  # Add an empty line between scopes

            # print("\n".join(table_repr))
            return True, self.full_scopes[scopee].symbols[name].data_type
        return False, None
    
    def getScope(self):
        return self.scopes2[-1].name

    def enter_scope2(self):
        self.scopes2.append(Scope(len(self.full_scopes2)))
        self.full_scopes2.append(Scope(len(self.full_scopes2)))
    
    def exit_scope2(self):
       self.scopes2.pop()
    
    def put2(self, name, line, symbol_type, data_type=None):
        current_scope = self.scopes2[-1].name
        print("El put se haria en el scope: ", current_scope)
        print(name, line, symbol_type, current_scope, data_type)

    
    def __repr__(self):

        table_repr = []
        for index, scope in enumerate(self.full_scopes):
            table_repr.append(f"Scope {index}:")
            table_repr.extend([str(symbol) for symbol in scope.symbols.values()])
            table_repr.append("")  # Add an empty line between scopes

        return "\n".join(table_repr)