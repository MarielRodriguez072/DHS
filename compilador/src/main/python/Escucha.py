from compiladorParser import compiladorParser
from compiladorListener import compiladorListener


class Escucha (compiladorListener) :
    def enterPrograma(self, ctx:Parser.ProgramaContext) :
        print("Comienza el parsing")
        
    def exitPrograma(self, ctx:Parser.ProgramaContext) :
        print("Fin del parsing")
    
    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        self.declaracion +=1
        