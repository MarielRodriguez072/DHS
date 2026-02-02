import os
import sys
from antlr4 import *
from compiladorLexer  import compiladorLexer
from compiladorParser import compiladorParser
#from Escucha import Escucha
from Caminante import Caminante
import TablaSimbolos
from Optimizacion import Optimizacion

#Ir a la carpera donde esta el archivo .g4 y ejecutar antlr4 -Dlanguage=Python3 -visitor compilador.g4 -o .

def main(argv):
    archivo = "input/prueba.txt"
    if len(argv) > 1:
        archivo = argv[1]

    input_stream = FileStream(archivo, encoding="utf-8")
    lexer = compiladorLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = compiladorParser(tokens)

    tree = parser.programa()

    caminante = Caminante()
    caminante.visit(tree)

    print("Codigo intermedio generado en codigo_intermedio.txt")

    opt = Optimizacion("codigo_intermedio.txt", "codigo_optimizado.txt")


if __name__ == '__main__':
    main(sys.argv)