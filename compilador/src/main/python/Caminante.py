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
        
        self.visit(ctx.getChild(4))  # Visitar el bloque dentro del while
        
        self.c3d.agregar_instruccion(f"goto {L1}")
        
        self.c3d.agregar_instruccion(f"{L2}:")
        return None

    def visitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        nombre = ctx.getChild(1).getText()
        self.c3d.agregar_instruccion(f"{nombre} = 0")
        return None

    def visitListaVar (self, ctx:compiladorParser.ListavarContext):
        print("Listavar procesada")
        return self.visitChildren(ctx)

    def visitAsignacion (self, ctx:compiladorParser.AsignacionContext):
        var = ctx.getChild(0).getText()
        valor = ctx.getChild(2).getText()
        self.c3d.agregar_instruccion(f"{var} = {valor}")
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