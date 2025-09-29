// Generated from compilador.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link compiladorParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface compiladorVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link compiladorParser#programa}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrograma(compiladorParser.ProgramaContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#instrucciones}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInstrucciones(compiladorParser.InstruccionesContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#instruccion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInstruccion(compiladorParser.InstruccionContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#bloque}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBloque(compiladorParser.BloqueContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#ireturn}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIreturn(compiladorParser.IreturnContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#incremento}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIncremento(compiladorParser.IncrementoContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#iwhile}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIwhile(compiladorParser.IwhileContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#iif}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIif(compiladorParser.IifContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#ielse}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIelse(compiladorParser.IelseContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#ifor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIfor(compiladorParser.IforContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#prototipo}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrototipo(compiladorParser.PrototipoContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#argumentos}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgumentos(compiladorParser.ArgumentosContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#argLlamada}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgLlamada(compiladorParser.ArgLlamadaContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#funcion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncion(compiladorParser.FuncionContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#llamada}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLlamada(compiladorParser.LlamadaContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#declaracion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDeclaracion(compiladorParser.DeclaracionContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#listavar}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitListavar(compiladorParser.ListavarContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#inic}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInic(compiladorParser.InicContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#tipo}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTipo(compiladorParser.TipoContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#asignacion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAsignacion(compiladorParser.AsignacionContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#opal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOpal(compiladorParser.OpalContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#comp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComp(compiladorParser.CompContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#exp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExp(compiladorParser.ExpContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#e}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitE(compiladorParser.EContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#expresion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpresion(compiladorParser.ExpresionContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#term}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerm(compiladorParser.TermContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#t}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT(compiladorParser.TContext ctx);
	/**
	 * Visit a parse tree produced by {@link compiladorParser#factor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFactor(compiladorParser.FactorContext ctx);
}