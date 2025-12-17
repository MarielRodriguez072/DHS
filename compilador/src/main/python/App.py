import os
import sys
from antlr4 import *
from compiladorLexer  import compiladorLexer
from compiladorParser import compiladorParser
from Escucha import Escucha
from Caminante import Caminante
import TablaSimbolos


#Ir a la carpera donde esta el archivo .g4 y ejecutar antlr4 -Dlanguage=Python3 -visitor compilador.g4 -o .

def main(argv):
    archivo = "input/prueba.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladorLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladorParser(stream)
    escucha = Escucha()
    parser.addParseListener(escucha)
    #tree = parser.bloque()
    tree = parser.programa()
    caminante = Caminante()
    parser.addParseListener(caminante)
    #print(escucha)
    print(caminante)
    #print(tree.toStringTree(recog=parser))
  
if __name__ == '__main__':
    main(sys.argv)