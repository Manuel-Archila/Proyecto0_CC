from tabulate import tabulate

class Traductor:
    def __init__(self, cuadruplas, classes):
        self.cuadruplas = cuadruplas
        self.indent_level = 0
        self.classes = classes
        self.fijas = ['Main', 'IO', 'Object', 'String', 'Int', 'Bool']
        self.data = False
        self.data_content = ['.data', '\tinput_prompt: .asciiz "Ingrese el numero: "', '\tinput_number: .word 0', '\tstring_buffer: .space 256']
        self.text_content = [".text", "\t.globl main"]
        self.constructors = []
        self.functions = []
        self.add_fijas()
    
    def increment_indent(self):
        self.indent_level += 1

    def decrement_indent(self):
        self.indent_level -= 1

    def get_indent(self):
        return "\t" * self.indent_level  # Suponiendo 4 espacios por nivel de indentación
    
    def add_fijas(self):
            self.functions.append("in_int:")
            self.increment_indent()
            self.functions.append(f"{self.get_indent()}li $v0, 4")
            self.functions.append(f"{self.get_indent()}la $a0, input_prompt")
            self.functions.append(f"{self.get_indent()}syscall")
            self.functions.append(f"{self.get_indent()}li $v0, 5")
            self.functions.append(f"{self.get_indent()}syscall")
            self.functions.append(f"{self.get_indent()}sw $v0, input_number")
            self.functions.append(f"{self.get_indent()}jr $ra")

            self.decrement_indent()
            self.functions.append("out_int:")
            self.increment_indent()
            self.functions.append(f"{self.get_indent()}li $v0, 1")
            self.functions.append(f"{self.get_indent()}lw $a0, input_number")
            self.functions.append(f"{self.get_indent()}syscall")
            self.functions.append(f"{self.get_indent()}jr $ra")
            self.decrement_indent()

            self.functions.append("in_string:")
            self.increment_indent()
            self.functions.append(f"{self.get_indent()}li $v0, 8")
            self.functions.append(f"{self.get_indent()}la $a0, string_buffer")
            self.functions.append(f"{self.get_indent()}li $a1, 256")
            self.functions.append(f"{self.get_indent()}syscall")
            self.functions.append(f"{self.get_indent()}jr $ra")
            self.decrement_indent()

            self.functions.append("out_string:")
            self.increment_indent()
            self.functions.append(f"{self.get_indent()}li $v0, 4")
            self.functions.append(f"{self.get_indent()}lw $a0, string_buffer")
            self.functions.append(f"{self.get_indent()}syscall")
            self.functions.append(f"{self.get_indent()}jr $ra")
            self.decrement_indent()


    def generar_codigo_mips(self):
        # Este método ahora generará el código MIPS completo
        codigo_mips = []

        # Definimos manejadores para cada tipo de operación
        def handle_class(quad):
            operador, op1, op2, result = quad

            if op1 not in self.fijas:
                self.increment_indent()

                size = self.classes[op1]['size']
                metodos =  self.classes[op1]['metodos']
                string_vtalbe = f"{self.get_indent()} {op1}_vtable: .word "

                for metodo in metodos:
                    string_vtalbe += f"{metodo}, "
                
                string_vtalbe = string_vtalbe[:-2]
                self.data_content.append(string_vtalbe)
                
                # codigo_mips.append(string_vtalbe)

                # codigo_mips.append(f"object_{op1}: .word {size}")
                self.data_content.append(f"{self.get_indent()} object_{op1}: .word {size}")
                self.decrement_indent()

                constructor_name = f"{op1}_constructor"
                self.constructors.append(f"{constructor_name}:")
                self.increment_indent()
                self.constructors.append(f"{self.get_indent()}la $t0, {op1}_vtable")
                self.constructors.append(f"{self.get_indent()}sw $t0, object_{op1}")
                self.constructors.append(f"{self.get_indent()}jr $ra")
                self.decrement_indent()
                print(self.constructors)


                

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
                codigo_mips.append(f"{indent}add ${result}, ${op1}, ${op2}")
            elif operador == "-":
                codigo_mips.append(f"{indent}sub ${result}, ${op1}, ${op2}")
            elif operador == "*":
                codigo_mips.append(f"{indent}mul ${result}, ${op1}, ${op2}")
            elif operador == "/":
                codigo_mips.append(f"{indent}div ${result}, ${op1}, ${op2}")

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

        def handle_put(quad):
            operador, op1, op2, result = quad
            indent = self.get_indent()

            codigo_mips.append(f"{indent}li ${result}, {op1}")
        
        def handle_new(quad):
            clase = quad[1]
            indent = self.get_indent()
            size = self.classes[clase]['size']
            temp_reg = quad[3]

            # Asignar memoria
            codigo_mips.append(f"{indent}li $v0, 9")
            codigo_mips.append(f"{indent}li $a0, {size}")
            codigo_mips.append(f"{indent}syscall")
            codigo_mips.append(f"{indent}move ${temp_reg}, $v0")

            # Configurar el puntero a la vtable
            codigo_mips.append(f"{indent}la $t0, {clase}_vtable")
            codigo_mips.append(f"{indent}sw $t0, 0(${temp_reg})")
            

        def handle_vardeclare(quad):
            pass
        #     nombre_var = quad[1]
        #     clase = quad[2]
        #     offset = self.classes[clase]['offsets'][nombre_var]
        #     temp_reg = quad[3]
        #     indent = self.get_indent()

        #     codigo_mips.append(f"{indent}sw ${temp_reg}, {offset}($fp)")

        def handle_method_call(quad):
            operador, op1, op2, result = quad

            # if op1 == "in_int":
            #     self.
                
            
        
        def find_method_address(self, objeto_reg, metodo):
            indent = self.get_indent()
            codigo_mips = []
            metodo_offset = self.classes[clase]['metodos'][metodo]

            # Cargar la vTable del objeto
            codigo_mips.append(f"{indent}lw $t0, 0(${objeto_reg})")  # $t0 tiene la vTable

            # Cargar la dirección del método desde la vTable
            codigo_mips.append(f"{indent}lw $t1, {metodo_offset}($t0)")  # $t1 tiene la dirección del método

            return codigo_mips, '$t1'  # Devuelve el código generado y el registro con la dirección del método

            
        # ... (más manejadores)

        # Mapeo de operaciones a sus manejadores
        quad_handlers = {
            'CLASS': handle_class,
            'DECLARE': handle_declare,
            '+': handle_arithmetic,
            '-': handle_arithmetic,
            '*': handle_arithmetic,
            '/': handle_arithmetic,
            'PUT': handle_put,
            'RETURN_FUNCTION': handle_return_function,
            'END_FUNCTION': handle_end_function,
            'NEW' : handle_new,
            'DECLARE_VAR': handle_vardeclare,
            'CALL': handle_method_call,

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

        for data in self.data_content:
            cuadruplas_data.append(data)
        
        for text in self.text_content:
            cuadruplas_data.append(text)
        
        for constructor in self.constructors:
            cuadruplas_data.append(constructor)

        for cuadrupla in lis:
            cuadruplas_data.append(cuadrupla)

        cuadruplas_str = '\n'.join(cuadruplas_data) 

        with open(nombre_archivo, 'w') as archivo:
            archivo.write(cuadruplas_str)