from antlr4 import TerminalNode
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
import TablaSimbolos

class Escucha (compiladorListener) :
    indent = 1
    declaracion = 0
    profundidad = 0
    numNodos = 0
    asignacion =0
       
    tabla = TablaSimbolos.TablaSimbolos()

    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Comienza el parsing")

    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Termina el parsing")
        tabla = TablaSimbolos.TablaSimbolos()
        
        with open("tabla.txt", "w", encoding='utf-8') as f:
            print("Exportando tabla de simbolos a archivo tabla.txt")
            f.write("TABLA DE SIMBOLOS COMPLETA:\n\n")
            tabla.exportarTabla(f)

        for context in self.tabla.ts:
            for key, value in context.items():
                print(f"  {key} : {value.type}, inicializado: {value.initialized}, usado: {value.used}, varFunc: {value.varFunc}")
                if not value.used:
                    print(f"  -- WARNING SEMANTICO: La variable |{key}| fue declarada pero nunca usada")
        
        
    def enterInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        print("  "*self.indent + "Comienzan las instrucciones")
        
    def exitInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        print("  "*self.indent + "Terminan las instrucciones")
        print("instrucciones EXIT -> |" + ctx.getText() + "|")
        

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

    def enterFuncion(self, ctx:compiladorParser.FuncionContext):
        print("Entrando a funcion \n")
    
    def exitFuncion(self, ctx:compiladorParser.FuncionContext):
        tipo = ctx.getChild(0).getText()
    
        id_nombre = ctx.getChild(1).getText()

        funcion = TablaSimbolos.Id(id_nombre, tipo)

        if(tipo != 'int' and tipo != 'double'):
            print("  -- ERROR SEMANTICO: Tipo de dato |%s| no reconocido" % tipo)
            return

        if self.tabla.buscarPorKey(id_nombre) is not False:
            print("  -- ERROR SEMANTICO: La funcion |%s| ya fue declarada anteriormente" % id_nombre)
        else:
            self.tabla.addFunction(funcion)
            print("  -- Se declaro la funcion |%s| de tipo |%s|" % (id_nombre, tipo))
        self.declaracion += 1
    
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print("  "*self.indent + "Comienza while")
        self.indent += 1
        
    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print("  "*self.indent + "Fin while")

    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        
        print("Declaracion ENTER -> |" + ctx.getText() + "|")
    
    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        tipo = ctx.getChild(0).getText()
    
        id_nombre = ctx.getChild(1).getText()

        variable = TablaSimbolos.Id(id_nombre, tipo)

        if(tipo != 'int' and tipo != 'double'):
            print("  -- ERROR SEMANTICO: Tipo de dato |%s| no reconocido" % tipo)
            return

        #print("buscar por key "+str(self.tabla.buscarPorKey(id_nombre)))
        # TODO revisar si la variable ya fue declarada en la tabla de simbolos
        if self.tabla.buscarPorKey(id_nombre) is not False:
            print("  -- ERROR SEMANTICO: La variable |%s| ya fue declarada anteriormente" % id_nombre)
        else:
            self.tabla.addVariable(variable)
            print("  -- Se declaro la variable |%s| de tipo |%s|" % (id_nombre, tipo))
        self.declaracion += 1
        
        if ctx.listavar():
            self.procesamientoListaVar(ctx.listavar(),tipo)
        if ctx.getChildCount() == 6:
            dato = ctx.getChild(3).getText()
            #self.validar_asignacion(id_nombre, dato, tipo)
    
    def procesamientoListaVar(self, ctx, tipo):
        if ctx is None:
            return
        #Esto en teoria debería tomar la parte que le sigue a la lista de variables
        #osea ver los hijos ", y =  numero"
        if ctx.getChildCount() >=2:
            id_nombre = ctx.getChild(1).getText()
            inicializado = False
            dato = None
            if ctx.getChildCount() > 2 and ctx.getChild(2).getText() == '=':
                inicializado = True
                dato = ctx.getChild(3).getText()
                
            variable = TablaSimbolos.Id(id_nombre, tipo)
            
            if self.tabla.buscarPorKey(id_nombre) is not False:
                print("  -- ERROR SEMANTICO: La variable |%s| ya fue declarada anteriormente" % id_nombre)
            else:
                self.tabla.addVariable(variable)
                print("  -- Se declaro la variable |%s| de tipo |%s|" % (id_nombre, tipo))
            
            if inicializado:
                print("  -- Se inicializa la variable |%s| con el valor |%s|" % (id_nombre, dato))
                variable.initialized = True
                variable.used = True
                print(f"  -- La variable |{id_nombre}| ahora esta inicializada")
                
        #Recursividad para seguir procesando la lista
        if ctx.listavar():
            self.procesamientoListaVar(ctx.listavar(), tipo)
        
        #para una declaración y una asignacion debemos usar la misma logica en el caso de los errores 
        # Dentro de la declaración puedo hacer asignaciones y es en la asignacion donde vamos a
        #ver si el tipo de dato es incomptible int x=i;
    def enterAsignacion(self, ctx:compiladorParser.AsignacionContext):
        print("Asignacion ENTER -> |" + ctx.getText() + "|")
    
    def exitAsignacion(self, ctx:compiladorParser.AsignacionContext):
        
        print("Estoy en asignacion viendo cosas...")

        id_nombre = ctx.getChild(0).getText()
        dato = ctx.getChild(2).getText()

        if not dato.isdigit():
            if dato.count('.') > 1:
                print("  -- ERROR SEMANTICO: El valor asignado a la variable |%s| no es del tipo esperado" % id_nombre)
         
        if(self.tabla.buscarPorKey(id_nombre) is False):
            print("  -- ERROR SEMANTICO: La variable |%s| no fue declarada anteriormente" % id_nombre)

        for context in self.tabla.ts:
            for key, value in context.items():
                if key == id_nombre:
                    if value.type == 'double' and "." not in dato:
                        print("  -- ERROR SEMANTICO: Tipo de dato incompatible en la asignacion a la variable |%s|" % id_nombre)
                        return
                    elif value.type == 'int' and "." in dato:
                        print("  -- ERROR SEMANTICO: Tipo de dato incompatible en la asignacion a la variable |%s|" % id_nombre)
                        return

                    print(f"  -- Se asigna un valor a la variable |{key}|")
                    value.used = True
                    value.initialized = True
                    print(f"  -- La variable |{key}| ahora esta inicializada")
        
    
    def enterBloque(self, ctx:compiladorParser.BloqueContext):
        '''-> {'''
        self.tabla.addContex()
        print("Nuevo bloque. \n")
    '''
    def exitBloque(self, ctx:compiladorParser.BloqueContext):
       
        #print(str(self.tabla.ts)+"\n")
        self.tabla.removeContex()
        print("Fin de bloque" +"\n")
   '''
    
    def exitBloque(self, ctx):
        if len(self.tabla.ts) > 1:
            self.tabla.removeContex()
        print("Fin de bloque")


    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1

    
    # TODO revisar if y los ctx
    
    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        print("  -- ListaVar(%d) Cant. hijos  = %d" % (self.profundidad, ctx.getChildCount()))
        self.profundidad -= 1 

    # def visitTerminal(self, node: TerminalNode):
    #     print(" ---> Token: " + node.getText())
        # self.numTokens += 1
    
    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR ")
        
        
    def enterEveryRule(self, ctx):
        self.numNodos += 1
    
    def __str__(self):

        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
                "Se visitaron " + str(self.numNodos) + " nodos"
