# errores.py
from antlr4.error.ErrorListener import ErrorListener

class SintacticErrorListener(ErrorListener):
    def __init__(self):
        self.hay_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.hay_error = True
        print(f"ERROR SINTACTICO (linea {line}:{column}): {msg}")
