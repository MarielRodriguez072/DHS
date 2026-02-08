import os
import sys
from antlr4 import *
from compiladorLexer  import compiladorLexer
from compiladorParser import compiladorParser
from Escucha import Escucha
from Caminante import Caminante
import TablaSimbolos
from Optimizacion import Optimizacion
from errores import SintacticErrorListener

#Ir a la carpera donde esta el archivo .g4 y ejecutar antlr4 -Dlanguage=Python3 -visitor compilador.g4 -o .

def main(argv):
    archivo = "input/prueba.txt"
    if len(argv) > 1:
        archivo = argv[1]

    input_stream = FileStream(archivo, encoding="utf-8")
    lexer = compiladorLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = compiladorParser(tokens)

    lexer.removeErrorListeners()
    parser.removeErrorListeners()

    sintactic_listener = SintacticErrorListener()
    parser.addErrorListener(sintactic_listener)

    sintactic_listener = SintacticErrorListener()
    parser.addErrorListener(sintactic_listener)

    escucha = Escucha()
    
    parser.addParseListener(escucha)
    

    tree = parser.programa()

    if sintactic_listener.hay_error:
        print("Se encontraron errores sintacticos. No se puede continuar con la generacion de codigo intermedio.")
        return
    
    if escucha.hay_error_semantico:
        print("Se encontraron errores semanticos. No se puede continuar con la generacion de codigo intermedio.")
        return
    
    print(escucha)

    caminante = Caminante()
    caminante.visit(tree)

    print("Codigo intermedio generado en codigo_intermedio.txt")
    print("SUPEREXCELENTE🔪🔪🔪🎯")

    opt = Optimizacion("codigo_intermedio.txt", "codigo_optimizado.txt")


if __name__ == '__main__':
    main(sys.argv)