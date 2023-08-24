class Symbol:
    def __init__(self, name, symbol_type, data_type=None):
        self.name = name  # Name of the symbol (e.g., variable name)
        self.symbol_type = symbol_type  # e.g., "variable", "function", "class"
        self.data_type = data_type  # e.g., "int", "string", custom class name
        # Add more attributes if needed


class Scope:
    def __init__(self, parent=None):
        self.symbols = {}  # Dictionary to store symbols by name
        self.parent = parent  # Reference to the parent scope

    def put(self, name, symbol):
        """Add a symbol to the current scope."""
        self.symbols[name] = symbol

    def get(self, name):
        """Get a symbol from this scope or its parent scopes."""
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def remove(self, name):
        """Remove a symbol from the current scope."""
        del self.symbols[name]


class SymbolTable:
    def __init__(self):
        self.stack = [Scope()]  # Initialize with a global scope

    def put(self, name, symbol_type, data_type=None):
        """Add a symbol to the current scope."""
        symbol = Symbol(name, symbol_type, data_type)
        self.stack[-1].put(name, symbol)

    def get(self, name):
        """Get a symbol from the current scope or its parent scopes."""
        return self.stack[-1].get(name)

    def remove(self, name):
        """Remove a symbol from the current scope."""
        self.stack[-1].remove(name)

    def push_scope(self):
        """Push a new scope onto the stack."""
        self.stack.append(Scope(self.stack[-1]))

    def pop_scope(self):
        """Remove and return the current scope from the stack."""
        return self.stack.pop()
    
    def print_table(self):
        """Print the content of the symbol table."""
        for index, scope in enumerate(self.stack):
            print("Scope Level:", index)
            for name, symbol in scope.symbols.items():
                print(f"  Name: {symbol.name}, Type: {symbol.symbol_type}, Data Type: {symbol.data_type}")
            print()

