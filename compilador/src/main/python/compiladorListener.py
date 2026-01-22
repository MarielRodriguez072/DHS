# Generated from /home/faq/Documentos/iua/dhs/DHS/compilador/src/main/python/compilador.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .compiladorParser import compiladorParser
else:
    from compiladorParser import compiladorParser

# This class defines a complete listener for a parse tree produced by compiladorParser.
class compiladorListener(ParseTreeListener):

    # Enter a parse tree produced by compiladorParser#programa.
    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        pass

    # Exit a parse tree produced by compiladorParser#programa.
    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
        pass


    # Enter a parse tree produced by compiladorParser#instruccionesOpt.
    def enterInstruccionesOpt(self, ctx:compiladorParser.InstruccionesOptContext):
        pass

    # Exit a parse tree produced by compiladorParser#instruccionesOpt.
    def exitInstruccionesOpt(self, ctx:compiladorParser.InstruccionesOptContext):
        pass


    # Enter a parse tree produced by compiladorParser#instrucciones.
    def enterInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        pass

    # Exit a parse tree produced by compiladorParser#instrucciones.
    def exitInstrucciones(self, ctx:compiladorParser.InstruccionesContext):
        pass


    # Enter a parse tree produced by compiladorParser#instruccion.
    def enterInstruccion(self, ctx:compiladorParser.InstruccionContext):
        pass

    # Exit a parse tree produced by compiladorParser#instruccion.
    def exitInstruccion(self, ctx:compiladorParser.InstruccionContext):
        pass


    # Enter a parse tree produced by compiladorParser#bloque.
    def enterBloque(self, ctx:compiladorParser.BloqueContext):
        pass

    # Exit a parse tree produced by compiladorParser#bloque.
    def exitBloque(self, ctx:compiladorParser.BloqueContext):
        pass


    # Enter a parse tree produced by compiladorParser#cuerpo.
    def enterCuerpo(self, ctx:compiladorParser.CuerpoContext):
        pass

    # Exit a parse tree produced by compiladorParser#cuerpo.
    def exitCuerpo(self, ctx:compiladorParser.CuerpoContext):
        pass


    # Enter a parse tree produced by compiladorParser#ireturn.
    def enterIreturn(self, ctx:compiladorParser.IreturnContext):
        pass

    # Exit a parse tree produced by compiladorParser#ireturn.
    def exitIreturn(self, ctx:compiladorParser.IreturnContext):
        pass


    # Enter a parse tree produced by compiladorParser#incdec.
    def enterIncdec(self, ctx:compiladorParser.IncdecContext):
        pass

    # Exit a parse tree produced by compiladorParser#incdec.
    def exitIncdec(self, ctx:compiladorParser.IncdecContext):
        pass


    # Enter a parse tree produced by compiladorParser#iwhile.
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        pass

    # Exit a parse tree produced by compiladorParser#iwhile.
    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        pass


    # Enter a parse tree produced by compiladorParser#iif.
    def enterIif(self, ctx:compiladorParser.IifContext):
        pass

    # Exit a parse tree produced by compiladorParser#iif.
    def exitIif(self, ctx:compiladorParser.IifContext):
        pass


    # Enter a parse tree produced by compiladorParser#ielse.
    def enterIelse(self, ctx:compiladorParser.IelseContext):
        pass

    # Exit a parse tree produced by compiladorParser#ielse.
    def exitIelse(self, ctx:compiladorParser.IelseContext):
        pass


    # Enter a parse tree produced by compiladorParser#incioFor.
    def enterIncioFor(self, ctx:compiladorParser.IncioForContext):
        pass

    # Exit a parse tree produced by compiladorParser#incioFor.
    def exitIncioFor(self, ctx:compiladorParser.IncioForContext):
        pass


    # Enter a parse tree produced by compiladorParser#declaracionFor.
    def enterDeclaracionFor(self, ctx:compiladorParser.DeclaracionForContext):
        pass

    # Exit a parse tree produced by compiladorParser#declaracionFor.
    def exitDeclaracionFor(self, ctx:compiladorParser.DeclaracionForContext):
        pass


    # Enter a parse tree produced by compiladorParser#asignacionFor.
    def enterAsignacionFor(self, ctx:compiladorParser.AsignacionForContext):
        pass

    # Exit a parse tree produced by compiladorParser#asignacionFor.
    def exitAsignacionFor(self, ctx:compiladorParser.AsignacionForContext):
        pass


    # Enter a parse tree produced by compiladorParser#condicionFor.
    def enterCondicionFor(self, ctx:compiladorParser.CondicionForContext):
        pass

    # Exit a parse tree produced by compiladorParser#condicionFor.
    def exitCondicionFor(self, ctx:compiladorParser.CondicionForContext):
        pass


    # Enter a parse tree produced by compiladorParser#incrementoFor.
    def enterIncrementoFor(self, ctx:compiladorParser.IncrementoForContext):
        pass

    # Exit a parse tree produced by compiladorParser#incrementoFor.
    def exitIncrementoFor(self, ctx:compiladorParser.IncrementoForContext):
        pass


    # Enter a parse tree produced by compiladorParser#ifor.
    def enterIfor(self, ctx:compiladorParser.IforContext):
        pass

    # Exit a parse tree produced by compiladorParser#ifor.
    def exitIfor(self, ctx:compiladorParser.IforContext):
        pass


    # Enter a parse tree produced by compiladorParser#prototipo.
    def enterPrototipo(self, ctx:compiladorParser.PrototipoContext):
        pass

    # Exit a parse tree produced by compiladorParser#prototipo.
    def exitPrototipo(self, ctx:compiladorParser.PrototipoContext):
        pass


    # Enter a parse tree produced by compiladorParser#argumentos.
    def enterArgumentos(self, ctx:compiladorParser.ArgumentosContext):
        pass

    # Exit a parse tree produced by compiladorParser#argumentos.
    def exitArgumentos(self, ctx:compiladorParser.ArgumentosContext):
        pass


    # Enter a parse tree produced by compiladorParser#masParametros.
    def enterMasParametros(self, ctx:compiladorParser.MasParametrosContext):
        pass

    # Exit a parse tree produced by compiladorParser#masParametros.
    def exitMasParametros(self, ctx:compiladorParser.MasParametrosContext):
        pass


    # Enter a parse tree produced by compiladorParser#parametro.
    def enterParametro(self, ctx:compiladorParser.ParametroContext):
        pass

    # Exit a parse tree produced by compiladorParser#parametro.
    def exitParametro(self, ctx:compiladorParser.ParametroContext):
        pass


    # Enter a parse tree produced by compiladorParser#argLlamada.
    def enterArgLlamada(self, ctx:compiladorParser.ArgLlamadaContext):
        pass

    # Exit a parse tree produced by compiladorParser#argLlamada.
    def exitArgLlamada(self, ctx:compiladorParser.ArgLlamadaContext):
        pass


    # Enter a parse tree produced by compiladorParser#masArgLlamada.
    def enterMasArgLlamada(self, ctx:compiladorParser.MasArgLlamadaContext):
        pass

    # Exit a parse tree produced by compiladorParser#masArgLlamada.
    def exitMasArgLlamada(self, ctx:compiladorParser.MasArgLlamadaContext):
        pass


    # Enter a parse tree produced by compiladorParser#funcion.
    def enterFuncion(self, ctx:compiladorParser.FuncionContext):
        pass

    # Exit a parse tree produced by compiladorParser#funcion.
    def exitFuncion(self, ctx:compiladorParser.FuncionContext):
        pass


    # Enter a parse tree produced by compiladorParser#llamada.
    def enterLlamada(self, ctx:compiladorParser.LlamadaContext):
        pass

    # Exit a parse tree produced by compiladorParser#llamada.
    def exitLlamada(self, ctx:compiladorParser.LlamadaContext):
        pass


    # Enter a parse tree produced by compiladorParser#declaracion.
    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        pass

    # Exit a parse tree produced by compiladorParser#declaracion.
    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        pass


    # Enter a parse tree produced by compiladorParser#listavar.
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        pass

    # Exit a parse tree produced by compiladorParser#listavar.
    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        pass


    # Enter a parse tree produced by compiladorParser#inic.
    def enterInic(self, ctx:compiladorParser.InicContext):
        pass

    # Exit a parse tree produced by compiladorParser#inic.
    def exitInic(self, ctx:compiladorParser.InicContext):
        pass


    # Enter a parse tree produced by compiladorParser#tipo.
    def enterTipo(self, ctx:compiladorParser.TipoContext):
        pass

    # Exit a parse tree produced by compiladorParser#tipo.
    def exitTipo(self, ctx:compiladorParser.TipoContext):
        pass


    # Enter a parse tree produced by compiladorParser#asignacion.
    def enterAsignacion(self, ctx:compiladorParser.AsignacionContext):
        pass

    # Exit a parse tree produced by compiladorParser#asignacion.
    def exitAsignacion(self, ctx:compiladorParser.AsignacionContext):
        pass


    # Enter a parse tree produced by compiladorParser#opal.
    def enterOpal(self, ctx:compiladorParser.OpalContext):
        pass

    # Exit a parse tree produced by compiladorParser#opal.
    def exitOpal(self, ctx:compiladorParser.OpalContext):
        pass


    # Enter a parse tree produced by compiladorParser#comp.
    def enterComp(self, ctx:compiladorParser.CompContext):
        pass

    # Exit a parse tree produced by compiladorParser#comp.
    def exitComp(self, ctx:compiladorParser.CompContext):
        pass


    # Enter a parse tree produced by compiladorParser#exp.
    def enterExp(self, ctx:compiladorParser.ExpContext):
        pass

    # Exit a parse tree produced by compiladorParser#exp.
    def exitExp(self, ctx:compiladorParser.ExpContext):
        pass


    # Enter a parse tree produced by compiladorParser#e.
    def enterE(self, ctx:compiladorParser.EContext):
        pass

    # Exit a parse tree produced by compiladorParser#e.
    def exitE(self, ctx:compiladorParser.EContext):
        pass


    # Enter a parse tree produced by compiladorParser#term.
    def enterTerm(self, ctx:compiladorParser.TermContext):
        pass

    # Exit a parse tree produced by compiladorParser#term.
    def exitTerm(self, ctx:compiladorParser.TermContext):
        pass


    # Enter a parse tree produced by compiladorParser#t.
    def enterT(self, ctx:compiladorParser.TContext):
        pass

    # Exit a parse tree produced by compiladorParser#t.
    def exitT(self, ctx:compiladorParser.TContext):
        pass


    # Enter a parse tree produced by compiladorParser#factor.
    def enterFactor(self, ctx:compiladorParser.FactorContext):
        pass

    # Exit a parse tree produced by compiladorParser#factor.
    def exitFactor(self, ctx:compiladorParser.FactorContext):
        pass


    # Enter a parse tree produced by compiladorParser#condicion.
    def enterCondicion(self, ctx:compiladorParser.CondicionContext):
        pass

    # Exit a parse tree produced by compiladorParser#condicion.
    def exitCondicion(self, ctx:compiladorParser.CondicionContext):
        pass



del compiladorParser