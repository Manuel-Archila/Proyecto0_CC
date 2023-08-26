class Symbol:
    def __init__(self, name, line, symbol_type, scope, data_type=None):
        self.name = name  # Name of the symbol (e.g., variable name)
        self.line = line  # Line where the symbol was declared
        self.symbol_type = symbol_type  # e.g., "variable", "function", "class"
        self.data_type = data_type  # e.g., "int", "string", custom class name
        self.scope = scope  # Scope where the symbol was declared
        # Add more attributes if needed
    def __repr__(self):
        return str(self.name) + " " + str(self.line) + " " + str(self.symbol_type) + " " + str(self.data_type) + " " + str(self.scope)


class SymbolTable:
    def __init__(self):
        self.scopeTOTAL = 0
        self.scope = 0  # Initialize with a global scope
        self.stack = [Scope()]  # List of scopes, the last one is the current scope
        self.actual = self.scope

    def put(self, name, line, symbol_type, data_type=None):
        print(self.stack)
        """Add a symbol to the current scope."""
        symbol = Symbol(name, line, symbol_type, self.scope, data_type)
        self.stack[self.scope].put(name, symbol)

    def get(self, name):
        """Get a symbol from the current scope or its parent scopes."""
        return self.stack[-1].get(name)

    def remove(self, name):
        """Remove a symbol from the current scope."""
        self.stack[-1].remove(name)

    def push_scope(self):
        """Push a new scope onto the stack."""
        self.scope += 1
        self.scopeTOTAL += 1

        if self.scope < self.scopeTOTAL:

            self.scope = self.scopeTOTAL
            
            self.stack.append(Scope(self.stack[-1]))

        else:
            self.scope -= 1
            


    def pop_scope(self):
        """Remove and return the current scope from the stack."""
        self.scope -= 1
    
    def print_table(self):
        """Print the content of the symbol table."""
        print()
        for index, scope in enumerate(self.stack):
            for name, symbol in scope.symbols.items():
                print(f"  Name: {symbol.name}, Type: {symbol.symbol_type}, Line: {symbol.line}, Scope: {symbol.scope}, Data Type: {symbol.data_type}")
            print()




class Scope:
    def _init_(self, parent=None):
        self.parent = parent
        self.entries = {}

    def insert(self, identifier, info):
        self.entries[identifier] = info

    def lookup(self, identifier):
        return self.entries.get(identifier, None)

class SymbolTable:
    def _init_(self):
        self.current_scope = Scope()

    def enter_scope(self):
        new_scope = Scope(self.current_scope)
        self.current_scope = new_scope

    def exit_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
        else:
            print("Warning: Already at the outermost scope!")


    def insert(self, identifier, info):
        self.current_scope.insert(identifier, info)

    def lookup(self, identifier):
        scope = self.current_scope
        while scope:
            info = scope.lookup(identifier)
            if info is not None:
                return info
            scope = scope.parent
        return None