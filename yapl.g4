grammar yapl;

/* GRAMATICA */

program: (class SEMICOLON)+;

class: CLASS TYPE (INHERITS TYPE)? LBRACE (feature SEMICOLON)* RBRACE ;

feature: ID LPAR (formal (COMMA formal)*)? RPAR COLON TYPE LBRACE expr RBRACE
    | ID COLON TYPE (ASSIGN expr)? ;

formal: ID COLON TYPE;

expr: ID ASSIGN expr
    | expr (AT TYPE)? DOT ID LPAR (expr (COMMA expr)*)? RPAR
    | ID LPAR (expr (COMMA expr)*)? RPAR
    | IF expr THEN expr ELSE expr FI
    | WHILE expr LOOP expr POOL
    | LBRACE (expr SEMICOLON)+ RBRACE
    | LET ID COLON TYPE (ASSIGN expr)? (COMMA ID COLON TYPE (ASSIGN expr)?)* IN expr
    | NEW TYPE
    | ISVOID expr
    | expr PLUS expr
    | expr MINUS expr
    | expr TIMES expr
    | expr DIVIDE expr
    | DIAC expr
    | expr LT expr
    | expr LE expr
    | expr EQUALS expr
    | NOT expr
    | LPAR expr RPAR
    | ID
    | DIGIT
    | STRING
    | TRUE
    | FALSE;

/* REGLAS */

// ENTEROS
DIGIT: [0-9];
UPPERCASE: [A-Z];
LOWERCASE: [a-z];
LETTER: [a-zA-Z];

// Caracteres especiales
DOT: '.';
AT: '@';
DIAC: '~';
TIMES: '*';
DIVIDE: '/';
PLUS: '+';
MINUS: '-';
LT: '<';
LE: '<=';
EQUALS: '=';
ASSIGN: '<-';
LPAR: '(';
RPAR: ')';
COLON: ':';
SEMICOLON: ';';
LBRACE: '{';
RBRACE: '}';
COMMA: ',';
LSQUARE: '[';
RSQUARE: ']';

// Identificadores especiales
SELF: 'self';
SELF_TYPE: 'SELF_TYPE';

// Palabras reservadas
FALSE: 'false';
TRUE: 'true';
CLASS: [cC][lL][aA][sS][sS];
ELSE: [eE][lL][sS][eE];
FI: [fF][iI];
IF: [iI][fF];
IN: [iI][nN];
INHERITS: [iI][nN][hH][eE][rR][iI][tT][sS];
ISVOID: [iI][sS][vV][oO][iI][dD];
LOOP: [lL][oO][oO][pP];
POOL: [pP][oO][oO][lL];
THEN: [tT][hH][eE][nN];
WHILE: [wW][hH][iI][lL][eE];
NEW: [nN][eE][wW];
NOT: [nN][oO][tT];
LET: [lL][eE][tT];
TYPE: UPPERCASE (LETTER | DIGIT | '_')*;

ID: LOWERCASE (LETTER | DIGIT | '_')*;
STRING: '"' .*? '"';

// comentarios
COMMENT: '--' ~[\r\n]* -> skip;
CLOSED_COMMENT: '(*' .*? '*)' -> skip;
WHITESPACE: [ \t\r\n\f]+ -> skip;

ERROR: . ;