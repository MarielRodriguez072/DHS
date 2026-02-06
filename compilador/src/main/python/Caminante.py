from antlr4 import TerminalNode
from compiladorVisitor import compiladorVisitor
from compiladorParser import compiladorParser
from CodigoTresDirecciones import CodigoTresDirecciones

class Caminante (compiladorVisitor) :
    instr = 0
    hojas = 0

    def __init__(self):
        self.c3d = CodigoTresDirecciones()
        self.temp = 0
        self.tiene_return = False

    def nuevo_temp(self):
        t = f"t{self.temp}"
        self.temp += 1
        return t

    def visitPrograma (self, ctx:compiladorParser.ProgramaContext):
        self.visitChildren(ctx)
        self.c3d.escribir_codigo()
        return None
    
    def visitInstruccion(self, ctx:compiladorParser.InstruccionContext):
        return self.visit(ctx.getChild(0))


    def visitInstrucciones (self, ctx:compiladorParser.InstruccionesContext):
        return self.visitChildren(ctx)
    
    def visitIif(self, ctx):
        L_true = self.c3d.nuevo_label()
        L_fin  = self.c3d.nuevo_label()
    
        if ctx.ielse():
            # IF CON ELSE
            L_else = self.c3d.nuevo_label()
    
            self.generar_condicion(ctx.condicion(), L_true, L_else)
    
            self.c3d.agregar_instruccion(f"{L_true}:")
            self.visit(ctx.instruccion())
            self.c3d.agregar_instruccion(f"goto {L_fin}")
    
            self.c3d.agregar_instruccion(f"{L_else}:")
            self.visit(ctx.ielse().instruccion())
    
            self.c3d.agregar_instruccion(f"{L_fin}:")
        else:
            # IF SIN ELSE
            self.generar_condicion(ctx.condicion(), L_true, L_fin)
    
            self.c3d.agregar_instruccion(f"{L_true}:")
            self.visit(ctx.instruccion())
    
            self.c3d.agregar_instruccion(f"{L_fin}:")



    def gen_and(self, ctx, L_true, L_false):
        L_next = self.c3d.nuevo_label()

        self.gen_atom(ctx.cond_atom(), L_next, L_false)
        self.c3d.agregar_instruccion(f"{L_next}:")

        if ctx.cond_and_p():
            self.gen_and_p(ctx.cond_and_p(), L_true, L_false)
        else:
            self.c3d.agregar_instruccion(f"goto {L_true}")


    def gen_and_p(self, ctx, L_true, L_false):

        if ctx is None or ctx.getChildCount() == 0:
            self.c3d.agregar_instruccion(f"goto {L_true}")
            return

        L_next = self.c3d.nuevo_label()
        self.gen_atom(ctx.cond_atom(), L_next, L_false)
        self.c3d.agregar_instruccion(f"{L_next}:")

        self.gen_and_p(ctx.cond_and_p(), L_true, L_false)


    def gen_or(self, ctx, L_true, L_false):
        L_next = self.c3d.nuevo_label()

        self.gen_and(ctx.cond_and(), L_true, L_next)
        self.c3d.agregar_instruccion(f"{L_next}:")

        self.gen_or_p(ctx.cond_or_p(), L_true, L_false)



    def gen_or_p(self, ctx, L_true, L_false):

        if ctx is None or ctx.getChildCount() == 0:
            self.c3d.agregar_instruccion(f"goto {L_false}")
            return

        self.gen_and(ctx.cond_and(), L_true, L_false)



    def gen_atom(self, ctx, L_true, L_false):

        if ctx is None:
            return

        # ( condicion )
        if ctx.condicion():
            self.generar_condicion(ctx.condicion(), L_true, L_false)
            return

        # comparación: ID op opal
        if ctx.comp():
            comp = ctx.comp()

            izq = comp.getChild(0).getText() #ID
            op  = comp.getChild(1).getText() # <,>,!=,==
            der = comp.getChild(2).getText() # opal

            t = self.c3d.nuevo_temp()
            self.c3d.agregar_instruccion(f"{t} = {izq} {op} {der}")
            self.c3d.agregar_instruccion(f"ifFalse {t} goto {L_false}")
            return

        # valor booleano / expresión simple
        if ctx.opal():
            val = ctx.opal().getText()
            self.c3d.agregar_instruccion(f"ifFalse {val} goto {L_false}")
            return

        raise Exception(f"cond_atom inválido: {ctx.getText()}")



    def gen_comp(self, ctx, L_true, L_false):
        izq = ctx.ID().getText()
        op  = ctx.OPERADORES().getText()
        der = self.procesar_opal(ctx.opal())

        t = self.c3d.nuevo_temp()
        self.c3d.agregar_instruccion(f"{t} = {izq} {op} {der}")
        self.c3d.agregar_instruccion(f"ifFalse {t} goto {L_false}")
        self.c3d.agregar_instruccion(f"goto {L_true}")



    def generar_condicion(self, ctx, L_true, L_false):
        self.gen_or(ctx.cond_or(), L_true, L_false)


    def visitPrototipo (self, ctx:compiladorParser.PrototipoContext):
        print("Prototipo procesado")
        return self.visitChildren(ctx)

    def visitIwhile(self, ctx):
        L_inicio = self.c3d.nuevo_label()
        L_true   = self.c3d.nuevo_label()
        L_fin    = self.c3d.nuevo_label()

        # inicio del loop
        self.c3d.agregar_instruccion(f"{L_inicio}:")

        # condición con && || !=
        self.generar_condicion(ctx.condicion(), L_true, L_fin)

        # cuerpo
        self.c3d.agregar_instruccion(f"{L_true}:")
        self.visit(ctx.instruccion())

        # volver a evaluar
        self.c3d.agregar_instruccion(f"goto {L_inicio}")
        self.c3d.agregar_instruccion(f"{L_fin}:")

    
    def visitIfor(self, ctx):
        #inicialización
        if ctx.incioFor():
            self.visit(ctx.incioFor())

        L_inicio = self.c3d.nuevo_label()
        L_true   = self.c3d.nuevo_label()
        L_fin    = self.c3d.nuevo_label()

        self.c3d.agregar_instruccion(f"{L_inicio}:")

        #condición
        if ctx.condicionFor():
            self.generar_condicion(ctx.condicionFor().getChild(0), L_true, L_fin)
        else:
            # for(;;) → siempre verdadero
            self.c3d.agregar_instruccion(f"goto {L_true}")

        #cuerpo
        self.c3d.agregar_instruccion(f"{L_true}:")
        self.visit(ctx.instruccion())

        # incremento
        if ctx.incrementoFor():
            self.visit(ctx.incrementoFor())

        #volver
        self.c3d.agregar_instruccion(f"goto {L_inicio}")
        self.c3d.agregar_instruccion(f"{L_fin}:")


    def visitIncdec(self, ctx):
        # ++a o a++
        if ctx.INC():
            nombre = ctx.ID().getText()
            t = self.c3d.nuevo_temp()
            self.c3d.operacion(t, nombre, '+', '1')
            self.c3d.asignacion(nombre, t)
            return None

        # --a o a--
        if ctx.DEC():
            nombre = ctx.ID().getText()
            t = self.c3d.nuevo_temp()
            self.c3d.operacion(t, nombre, '-', '1')
            self.c3d.asignacion(nombre, t)
            return None


    def visitIncrementoFor(self, ctx):
        return self.visitChildren(ctx)

    def visitAsignacionFor(self, ctx):
        nombre = ctx.ID().getText()
        temp = self.procesar_expresion(ctx.exp())
        self.c3d.asignacion(nombre, temp)
        return None

    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()

        # inicialización
        self.c3d.agregar_instruccion(f"{nombre} = 0")

        # asignación si existe
        if ctx.ASIG():
            valor_ctx = ctx.opal() or ctx.exp()
            temp = self.procesar_expresion(valor_ctx)
            self.c3d.asignacion(nombre, temp)

        # procesar lista inmediatamente
        if ctx.listavar():
            self.procesar_listavar(ctx.listavar())

        return None



    def procesar_listavar(self, ctx):
        if ctx is None or ctx.getChildCount() == 0:
            return

        nombre = ctx.ID().getText()

        self.c3d.agregar_instruccion(f"{nombre} = 0")

        if ctx.ASIG():
            valor_ctx = ctx.opal() or ctx.exp()
            temp = self.procesar_expresion(valor_ctx)
            self.c3d.asignacion(nombre, temp)

        if ctx.listavar():
            self.procesar_listavar(ctx.listavar())



    def visitListaVar(self, ctx: compiladorParser.ListavarContext):
        for i in range(ctx.getChildCount()):
            hijo = ctx.getChild(i)

            # buscamos IDs explícitos
            if isinstance(hijo, TerminalNode) and hijo.getSymbol().type == compiladorParser.ID:
                nombre = hijo.getText()
                self.c3d.agregar_instruccion(f"{nombre} = 0")

            # asignaciones explícitas
            if isinstance(hijo, compiladorParser.ExpContext) or isinstance(hijo, compiladorParser.OpalContext):
                nombre = ctx.getChild(i - 2).getText()
                temp = self.procesar_expresion(hijo)
                self.c3d.asignacion(nombre, temp)

        return None



    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()
        temp = self.procesar_expresion(ctx.exp())
        self.c3d.asignacion(nombre, temp)
        return None

    def visitBloque(self, ctx):
        return self.visitChildren(ctx)

    def visitTerminal(self, node):
        # print(node.getText())
        self.hojas += 1
        return super().visitTerminal(node)
    

    def visitFuncion(self, ctx: compiladorParser.FuncionContext):
        nombre = ctx.ID().getText()

        self.tiene_return = False

        # etiqueta de la función
        self.c3d.agregar_instruccion(f"{nombre}:")

        # cuerpo de la función
        self.visit(ctx.bloque())

        # return agregado automáticamente si no se encuentra un return explícito
        if not self.tiene_return:
            self.c3d.agregar_instruccion("return")
    
        return None
    
    
    def visitIreturn(self, ctx):
        self.tiene_return = True
        if ctx.opal():
            valor = ctx.opal().getText()
            self.c3d.retorno(valor)
        else:
            temp = self.visit(ctx.llamada())
            self.c3d.retorno(temp)
        return None

    def visitLlamada(self, ctx):
        nombre = ctx.ID().getText()

        args = []
        if ctx.argLlamada():
            args = self.obtener_argumentos(ctx.argLlamada())

        return self.c3d.llamada_funcion(nombre, args)

    def obtener_argumentos(self, ctx):
        args = []

        # primer argumento
        if ctx.opal():
            args.append(ctx.opal().getText())

        # siguientes
        mas = ctx.masArgLlamada()
        while mas and mas.getChildCount() > 0:
            args.append(mas.opal().getText())
            mas = mas.masArgLlamada()

        return args



    def printNumeroHojas (self) :
        print("Hojas " + str(self.hojas))

    def visitEveryRule(self, ctx):
        
        return self.visitChildren(ctx)
    

    def procesar_expresion(self, ctx):
        #print(">> procesar_expresion:", type(ctx).__name__, ctx.getText())

        if isinstance(ctx, compiladorParser.FactorContext):
            # llamada a función
            if isinstance(ctx.getChild(0), compiladorParser.LlamadaContext):
                return self.visit(ctx.getChild(0))

            if ctx.getChildCount() == 1:
                return ctx.getChild(0).getText()

            return self.procesar_expresion(ctx.getChild(1))

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
        if ctx is None or ctx.getChildCount() == 0:
            return izq

        operador = ctx.getChild(0).getText()
        der = self.procesar_expresion(ctx.getChild(1))

        temp = self.c3d.nuevo_temp()
        self.c3d.operacion(temp, izq, operador, der)

        return self.procesar_e(ctx.getChild(2), temp)

    def procesar_t(self, ctx, izq):
        if ctx is None or ctx.getChildCount() == 0:
            return izq

        operador = ctx.getChild(0).getText()
        der = self.procesar_expresion(ctx.getChild(1))

        temp = self.c3d.nuevo_temp()
        self.c3d.operacion(temp, izq, operador, der)

        return self.procesar_t(ctx.getChild(2), temp)
    

    def visitDeclaracionFor(self, ctx: compiladorParser.DeclaracionForContext):
        nombre = ctx.ID().getText()

        # hijo 3 = exp u opal
        valor_ctx = ctx.getChild(3)

        temp = self.procesar_expresion(valor_ctx)
        self.c3d.asignacion(nombre, temp)

        return None

    def procesar_condicion(self, ctx):
        # opal
        if isinstance(ctx, compiladorParser.OpalContext):
            return ctx.getText()

        # comp
        if isinstance(ctx, compiladorParser.CompContext):
            izq = ctx.ID().getText()
            operador = ctx.OPERADORES().getText()
            der = ctx.opal().getText()

            temp = self.c3d.nuevo_temp()
            self.c3d.operacion(temp, izq, operador, der)
            return temp

        if ctx.getChildCount() == 1:
            return self.procesar_condicion(ctx.getChild(0))

        raise Exception(f"Condición no reconocida: {ctx.getText()}")
    