program ::= class_list

class_list ::= class_declaration class_list
    | class_declaration

class_declaration ::= class_type '{' feature_list '}'

class_type ::= TYPE

feature_list ::= feature ';' feature_list
    | feature ';'

feature ::= attribute
    | method

attribute ::= object_identifier ':' TYPE [<- expression]

method ::= object_identifier '(' formal_list ')' ':' TYPE '{' expression '}'

formal_list ::= formal ',' formal_list
    | formal

formal ::= object_identifier ':' TYPE

expression ::= if_expression
    | while_expression
    | let_expression
    | case_expression
    | new_expression
    | isvoid_expression
    | assignment_expression
    | dispatch_expression
    | binary_expression
    | unary_expression
    | object_identifier
    | integer_literal
    | string_literal
    | true
    | false
    | '(' expression ')'