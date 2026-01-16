class CodigoTresDirecciones:

    def __init__(self):
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0

    # ---------- temporales ----------
    def nuevo_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    # ---------- etiquetas ----------
    def nueva_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    # ---------- instrucciones ----------
    def emitir(self, instruccion):
        self.codigo.append(instruccion)

    # ---------- operaciones ----------
    def asignacion(self, destino, fuente):
        self.emitir(f"{destino} = {fuente}")

    def operacion(self, resultado, op1, operador, op2):
        self.emitir(f"{resultado} = {op1} {operador} {op2}")

    def salto(self, label):
        self.emitir(f"goto {label}")

    def salto_condicional(self, op1, rel, op2, label):
        self.emitir(f"if {op1} {rel} {op2} goto {label}")

    def label(self, label):
        self.emitir(f"{label}:")

    def retorno(self, valor):
        self.emitir(f"return {valor}")

    # ---------- funciones ----------
    def iniciar_funcion(self, nombre):
        self.emitir(f"\nfunc {nombre}:")

    def fin_funcion(self):
        self.emitir("endfunc\n")

    # ---------- salida ----------
    def obtener_codigo(self):
        return "\n".join(self.codigo)

    def escribir_codigo(self, archivo="codigo_intermedio.txt"):
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(self.obtener_codigo())
