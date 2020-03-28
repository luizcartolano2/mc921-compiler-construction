# import the lex class
from uc_lex import UCLexer
# import the yacc lib
from ply.yacc import yacc


class UCParser():
    """ 
        A parser for the uC language.
    """
    
   def build(self):
    """ Builds the parser from the specification. Must be
        called after the parser object is created.

        This method exists separately, because the PLY
        manual warns against calling lex.lex inside __init__
    """
    self.parser = yacc(write_tables=False)

    
    def p_program(self, p):
        """ 
            <program> ::= {<global_declaration>}+ 
        """

        pass


    def p_global_declaration(self, p):
        """
            <global_declaration> ::= <function_definition>
                       | <declaration>
        """
        pass


    def p_function_definition(self, p):
        """
            <function_definition> ::= {<type_specifier>}? <declarator> {<declaration>}* <compound_statement>
        """
        pass


    def p_type_specifier(self, p):
        """
            <type_specifier> ::= void
                   | char
                   | int
                   | float
        """
        pass


    def p_declarator(self, p):
        """
            <declarator> ::= {<pointer>}? <direct_declarator>
        """
        pass


    def p_pointer(self, p):
        """
            <pointer> ::= * {<pointer>}?
        """
        pass


    def p_direct_declarator(self, p):
        """
            <direct_declarator> ::= <identifier>
                                    | ( <declarator> )
                                    | <direct_declarator> [ {<constant_expression>}? ]
                                    | <direct_declarator> ( <parameter_list> )
                                    | <direct_declarator> ( {<identifier>}* )
        """
        pass


    def p_constant_expression(self, p):
        """
            <constant_expression> ::= <binary_expression>
        """
        pass


    def p_binary_expression(self, p):
        """
            <binary_expression> ::= <cast_expression>
                                  | <binary_expression>  *   <binary_expression>
                                  | <binary_expression>  /   <binary_expression>
                                  | <binary_expression>  %   <binary_expression>
                                  | <binary_expression>  +   <binary_expression>
                                  | <binary_expression>  -   <binary_expression>
                                  | <binary_expression>  <   <binary_expression>
                                  | <binary_expression>  <=  <binary_expression>
                                  | <binary_expression>  >   <binary_expression>
                                  | <binary_expression>  >=  <binary_expression>
                                  | <binary_expression>  ==  <binary_expression>
                                  | <binary_expression>  !=  <binary_expression>
                                  | <binary_expression>  &&  <binary_expression>
                                  | <binary_expression>  ||  <binary_expression>
        """
        pass


    def p_cast_expression(self, p):
        """
            <cast_expression> ::= <unary_expression>
                                | ( <type_specifier> ) <cast_expression>
        """ 
        pass


    def p_unary_expression(self, p):
        """
            <unary_expression> ::= <postfix_expression>
                                 | ++ <unary_expression>
                                 | -- <unary_expression>
                                 | <unary_operator> <cast_expression>
        """
        pass


    def p_postfix_expression(self, p):
        """
            <postfix_expression> ::= <primary_expression>
                       | <postfix_expression> [ <expression> ]
                       | <postfix_expression> ( {<argument_expression>}? )
                       | <postfix_expression> ++
                       | <postfix_expression> --
        """
        pass


    def p_primary_expression(self, p):
        """
            <primary_expression> ::= <identifier>
                       | <constant>
                       | <string>
                       | ( <expression> )
        """
        pass


    def p_constant(self, p):
        """
            <constant> ::= <integer_constant>
             | <character_constant>
             | <floating_constant>
        """
        pass


    def p_expression(self, p):
        """
            <expression> ::= <assignment_expression>
               | <expression> , <assignment_expression>
        """
        pass


    def p_argument_expression(self, p):
        """
            <argument_expression> ::= <assignment_expression>
                        | <argument_expression> , <assignment_expression>
        """
        pass


    def p_assignment_expression(self, p):
        """
            <assignment_expression> ::= <binary_expression>
                          | <unary_expression> <assignment_operator> <assignment_expression>
        """
        pass


    def p_assignment_operator(self, p):
        """
            <assignment_operator> ::= =
                        | *=
                        | /=
                        | %=
                        | +=
                        | -=
        """
        pass


    def p_unary_operator(self, p):
        """
            <unary_operator> ::= &
                   | *
                   | +
                   | -
                   | !
        """
        pass


    def p_parameter_list(self, p):
        """
            <parameter_list> ::= <parameter_declaration>
                   | <parameter_list> , <parameter_declaration>
        """
        pass


    def p_parameter_declaration(self, p):
        """
            <parameter_declaration> ::= <type_specifier> <declarator>
        """
        pass


    def p_declaration(self, p):
        """
            <declaration> ::=  <type_specifier> {<init_declarator_list>}? ;
        """
        pass     


    def p_init_declarator_list(self, p):
        """
            <init_declarator_list> ::= <init_declarator>
                         | <init_declarator_list> , <init_declarator>
        """
        pass     


    def p_init_declarator(self, p):
        """
            <init_declarator> ::= <declarator>
                    | <declarator> = <initializer>
        """
        pass     


    def p_initializer(self, p):
        """
            <initializer> ::= <assignment_expression>
                | { <initializer_list> }
                | { <initializer_list> , }
        """
        pass     


    def p_initializer_list(self, p):
        """
            <initializer_list> ::= <initializer>
                     | <initializer_list> , <initializer>

        """
        pass     


    def p_compound_statement(self, p):
        """
            <compound_statement> ::= { {<declaration>}* {<statement>}* }
        """
        pass     


    def p_statement(self, p):
        """
            <statement> ::= <expression_statement>
              | <compound_statement>
              | <selection_statement>
              | <iteration_statement>
              | <jump_statement>
              | <assert_statement>
              | <print_statement>
              | <read_statement>
        """
        pass     


    def p_expression_statement(self, p):
        """
            <expression_statement> ::= {<expression>}? ;
        """
        pass     


    def p_selection_statement(self, p):
        """
            <selection_statement> ::= if ( <expression> ) <statement>
                        | if ( <expression> ) <statement> else <statement>
        """
        pass     


    def p_iteration_statement(self, p):
        """
            <iteration_statement> ::= while ( <expression> ) <statement>
                        | for ( {<expression>}? ; {<expression>}? ; {<expression>}? ) <statement>
        """
        pass     


    def p_jump_statement(self, p):
        """
            <jump_statement> ::= break ;
                   | return {<expression>}? ;
        """
        pass     


    def p_assert_statement(self, p):
        """
            <assert_statement> ::= assert <expression> ;
        """
        pass     


    def p_print_statement(self, p):
        """
            <print_statement> ::= print ( {<expression>}* ) ;
        """
        pass     


    def p_read_statement(self, p):
        """
            <read_statement> ::= read ( <argument_expression> );
        """
        pass     
