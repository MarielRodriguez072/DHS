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

NUMERO : DIGITO+ ;

//funciones y tipos de datos
INT : 'int' ;
DOUBLE : 'double' ;
IF : 'if' ;
ELSE : 'else' ;
FOR : 'for' ;
WHILE : 'while' ;
INCDEC : ('++'| '--' );
RETURN : 'return' ; 

//para los nombres de las variables
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

//simbolos de formato
WS : [ \n\r\t] -> skip ;
OTRO : . ;

//lo dejo por las dudas
// s : ID     {print("ID ->" + $ID.text + "<--") }         s
//   | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
//   | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
//   | EOF
//   ;

// s : PA s PC s
//   |
//   ;

programa : instrucciones EOF ;

instrucciones : instruccion instrucciones
              |
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
            ;

bloque : LLA instrucciones LLC ; 

ireturn : RETURN opal PYC ;

incremento: INCDEC ID | ID INCDEC;

iwhile : WHILE PA comp PC instruccion | bloque
       | WHILE PA opal PC instruccion | bloque
       ;

iif : IF PA opal PC instrucciones ielse
    | IF PA comp PC instrucciones ielse
    | IF PA opal PC bloque ielse
    | IF PA comp PC instrucciones //por si no viene un else
    | IF PA opal PC instrucciones //por si no viene un else
    ;

ielse: ELSE instruccion //puede venir una instrucicion que es un bloque 
     |
     ;

ifor : FOR PA asignacion comp PYC incremento PC instruccion ;

//int suma(int a, int b);
prototipo: tipo ID PA tipo ID argumentos PC PYC;
argumentos : COMA ID argumentos
           | COMA tipo ID
           | tipo ID argumentos
           | 
           ;

funcion: tipo ID PA argumentos PC LLA instrucciones ireturn PYC LLC
       | tipo ID PA argumentos PC bloque PYC
       ;

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
         ;

inic : ASIG opal
     |
     ;

tipo : INT
     | DOUBLE
     ;

asignacion : ID ASIG opal PYC 
           | ID ASIG exp PYC
           ;

opal : NUMERO
     | ID
     | exp
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
       | ID
       | funcion
       | PA exp PC
       ;

