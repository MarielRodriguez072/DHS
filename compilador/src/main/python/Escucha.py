from antlr4 import TerminalNode
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from TablaSimbolos import *

class Escucha (compiladorListener) :
    indent = 1
    declaracion = 0
    profundidad = 0
    numNodos = 0
    
    tabla = TablaSimbolos()
    
    prueba = open("input/prueba.txt","r")

    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Comienza el parsing")

    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Termina el parsing")
        

    def enterInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        print("  "*self.indent + "Comienzan las instrucciones")
        
    def exitInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        print("  "*self.indent + "Terminan las instrucciones")
        for context in self.tabla.ts:
            for key, value in context.items():
                print(f"  {key} : {value.type}, inicializado: {value.initialized}, usado: {value.used}, varFunc: {value.varFunc}")
                if not value.used:
                    print(f"  -- WARNING SEMANTICO: La variable |{key}| fue declarada pero nunca usada")


    def enterIif(self, ctx:compiladorParser.IifContext):
        print("  "*self.indent + "Comienza if")
        print("Entramos al if")
        self.indent += 1
        
    def exitIif(self, ctx:compiladorParser.IifContext):
        self.indent -= 1
        print("  "*self.indent + "Fin if")
        
    def enterPrototipo(self, ctx:compiladorParser.PrototipoContext):
        print("  "*self.indent + "Comienza prototipo")
        self.indent += 1
    
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print("  "*self.indent + "Comienza while")
        self.indent += 1
        
    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print("  "*self.indent + "Fin while")

    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        
        print("Declaracion ENTER -> |" + ctx.getText() + "|")
        print("  -- Cant. hijos = " + str(ctx.getChildCount()))
    
    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        tipo = ctx.getChild(0).getText()
    
        id_nombre = ctx.getChild(1).getText()

        variable = Id(id_nombre, tipo)

        print("buscar por key "+str(self.tabla.buscarPorKey(id_nombre)))
        
        if self.tabla.buscarPorKey(id_nombre) is not False:
            print("  -- ERROR SEMANTICO: La variable |%s| ya fue declarada anteriormente" % id_nombre)
        else:
            self.tabla.addVariable(variable)
            print("  -- Se declaro la variable |%s| de tipo |%s|" % (id_nombre, tipo))
        self.declaracion += 1
        
        #para una declaración y una asignacion debemos usar la misma logica en el caso de los errores 
        # Dentro de la declaración puedo hacer asignaciones y es en la asignacion donde vamos a
        #ver si el tipo de dato es incomptible int x=i;
    def enterAsignacion(self, ctx:compiladorParser.AsignacionContext):
        print("Asignacion ENTER -> |" + ctx.getText() + "|")
        
    def exitAsignacion(self, ctx:compiladorParser.AsignacionContext):
        
        print("asignacion")

        id_nombre = ctx.getChild(0).getText()

        if(self.tabla.buscarPorKey(id_nombre) is False):
            print("  -- ERROR SEMANTICO: La variable |%s| no fue declarada anteriormente" % id_nombre)

        if(ctx.getChildCount() == 4): #caso de asignacion con declaracion
            if(ctx.getChild(0).getText() == 'int' or ctx.getChild(0).getText() == 'doble' and ctx.getChild(2).getText().isdigit()):
                print("  -- Asignacion correcta")
                
            else:
                print("  -- ERROR SEMANTICO: Tipo de dato incompatible en la asignacion")
        else:
            #aca tengo que buscar en mi tabla de simbolos la variable id_nombre y ver su tipo para ver que la asignacion sea correcta
            id_nombre = ctx.getChild(0).getText()

        for context in self.tabla.ts:
            for key, value in context.items():
                if key == id_nombre:
                    print(f"  -- Se asigna un valor a la variable |{key}|")
                    value.used = True
                    print(f"  -- La variable |{key}| ahora esta inicializada")
        
            
    def enterBloque(self, ctx:compiladorParser.BloqueContext):
        '''-> {'''
        self.tabla.addContex()
        print("Nuevo bloque. Tabla de simbolos actual:\n"+ str(self.tabla.ts)+"\n")
        
    def exitBloque(self, ctx:compiladorParser.BloqueContext):
        '''-> }'''
        print(str(self.tabla.ts)+"\n")
        self.tabla.removeContex()
        print("Fin de bloque. Tabla de simbolos actual:\n"+ str(self.tabla.ts)+"\n")
   
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1

    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        print("  -- ListaVar(%d) Cant. hijos  = %d" % (self.profundidad, ctx.getChildCount()))
        self.profundidad -= 1
        if ctx.getChildCount() == 4 :
            print("      hoja ID --> |%s|" % ctx.getChild(1).getText())

    # def visitTerminal(self, node: TerminalNode):
    #     print(" ---> Token: " + node.getText())
        # self.numTokens += 1
    
    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR")
        
    def enterEveryRule(self, ctx):
        self.numNodos += 1
    
    def __str__(self):
    
        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
                "Se visitaron " + str(self.numNodos) + " nodos"
                
    prueba.close()