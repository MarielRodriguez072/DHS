# Escucha.py
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from TablaSimbolos import TablaSimbolos, Id, Variable, Function
import os
from datetime import datetime
from CodigoTresDirecciones import CodigoTresDirecciones as C3D

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
        self.c3d = C3D()

    def dbg_contexts(self, msg=""):
        print("\n--- CONTEXTOS", msg, "---")
        for i, ctx in enumerate(self.tabla.ts):
            print(f"  [{i}] -> {list(ctx.keys())}")
        print("-------------------------\n")

    def procesar_expresion(self, ctx):
        print(">> procesar_expresion:", type(ctx).__name__, ctx.getText())
        # NUMERO | FLOTANTE | ID
        if isinstance(ctx, compiladorParser.OpalContext):
            if ctx.getChildCount() == 1:
                return ctx.getChild(0).getText()
            return self.procesar_expresion(ctx.getChild(0))

        # exp : term e
        if isinstance(ctx, compiladorParser.ExpContext):
            izq = self.procesar_expresion(ctx.getChild(0))
            return self.procesar_e(ctx.getChild(1), izq)

        # term : factor t
        if isinstance(ctx, compiladorParser.TermContext):
            izq = self.procesar_expresion(ctx.getChild(0))
            return self.procesar_t(ctx.getChild(1), izq)

        # factor
        if isinstance(ctx, compiladorParser.FactorContext):
            if ctx.getChildCount() == 1:
                return ctx.getChild(0).getText()
            return self.procesar_expresion(ctx.getChild(1))  # ( exp )

        return ctx.getText()
    
    def procesar_e(self, ctx, izq):
        if ctx.getChildCount() == 0:
            return izq

        operador = ctx.getChild(0).getText()
        der = self.procesar_expresion(ctx.getChild(1))

        temp = self.c3d.nuevo_temp()
        self.c3d.operacion(temp, izq, operador, der)

        return self.procesar_e(ctx.getChild(2), temp)

    def procesar_t(self, ctx, izq):
        if ctx.getChildCount() == 0:
            return izq

        operador = ctx.getChild(0).getText()
        der = self.procesar_expresion(ctx.getChild(1))

        temp = self.c3d.nuevo_temp()
        self.c3d.operacion(temp, izq, operador, der)

        return self.procesar_t(ctx.getChild(2), temp)


    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
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
            for i, contexto in enumerate(self.tabla.ts):
                f.write(f"CONTEXTO {i}:\n")
                self.tabla.exportar_contexto(f, contexto)


        # mensajes semánticos
        for context in self.tabla.ts:
            for key, value in context.items():
                if not value.used and getattr(value, 'varFunc', None) != "function":
                    print(f"  -- WARNING SEMANTICO: La variable |{key}| fue declarada pero nunca usada")
        # resumen
        print(self)
        print("\n--- CÓDIGO DE TRES DIRECCIONES ---")
        print("Cantidad de instrucciones:", len(self.c3d.codigo))
        print(self.c3d.obtener_codigo())
        self.c3d.escribir_codigo()


    # ---------- bloques ----------
    def enterBloque(self, ctx:compiladorParser.BloqueContext):
        # siempre que entremos a un bloque con { ... } abrimos contexto
        self.tabla.push_context()
        print("Nuevo bloque.")
        self.indent += 1 

    def exitBloque(self, ctx:compiladorParser.BloqueContext):
        self.indent -= 1
        self.ctx += 1
        archivo = "prueba.txt"
        tablaFile = os.path.join(os.path.dirname(archivo), "tablaSimbolos.txt")
        with open(tablaFile, 'a', encoding='utf-8') as f:
            self.tabla.exportarTabla(f,self.ctx)
            f.write(f"\n")

        self.tabla.pop_context()
        print("Fin de bloque")

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

        self.label_fin = self.c3d.nuevo_label()

        cond_temp = self.procesar_expresion(ctx)
        self.c3d.agregar_instruccion(f"ifFalse{cond_temp} goto {self.label_fin}")


    def exitIif(self, ctx:compiladorParser.IifContext):
        self.indent -= 1
        print("  " * self.indent + "Fin if")
        self.c3d.agregar_instruccion(f"{self.label_fin}:")

    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print("  " * self.indent + "Comienza while")
        self.indent += 1

        self.label_inicio = self.c3d.nuevo_label()
        self.label_fin = self.c3d.nuevo_label()
        self.c3d.agregar_instruccion(f"{self.label_inicio}:")
        cond_temp = self.procesar_expresion(ctx)
        self.c3d.agregar_instruccion(f"ifFalse {cond_temp} goto {self.label_fin}")

    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print("  " * self.indent + "Fin while")

        self.c3d.agregar_instruccion(f"goto {self.label_inicio}")
        self.c3d.agregar_instruccion(f"{self.label_fin}:")

    def enterIfor(self, ctx:compiladorParser.IforContext):
        self.label_inicio = self.c3d.nuevo_label()
        self.label_fin = self.c3d.nuevo_label()

        cond_ctx = ctx.condicionFor()

        if cond_ctx is None or cond_ctx.getChildCount() == 0:
            raise Exception("ERROR: condición vacía en for/while")


        self.c3d.agregar_instruccion(f"{self.label_inicio}:")

        # condición
        cond = self.procesar_expresion(ctx)
        self.c3d.agregar_instruccion(
            f"ifFalse {cond} goto {self.label_fin}"
        )

    def exitIfor(self, ctx:compiladorParser.IforContext):
        self.c3d.agregar_instruccion(f"goto {self.label_inicio}")
        self.c3d.agregar_instruccion(f"{self.label_fin}:")


    def enterPrototipo(self, ctx:compiladorParser.PrototipoContext):
        # prototipo: tipo ID PA argumentos PC PYC
        if ctx is None or ctx.getChildCount() < 6:
            return
        tipo = ctx.getChild(0).getText()
        id_nombre = ctx.getChild(1).getText()
        if tipo not in ('int', 'double'):
            print(f"  -- ERROR SEMANTICO: Tipo de dato |{tipo}| no reconocido")
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

    def obtener_parametros(self, argumentos_ctx):
        params = []
        if argumentos_ctx is None:
            return params

        for i in range(argumentos_ctx.getChildCount()):
            hijo = argumentos_ctx.getChild(i)

            if isinstance(hijo, compiladorParser.ParametroContext):
                tipo = hijo.getChild(0).getText()
                nombre = hijo.getChild(1).getText()
                params.append((tipo, nombre))
            else:
                # recorrer hijos internos
                for j in range(hijo.getChildCount()):
                    sub = hijo.getChild(j)
                    if isinstance(sub, compiladorParser.ParametroContext):
                        tipo = sub.getChild(0).getText()
                        nombre = sub.getChild(1).getText()
                        params.append((tipo, nombre))

        return params


    # ---------- funcion (definicion) ----------
    def enterFuncion(self, ctx:compiladorParser.FuncionContext):
        #abrir contexto local para la función
        if self.tabla is None:
            self.tabla = TablaSimbolos()
        self.tabla.push_context()
        print("Entrando a funcion")
        self.indent += 1

        #extraer parámetros y declararlos como variables en el contexto local
        #argumentos está en child index 3 (tipo ID PA argumentos PC bloque)
        try:
            argumentos_ctx = ctx.getChild(3)
        except Exception:
            argumentos_ctx = None
        params = self.obtener_parametros(argumentos_ctx)
        for tipo, nombre in params:
            variable = Variable(nombre, tipo)
            try:
                self.tabla.declare_variable(variable)
                print(f"  -- Parametro declarado |{nombre}| de tipo |{tipo}|")
            except KeyError:
                print(f"  -- ERROR SEMANTICO: Parametro |{nombre}| ya declarado en la función")

    def exitFuncion(self, ctx:compiladorParser.FuncionContext):
        #antes de cerrar contexto, copiamos el scope local para adjuntar a la Function
        local_ctx = None
        if len(self.tabla.ts) >= 1:
            local_ctx = dict(self.tabla.ts[-1])  # copia del contexto local

        #cerramos contexto local
        self.indent -= 1
        self.tabla.pop_context()

        # ahora registramos la función en el global (o actualizamos prototipo exist.)
        # verificamos que ctx tenga hijos válidos
        if ctx is None or ctx.getChildCount() < 6:
            print("WARNING: FuncionContext inválido (se ignora)")
            return

        tipo = ctx.getChild(0).getText()
        nombre = ctx.getChild(1).getText()

        argumentos_ctx = ctx.getChild(3)
        params = self.obtener_parametros(argumentos_ctx)

        funcion = Function(nombre, tipo, parameters=params)
        funcion.scope = local_ctx

        try:
            self.tabla.declare_function(funcion)
            print(f"  -- Se declaro la funcion |{nombre}| de tipo |{tipo}|")
        except KeyError:
            #si ya existía prototipo, actualizamos el objeto
            existing = self.tabla.lookup(nombre)
            if existing and getattr(existing, 'varFunc', None) == "function":
                existing.scope = local_ctx
                existing.parameters = params or existing.parameters
                print(f"  -- Se completó la definición de la funcion |{nombre}| (prototipo previo actualizado)")
            else:
                print(f"  -- ERROR SEMANTICO: La funcion |{nombre}| ya fue declarada anteriormente")

        self.declaracion += 1

    # ---------- declaraciones ----------
    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        print("Declaracion ENTER -> |" + ctx.getText() + "|")

    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        tipo = ctx.getChild(0).getText()
        id_nombre = ctx.getChild(1).getText()
        if tipo not in ('int', 'double'):
            print(f"  -- ERROR SEMANTICO: Tipo de dato |{tipo}| no reconocido")
            return

        if self.tabla.exists(id_nombre):
            print(f"  -- ERROR SEMANTICO: La variable |{id_nombre}| ya fue declarada anteriormente")
        else:
            variable = Variable(id_nombre, tipo)
            try:
                self.tabla.declare_variable(variable)
                print(f"  -- Se declaro la variable |{id_nombre}| de tipo |{tipo}|")
            except KeyError as e:
                print("  -- ERROR:", e)
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

            if self.tabla.exists(id_nombre):
                print(f"  -- ERROR SEMANTICO: La variable |{id_nombre}| ya fue declarada anteriormente")
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

        symbol = self.tabla.lookup(id_nombre)
        if symbol is None:
            print(f"  -- ERROR SEMANTICO: La variable |{id_nombre}| no fue declarada anteriormente")
            return

        if symbol.type == 'double' and "." not in dato:
            print(f"  -- ERROR SEMANTICO: Tipo de dato incompatible en la asignacion a la variable |{id_nombre}|")
            return
        if symbol.type == 'int' and "." in dato:
            print(f"  -- ERROR SEMANTICO: Tipo de dato incompatible en la asignacion a la variable |{id_nombre}|")
            return

        symbol.used = True
        symbol.initialized = True
        print(f"  -- Se asigna un valor a la variable |{id_nombre}|")

        # generar código 3 direcciones de la expresión        
        resultado = self.procesar_expresion(ctx.exp())

        self.c3d.asignacion(id_nombre, resultado)

    # ---------- listavar ----------
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1

    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        print("  -- ListaVar(%d) Cant. hijos  = %d" % (self.profundidad, ctx.getChildCount()))
        self.profundidad -= 1

    # ---------- errors & counters ----------
    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR ")

    def enterEveryRule(self, ctx):
        self.numNodos += 1

    def __str__(self):
        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
               "Se visitaron " + str(self.numNodos) + " nodos"

