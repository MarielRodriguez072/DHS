# TablaSimbolos.py
class TablaSimbolos:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TablaSimbolos, cls).__new__(cls)
            cls._instance.ts = [dict()] 
            cls._instance.historial = []
        return cls._instance

    #Context management
    def push_context(self):
        ctx = dict()
        self.ts.append(ctx)
        self.historial.append(ctx)

    def pop_context(self):
        if len(self.ts) > 1:
            self.ts.pop()
        else:
            print("WARNING: intento de eliminar el contexto global; operación ignorada.")

    #Declarar variable en contexto actual
    def declare_variable(self, id_obj):
        name = id_obj.name
        if name in self.ts[-1]:
            raise KeyError(f"Ya existe '{name}' en el contexto actual")
        self.ts[-1][name] = id_obj

    #Declarar función: se guarda en contexto GLOBAL (ts[0])
    def declare_function(self, func_obj):
        name = func_obj.name
        if name in self.ts[0]:
            raise KeyError(f"Ya existe la función '{name}' en el contexto global")
        self.ts[0][name] = func_obj

    #Buscar desde contexto más interno hacia afuera
    def lookup(self, name):
        for context in reversed(self.ts):
            if name in context:
                return context[name]
        return None

    def exists(self, name):
        return self.lookup(name) is not None
    
    def exists_local(self, name):
        return name in self.ts[-1]

    def exportarTabla(self, archivo, ctx_num):
        contexto = self.ts[-1]

        archivo.write(f"CONTEXTO {ctx_num}:\n")
        if contexto:
            for nombre, item in contexto.items():
                tipo = getattr(item, 'type', 'desconocido')
                varfunc = getattr(item, 'varFunc', None)
                if varfunc == "function":
                    archivo.write(f"  - {nombre}: función {tipo}\n")
                    scope = getattr(item, 'scope', None)
                    params = getattr(item, 'parameters', None)
                    if params:
                        if params and isinstance(params[0], tuple):
                            archivo.write(f"     parametros: {', '.join([f'{t} {n}' for t,n in params])}\n")
                        else:
                            archivo.write(f"     parametros: {', '.join(params)}\n")
                    if scope:
                        archivo.write(f"     scope local:\n")
                        for lname, litem in scope.items():
                            ltipo = getattr(litem, 'type', 'desconocido')
                            archivo.write(f"       * {lname}: {ltipo}\n")
                else:
                    archivo.write(f"  - {nombre}: variable {tipo}\n")
        else:
            archivo.write("  (vacío)\n")
        archivo.write("\n")

    def exportar_contexto(self, archivo, contexto):
        if contexto:
            for nombre, item in contexto.items():
                tipo = getattr(item, 'type', 'desconocido')
                varfunc = getattr(item, 'varFunc', None)
    
                if varfunc == "function":
                    archivo.write(f"  - {nombre}: función {tipo}\n")
                    if item.parameters:
                        archivo.write(
                            "     parametros: " +
                            ", ".join([f"{t} {n}" for t,n in item.parameters]) + "\n"
                        )
                    if item.scope:
                        archivo.write("     scope local:\n")
                        for lname, litem in item.scope.items():
                            archivo.write(f"       * {lname}: {litem.type}\n")
                else:
                    archivo.write(f"  - {nombre}: variable {tipo}\n")
        else:
            archivo.write("  (vacío)\n")
        archivo.write("\n")



class Id:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_
        self.initialized = False
        self.used = False
        self.varFunc = None

    def __str__(self):
        return f"(name->{self.name}, type->{self.type}, init->{self.initialized}, used->{self.used}, varFunc->{self.varFunc})"

    __repr__ = __str__


class Variable(Id):
    def __init__(self, name, type_):
        super().__init__(name, type_)
        self.varFunc = "variable"



class Function(Id):
    def __init__(self, name, type_, parameters=None):
        super().__init__(name, type_)
        self.parameters = parameters or []
        self.varFunc = "function"
        self.scope = None
