from compiladorVisitor import compiladorVisitor
from compiladorParser import compiladorParser
from CodigoTresDirecciones import CodigoTresDirecciones

class Caminante (compiladorVisitor) :
    instr = 0
    hojas = 0

    def __init__(self):
        self.c3d = CodigoTresDirecciones()
        self.temp = 0

    def nuevo_temp(self):
        t = f"t{self.temp}"
        self.temp += 1
        return t

    def visitPrograma (self, ctx:compiladorParser.ProgramaContext):
        self.visitChildren(ctx)
        self.c3d.escribir_codigo()
        return None
    
    def visitInstruccion(self, ctx:compiladorParser.InstruccionContext):
        self.instr += 1
        print("Instruccion " + str(self.instr))
        print("\t" + ctx.getText())
        return self.visitChildren(ctx)


    def visitInstrucciones (self, ctx:compiladorParser.InstruccionesContext):
        print("Instruccion procesada")
        return self.visitChildren(ctx)
    

    def visitIif (self, ctx:compiladorParser.IifContext):
        print("If procesado")
        return self.visitChildren(ctx)
    

    def visitPrototipo (self, ctx:compiladorParser.PrototipoContext):
        print("Prototipo procesado")
        return self.visitChildren(ctx)


    def visitIwhile(self, ctx:compiladorParser.IwhileContext):
        L1 = f"L{self.c3d.label_count}"
        self.c3d.label_count += 1
        L2 = f"L{self.c3d.label_count}"
        self.c3d.label_count += 1

        cond = ctx.getChild(2).getText()

        self.c3d.agregar_instruccion(f"{L1}:")
        self.c3d.agregar_instruccion(f"if not {cond} goto {L2}")
        
        self.visit(ctx.getChild(4))
        
        self.c3d.agregar_instruccion(f"goto {L1}")
        
        self.c3d.agregar_instruccion(f"{L2}:")
        return None
    
    def visitIfor(self, ctx: compiladorParser.IforContext):

        # 1. inicialización
        if ctx.incioFor():
            self.visit(ctx.incioFor())

        L0 = self.c3d.nuevo_label()
        L1 = self.c3d.nuevo_label()

        self.c3d.agregar_instruccion(f"{L0}:")

        # 2. condición
        if ctx.condicionFor():
            cond_ctx = ctx.condicionFor().getChild(0)
            cond_temp = self.procesar_condicion(cond_ctx)
            self.c3d.agregar_instruccion(f"ifFalse {cond_temp} goto {L1}")

        # 3. CUERPO
        cuerpo = ctx.cuerpo()
        if cuerpo:
            self.visit(cuerpo)

        # 4. incremento
        if ctx.incrementoFor():
            self.visit(ctx.incrementoFor())

        # 5. loop
        self.c3d.agregar_instruccion(f"goto {L0}")
        self.c3d.agregar_instruccion(f"{L1}:")



    def visitIncrementoFor(self, ctx):
        return self.visitChildren(ctx)

    def visitAsignacionFor(self, ctx):
        nombre = ctx.ID().getText()
        temp = self.procesar_expresion(ctx.exp())
        self.c3d.asignacion(nombre, temp)
        return None


    def visitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        nombre = ctx.getChild(1).getText()
        self.c3d.agregar_instruccion(f"{nombre} = 0")
        return None

    def visitListaVar (self, ctx:compiladorParser.ListavarContext):
        print("Listavar procesada")
        return self.visitChildren(ctx)

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()
        temp = self.procesar_expresion(ctx.exp())
        self.c3d.asignacion(nombre, temp)
        return None

    def visitBloque (self, ctx:compiladorParser.BloqueContext):
        print("bloque procesado")
        return self.visitChildren(ctx)
    
    def visitTerminal(self, node):
        # print(node.getText())
        self.hojas += 1
        return super().visitTerminal(node)
    
    def printNumeroHojas (self) :
        print("Hojas " + str(self.hojas))

    def visitEveryRule(self, ctx):
        
        return self.visitChildren(ctx)
    

    def procesar_expresion(self, ctx):
        print(">> procesar_expresion:", type(ctx).__name__, ctx.getText())
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

