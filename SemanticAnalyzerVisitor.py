
class SemanticError(Exception):
    """Exception raised for semantic errors."""
    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line


class SemanticAnalyzerVisitor:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []

    def visit_program(self, node):
        # Example: Visit all classes in the program
        for class_node in node.class_():
            self.visit_class(class_node)

    def visit_class(self, node):
        # Example: Check if class is already defined
        class_name = node.TYPE()[0].getText()
        if self.symbol_table.get(class_name):
            self.errors.append(SemanticError(f"Class {class_name} already defined", node.line))
        else:
            self.symbol_table.put(class_name, "class")
            # Add other semantic checks or visits here...

    def visit_expr(self, node):
        # Example: Check type consistency in binary operations
        if node.operation in ['+', '-', '*', '/']:
            left_type = self.get_expr_type(node.left_expr)
            right_type = self.get_expr_type(node.right_expr)
            
            if left_type != 'int' or right_type != 'int':
                self.report_error(SemanticError(f"Invalid operand types for {node.operation}: {left_type} and {right_type}", node.line))
            
            # Assuming the result type of these operations is 'int'
            node.evaluated_type = 'int'
        
        # Add more checks for other types of expressions...

    def visit_formal(self, node):
        # Example: Check if the formal parameter is already defined in the current scope
        if self.symbol_table.get(node.name):
            self.errors.append(SemanticError(f"Variable {node.name} already defined in the current scope", node.line))
        else:
            self.symbol_table.put(node.name, "variable", node.type)
        
        # Add more checks for formal declarations if needed...
        
    def get_expr_type(self, expr):
        # Handle literals
        if expr.type in ['int_literal', 'string_literal', 'bool_literal']:
            return expr.type.split('_')[0]
        
        # Handle variables
        elif expr.type == 'variable':
            symbol = self.symbol_table.get(expr.variable_name)
            if symbol:
                return symbol.data_type
            else:
                self.report_error(SemanticError(f"Variable {expr.variable_name} not declared", expr.line))
                return None
        
        # Handle binary operations
        elif expr.operation in ['+', '-', '*', '/']:
            return 'int'
        elif expr.operation in ['<', '<=', '>', '>=', '==', '!=']:
            return 'bool'
        
        # Handle function or method calls (placeholder logic)
        elif expr.type == 'function_call':
            function_name = expr.function_name
            # Here, you'd check the return type of the function or method.
            # For now, let's assume all functions return 'int' for simplicity.
            return 'function'
        
        # Add more checks for other types of expressions...
        else:
            return None

    def report_error(self, error):
        self.errors.append(error)

