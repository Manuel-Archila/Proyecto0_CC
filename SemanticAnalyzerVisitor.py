from antlr4.tree.Tree import TerminalNode
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
        for class_node in node.class_():
            self.visit_class(class_node)

    def visit_class(self, node):
        # Example: Check if class is already defined
        class_name = node.TYPE()[0].getText()
        if self.symbol_table.get(class_name):
            self.errors.append(SemanticError(f"Class {class_name} already defined", node.line))
        else:
            self.symbol_table.put(class_name, node.start.line, "class")

            #self.symbol_table.push_scope()

            for feature in node.feature():
                self.visit_feature(feature)

            #self.symbol_table.pop_scope()

    
    def visit_feature(self, node):
        if node.LPAR():
            self.visit_method(node)
        else:
            self.visit_attribute(node)

    def visit_method(self, node):
        self.symbol_table.put(node.ID().getText(), node.start.line, "function")

        #self.symbol_table.push_scope()
        for formal in node.formal():
            self.visit_formal(formal)

        if node.expr():
            self.visit_expr(node.expr())
        
        #self.symbol_table.pop_scope()

    def visit_attribute(self, node):
        self.symbol_table.put(node.ID().getText(), node.start.line, "atribute")


    def visit_expr(self, node):
        for hijo in node.getChildren():
            self.verify_expr(hijo)

        #self.symbol_table.put(node.ID()[0].getText(), "expr")

        # # Example: Check type consistency in binary operations
        # if node.operation in ['+', '-', '*', '/']:
        #     left_type = self.get_expr_type(node.left_expr)
        #     right_type = self.get_expr_type(node.right_expr)
            
        #     if left_type != 'int' or right_type != 'int':
        #         self.report_error(SemanticError(f"Invalid operand types for {node.operation}: {left_type} and {right_type}", node.line))
            
        #     # Assuming the result type of these operations is 'int'
        #     node.evaluated_type = 'int'
        
        # # Add more checks for other types of expressions...

    def visit_formal(self, node):

        for hijo in node.getChildren():
            self.verify_expr(hijo)

        #self.symbol_table.put(node.ID()[0].getText(), "formal")

        # Example: Check if the formal parameter is already defined in the current scope
        if self.symbol_table.get(node.name):
            self.errors.append(SemanticError(f"Variable {node.name} already defined in the current scope", node.line))
        else:
            self.symbol_table.put(node.name, "variable", node.type)
        
        # Add more checks for formal declarations if needed...
    
    def verify_expr(self, node):
        node_type = node.getText()
        line = self.get_line(node)
        self.symbol_table.put(node_type, line, node)
        

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

    def get_line(self, node):
        # Si el nodo es un TerminalNode, se puede obtener la línea directamente.
        if isinstance(node, TerminalNode):
            return node.symbol.line
        # De lo contrario, si es un nodo de una regla, se utiliza `start`.
        elif hasattr(node, 'start'):
            return node.start.line
        # Si el nodo no tiene información de línea, devuelve None o cualquier valor por defecto.
        else:
            return None

    def report_error(self, error):
        self.errors.append(error)

