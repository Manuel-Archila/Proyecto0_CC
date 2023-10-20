from tabulate import tabulate

class Traductor:
    def __init__(self, cuadruplas):
        self.cuadruplas = cuadruplas

    def buscar_operadores_aritmeticos(self):
        operadores_aritmeticos = ['+', '-', '*', '/']
        cuadruplas_con_operadores = {}

        for num_cuadrupla, cuadrupla in self.cuadruplas.items():
            operador = cuadrupla[0]
            if operador in operadores_aritmeticos:
                cuadruplas_con_operadores[num_cuadrupla] = cuadrupla

        return cuadruplas_con_operadores
    
    
    def generar_codigo_mips(self, lis):
        codigo_mips = []

        for num_cuadrupla, cuadrupla in lis.items():
            operador, operando1, operando2, resultado = cuadrupla

            if operador == "+":
                codigo_mips.append(f"li {resultado}, {operando1}")
                codigo_mips.append(f"addi {resultado}, {resultado}, {operando2}")

            elif operador == "-":
                codigo_mips.append(f"li {resultado}, {operando1}")
                codigo_mips.append(f"sub {resultado}, {resultado}, {operando2}")

            
            elif operador == "*":
                codigo_mips.append(f"li {resultado}, {operando1}")
                codigo_mips.append(f"mul {resultado}, {resultado}, {operando2}")

            elif operador == "/":
                codigo_mips.append(f"li {resultado}, {operando1}")
                codigo_mips.append(f"div {resultado}, {resultado}, {operando2}")
                

        return codigo_mips
    

    def escribir_cuadruplaTrad_en_archivo(self, nombre_archivo, lis):
        cuadruplas_data = []

        for cuadrupla in lis:
            cuadruplas_data.append(cuadrupla)

        cuadruplas_str = '\n'.join(cuadruplas_data) 

        with open(nombre_archivo, 'w') as archivo:
            archivo.write(cuadruplas_str)