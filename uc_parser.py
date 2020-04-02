# import the lex class
from uc_lex import UCLexer
# import the yacc lib
from ply.yacc import yacc
# get the tokens list
tokens = UCLexer.tokens


class UCParser():
    '''
        A parser for the uC language.
    '''
    def __init__(self, error_function):
        # get the tokens list
        self.tokens = UCLexer.tokens
        # create lexer object
        self.lexer = UCLexer(error_function)


    def build(self):
        '''
        Builds the parser from the specification. Must be
        called after the parser object is created.
        '''
        self.parser = yacc(module=self,)


    def p_program(self, p):
        '''
            program : global_declaration_list
        '''

        p[0] = p[1]


    def p_global_declaration_1(self, p):
        '''
            global_declaration : function_definition
        '''
        p[0] = p[1]


    def p_global_declaration_2(self, p):
        '''
            global_declaration : declaration
        '''
        p[0] = p[1]


    def p_global_declaration_list(self, p):
        '''
            global_declaration_list : global_declaration
                                    | global_declaration_list global_declaration
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]


    def p_function_definition(self, p):
        '''
            function_definition : type_specifier_opt declarator declaration_list compound_statement
        '''
        pass


    def p_type_specifier(self, p):
        '''
            type_specifier : VOID
                           | CHAR
                           | INT
                           | FLOAT
        '''
        p[0] = p[1]


    def p_type_specifier_opt(self, p):
        '''
            type_specifier_opt : empty
                               | type_specifier
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = None


    def p_empty(self, p):
        '''
            empty :
        '''
        p[0] = None


    #TODO
    def p_declarator(self, p):
        '''
            declarator : pointer_opt direct_declarator
        '''
        pass


    def p_pointer(self, p):
        '''
            pointer : pointer_opt   %prec PTIMES
        '''
        pass


    def p_pointer_opt(self, p):
        '''
            pointer_opt : TIMES empty
                        | TIMES pointer 
                        
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = None


    #TODO
    def p_direct_declarator(self, p):
        '''
            direct_declarator : LPAREN declarator RPAREN
                              | direct_declarator LBRACKET constant_expression_opt RBRACKET
                              | direct_declarator LPAREN parameter_list RPAREN
                              | direct_declarator LPAREN identifier_list RPAREN
        '''
        pass

    def p_direct_declarator_01(self, p):
        '''
            direct_declarator : identifier
        '''


    def p_identifier(self, p):
        '''
            identifier : ID
        '''
        p[0] = ('ID', p[1])


    def p_identifier_list(self, p):
        '''
            identifier_list : identifier
                            | identifier_list identifier
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[3])


    def p_constant_expression(self, p):
        '''
            constant_expression : binary_expression
        '''
        p[0] = p[1]


    def p_constant_expression_opt(self, p):
        '''
            constant_expression_opt : empty
                                    | constant_expression
        '''
        if len(p) == 2:
            p[0] = p[1]


    def p_binary_expression(self, p):
        '''
            binary_expression : cast_expression
                              | binary_expression  TIMES   binary_expression
                              | binary_expression  DIVIDE  binary_expression
                              | binary_expression  MOD     binary_expression
                              | binary_expression  PLUS    binary_expression
                              | binary_expression  MINUS   binary_expression
                              | binary_expression  LT      binary_expression
                              | binary_expression  LE      binary_expression
                              | binary_expression  GT      binary_expression
                              | binary_expression  GE      binary_expression
                              | binary_expression  EQ      binary_expression
                              | binary_expression  NE      binary_expression
                              | binary_expression  AND     binary_expression
                              | binary_expression  OR      binary_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[2], p[1], p[3])


    def p_cast_expression(self, p):
        '''
            cast_expression : unary_expression
                            | LPAREN type_specifier RPAREN cast_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[2], p[4])


    #TODO
    def p_unary_expression(self, p):
        '''
            unary_expression : postfix_expression
                             | PLUSPLUS unary_expression %prec UPLUSPLUS
                             | MINUSMINUS unary_expression %prec UMINUSMINUS
                             | unary_operator cast_expression
        '''
        pass


    #TODO
    def p_postfix_expression(self, p):
        '''
            postfix_expression : primary_expression
                               | postfix_expression LBRACKET expression RBRACKET
                               | postfix_expression LPAREN argument_expression_opt RPAREN
                               | postfix_expression PLUSPLUS
                               | postfix_expression MINUSMINUS
        '''
        pass


    def p_primary_expression(self, p):
        '''
            primary_expression : ID
                               | constant
                               | LPAREN expression RPAREN
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]


    def p_constant(self, p):
        '''
            constant : INT_CONST
                     | STRING_LITERAL
                     | FLOAT_CONST
        '''
        p[0] = p[1]


    #TODO
    def p_expression(self, p):
        '''
            expression : assignment_expression
                       | expression COMMA assignment_expression
        '''
        pass


    def p_expression_list(self, p):
        '''
            expression_list : expression
                            | expression_list expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[2])


    def p_expression_opt(self, p):
        '''
            expression_opt : empty
                           | expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = None


    #TODO
    def p_argument_expression(self, p):
        '''
            argument_expression : assignment_expression
                                | argument_expression COMMA assignment_expression
        '''
        pass


    def p_argument_expression_opt(self, p):
        '''
            argument_expression_opt : empty
                                    | argument_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = None


    #TODO
    def p_assignment_expression(self, p):
        '''
            assignment_expression : binary_expression
                                  | unary_expression assignment_operator assignment_expression
        '''
        pass


    def p_assignment_operator(self, p):
        '''
            assignment_operator : EQUALS
                                | TIMESEQUAL
                                | DIVIDEEQUAL
                                | MODEQUAL
                                | PLUSEQUAL
                                | MINUSEQUAL
        '''
        if p[1] == "=":
            p[0] = p[2]
        else:
            p[0] = (p[1], p[3], p[4])


    def p_unary_operator(self, p):
        '''
            unary_operator : ADDRESS    %prec UADDRESS
                           | TIMES      %prec UTIMES
                           | PLUS       %prec UPLUS
                           | MINUS      %prec UMINUS
                           | NOT        %prec UNOT
        '''
        p[0] = p[1]


    #TODO
    def p_parameter_list(self, p):
        '''
            parameter_list : parameter_declaration
                           | parameter_list COMMA parameter_declaration
        '''
        pass


    def p_parameter_declaration(self, p):
        '''
            parameter_declaration : type_specifier declarator
        '''
        p[0] = (p[1], p[2])


    #TODO
    def p_declaration(self, p):
        '''
            declaration :  type_specifier init_declarator_list_opt SEMI
        '''
        pass


    def p_declaration_list(self, p):
        '''
            declaration_list : declaration
                             | declaration_list declaration
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[2])


    def p_init_declarator_list(self, p):
        '''
            init_declarator_list : init_declarator
                                 | init_declarator_list COMMA init_declarator
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[2])


    def p_init_declarator_list_opt(self, p):
        '''
            init_declarator_list_opt : empty
                                     | init_declarator_list
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = None


    def p_init_declarator(self, p):
        '''
            init_declarator : declarator
                            | declarator EQUALS initializer
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2])

   
    #TODO
    def p_initializer(self, p):
        '''
            initializer : assignment_expression
                        | LBRACE initializer_list RBRACE
                        | LBRACE initializer_list COMMA RBRACE
        '''
        pass


    #TODO
    def p_initializer_list(self, p):
        '''
            initializer_list : initializer
                             | initializer_list COMMA initializer
        '''
        pass


    #TODO
    def p_compound_statement(self, p):
        '''
            compound_statement : LBRACE declaration_list statement_list RBRACE
        '''
        pass


    def p_statement(self, p):
        '''
            statement : expression_statement
                      | compound_statement
                      | selection_statement
                      | iteration_statement
                      | jump_statement
                      | assert_statement
                      | print_statement
                      | read_statement
        '''
        p[0] = p[1]


    def p_statement_list(self, p):
        '''
            statement_list : statement_list statement
                           | statement
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[2])


    def p_expression_statement(self, p):
        '''
            expression_statement : expression_opt SEMI
        '''
        p[0] = p[1]


    #TODO
    def p_selection_statement(self, p):
        '''
            selection_statement : IF LPAREN expression RPAREN statement
                                | IF LPAREN expression RPAREN statement ELSE statement
        '''
        pass


    def p_iteration_statement(self, p):
        '''
            iteration_statement : WHILE LPAREN expression RPAREN statement
                                | FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement
        '''
        if p[1] == "WHILE":
            p[0] = (p[1], p[3], p[5])
        else:
            p[0] = (p[1], p[3], p[5], p[7], p[9])


    def p_jump_statement(self, p):
        '''
            jump_statement : BREAK SEMI
                           | RETURN expression_opt SEMI
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2])


    def p_assert_statement(self, p):
        '''
            assert_statement : ASSERT expression SEMI
        '''
        p[0] = ("assert", p[2])


    def p_print_statement(self, p):
        '''
            print_statement : PRINT LPAREN expression_list RPAREN SEMI
        '''
        p[0] = ("print", p[3])


    def p_read_statement(self, p):
        '''
            read_statement : READ LPAREN argument_expression RPAREN SEMI
        '''
        p[0] = ("read", p[3])


    def p_error(self, p):
        if p:
            print("Error near the symbol %s" % p.value)
        else:
            print("Error at the end of input")


    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS', 'PLUSPLUS', 'MINUSMINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('right', 'PTIMES'),
        # precedence for unary operators
        ('right', 'UADDRESS', 'UPLUSPLUS', 'UMINUSMINUS', 'UTIMES', 'UPLUS', 'UMINUS', 'UNOT'),
    )


if __name__ == '__main__':
    def print_error(msg, x, y):
        print("Lexical error: %s at %d:%d" % (msg, x, y))

    parser = UCParser(print_error).build()
