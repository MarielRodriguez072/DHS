import re

class Optimizacion:
    def __init__(self, archivo_entrada, archivo_salida):
        self.archivo_entrada = archivo_entrada
        self.archivo_salida = archivo_salida
        self.codigo = []

        self.leer_codigo()
        self.optimizar()
        self.escribir_codigo()

    # =============================
    # IO
    # =============================

    def leer_codigo(self):
        with open(self.archivo_entrada, "r", encoding="utf-8") as f:
            self.codigo = [l.strip() for l in f if l.strip()]

    def escribir_codigo(self):
        with open(self.archivo_salida, "w", encoding="utf-8") as f:
            for l in self.codigo:
                f.write(l + "\n")

    # =============================
    # Helpers
    # =============================

    def es_label(self, l):
        return l.endswith(":")

    def es_salto(self, l):
        return l.startswith("goto") or l.startswith("if")

    def variables_modificadas(self):
        mods = set()
        for l in self.codigo:
            if "=" in l and not l.startswith("if"):
                var = l.split("=")[0].strip()
                if not var.startswith("t"):
                    mods.add(var)
        return mods

    # =============================
    # Optimizaciones
    # =============================

    def constant_folding(self):
        cambio = False
        for i, l in enumerate(self.codigo):
            if l.endswith(":") or l.startswith("if") or l.startswith("goto"):
                continue

            m = re.match(r"(t\d+)\s*=\s*(\d+)\s*([+\-*/])\s*(\d+)", l)
            if m:
                t, a, op, b = m.groups()
                res = eval(f"{a}{op}{b}")
                nueva = f"{t} = {res}"
                if self.codigo[i] != nueva:
                    self.codigo[i] = nueva
                    cambio = True
        return cambio

    def peephole(self):
        cambio = False
        i = 0
        while i < len(self.codigo) - 1:
            l1 = self.codigo[i]
            l2 = self.codigo[i + 1]

            if "=" in l1 and "=" in l2:
                t, expr = map(str.strip, l1.split("=", 1))
                var, val = map(str.strip, l2.split("=", 1))

                if val == t and t.startswith("t"):
                    self.codigo[i] = f"{var} = {expr}"
                    del self.codigo[i + 1]
                    cambio = True
                    continue
            i += 1
        return cambio

    def cse_local(self):
        cambio = False
        exprs = {}
        for i, l in enumerate(self.codigo):
            if self.es_label(l) or self.es_salto(l):
                exprs.clear()
                continue

            if "=" in l and not l.startswith("if"):
                t, expr = map(str.strip, l.split("=", 1))
                if expr in exprs:
                    self.codigo[i] = f"{t} = {exprs[expr]}"
                    cambio = True
                else:
                    exprs[expr] = t
        return cambio

    def eliminar_codigo_muerto(self):
        usados = set()

        for l in self.codigo:
            if "=" in l:
                rhs = l.split("=", 1)[1]
                for tok in rhs.split():
                    if tok.startswith("t"):
                        usados.add(tok)
            if "if" in l or "goto" in l:
                for tok in l.split():
                    if tok.startswith("t"):
                        usados.add(tok)

        nueva = []
        cambio = False
        for l in self.codigo:
            if l.startswith("t") and "=" in l:
                t = l.split("=")[0].strip()
                if t not in usados:
                    cambio = True
                    continue
            nueva.append(l)

        self.codigo = nueva
        return cambio

    def eliminar_labels_vacias(self):
        cambio = False
        i = 0
        while i < len(self.codigo) - 1:
            if self.es_label(self.codigo[i]) and self.es_label(self.codigo[i + 1]):
                self.codigo.pop(i)
                cambio = True
            else:
                i += 1
        return cambio

    # =============================
    # Pipeline
    # =============================

    def optimizar(self):
        MAX_ITER = 10
        iteraciones = 0
        cambio = True

        while cambio and iteraciones < MAX_ITER:
            cambio = False
            iteraciones += 1

            cambio |= self.constant_folding()
            cambio |= self.peephole()
            cambio |= self.cse_local()
            cambio |= self.eliminar_codigo_muerto()
            cambio |= self.eliminar_labels_vacias()

