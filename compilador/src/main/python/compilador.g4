grammar compilador;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

//generales
PA : '(' ;
PC : ')' ;
LLA : '{' ;
LLC : '}' ;
PYC : ';' ;
ASIG : '=' ;
COMA : ',' ;
OPERADORES : ('>'|'<'|'=='|'<='|'>='|'!='|'&&'|'||');
SUMA : '+';
RESTA : '-';
MULT : '*' ;
DIV : '/' ;
MOD : '%' ;
INC : '++';
DEC : '--' ;

FLOTANTE : DIGITO+ '.' DIGITO+ ;
NUMERO : DIGITO+ ;

//funciones y tipos de datos
INT : 'int' ;
DOUBLE : 'double' ;
IF : 'if' ;
ELSE : 'else' ;
FOR : 'for' ;
WHILE : 'while' ;
RETURN : 'return' ; 

//para los nombres de las variables
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

//simbolos de formato
WS : [ \n\r\t] -> skip ;

programa : instruccionesOpt EOF ;

instruccionesOpt : instrucciones
                 |
                 ;

instrucciones : instruccion instrucciones
              | instruccion
              ;

instruccion : asignacion
            | declaracion
            | iif
            | iwhile
            | ifor
            | bloque
            | prototipo
            | funcion
            | ireturn
            | llamada PYC
            ;

bloque : LLA instrucciones LLC ;

cuerpo : instruccionesOpt
       | bloque
       ;

ireturn : RETURN opal PYC 
        | RETURN llamada
        ;

incdec: INC ID 
      | ID INC
      | DEC ID 
      | ID DEC
      ;

iwhile : WHILE PA condicion PC cuerpo
       ;

iif : IF PA condicion PC cuerpo ielse
    ;

ielse: ELSE cuerpo
     |
     ;

incioFor: asignacion
         | declaracion
         |
         ;

condicionFor: condicion
            |
            ;

incrementoFor: incdec
              |
              ;

ifor : FOR PA incioFor PYC condicionFor PYC incrementoFor PC cuerpo
     ;

prototipo: tipo ID PA argumentos PC PYC;

argumentos : parametro masParametros
           |
           ;

masParametros : COMA parametro masParametros
               |
               ;

parametro : tipo ID ;

argLlamada : opal masArgLlamada 
           | 
           ;

masArgLlamada : COMA opal masArgLlamada 
               |
               ;

funcion: tipo ID PA argumentos PC bloque;

llamada : ID PA argLlamada PC ;

declaracion : tipo ID listavar PYC 
            | tipo ID ASIG opal listavar PYC
            | tipo ID ASIG exp PYC 
            | tipo ID ASIG exp listavar PYC
            ;

listavar : COMA ID listavar 
         | COMA ID ASIG opal listavar 
         | COMA ID inic 
         | COMA ID ASIG exp listavar
         | COMA ID ASIG opal 
         | COMA ID ASIG exp
         |
         ;

inic : ASIG opal
     |
     ;

tipo : INT
     | DOUBLE
     | FLOTANTE
     ;

asignacion : ID ASIG exp PYC
           ;

opal : NUMERO
     | FLOTANTE
     | ID
     ;
     
comp : ID OPERADORES opal;

exp : term e;

e : SUMA term e
  | RESTA term e
  |
  ;

expresion : exp PYC ; 

term : factor t ;

t : MULT factor t 
  | DIV factor t
  | MOD factor t
  |
  ;

factor : NUMERO
       | FLOTANTE
       | ID
       | llamada
       | PA exp PC
       ;

condicion: opal
           | comp
           |
           ;
