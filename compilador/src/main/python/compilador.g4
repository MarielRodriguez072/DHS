grammar compilador;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

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

INT : 'int' ;
DOUBLE : 'double' ;
IF : 'if' ;
ELSE : 'else' ;
FOR : 'for' ;
WHILE : 'while' ;
INCDEC : ('++'| '--' );

ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

WS : [ \n\r\t] -> skip ;
OTRO : . ;

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
            | bloque
            | ifor
            ;

bloque : LLA instrucciones LLC ; 

incremento: INCDEC ID | ID INCDEC;

iwhile : WHILE PA comp PC instruccion ;

iif : IF opal PC instruccion ielse;

ielse: ELSE instruccion
     |
     ;

ifor : FOR PA asignacion comp PYC incremento PC instruccion ;
//int suma(int a, int b);
prototipo: tipo ID PA tipo ID listavar PC PYC;


funcion: tipo ID PA tipo ID listavar PC bloque PYC
       | tipo ID PA PC bloque PYC
       ;

declaracion : tipo ID listavar PYC 
            | tipo ID ASIG opal listavar PYC
            ;

listavar : COMA ID listavar
         | COMA ID ASIG opal listavar
         | COMA ID inic 
         ;

inic : ASIG opal
     |
     ;

tipo : INT
     | DOUBLE
     ;

asignacion : ID ASIG opal PYC ;

opal : NUMERO
     | ID
     ;
     
comp : ID OPERADORES opal;

exp : term e;

e : SUMA term e
  | RESTA term e
  |
  ;

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
//cambio para subir al git 
