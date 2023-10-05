from tabulate import tabulate

class Cuadruplas:
    def __init__(self):
        self.cuadruplas = {}
        self.temporal_counter = 0
        self.labels = 1
        self.contCuadruplas = 1

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
    
    def get_last_cuadrupla(self):
        return self.cuadruplas[self.contCuadruplas-1]
    