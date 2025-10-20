class TablaSimbolos:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
           cls._instance = super(TablaSimbolos, cls).__new__(cls)
        return cls._instance
    
    ts = [dict()]
    
    # cada vez que se mete a un bloque se debe crear un contexto
    def addContex(self):
        self.ts.append(dict())
    
    # cada vez que se sale del bloque se debe borrar el ULTIMO un contexto
    def removeContex(self):
        self.ts.pop()
        
    # Mete la variable en el ultimo diccionario
    # dict('key':'value')
    # [... , {'nomID' : ID }]
    def addVariable(self, id):
        self.ts[-1][id.name] = id
    
    # Buscar a partir de una Key si esta se encuentra en algun contexto
    # buscamos la key = 'a'
    # context [{'c':c},{ 'a':a , 'b':b },{}]
    # la key 'a' esta en el la pos 1 ( ts[1])
    # la funcion nos deberia retornar True 
    def buscarPorKey(self,key):
        #print(f'TS -> {self.ts}')
        #print(f'TS -> key:{key}')
        for context in self.ts:
            if key in context:
                return True
        return False
    
    # Devolver la ID en base a una Key
    def returnKey(self,key):
        for context in self.ts:
            if key in context:
                return context[key]
        return False


class Id:
    # Una ID debe tener un nombre y un tipo
    # name -> identificador
    # type -> tipo de ID
    def __init__(self,name, type):
        self.name = name
        self.type = type
        self.initialized = False
        self.used = False
        self.varFunc = "variable" 
        
    def toString(self):
        return f'(name->{self.name},type->{self.type},init->{self.initialized},used->{self.used},varFun->{self.varFunc})'
    


class Variable(Id):
    pass

class Function(Id):
    
    # Una fucion debe recibir un nombre, tipo y parametros
    # name -> nombre de la funcion
    # type -> tipo de funcion
    # parameters -> ARREGLO con VARIABLES que acepta la funcion
    def __init__(self, name, type, parameters):
        super().__init__(name, type)
        self.parameters = parameters
        self.varFunc = "function"
    
        