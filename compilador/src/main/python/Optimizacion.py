import re

class Optimizacion:
    def __init__(self, archivo_entrada, archivo_salida):
        self.archivo_entrada = archivo_entrada
        self.archivo_salida = archivo_salida
        self.codigo = []

        self.leer_codigo()
        self.optimizar()
        self.escribir_codigo()

    # Entrada/salida
    def leer_codigo(self):
        with open(self.archivo_entrada, "r", encoding="utf-8") as f:
            self.codigo = [l.strip() for l in f if l.strip()]

    def escribir_codigo(self):
        with open(self.archivo_salida, "w", encoding="utf-8") as f:
            for l in self.codigo:
                f.write(l + "\n")

    # Helpers
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
    
    def es_inicio_funcion(self, l):
        return l.endswith(":") and not l.startswith("L")
    
    def separar_por_funciones(self):
        funciones = []
        actual = []

        for l in self.codigo:
            if self.es_inicio_funcion(l) and actual:
                funciones.append(actual)
                actual = []
            actual.append(l)

        if actual:
            funciones.append(actual)

        return funciones



    # Optimizaciones
    # elimina asignaciones inutiles donde una variable se asigna a si misma
    def eliminar_asignaciones_triviales(self):
        nueva = []
        cambio = False

        for l in self.codigo:
            if "=" in l and not l.startswith("if"):
                var, expr = map(str.strip, l.split("=", 1))
                if var == expr:
                    cambio = True
                    continue
            nueva.append(l)

        self.codigo = nueva
        return cambio

    # elimina asignaciones a una variable que son sobrescritas antes de ser usadas
    def eliminar_asignaciones_sobrescritas(self):
        cambio = False
        ultima_def = {}
        nueva = []
    
        for l in self.codigo:
            if self.es_label(l) or self.es_salto(l):
                ultima_def.clear()
                nueva.append(l)
                continue
            
            if "=" in l:
                var = l.split("=")[0].strip()
                if var in ultima_def:
                    idx = ultima_def[var]
                    nueva[idx] = None
                    cambio = True
                ultima_def[var] = len(nueva)
                nueva.append(l)
            else:
                nueva.append(l)
    
        self.codigo = [l for l in nueva if l is not None]
        return cambio


    # reemplaza el uso de variables por sus valores constantes conocidos
    def propagacion_constantes(self):
        const = {}
        cambio = False

        for i, l in enumerate(self.codigo):
            l = l.strip()

            if l.endswith(":") or l.startswith("if") or l.startswith("goto"):
                const.clear()
                continue

            if "=" in l:
                var, expr = map(str.strip, l.split("=", 1))

                if expr.isdigit():
                    const[var] = expr
                else:
                    const.pop(var, None)

                if var in const:
                    del const[var]

                nueva_expr = expr
                for k, v in const.items():
                    nueva_expr = re.sub(rf"\b{k}\b", v, nueva_expr)

                if nueva_expr != expr:
                    self.codigo[i] = f"{var} = {nueva_expr}"
                    cambio = True

        return cambio

    # Evalua en tiempo de compilacion expresiones aritmeticas cuyoos operandos son constantes
    def constant_folding(self):
        cambio = False

        for i, l in enumerate(self.codigo):
            if l.endswith(":") or l.startswith("if") or l.startswith("goto"):
                continue

            m = re.match(r"(\w+)\s*=\s*(\d+)\s*([+\-*/])\s*(\d+)", l)
            if m:
                var, a, op, b = m.groups()
                res = eval(f"{a}{op}{b}")
                nueva = f"{var} = {res}"
                if self.codigo[i] != nueva:
                    self.codigo[i] = nueva
                    cambio = True

        return cambio
    
    # simplifica patrones comunes de codigo intermedio
    #ej t1= a+b
    #   c = t1
    #despues c = a + b
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

    # common subexpression elimination 
    #detecta expresiones identicas ya calculadas y reutiliza el resultado
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

    #elimina temporales que nunca son usados
    def eliminar_codigo_muerto(self):
        usados = set()

        for l in self.codigo:
            l = l.strip()
            if "=" in l:
                _, rhs = l.split("=", 1)
                for tok in re.findall(r"\bt\d+\b", rhs):
                    usados.add(tok)
            elif l.startswith("if"):
                for tok in re.findall(r"\bt\d+\b", l):
                    usados.add(tok)

        nueva = []
        cambio = False

        for l in self.codigo:
            l = l.strip()
            if l.startswith("t") and "=" in l:
                t = l.split("=")[0].strip()
                if t not in usados:
                    cambio = True
                    continue
            nueva.append(l)

        self.codigo = nueva
        return cambio

    # elimina labels vacias
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
    
    # elimina estructuras if-else donde ambas ramas asignan el mismo valor
    # patrón:
            # ifFalse t goto Lx
            # c = 7
            # goto Ly
            # Lx:
            # c = 7
    def eliminar_if_asignacion_igual(self):
        cambio = False
        i = 0
    
        while i < len(self.codigo) - 6:
            
            if (self.codigo[i].startswith("ifFalse") and
                "=" in self.codigo[i+1] and
                self.codigo[i+2].startswith("goto") and
                self.codigo[i+3].endswith(":") and
                self.codigo[i+4] == self.codigo[i+1]):
    
                # eliminar else redundante
                del self.codigo[i+2:i+5]
                cambio = True
                continue
            
            i += 1
    
        return cambio

    #elimina temporales usados solo en condiciones
    def peephole_condiciones(self):
        cambio = False
        for i in range(len(self.codigo) - 1):
            l1 = self.codigo[i]
            l2 = self.codigo[i + 1]

            if l1.startswith("t") and " = " in l1 and l2.startswith("ifFalse"):
                t, expr = map(str.strip, l1.split("=", 1))
                if f"ifFalse {t}" in l2:
                    self.codigo[i + 1] = l2.replace(t, expr)
                    self.codigo[i] = None
                    cambio = True

        self.codigo = [l for l in self.codigo if l is not None]
        return cambio
    
    # elimina codigo despues de un return o goto hasta la siguiente etiqueta
    def eliminar_codigo_inalcanzable(self):
        cambio = False
        nueva = []
        muerto = False

        for l in self.codigo:
            if self.es_label(l):
                muerto = False
                nueva.append(l)
                continue

            if muerto:
                cambio = True
                continue

            nueva.append(l)

            if l.startswith("return") or l.startswith("goto"):
                muerto = True

        self.codigo = nueva
        return cambio
    
    #detecta labels que son usados
    def labels_usados(self):
        usados = set()
        for l in self.codigo:
            if l.startswith("goto"):
                usados.add(l.split()[-1])
            elif l.startswith("if"):
                usados.add(l.split()[-1])
        return usados

    #elimina labels que no son usados
    def eliminar_labels_no_usados(self):
        usados = self.labels_usados()
        nueva = []
        cambio = False

        for l in self.codigo:
            if self.es_label(l):
                nombre = l[:-1]
                if nombre not in usados:
                    cambio = True
                    continue
            nueva.append(l)

        self.codigo = nueva
        return cambio
    
    #redirecciona saltos a labels puente eliminando el salto intermedio
    def redireccionar_saltos(self):
        cambio = False
        redir = {}

        # detectar labels puente
        for i in range(len(self.codigo) - 1):
            if self.es_label(self.codigo[i]) and self.codigo[i+1].startswith("goto"):
                label = self.codigo[i][:-1]
                destino = self.codigo[i+1].split()[-1]
                redir[label] = destino

        # aplicar redirecciones
        for i, l in enumerate(self.codigo):
            for k, v in redir.items():
                if f"goto {k}" in l:
                    self.codigo[i] = l.replace(k, v)
                    cambio = True

        return cambio


    def optimizar(self):
        funciones = self.separar_por_funciones()
        codigo_final = []

        for func in funciones:
            self.codigo = func
            self.optimizar_funcion()
            codigo_final.extend(self.codigo)

        self.codigo = codigo_final


    # Pipeline
    def optimizar_funcion(self):
        cambio = True
        MAX_ITER = 20
        iteraciones = 0

        while cambio and iteraciones < MAX_ITER:
            cambio = False
            iteraciones += 1
        
            cambio |= self.constant_folding()
            cambio |= self.propagacion_constantes()
        
            cambio |= self.peephole()
            cambio |= self.peephole_condiciones()
        
            cambio |= self.eliminar_asignaciones_triviales()
            cambio |= self.eliminar_asignaciones_sobrescritas()
        
            cambio |= self.cse_local()
        
            cambio |= self.eliminar_if_asignacion_igual()
            cambio |= self.eliminar_codigo_inalcanzable()
            cambio |= self.eliminar_codigo_muerto()
            cambio |= self.eliminar_labels_vacias()

            cambio |= self.redireccionar_saltos()
            cambio |= self.eliminar_labels_no_usados()

