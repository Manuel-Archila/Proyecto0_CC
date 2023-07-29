class TS:
    def __init__(self):
        self.table = {}

    def agregar_simbolo(self, lexema, linea, columna, token):
        counter = sum(1 for x in self.table if x == lexema)
        par = (lexema, )
        if lexema in self.table:
            self.table[lexema].append({'linea': linea, 'columna': columna, 'token': token})
        else:
            self.table[lexema] = [{'linea': linea, 'columna': columna, 'token': token}]

    def buscar_simbolo(self, lexema):
        return self.table.get(lexema, None)

    def get_table(self):
        return self.table
