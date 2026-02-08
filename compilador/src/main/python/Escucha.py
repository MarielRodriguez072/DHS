# Escucha.py
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from TablaSimbolos import TablaSimbolos, Id, Variable, Function
import os
from datetime import datetime

class Escucha(compiladorListener):
    def __init__(self):
        super().__init__()
        self.indent = 1
        self.declaracion = 0
        self.profundidad = 0
        self.numNodos = 0
        self.asignacion = 0
        self.tabla = None
        self.ctx = 0
        self.hay_error_semantico = False

    def dbg_contexts(self, msg=""):
        print("\n--- CONTEXTOS", msg, "---")
        for i, ctx in enumerate(self.tabla.ts):
            print(f"  [{i}] -> {list(ctx.keys())}")
        print("-------------------------\n")

    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        #self.tabla = TablaSimbolos()
        #self.tabla.ts = [dict()]
        if self.tabla is None:
            self.tabla = TablaSimbolos()

        print("Comienza el parsing")
        archivo = "prueba.txt"
        tablaFile = os.path.join(os.path.dirname(archivo), "tablaSimbolos.txt")
        with open(tablaFile, 'a', encoding='utf-8') as f:
            f.write(f"Tabla de Simbolos generada el {datetime.now()}\n\n")

    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Termina el parsing")
        
        archivo = "prueba.txt"
        tablaFile = os.path.join(os.path.dirname(archivo), "tablaSimbolos.txt")

        with open(tablaFile, 'a', encoding='utf-8') as f:
            f.write("CONTEXTO 0 (global):\n")
            self.tabla.exportar_contexto(f, self.tabla.ts[0])
            
            for i, contexto in enumerate(self.tabla.historial):
                f.write(f"CONTEXTO {i+1}:\n")
                self.tabla.exportar_contexto(f, contexto)
            
        # mensajes semánticos
        for context in self.tabla.ts:
            for key, value in context.items():
                if not value.used and getattr(value, 'varFunc', None) != "function":
                    print(f"  -- WARNING SEMANTICO: La variable |{key}| fue declarada pero nunca usada")

        print(self)

    # ---------- bloques ----------
    def enterBloque(self, ctx):
        self.tabla.push_context()  # contexto de función

        if isinstance(ctx.parentCtx, compiladorParser.FuncionContext):

            argumentos_ctx = ctx.parentCtx.argumentos()
            params = self.obtener_parametros(argumentos_ctx)

            for tipo, nombre in params:
                self.tabla.declare_variable(Variable(nombre, tipo))

        
        # Si el padre es una función → scope de función
       # if isinstance(ctx.parentCtx, compiladorParser.FuncionContext):
       #     print("Bloque de función (declarando parámetros)")
       #     self.tabla.push_context()
#
       #     argumentos_ctx = ctx.parentCtx.getChild(3)
       #     params = self.obtener_parametros(argumentos_ctx)
#
       #     for tipo, nombre in params:
       #         variable = Variable(nombre, tipo)
       #         self.tabla.declare_variable(variable)
       #         print(f"  -- Parametro declarado |{nombre}| de tipo |{tipo}|")
       # else:
       #     self.tabla.push_context()
