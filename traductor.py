from tabulate import tabulate

class Traductor:
    def __init__(self, cuadruplas):
        self.cuadruplas = cuadruplas
        self.indent_level = 0
    
    def increment_indent(self):
        self.indent_level += 1

    def decrement_indent(self):
        self.indent_level -= 1

    def get_indent(self):
        return "    " * self.indent_level  # Suponiendo 4 espacios por nivel de indentación


    def generar_codigo_mips(self):
        # Este método ahora generará el código MIPS completo
        codigo_mips = []

        # Definimos manejadores para cada tipo de operación
        def handle_class(quad):
            pass  # Por ahora, ignoramos las clases

        def handle_declare(quad):
            nombre_funcion = quad[1]
            if nombre_funcion == 'main':
                codigo_mips.append('main:')
                self.increment_indent()
                codigo_mips.append(f"{self.get_indent()}move $fp, $sp")
            else:
                codigo_mips.append(f"{self.get_indent()}{nombre_funcion}:")
                self.increment_indent()
                # Resto de la lógica para la declaración de otras funciones

        def handle_arithmetic(quad):
            operador, op1, op2, result = quad
            indent = self.get_indent()
            if operador == "+":
                codigo_mips.append(f"{indent}li $t1, {op1}")
                codigo_mips.append(f"{indent}li $t2, {op2}")
                codigo_mips.append(f"{indent}add $t0, $t1, $t2")
            elif operador == "-":
                codigo_mips.append(f"{indent}li $t1, {op1}")
                codigo_mips.append(f"{indent}li $t2, {op2}")
                codigo_mips.append(f"{indent}sub $t0, $t1, $t2")
            elif operador == "*":
                codigo_mips.append(f"{indent}li $t1, {op1}")
                codigo_mips.append(f"{indent}li $t2, {op2}")
                codigo_mips.append(f"{indent}mul $t0, $t1, $t2")
            elif operador == "/":
                codigo_mips.append(f"{indent}li $t1, {op1}")
                codigo_mips.append(f"{indent}li $t2, {op2}")
                codigo_mips.append(f"{indent}div $t0, $t1, $t2")

        def handle_return_function(quad):
            codigo_mips.append(f"{self.get_indent()}move $v0, $t0")

        def handle_end_function(quad):
            nombre_funcion = quad[1]
            if nombre_funcion == 'main':
                codigo_mips.append(f"{self.get_indent()}li $v0, 10")  # Termina la ejecución del programa
                codigo_mips.append(f"{self.get_indent()}syscall")
                self.indent_level -= 1
            else:
                codigo_mips.append(f"{self.get_indent()}jr $ra")
                self.decrement_indent()

        # ... (más manejadores)

        # Mapeo de operaciones a sus manejadores
        quad_handlers = {
            'CLASS': handle_class,
            'DECLARE': handle_declare,
            '+': handle_arithmetic,
            '-': handle_arithmetic,
            '*': handle_arithmetic,
            '/': handle_arithmetic,
            'RETURN_FUNCTION': handle_return_function,
            'END_FUNCTION': handle_end_function,
            # ... (más manejadores)
        }

        # Recorremos las cuádruplas y generamos el código MIPS
        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            operation = cuadrupla[0]
            if operation in quad_handlers:
                quad_handlers[operation](cuadrupla)

        return codigo_mips
    

    def escribir_cuadruplaTrad_en_archivo(self, nombre_archivo, lis):
        cuadruplas_data = []

        for cuadrupla in lis:
            cuadruplas_data.append(cuadrupla)

        cuadruplas_str = '\n'.join(cuadruplas_data) 

        with open(nombre_archivo, 'w') as archivo:
            archivo.write(cuadruplas_str)