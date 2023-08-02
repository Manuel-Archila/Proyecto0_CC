class TS:
    def __init__(self):
        self.table = []

    def agregar_simbolo(self, lexema, linea, columna, token):
        self.table.append({'lexema': lexema, 'linea': linea, 'columna': columna, 'token': token})

    def buscar_simbolo(self, lexema):
        lexemas = []
        for i in self.table:
            if i['lexema'] == lexema:
                lexemas.append(i)
        return lexemas

    def get_table(self):
        return self.table