#
       # self.indent += 1


    def exitBloque(self, ctx:compiladorParser.BloqueContext):
        if isinstance(ctx.parentCtx, compiladorParser.FuncionContext):
            nombre = ctx.parentCtx.getChild(1).getText()
            funcion = self.tabla.lookup(nombre)

            if funcion:
                funcion.scope = dict(self.tabla.ts[-1])  # 👈 CLAVE

        self.indent -= 1
        self.tabla.pop_context()


    # ---------- instrucciones ----------
    def enterInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        print("  " * self.indent + "Comienzan las instrucciones")

    def exitInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        print("  " * self.indent + "Terminan las instrucciones")
        # para depuración: muestra el texto de la subárbol (sin espacios)
        try:
            txt = ctx.getText()
        except Exception:
            txt = ''
        print("instrucciones EXIT -> |" + txt + "|")

    def enterIif(self, ctx:compiladorParser.IifContext):
        print("  " * self.indent + "Comienza if")
        self.indent += 1

    def exitIif(self, ctx:compiladorParser.IifContext):
        self.indent -= 1
        print("  " * self.indent + "Fin if")

    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print("  " * self.indent + "Comienza while")
        self.indent += 1

    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print("  " * self.indent + "Fin while")

    def enterIfor(self, ctx: compiladorParser.IforContext):
        self.indent += 1
        print("  " * self.indent + "Comienza for")

    def exitIfor(self, ctx: compiladorParser.IforContext):
        self.indent -= 1
        print("  " * self.indent + "Fin for")

    def enterPrototipo(self, ctx:compiladorParser.PrototipoContext):
        # prototipo: tipo ID PA argumentos PC PYC
        if ctx is None or ctx.getChildCount() < 6:
            return
        tipo = ctx.getChild(0).getText()
        id_nombre = ctx.getChild(1).getText()
        if tipo not in ('int', 'double'):
            print(f"  -- ERROR SEMANTICO: Tipo de dato |{tipo}| no reconocido")
            self.hay_error_semantico = True
            return
        # extraer parámetros
        argumentos_ctx = ctx.getChild(3)
        params = self.obtener_parametros(argumentos_ctx)
        funcion = Function(id_nombre, tipo, parameters=params)
        try:
            self.tabla.declare_function(funcion)
            print(f"  -- Se declaro prototipo |{id_nombre}| de tipo |{tipo}|")
        except KeyError:
            print(f"  -- ERROR SEMANTICO: El prototipo |{id_nombre}| ya fue declarado anteriormente")
            self.hay_error_semantico = True

    def obtener_parametros(self, ctx):
        params = []
        if ctx is None:
            return params
    
        def recorrer(nodo):
            if isinstance(nodo, compiladorParser.ParametroContext):
                tipo = nodo.tipo().getText()
                nombre = nodo.ID().getText()
                params.append((tipo, nombre))
            for i in range(nodo.getChildCount()):
                recorrer(nodo.getChild(i))
    
        recorrer(ctx)
        return params


    # ---------- funcion (definicion) ----------
    def enterFuncion(self, ctx:compiladorParser.FuncionContext):
        print("  " * self.indent + "Comienza función")
        self.indent += 1


    def exitFuncion(self, ctx:compiladorParser.FuncionContext):
        if ctx.getChildCount() < 4:
            print(ctx.getChildCount())
            print("  -- ERROR SEMANTICO: Función mal definida, falta tipo o nombre")
            self.hay_error_semantico = True
            return
        
        tipo = ctx.getChild(0).getText()
        nombre = ctx.getChild(1).getText()

        argumentos_ctx = ctx.getChild(3)
        params = self.obtener_parametros(argumentos_ctx)

        funcion = Function(nombre, tipo, parameters=params)

        try:
            self.tabla.declare_function(funcion)
            print(f"  -- Se declara función |{nombre}|")
        except KeyError:
            print(f"  -- ERROR SEMANTICO: La función |{nombre}| ya fue declarada")
            self.hay_error_semantico = True


    def exitLlamada(self, ctx: compiladorParser.LlamadaContext):
        nombre = ctx.ID().getText()

        # buscar función SOLO en global
        funcion = self.tabla.ts[0].get(nombre)

        if funcion is None:
            print(f"  -- ERROR SEMANTICO: La función |{nombre}| no está declarada")
            self.hay_error_semantico = True
            return

        args = []
        arg_ctx = ctx.argLlamada()

        if arg_ctx:
            args.append(arg_ctx.opal().getText())
            mas = arg_ctx.masArgLlamada()
            while mas and mas.opal():
                args.append(mas.opal().getText())
                mas = mas.masArgLlamada()

        if len(args) != len(funcion.parameters):
            print(
                f"  -- ERROR SEMANTICO: La función |{nombre}| espera "
                f"{len(funcion.parameters)} argumentos y se pasaron {len(args)}"
            )
            self.hay_error_semantico = True
            return

        print(f"  -- Llamada válida a |{nombre}|")


    def exitFactor(self, ctx: compiladorParser.FactorContext):
        if ctx.ID():
            nombre = ctx.ID().getText()

            symbol = self.tabla.lookup(nombre)
            if symbol is None:
                print(f"  -- ERROR SEMANTICO: La variable |{nombre}| no fue declarada")
                self.hay_error_semantico = True
            else:
                symbol.used = True

    def exitOpal(self, ctx: compiladorParser.OpalContext):
        if ctx.ID():
            nombre = ctx.ID().getText()

            symbol = self.tabla.lookup(nombre)
            if symbol is None:
                print(f"  -- ERROR SEMANTICO: La variable |{nombre}| no fue declarada")
                self.hay_error_semantico = True
            else:
                symbol.used = True




    # ---------- declaraciones ----------
    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        print("Declaracion ENTER -> |" + ctx.getText() + "|")

    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        tipo = ctx.getChild(0).getText()
        id_nombre = ctx.getChild(1).getText()
        if tipo not in ('int', 'double'):
            print(f"  -- ERROR SEMANTICO: Tipo de dato |{tipo}| no reconocido")
            self.hay_error_semantico = True
            return

        if self.tabla.exists_local(id_nombre):
            print(f"  -- ERROR SEMANTICO: La variable |{id_nombre}| ya fue declarada anteriormente")
            self.hay_error_semantico = True
        else:
            variable = Variable(id_nombre, tipo)
            try:
                self.tabla.declare_variable(variable)
                print(f"  -- Se declaro la variable |{id_nombre}| de tipo |{tipo}|")
            except KeyError as e:
                print("  -- ERROR:", e)
                self.hay_error_semantico = True
        self.declaracion += 1

        if ctx.listavar():
            self.procesamientoListaVar(ctx.listavar(), tipo)

    def procesamientoListaVar(self, ctx, tipo):
        if ctx is None:
            return
        if ctx.getChildCount() >= 2:
            id_nombre = ctx.getChild(1).getText()
            inicializado = False
            dato = None
            if ctx.getChildCount() > 2 and ctx.getChild(2).getText() == '=':
                inicializado = True
                dato = ctx.getChild(3).getText()

            if self.tabla.exists_local(id_nombre):
                print(f"  -- ERROR SEMANTICO: La variable |{id_nombre}| ya fue declarada anteriormente")
                self.hay_error_semantico = True
            else:
                variable = Variable(id_nombre, tipo)
                self.tabla.declare_variable(variable)
                print(f"  -- Se declaro la variable |{id_nombre}| de tipo |{tipo}|")

            if inicializado:
                variable.initialized = True
                variable.used = True
                print(f"  -- Se inicializa la variable |{id_nombre}| con el valor |{dato}|")

        if ctx.listavar():
            self.procesamientoListaVar(ctx.listavar(), tipo)

    # ---------- asignaciones ----------
    def enterAsignacion(self, ctx:compiladorParser.AsignacionContext):
        print("Asignacion ENTER -> |" + ctx.getText() + "|")

    def exitAsignacion(self, ctx:compiladorParser.AsignacionContext):
        print(">>> EXIT ASIGNACION EJECUTADO <<<")
        id_nombre = ctx.ID().getText()
        dato = ctx.getChild(2).getText()

        if not dato.isdigit():
            if dato.count('.') > 1:
                print(f"  -- ERROR SEMANTICO: El valor asignado a la variable |{id_nombre}| no es del tipo esperado")
                self.hay_error_semantico = True

        symbol = self.tabla.lookup(id_nombre)
        if symbol is None:
            print(f"  -- ERROR SEMANTICO: La variable |{id_nombre}| no fue declarada anteriormente")
            self.hay_error_semantico = True
            return

        if symbol.type == 'double' and "." not in dato:
            print(f"  -- ERROR SEMANTICO: Tipo de dato incompatible en la asignacion a la variable |{id_nombre}|")
            self.hay_error_semantico = True
            return
        if symbol.type == 'int' and "." in dato:
            print(f"  -- ERROR SEMANTICO: Tipo de dato incompatible en la asignacion a la variable |{id_nombre}|")
            self.hay_error_semantico = True
            return

        symbol.used = True
        symbol.initialized = True
        print(f"  -- Se asigna un valor a la variable |{id_nombre}|")


    # ---------- listavar ----------
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1

    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        print("  -- ListaVar(%d) Cant. hijos  = %d" % (self.profundidad, ctx.getChildCount()))
        self.profundidad -= 1

    # ---------- errors & counters ----------
    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR ")
        self.hay_error_semantico = True

    def enterEveryRule(self, ctx):
        self.numNodos += 1

    def __str__(self):
        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
               "Se visitaron " + str(self.numNodos) + " nodos"
    



