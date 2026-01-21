class CodigoTresDirecciones:

    def __init__(self):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0

    # -------------------------
    # utilidades básicas
    # -------------------------
    def agregar_instruccion(self, instruccion):
        self.codigo.append(instruccion)

    def nuevo_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def nuevo_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    # -------------------------
    # instrucciones 3D
    # -------------------------
    def operacion(self, resultado, op1, operador, op2):
        self.agregar_instruccion(f"{resultado} = {op1} {operador} {op2}")

    def asignacion(self, variable, valor):
        self.agregar_instruccion(f"{variable} = {valor}")

    def retorno(self, valor):
        self.agregar_instruccion(f"return {valor}")

    def llamada_funcion(self, nombre, args):
        for arg in args:
            self.agregar_instruccion(f"param {arg}")
        temp = self.nuevo_temp()
        self.agregar_instruccion(f"{temp} = call {nombre}, {len(args)}")
        return temp

    # -------------------------
    # salida
    # -------------------------
    def obtener_codigo(self):
        return "\n".join(self.codigo)

    def escribir_codigo(self, archivo="codigo_intermedio.txt"):
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(self.obtener_codigo())
