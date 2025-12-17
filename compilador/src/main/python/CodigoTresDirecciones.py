import os


class CodigoTresDirecciones:

    def __init__(self):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0

    def agregar_instruccion(self, instruccion):
        self.codigo.append(instruccion)
    
    def nueva_variable(self, nombre):
        instruccion = f"t {self.temp_count}"
        self.temp_count += 1

        self.agregar_instruccion(instruccion)

    def obtener_codigo(self):
        return "\n".join(self.codigo)

    def escribir_codigo(self):
        tablaFile = os.path.join(os.path.dirname("prueba.txt"), "codigo.txt")
        with open(tablaFile, 'w') as f:
            f.write(self.obtener_codigo()) 