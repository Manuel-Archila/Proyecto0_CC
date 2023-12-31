from tabulate import tabulate

class Cuadruplas:
    def __init__(self, clases):
        self.cuadruplas = {}
        self.temporal_counter = 0
        self.labels = 1
        self.contCuadruplas = 1
        self.fijas()
        self.clases = clases

    def fijas(self):

        cuadrupla = ["CLASS", "Object", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "abort", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "abort", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "type_name", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "type_name", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "copy", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "copy", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_CLASS", "Object", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["CLASS", "String", "Object", None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "length", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "length", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["PARAM", None, None, "str"]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "concat", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "concat", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["PARAM", None, None, "index1"]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["PARAM", None, None, "index2"]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "substr", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "substr", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_CLASS", "String", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["CLASS", "Int", "Object", None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_CLASS", "Int", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["CLASS", "Bool", "Object", None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_CLASS", "Bool", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["CLASS", "IO", "Object", None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["PARAM", None, None, "stringy"]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "out_string", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "out_string", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1
        
        cuadrupla = ["PARAM", None, None, "inty"]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "out_int", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "out_int", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "out_int", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "out_int", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "in_string", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "in_string", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["DECLARE", "in_int", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_FUNCTION", "int_int", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

        cuadrupla = ["END_CLASS", "IO", None, None]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        self.contCuadruplas += 1

    
    def agregar_cuadrupla(self, operador, operando1, operando2, resultado):

        if resultado == "t":
            resultado = resultado + str(self.temporal_counter)
            self.temporal_counter += 1
        elif resultado == "L":
            resultado = resultado + str(self.labels)
            self.labels += 1
        

        cuadrupla = [operador, operando1, operando2, resultado]
        self.cuadruplas[self.contCuadruplas] = cuadrupla
        
        self.contCuadruplas += 1
        
        if resultado is not None:
            if "L" in resultado:
                return resultado
            if "t" in resultado:
                return resultado
            
        if operador == "END_FUNCTION":
            self.temporal_counter = 0

    def nuevoLabel(self, resultado):
        resultado = resultado + str(self.labels)
        self.labels += 1
        return resultado

    def encontrar_cuadrupla_param(self, parametro):
        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            if cuadrupla[0] == "PARAM" and cuadrupla[3] == parametro:
                return num_cuadrupla
        return None

    def imprimir_cuadruplas(self):
        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            print(f"Cuadrupla {num_cuadrupla}: {cuadrupla}")

    def escribir_cuadruplas_en_archivo(self, nombre_archivo):
        headers = ['Cuadrupla', 'Operador', 'Operando1', 'Operando2', 'Resultado']
        cuadruplas_data = []

        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            cuadruplas_data.append([num_cuadrupla] + cuadrupla)

        tabla_formateada = tabulate(cuadruplas_data, headers, tablefmt='grid')

        with open(nombre_archivo, 'w') as archivo:
            archivo.write(tabla_formateada)

        
        nombre_archivo = nombre_archivo.replace(".txt", "2.txt")

        with open(nombre_archivo, 'w') as file:
            for key, value in self.cuadruplas.items():
                file.write(','.join(str(x) for x in value) + '\n')
            
    def get_last_cuadrupla(self):
        return self.cuadruplas[self.contCuadruplas-1]
    
    def verIf(self):
        try:
            cua = self.cuadruplas[self.contCuadruplas-6]

            if "IF" in cua[0]:
                return True
            else:
                return False
        except:
            print(len(self.cuadruplas))

    def retIF(self):

        valT = self.cuadruplas[self.contCuadruplas-3][3]
        valF = self.cuadruplas[self.contCuadruplas-1][3]

        self.agregar_cuadrupla("RETURN_FUNCTION", valT, valF, None)

    def eliminarUltima(self):
        del self.cuadruplas[self.contCuadruplas-1]
        self.contCuadruplas -= 1
        self.temporal_counter -= 1

    def get_function_cuadrupla(self, function_name):
        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            if cuadrupla[0] == "DECLARE" and cuadrupla[1] == function_name:
                print("El numero de cuadrupla es: ", num_cuadrupla)
                return num_cuadrupla
        return None
    
    def get_function_params(self, function_name):
        params = []
        function_cuadrupla = self.get_function_cuadrupla(function_name)
        is_param = True
        while is_param:
            function_cuadrupla -= 1
            cuadrupla = self.cuadruplas[function_cuadrupla]
            if cuadrupla[0] == "PARAM":
                params.append(cuadrupla[3])
            else:
                is_param = False
        return params
    
    def get_last_call(self):
        last_counter = self.contCuadruplas - 1
        last_cuadrupla = self.cuadruplas[last_counter]
        while last_cuadrupla[0] != "CALL":
            last_counter -= 1
            last_cuadrupla = self.cuadruplas[last_counter]
        return self.cuadruplas[last_counter][3]
    
    def get_cuadrupla_put(self, valor):
        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            if cuadrupla[0] == "PUT" and cuadrupla[1] == valor:
                return cuadrupla[3]
        return None

    def eliminar_primeras_cuadruplas(self):
        if self.cuadruplas:
            for i in range(0, 37):
                primer_elemento = next(iter(self.cuadruplas))  
                self.cuadruplas.pop(primer_elemento)
    
    def get_metodos(self, clase):
        metodos = []
        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            if cuadrupla[0] == "CLASS" and cuadrupla[1] == clase:
                is_method = True
                while is_method:
                    num_cuadrupla += 1
                    cuadrupla = self.cuadruplas[num_cuadrupla]
                    if cuadrupla[0] == "DECLARE":
                        metodos.append(cuadrupla[1])
                    if cuadrupla[0] == "END_CLASS":
                        is_method = False
                        return metodos

        

    def agregar_metodos(self):
        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            if cuadrupla[0] == "CLASS":
                clase = cuadrupla[1]
                metodos = self.get_metodos(clase)
                self.clases[clase]["metodos"] = metodos
                if cuadrupla[2] != None:
                    self.clases[clase]["hereda"] = [cuadrupla[2]]
                
                