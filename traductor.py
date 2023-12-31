from tabulate import tabulate

class Traductor:
    def __init__(self, cuadruplas, classes):
        self.clase_actual = None
        self.cuadruplas = cuadruplas
        self.indent_level = 0
        self.classes = classes
        self.fijas = ['Main', 'IO', 'Object', 'String', 'Int', 'Bool']
        self.data = False
        self.data_content = ['.data', '\tinput_prompt: .asciiz "Ingrese el numero: "', '\tinput_number: .word 0', '\tstringy: .space 256', '\tstring_buffer: .space 256', '\tinty: .word 4', '\tIO_vtable: .word in_int, out_int, in_string, out_string', '\tobject_IO: .word 4']
        self.text_content = [".text", "\t.globl main"]
        self.constructors = ['IO_constructor:', '\tla $t0, IO_vtable', '\tsw $t0, object_IO', '\tjr $ra']
        self.functions = []
        self.metodos_fijos = ['in_int', 'out_int', 'in_string', 'out_string']
        self.atributos = {}

        print(self.classes)

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
            self.functions.append(f"{self.get_indent()}lw $a0, inty")
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
            self.clase_actual = op1
            self.atributos[self.clase_actual] = []

            if op1 not in self.fijas:
                self.increment_indent()

                size = self.classes[op1]['size']
                metodos =  self.classes[op1]['metodos']
                string_vtalbe = f"{self.get_indent()}{op1}_vtable: .word "


                if len(metodos) > 0:
                    for metodo in metodos:
                        string_vtalbe += f"{metodo}, "
                    
                    string_vtalbe = string_vtalbe[:-2]
                else:
                    string_vtalbe += "4"
                    
                self.data_content.append(string_vtalbe)
                
                # codigo_mips.append(string_vtalbe)

                # codigo_mips.append(f"object_{op1}: .word {size}")
                self.data_content.append(f"{self.get_indent()}object_{op1}: .word {size}")
                self.decrement_indent()

                constructor_name = f"{op1}_constructor"
                self.constructors.append(f"{constructor_name}:")
                self.increment_indent()
                self.constructors.append(f"{self.get_indent()}la $t0, {op1}_vtable")
                self.constructors.append(f"{self.get_indent()}sw $t0, object_{op1}")
                self.decrement_indent()

            if op1 =="Main":
                codigo_mips.append('main:')
                self.increment_indent()
                codigo_mips.append(f"{self.get_indent()}move $fp, $sp")
                codigo_mips.append(f"{self.get_indent()}jal IO_constructor")
                
                

        def handle_declare(quad):
            nombre_funcion = quad[1]
            if nombre_funcion == 'main':
                # codigo_mips.append('main:')
                # self.increment_indent()
                # codigo_mips.append(f"{self.get_indent()}move $fp, $sp")
                pass
            else:
                codigo_mips.append(f"{self.get_indent()}{nombre_funcion}:")
                self.increment_indent()
                # Resto de la lógica para la declaración de otras funciones

        def handle_arithmetic(quad):
            temps = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't0']
            operador, op1, op2, result = quad

            if op1 not in temps:
                codigo_mips.append(f"{self.get_indent()}la $t5, {op1}")
                codigo_mips.append(f"{self.get_indent()}lw $t6, 0($t5)")
                op1 = 't6'
            
            if op2 not in temps:
                codigo_mips.append(f"{self.get_indent()}la $t7, {op2}")
                codigo_mips.append(f"{self.get_indent()}lw $t8, 0($t7)")
                op2 = 't8'


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
            operador, op1, op2, result = quad
            #codigo_mips.append(f"{self.get_indent()}move $v0, $t0")

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
            operador, op1, op2, result = quad
            
            codigo_mips.append(f"{self.get_indent()}jal {op1}_constructor")

        def handle_vardeclare(quad):
            operador, op1, op2, result = quad
            self.atributos[self.clase_actual].append(op1)

            if op2 == "Int":
                self.data_content.append(f"\t{self.clase_actual}_{op1}: .word 4")
                self.constructors.append(f"\tli $t0, 0")
                self.constructors.append(f"\tsw $t0, {self.clase_actual}_{op1}")
            elif op2 == "String":
                self.data_content.append(f"\t{self.clase_actual}_{op1}: .space 256")
            elif op2 == "Bool":
                self.data_content.append(f"\t{self.clase_actual}_{op1}: .word 1")

        def handle_method_call(quad):
            operador, op1, op2, result = quad

            print("op1", op1)
            print("op2", op2)

            if op1 not in self.classes[op2]['metodos']:
                for clase in self.classes[op2]['hereda']:
                    print("clase", clase)
                    if op1 in self.classes[clase]['metodos']:
                        codigo_mips.append(f"{self.get_indent()}jal {clase}_constructor")
                        op2 = clase
                        break

            
            cant = 0
            metodos = self.classes[op2]['metodos']

            for metodo in metodos:
                if metodo == op1:
                    break
                cant += 4


            codigo_mips.append(f"{self.get_indent()}lw $t0, object_{op2}")
            codigo_mips.append(f"{self.get_indent()}lw $t1, {cant}($t0)")
            codigo_mips.append(f"{self.get_indent()}jalr $t1")
                

        def handle_param(quad):
            operador, op1, op2, result = quad

            if op2 == "Int":
                self.data_content.append(f"\t{result}: .word 4")
            elif op2 == "String":
                self.data_content.append(f"\t{result}: .space 256")
            elif op2 == "Bool":
                self.data_content.append(f"\t{result}: .word 1")

        
        def handle_assing_param(quad):
            operador, op1, op2, result = quad
            indent = self.get_indent()
            is_int = False

            if result == 'inty':
                try:
                    int(op1)
                    is_int = True
                except:
                    pass

                for elem in self.atributos[self.clase_actual]:
                    if elem == op1:
                        op1 = f"{self.clase_actual}_{op1}"
                        break


                if not is_int:
                    codigo_mips.append(f"{indent}lw $t0, {op1}")
                

                codigo_mips.append(f"{indent}sw $t0, {result}")
                codigo_mips.append(f"{indent}lw $a0, {result}")
            else:
            
                codigo_mips.append(f"{indent}la $t0, {result}")
                codigo_mips.append(f"{indent}sw ${op1}, 0($t0)")
        
        def handle_end_class(quad):
            operador, op1, op2, result = quad

            if op1 != 'Main':
                self.constructors.append(f"\tjr $ra")
        
        def handle_assign(quad):
            operador, op1, op2, result = quad
            indent = self.get_indent()
            var_name = result.replace('BaseInstancia + offset', "")
            print("var_name", var_name)
            variable = f"{self.clase_actual}_{var_name}"

            if op1 == 'in_int()':
                codigo_mips.append(f"{indent}lw $t0, input_number")
                codigo_mips.append(f"{indent}sw $t0, {variable}")
            

            

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
            'ASSIGN_PARAM': handle_assing_param,
            'PARAM' : handle_param,
            'END_CLASS' : handle_end_class,
            'ASSIGN': handle_assign,

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
        
        for function in self.functions:
            cuadruplas_data.append(function)

        for cuadrupla in lis:
            cuadruplas_data.append(cuadrupla)

        cuadruplas_str = '\n'.join(cuadruplas_data) 

        with open(nombre_archivo, 'w') as archivo:
            archivo.write(cuadruplas_str)