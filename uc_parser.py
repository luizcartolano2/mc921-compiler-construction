#################################################
# uc_parser.py                                  #
#                                               #
# uCParser: parser for the uC language          #
#                                               #
# Authors: Luiz Cartolano && Erico Faustino     #
#################################################


# import the AST classes
import uc_ast
# import the lexer class
from uc_lex import UCLexer
# import the yacc lib
from ply.yacc import yacc
# get the list of tokens
tokens = UCLexer.tokens


# define a print function because the lexer receives one as argument
def print_error(msg, x, y):
    print("Lexical error: %s at %d:%d" % (msg, x, y))


class UCParser():
    """
        A parser for the uC language.

        ...

        Methods
        -------
            _token_coord(self, p, token_idx, set_col)
                A function to build a Coord object.

            _type_modify_decl(self, decl, modifier)
                Tacks a type modifier on a declarator, and returns the modified declarator.

            _fix_decl_name_type(self, decl, typename)
                Fixes a declaration. Modifies decl.

            _build_declarations(self, spec, decls)
                Builds a list of declarations all sharing the given specifiers.

            _build_function_definition(self, spec, decl, param_decls, body)
                Builds a function definition.

            parse(self, text, filename='', debug=False)
                Parses C code and returns an AST.

            p_*(self, p)
                The parser rules extracted from the BNF language.
    """

    def __init__(self, error_function=print_error):
        # get the tokens list
        self.tokens = UCLexer.tokens
        # create lexer object
        self.lexer = UCLexer(error_function)
        # build the lexer
        self.lexer.build()
        # build the parser
        self.parser = yacc(module=self,)


    def _token_coord(self, p, token_idx, set_col=False):
        """
            A function to build a Coord object.
        """
        last_cr = p.lexer.lexer.lexdata.rfind('\n', 0, p.lexpos(token_idx))

        if last_cr < 0:
            last_cr = -1
        column = (p.lexpos(token_idx) - (last_cr))

        return uc_ast.Coord(p.lineno(token_idx), column)


    def _type_modify_decl(self, decl, modifier):
        """
            Tacks a type modifier on a declarator, and returns
            the modified declarator.
            Note: the declarator and modifier may be modified
        """
        modifier_head = modifier
        modifier_tail = modifier

        # The modifier may be a nested list. Reach its tail.
        while modifier_tail.type:
            modifier_tail = modifier_tail.type

        # If the decl is a basic type, just tack the modifier onto it
        if isinstance(decl, uc_ast.VarDecl):
            modifier_tail.type = decl

            return modifier

        else:
            # Otherwise, the decl is a list of modifiers. Reach
            # its tail and splice the modifier onto the tail,
            # pointing to the underlying basic type.
            decl_tail = decl

            while not isinstance(decl_tail.type, uc_ast.VarDecl):
                decl_tail = decl_tail.type

            modifier_tail.type = decl_tail.type
            decl_tail.type = modifier_head

            return decl


    def _fix_decl_name_type(self, decl, typename):
        """
            Fixes a declaration. Modifies decl.
        """
        # Reach the underlying basic type
        type = decl
        while not isinstance(type, uc_ast.VarDecl):
            type = type.type

        decl.name = type.declname

        # The typename is a list of types. If any type in this
        # list isn't an Type, it must be the only
        # type in the list.
        # If all the types are basic, they're collected in the
        # Type holder.
        for tn in typename:
            if not isinstance(tn, uc_ast.Type):
                if len(typename) > 1:
                    self._parse_error(
                        "Invalid multiple types specified", tn.coord)
                else:
                    type.type = tn
                    return decl

        if not typename:
            # Functions default to returning int
            if not isinstance(decl.type, uc_ast.FuncDecl):
                self._parse_error("Missing type in declaration", decl.coord)

            type.type = uc_ast.Type(
                            ['int'],
                            coord=decl.coord
                        )

        else:
            # At this point, we know that typename is a list of Type
            # nodes. Concatenate all the names into a single list.
            type.type = uc_ast.Type(
                            [typename.names[0]],
                            coord=typename.coord
                        )

        return decl


    def _build_declarations(self, spec, decls):
        """
            Builds a list of declarations all sharing the given specifiers.
        """
        declarations = []

        for decl in decls:
            assert decl['decl'] is not None
            declaration = uc_ast.Decl(
                    name=None,
                    type=decl['decl'],
                    init=decl.get('init'),
                    coord=decl['decl'].coord)

            if isinstance(declaration.type, uc_ast.Type):
                fixed_decl = declaration
            else:
                fixed_decl = self._fix_decl_name_type(declaration, spec)
            
            declarations.append(fixed_decl)

        return declarations


    def _build_function_definition(self, spec, decl, param_decls, body):
        """ 
            Builds a function definition.
        """
        declaration = self._build_declarations(
                            spec=spec,
                            decls=[dict(decl=decl, init=None)]
                        )[0]

        return uc_ast.FuncDef(
                    spec=spec,
                    decl=declaration,
                    param_decls=param_decls,
                    body=body,
                    coord=decl.coord
                )


    def parse(self, text, filename='', debug=False):
        """ 
            Parses C code and returns an AST.
            
            :input: text - a string containing the uC source code
            :input: filename - name of the file being parsed (for meaningful error messages)
            :input: debuglevel - debug level to yacc

            :return: an AST for the code
                
        """
        return self.parser.parse(
                input=text,
                lexer=self.lexer,
                debug=debug,
            )


    def p_program(self, p):
        '''
            program : global_declaration_list
        '''
        p[0] = uc_ast.Program(
                        gdecls=p[1], 
                        coord=self._token_coord(p,1)
                    )

    
    ##
    ## Declarations come as lists
    ##
    def p_global_declaration_list(self, p):
        '''
            global_declaration_list : global_declaration
                                    | global_declaration_list global_declaration
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]


    def p_global_declaration_1(self, p):
        '''
            global_declaration : declaration
        '''
        p[0] = uc_ast.GlobalDecl(
                        decls=p[1], 
                        coord=self._token_coord(p,1)
                    )


    def p_global_declaration_2(self, p):
        '''
            global_declaration : function_definition
        '''
        p[0] = p[1]


    ##
    ## For the functions, the declator may be followed by a list
    ##
    def p_function_definition_1(self, p):
        '''
            function_definition : declarator declaration_list_opt compound_statement
        '''
        specification = dict(
                            type=[uc_ast.Type(['void'], coord=self._token_coord(p,1))],
                            function=[]
                        )

        p[0] = self._build_function_definition(
                        spec=specification,
                        decl=p[1],
                        param_decls=p[2],
                        body=p[3]
                    )


    def p_function_definition_2(self, p):
        '''
            function_definition : type_specifier declarator declaration_list_opt compound_statement
        '''
        specification = p[1]

        p[0] = self._build_function_definition(
                        spec=specification,
                        decl=p[2],
                        param_decls=p[3],
                        body=p[4],
                    )


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


    ##
    ## For the project purpose we will split a declaration like
    ## int x, y, z; into three declarations, thats why we need to create
    ## a declaration_body parse rule.
    ##
    def p_declaration_body(self,p):
        '''
            declaration_body :  type_specifier init_declarator_list_opt
        '''
        specification = p[1]

        if p[2] is not None:
            decls = self._build_declarations(
                            spec=specification,
                            decls=p[2]
                        )
        else:
            decls = None

        p[0] = decls


    def p_declaration(self, p):
        '''
            declaration :  declaration_body SEMI
        '''
        p[0] = p[1]


    ##
    ##  Rule to combine all declarations and return just one
    ##
    def p_declaration_list(self, p):
        '''
            declaration_list : declaration
                             | declaration_list declaration
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]


    def p_type_specifier(self, p):
        '''
            type_specifier : VOID
                           | CHAR
                           | INT
                           | FLOAT
        '''
        p[0] = uc_ast.Type(
                        names=[p[1]], 
                        coord=self._token_coord(p,1)
                    )



    ##
    ##  Returns a dict of declarations or None
    ##
    def p_init_declarator_list(self, p):
        '''
            init_declarator_list : init_declarator
                                 | init_declarator_list COMMA init_declarator
        '''
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]


    def p_init_declarator(self, p):
        '''
            init_declarator : declarator
                            | declarator EQUALS initializer
        '''
        if len(p) > 2:
            init = p[3]
        else:
            init = None

        p[0] = dict(
                    decl=p[1],
                    init=init
                )

   
    def p_declarator_1(self, p):
        '''
            declarator : direct_declarator
        '''
        p[0] = p[1]


    def p_declarator_2(self, p):
        '''
            declarator : pointer direct_declarator
        '''
        p[0] = self._type_modify_decl(
                        decl=p[2], 
                        modifier=p[1]
                    )


    def p_declaration_list_opt(self,p):
        '''
            declaration_list_opt : empty
                                 | declaration_list
        '''
        p[0] = p[1]


    ##
    ##  Pointers nest from inside out.
    ##
    def p_pointer(self, p):
        '''
            pointer : TIMES
                    | TIMES pointer
        '''
        nest_type = uc_ast.PtrDecl(
                        ptr_quals= p[1] or [],
                        type=None,
                        coord=self._token_coord(p,1)
                    )

        if len(p) > 2:
            tail_type = p[2]
            while tail_type.type is not None:
                tail_type = tail_type.type

            tail_type.type = nest_type

            p[0] = p[2]
        else:
            p[0] = nest_type


    ##
    ##  Define the direct declarators functions
    ##
    def p_direct_declarator_1(self, p):
        '''
            direct_declarator : identifier
        '''
        p[0] = uc_ast.VarDecl(
                        declname=p[1],
                        type=None,
                        coord=self._token_coord(p,1),
                    )


    def p_direct_declarator_2(self, p):
        '''
            direct_declarator : LPAREN declarator RPAREN
        '''
        p[0] = p[2]


    def p_direct_declarator_3(self, p):
        '''
            direct_declarator : direct_declarator LBRACKET constant_expression_opt RBRACKET
        '''
        if len(p) > 4:
            dimension = p[3]
        else:
            dimension = None

        array = uc_ast.ArrayDecl(
                            type=None,
                            dimension=dimension,
                            coord=p[1].coord
                        )

        p[0] = self._type_modify_decl(
                        decl=p[1],
                        modifier=array
                    )


    def p_direct_declarator_4(self, p):
        '''
            direct_declarator : direct_declarator LPAREN parameter_list RPAREN
                              | direct_declarator LPAREN identifier_list_opt RPAREN
        '''
        func_decl = uc_ast.FuncDecl(
                                args=p[3],
                                type=None,
                                coord=p[1].coord,
                            )

        p[0] = self._type_modify_decl(
                        decl=p[1], 
                        modifier=func_decl
                    )


    def p_identifier(self, p):
        '''
            identifier : ID
        '''
        p[0] = uc_ast.ID(
                        name=p[1], 
                        coord=self._token_coord(p,1)
                    )


    def p_identifier_list(self, p):
        '''
            identifier_list : identifier
                            | identifier_list COMMA identifier
        '''
        if len(p) == 2:
            p[0] = uc_ast.ParamList(
                            params=[p[1]],
                            coord=p[1].coord
                        )
        else:
            p[1].params.append(p[3])
            p[0] = p[1]


    def p_identifier_list_opt(self, p):
        '''
            identifier_list_opt : empty
                                | identifier_list
        '''
        p[0] = p[1]


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
            p[0] = uc_ast.BinaryOp(
                            op=p[2],
                            left_value=p[1],
                            right_value=p[3],
                            coord=p[1].coord
                        )


    def p_cast_expression_1(self, p):
        '''
            cast_expression : unary_expression
        '''
        p[0] = p[1]


    def p_cast_expression_2(self, p):
        '''
            cast_expression : LPAREN type_specifier RPAREN cast_expression
        '''
        p[0] = uc_ast.Cast(
                        to_type=p[2],
                        expression=p[4],
                        coord=self._token_coord(p,1)
                    )


    def p_unary_expression_1(self, p):
        '''
            unary_expression : postfix_expression
        '''
        p[0] = p[1]

        
    def p_unary_expression_2(self, p):
        '''
            unary_expression : PLUSPLUS unary_expression
                             | MINUSMINUS unary_expression
                             | unary_operator cast_expression
        '''
        p[0] = uc_ast.UnaryOp(
                        op=p[1],
                        expr=p[2],
                        coord=p[2].coord
                    )


    def p_postfix_expression_1(self, p):
        '''
            postfix_expression : primary_expression
        '''
        p[0] = p[1]


    def p_postfix_expression_2(self, p):
        '''
            postfix_expression : postfix_expression LBRACKET expression RBRACKET
        '''
        p[0] = uc_ast.ArrayRef(
                        name=p[1],
                        subscript=p[3],
                        coord=p[1].coord
                    )


    def p_postfix_expression_3(self, p):
        '''
            postfix_expression : postfix_expression LPAREN argument_expression_opt RPAREN
        '''
        if len(p) > 4:
            args = p[3]
        else:
            args = None

        p[0] = uc_ast.FuncCall(
                        name=p[1],
                        args=args,
                        coord=p[1].coord
                    )


    def p_postfix_expression_4(self, p):
        '''
            postfix_expression : postfix_expression PLUSPLUS
                               | postfix_expression MINUSMINUS
        '''
        p[0] = uc_ast.UnaryOp(
                        op='p'+p[2],
                        expr=p[1],
                        coord=p[1].coord
                    )


    def p_argument_expression(self, p):
        '''
            argument_expression : assignment_expression
                                | argument_expression COMMA assignment_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if not isinstance(p[1], uc_ast.ExprList):
                p[1] = uc_ast.ExprList(
                                exprs=[p[1]],
                                coord=p[1].coord
                            )

            p[1].exprs.append(p[3])
            p[0] = p[1]


    def p_argument_expression_opt(self, p):
        '''
            argument_expression_opt : empty
                                    | argument_expression
        '''
        p[0] = p[1]


    def p_primary_expression_1(self, p):
        '''
            primary_expression : identifier
        '''
        p[0] = p[1]


    def p_primary_expression_2(self, p):
        '''
            primary_expression : constant
        '''
        p[0] = p[1]


    def p_primary_expression_3(self, p):
        '''
            primary_expression : CHAR_CONST
        '''
        p[0] = uc_ast.Constant(
                        type='string',
                        value=p[1],
                        coord=self._token_coord(p,1)
                    )


    def p_primary_expression_4(self, p):
        '''
            primary_expression : LPAREN expression RPAREN
        '''
        p[0] = p[2]


    def p_constant_1(self, p):
        '''
            constant : INT_CONST
        '''
        p[0] = uc_ast.Constant(
                        type='int',
                        value=p[1],
                        coord=self._token_coord(p,1)
                    )


    def p_constant_2(self, p):
        '''
            constant : STRING_LITERAL
        '''
        p[0] = uc_ast.Constant(
                        type='string',
                        value=p[1],
                        coord=self._token_coord(p,1)
                    )


    def p_constant_3(self, p):
        '''
            constant : FLOAT_CONST
        '''
        p[0] = uc_ast.Constant(
                        type='float',
                        value=p[1],
                        coord=self._token_coord(p,1)
                    )


    def p_expression(self, p):
        '''
            expression : assignment_expression
                       | expression COMMA assignment_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if not isinstance(p[1], uc_ast.ExprList):
                p[1] = uc_ast.ExprList(
                                exprs=[p[1]],
                                coord=p[1].coord
                            )

            p[1].exprs.append(p[3])
            p[0] = p[1]


    def p_expression_opt(self, p):
        '''
            expression_opt : empty
                           | expression
        '''
        p[0] = p[1]


    def p_assignment_expression(self, p):
        '''
            assignment_expression : binary_expression
                                  | unary_expression assignment_operator assignment_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = uc_ast.Assignment(
                            op=p[2],
                            left_value=p[1],
                            right_value=p[3],
                            coord=p[1].coord
                        )


    def p_assignment_operator(self, p):
        '''
            assignment_operator : EQUALS
                                | TIMESEQUAL
                                | DIVIDEEQUAL
                                | MODEQUAL
                                | PLUSEQUAL
                                | MINUSEQUAL
        '''
        p[0] = p[1]


    def p_unary_operator(self, p):
        '''
            unary_operator : ADDRESS
                           | TIMES
                           | PLUS
                           | MINUS
                           | NOT
        '''
        p[0] = p[1]


    ##
    ##  Threat the declaration of parameters
    ##
    def p_parameter_list(self, p):
        '''
            parameter_list : parameter_declaration
                           | parameter_list COMMA parameter_declaration
        '''
        if len(p) == 2:
            p[0] = uc_ast.ParamList(
                            params=[p[1]],
                            coord=p[1].coord
                        )
        else:
            p[1].params.append(p[3])
            p[0] = p[1]


    def p_parameter_declaration(self, p):
        '''
            parameter_declaration : type_specifier declarator
        '''
        decls = dict(
                    decl=p[2]
                )

        p[0] = self._build_declarations(
                        spec=p[1],
                        decls=[decls]
                    )[0]


    def p_init_declarator_list_opt(self, p):
        '''
            init_declarator_list_opt : empty
                                     | init_declarator_list
        '''
        p[0] = p[1]


    def p_initializer_1(self, p):
        '''
            initializer : assignment_expression
        '''
        p[0] = p[1]


    def p_initializer_2(self, p):
        '''
            initializer : LBRACE initializer_list_opt RBRACE
                        | LBRACE initializer_list COMMA RBRACE
        '''
        if p[2] is None:
            p[0] = uc_ast.InitList(
                            expressions=[],
                            coord=self._token_coord(p,1),
                        )
        else:
            p[0] = p[2]


    def p_initializer_list_opt(self, p):
        '''
            initializer_list_opt : empty
                                 | initializer_list
        '''
        p[0] = p[1]


    def p_initializer_list(self, p):
        '''
            initializer_list : initializer
                             | initializer_list COMMA initializer
        '''
        if len(p) == 2:
            p[0] = uc_ast.InitList(
                            expressions=[p[1]],
                            coord=p[1].coord
                        )
        else:
            p[1].expressions.append(p[3])
            p[0] = p[1]


    ##
    ##  The block item is created to make consistency between declarator and statement
    ##
    def p_block_item(self, p):
        '''
            block_item : declaration
                       | statement
        '''
        if isinstance(p[1], list):
            p[0] = p[1]
        else:
            p[0] = [p[1]]


    def p_block_item_list(self, p):
        '''
            block_item_list : block_item
                            | block_item_list block_item
        '''
        if len(p) == 2 or p[2] == [None]:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]


    def p_block_item_list_opt(self, p):
        '''
            block_item_list_opt : empty
                                | block_item_list
        '''
        p[0] = p[1]


    def p_compound_statement(self, p):
        '''
            compound_statement : LBRACE block_item_list_opt RBRACE
        '''
        p[0] = uc_ast.Compound(
                        block_items=p[2],
                        coord=self._token_coord(p,1,set_col=True)
                    )


    def p_expression_statement(self, p):
        '''
            expression_statement : expression_opt SEMI
        '''
        if p[1] is None:
            p[0] = uc_ast.EmptyStatement(
                            coord=self._token_coord(p,2)
                        )
        else:
            p[0] = p[1]


    ##
    ##  Rules to define if/else expressions
    ##
    def p_selection_statement_1(self, p):
        '''
            selection_statement : IF LPAREN expression RPAREN statement
        '''
        p[0] = uc_ast.If(
                        if_cond=p[3],
                        if_true=p[5],
                        if_false=None,
                        coord=self._token_coord(p,1)
                    )


    def p_selection_statement_2(self, p):
        '''
            selection_statement : IF LPAREN expression RPAREN statement ELSE statement
        '''
        p[0] = uc_ast.If(
                        if_cond=p[3],
                        if_true=p[5],
                        if_false=p[7],
                        coord=self._token_coord(p,1)
                    )        


    ##
    ##  Rules to define loop expressions (eg. For/While)
    ##
    def p_iteration_statement_1(self, p):
        '''
            iteration_statement : WHILE LPAREN expression RPAREN statement
        '''
        p[0] = uc_ast.While(
                        while_cond=p[3],
                        while_stmt=p[5],
                        coord=self._token_coord(p,1)
                    )


    def p_iteration_statement_2(self, p):
        '''
            iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement

        '''
        p[0] = uc_ast.For(
                        for_init=p[3],
                        for_cond=p[5],
                        for_next=p[7],
                        for_statement=p[9],
                        coord=self._token_coord(p,1)
                    )


    def p_iteration_statement_3(self, p):
        '''
            iteration_statement : FOR LPAREN declaration expression_opt SEMI expression_opt RPAREN statement
        '''
        decl = uc_ast.DeclList(
                        decls=p[3],
                        coord=self._token_coord(p,1)
                    )

        p[0] = uc_ast.For(
                        for_init=decl,
                        for_cond=p[4],
                        for_next=p[6],
                        for_statement=p[8],
                        coord=self._token_coord(p,1)
                    )


    ##
    ##  Rules to define control flow expressions (eg. Break/Return)
    ##
    def p_jump_statement_1(self, p):
        '''
            jump_statement : BREAK SEMI
        '''
        p[0] = uc_ast.Break(
                        coord=self._token_coord(p,1)
                    )


    def p_jump_statement_2(self, p):
        '''
            jump_statement : RETURN expression SEMI
                           | RETURN SEMI
        '''
        if len(p) == 4:
            expression = p[2]
        else:
            expression = None

        p[0] = uc_ast.Return(
                        expression=expression,
                        coord=self._token_coord(p,1)
                    )


    ##
    ##  Rules to define assert expressions
    ##
    def p_assert_statement(self, p):
        '''
            assert_statement : ASSERT expression SEMI
        '''
        p[0] = uc_ast.Assert(
                        expr=p[2],
                        coord=self._token_coord(p,1)
                    )


    ##
    ##  Rules to define print expressions
    ##
    def p_print_statement(self, p):
        '''
            print_statement : PRINT LPAREN expression_opt RPAREN SEMI
        '''
        p[0] = uc_ast.Print(
                        expr=p[3] if len(p) == 6 else None,
                        coord=self._token_coord(p,1)
                    )


    ##
    ##  Rules to define read expressions
    ##
    def p_read_statement(self, p):
        '''
            read_statement : READ LPAREN argument_expression RPAREN SEMI
        '''
        p[0] = uc_ast.Read(
                        names=p[3],
                        coord=self._token_coord(p,1)
                    )


    ##
    ##  Rules to deal with error and empty productions
    ##
    def p_error(self, p):
        if p:
            print("Error near the symbol %s" % p.value)
        else:
            print("Error at the end of input")


    def p_empty(self, p):
        '''
            empty :
        '''
        p[0] = None


    ##
    ## Precedence and associativity of operators
    ##
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS', 'PLUSPLUS', 'MINUSMINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
    )
