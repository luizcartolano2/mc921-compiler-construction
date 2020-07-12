"""
#################################################
# uc_sema.py                                    #
#                                               #
# Code for uC Semantic Checker                  #
#                                               #
# Authors: Luiz Cartolano && Erico Faustino     #
#################################################
"""

from uc_ast import *
from uc_type import *
from uc_env import *

class Visitor(NodeVisitor):
    """
        A Semantic Checker for the uC language.

        Program visitor class. This class uses the visitor pattern. You need to define methods
        of the form visit_NodeName() for each kind of AST node that you want to process.
        Note: You will need to adjust the names of the AST nodes if you picked different names.
        ...

        Methods
        -------
            __typemap(self, _type)
                The method that maps a type string to its corresponding object type

            __getline(self, node)
                The method returns the node coordinate (line:column) in which the error occured

            __check_type(self, func_name, type_name, node, index)
                The method verifies wheather the type in a function is correct

            __check_scope(self, node, line)
                The method checks if the scope exists

            __check_two_types(self, node, line, func, index)
                todo terminar aqui

            __check_operand_match(self, operator, node, operand_type, line, func_name)

            __check_location(self, var)

            __check_init(self, type, init, var, line)

            __set_dimension(self, node, length, line, var)

            visit_*(self, node)
                The methods that implements visit to all
                AST nodes
    """
    def __init__(self):
        # instantiate an env
        self.environment = Environment()


    def __typemap(self, _type):
        """
            A method used to map a type string to its corresponding object type

            ...

            Parameters
            ----------
                type : string
                    A string with the type.

        """
        return {
            'int'    : IntType,
            'float'  : FloatType,
            'char'   : CharType,
            'bool'   : BoolType,
            'array'  : ArrayType,
            'string' : StringType,
            'ptr'    : PtrType,
            'void'   : VoidType,
            }[_type]


    def __getline(self, node):
        """
            A method used to display the node coordinate (line:column) in which the error occured

            ...

            Parameters
            ----------
                node : Node
                    A generic node.

        """
        return f'@ {node.coord.line}:{node.coord.column} - '


    def __check_type(self, func_name, type_name, node, index=0):
        """
            A method used to check two types.

            ...

            Parameters
            ----------
                func_name : str
                    An string.
                type_name : str
                    An string.
                node : Node
                    A Node object.
        """

        msg = self.__getline(node) + "type in " + func_name + " must be a " + type_name

        if hasattr(node, "type"):
            if isinstance(node, Constant):
                assert node.rawtype.names[index] == self.__typemap(type_name), msg
            else:
                assert node.type.names[index] == self.__typemap(type_name), msg
        else:
            assert False, msg


    def __check_scope(self, node, line):
        """
            A method used to check var scope.

            ...

            Parameters
            ----------
                node : Node
                    An Node object.
                line : str
                    An string.
        """
        if isinstance(node, ID):
            assert node.scope is not None, line + f"{node} is not defined."


    def __check_two_types(self, node, line, func, index=-1):
        """
            A method used to check two types

            ...

            Parameters
            ----------
                param_type : Node
                    An Node object.
                line : str
                    An string.
                func : str
                    An string.
                index : int
                    An intenger.
        """
        if hasattr(node, 'left_value') and hasattr(node, 'right_value'):
            if isinstance(node.left_value, Constant):
                # get left type
                left_type = node.left_value.rawtype.names[index]
            else:
                # get left type
                left_type = node.left_value.type.names[index]

            if isinstance(node.right_value, Constant):
                # get right type
                right_type = node.right_value.rawtype.names[index]
            else:
                # get right type
                right_type = node.right_value.type.names[index]

            # assert if types match
            if left_type.typename == 'char' and right_type.typename == 'string':
                pass
            elif left_type.typename == 'string' and right_type.typename == 'char':
                pass
            else:
                assert left_type == right_type, line + f"Types {right_type.typename} and {left_type.typename} are different on function {func}!"


    def __check_operand_match(self, operator, node, operand_type, line, func_name):
        """
            A method used to check if operand is supported.

            ...

            Parameters
            ----------
                operator : str
                    An string.
                node : Node
                    An Node object.
                operand_type : str
                    An string.
                line : str
                    An string.
                func_name : str
                    An string.

        """
        # get operators
        node_operators = eval(f'node.{operand_type}')

        # check if supported
        assert operator in node_operators, line + f"{func_name} function does not support operator {operator}!"


    def __check_location(self, var):
        """
            A method used to check node location

            ...

            Parameters
            ----------
                var : str
                    An string.
        """
        # first get line
        var_line = self.__getline(var)

        # check if var is declared
        self.__check_scope(var, var_line)

        # test for type
        type_test = (isinstance(var, ArrayRef) and len(var.type.names) == 1) or isinstance(var, ID)

        # get var name
        var_name = var.name

        assert type_test, var_line + f'{var_name} isnt a simple variable for read function.'

        if isinstance(var_name, ArrayRef):
            var_name = var_name.name.name + '[' + var_name.subscript.name + '][' + var.subscript.name + ']'
        elif hasattr(var, 'subscript'):
            var_name = var.name.name + '[' + var.subscript.name + ']'

        assert len(var.type.names) == 1, var_line + f'{var_name} isnt a primitive type for read function.'


    def __check_init(self, param_type, init, var, line):
        """
            A method used to check an init decl.

            ...

            Parameters
            ----------
                param_type : Node
                    An Node object.
                init : Node
                    An Node object.
                var : str
                    An string.
                line : str
                    An string.

        """
        # first visit init
        self.visit(init)

        # if var is global init val must be a constant
        # or an array, we cant initiate an global with
        # ID or ArrayRef
        node_var = self.environment.lookup(var)
        if node_var.scope == 0:
            assert isinstance(init, (InitList, Constant)), f'Global {var} must have a Constant for initialization.'

        # need to deal if Constant because
        # they have a diff class attrs names
        if isinstance(init, Constant):
            # if initialization comes with a string
            # we are dealing with an array of chars
            # else we just make sure Constant and param
            # type are the same
            if init.type == 'string':
                # if initi comes with a VarDecl, we need
                # to check the type of the VarDecl if not
                # we can access the type directly
                if isinstance(param_type.type, VarDecl):
                    assert param_type.type.type.names == [self.__typemap("array"), self.__typemap("char")], line + f"{var} initialization type mismatch"
                else:
                    assert param_type.type.names == [self.__typemap("array"), self.__typemap("char")], line + f"{var} initialization type mismatch"

                # since we are dealing with an
                # array we must set his dimension
                self.__set_dimension(param_type, len(init.value), line, var)
            else:
                assert param_type.type.names[0] == init.rawtype.names[0], line + f"{var} initialization type mismatch"

        # on this branch we must deal
        # if init goes with more than one
        # value like in a[] = {1, 2, 3, 4}
        elif isinstance(init, InitList):
            # import pdb; pdb.set_trace()
            # get the list of expressions
            list_exprs = init.expressions

            # get the size of the
            # list expressions
            length = len(list_exprs)

            # when receiving an InitList for initialization
            # if the param_type (the obj) we are initializing
            # is a variable we must make a special check, that
            # is different than when we are make the initialization
            # of an array
            if isinstance(param_type, VarDecl):
                # make sure the list has a single element
                assert length == 1, line + f"Variable - {var} - must be initialize with a single element"

                # check if the element type matchs with the var
                assert param_type.type.names[0].typename == list_exprs[0].type, line + \
                f"Variable {var} has a type mismatch initialization. Should be {param_type.type.names[0].typename} instead of {list_exprs[0].type}."

            # when receiving an InitList for initialization
            # if the param_type (the obj) we are initializing
            # is an Array we must check if the length of the
            # array matches and if all numbers of the given array
            # has the same type of the declared array
            elif isinstance(param_type, ArrayDecl):
                size = length
                head = list_exprs
                decl = param_type
                # import pdb; pdb.set_trace()
                # here we deal with the special case
                # where we have an array of array init
                # like in a[3][2] = {{1,3}, {2,6}, {3,9}}
                while isinstance(param_type.type, ArrayDecl):
                    # if dealing with arrays of arrays, following
                    # the procedure of the C language, the first
                    # dimension is the only one that can be blank
                    if param_type.type.dimension is None:
                        param_type.type.dimension = Constant(type='int', value=len(list_exprs[0].expressions), rawtype=IntType)
                        # here is the right thing to do, but professor wants do the wrong way ¯\_(ツ)_/¯
                        # assert False, line + f"First array dimension is the only one who can be blank."

                    param_type = param_type.type
                    length = len(list_exprs[0].expressions)

                    # check for all sub arrays if
                    # the length matches with the
                    # given dimension for the array
                    for i, _ in enumerate(list_exprs):
                        assert len(list_exprs[i].expressions) == length, line + f"Sublist have different length."

                param_type = decl
                exprs = head
                length = size

                if not isinstance(param_type.type, ArrayDecl):
                    # check for array dimension if dimensin
                    # has not been declared we make it
                    if param_type.dimension is None:
                        param_type.dimension = Constant(type='int', value=size)
                        self.visit_Constant(param_type.dimension)
                    else:
                        assert param_type.dimension.value == length, line + f"Size mismatch on variable - {var} - initialization."

                    # besides the dimension, we must
                    # check if all values of the list
                    # has the same type of the variable
                    var_type = param_type.type.type.names[-1]
                    # iterate over all list comparing
                    # the value type of ID/CONST/ARR
                    for expr in init.expressions:
                        if isinstance(expr, Constant):
                            assert var_type == expr.rawtype.names[-1], line + \
                            f"Type mismatch on variable - {var} - initialization, element {expr.value} should be {var_type.typename}."
                        elif isinstance(expr, ID):
                            assert var_type == expr.type.names[-1], line + \
                            f"Type mismatch on variable - {var} - initialization, variable {expr.name} should be {var_type.typename}."
                        else:
                            assert var_type == expr.type.names[-1], line + \
                            f"Type mismatch on variable - {var} - initialization, array ref {expr.name.name} should be {var_type.typename}."
                else:
                    # check for array dimension if dimension
                    # has not been declared we make it
                    if param_type.dimension is None:
                        param_type.dimension = Constant(type='int', value=length)
                        self.visit_Constant(param_type.dimension)
                    else:
                        assert param_type.dimension.value == length, line + f"Size mismatch on variable - {var} - initialization."

                    # besides the dimension, we must
                    # check if all values of the list
                    # has the same type of the variable
                    var_type = param_type.type.type.type.names[-1]

                    # iterate over all list comparing
                    # the value type of ID/CONST/ARR
                    for exp in exprs:
                        for ex in exp:
                            if isinstance(ex, Constant):
                                assert var_type == ex.rawtype.names[-1], line + \
                                f"Type mismatch on variable - {var} - initialization, element {ex.value} should be {var_type.typename}."
                            elif isinstance(ex, ID):
                                assert var_type == ex.type.names[-1], line + \
                                f"Type mismatch on variable - {var} - initialization, variable {ex.name} should be {var_type.typename}."
                            else:
                                assert var_type == ex.type.names[-1], line + \
                                f"Type mismatch on variable - {var} - initialization, array ref {ex.name.name} should be {var_type.typename}."


    def __set_dimension(self, node, length, line, var):
        """
            A method used to set an ArrayDim.

            ...

            Parameters
            ----------
                node : Node
                    An Node object.
                length : int
                    An integer.
                var : str
                    An string.
                line : str
                    An string.

        """
        if not node.dimension:
            node.dimension = Constant(type='int', value=length)
            self.visit(node.dimension)
        else:
            assert node.dimension.value == length, line + f"Size mismatch on array initialization at {var}"


    def visit_ArrayDecl(self, node):
        """
            A method used to represent a visit of ArrayDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The ArrayDecl node.

        """
        # visit node type
        self.visit(node.type)

        # get the declaration
        _type = node.type
        while not isinstance(_type, VarDecl):
            _type = _type.type

        # get declaration name
        array_id = _type#.declname

        # add the  array name to the list of names
        array_id.type.names.insert(0, self.__typemap("array"))

        # visit array dimension
        if node.dimension:
            self.visit(node.dimension)


    def visit_ArrayRef(self, node):
        """
            A method used to represent a visit of ArrayRef node.

            ...

            Parameters
            ----------
                node : Node
                    The ArrayRef node.

        """
        # visit the array subscription
        self.visit(node.subscript)

        # check scope for subscript
        self.__check_scope(node=node.subscript, line=self.__getline(node.subscript))

        # the subscript must be a int
        self.__check_type(func_name="ArrayRef", type_name="int", node=node.subscript, index=-1)

        # visit name
        self.visit(node.name)

        # check scope for name
        self.__check_scope(node=node.name, line=self.__getline(node.name))

        # assert new type for node
        node.type = Type(names=node.name.type.names[1:], coord=node.coord)


    def visit_Assert(self, node):
        """
            A method used to represent a visit of Assert node.

            ...

            Parameters
            ----------
                node : Node
                    The Assert node.

        """
        # visit expression
        self.visit(node.expr)

        # check if expr has a type and if is a bool
        self.__check_type(func_name="Assert", type_name="bool", node=node.expr)


    def visit_Assignment(self, node):
        """
            A method used to represent a visit of Assignment node.

            ...

            Parameters
            ----------
                node : Node
                    The Assignment node.

        """
        # get line
        line = self.__getline(node)

        # first we visit the right value
        self.visit(node.right_value)

        # now we check on the left side
        self.visit(node.left_value)
        # the left side must be a location, so we check it
        self.__check_scope(node=node.left_value, line=line)
        # get the type of left value
        left_value_type = node.left_value.type.names[-1]

        # check two types
        self.__check_two_types(node=node, line=line, func='assign', index=0)

        # check if ops are supported
        self.__check_operand_match(operator=node.op, node=left_value_type, operand_type='assign_ops', line=line, func_name='Assignment')


    def visit_BinaryOp(self, node):
        """
            A method used to represent a visit of BinaryOp node.

            ...

            Parameters
            ----------
                node : Node
                    The BinaryOp node.

        """
        # get line
        line = self.__getline(node)
        # visit left operand
        self.visit(node.left_value)

        # need to deal if Constant because
        # they have a diff class attrs names
        if isinstance(node.left_value, Constant):
            ltype = node.left_value.rawtype.names[-1]
        else:
            ltype = node.left_value.type.names[-1]

        # visit right operand
        self.visit(node.right_value)

        # assert type
        self.__check_two_types(node=node, line=line, func='binop')

        # checks if the operands match
        if node.op in ltype.binary_ops:
            node.type = Type([ltype], node.coord)
        elif node.op in ltype.rel_ops:
            node.type = Type([self.__typemap("bool")], node.coord)
        else:
            assert False, line + f"Binary Operator {node.op} not supported by {ltype}"


    def visit_Break(self, node):
        """
            A method used to represent a visit of Break node.

            ...

            Parameters
            ----------
                node : Node
                    The Break node.

        """
        # get break line
        line = self.__getline(node)

        # assert if break is inside a loop
        assert self.environment.cur_loop != [], line + "Break must be inside a loop!"

        # bind the break with current loop
        node.bind = self.environment.cur_loop[-1]


    def visit_Cast(self, node):
        """
            A method used to represent a visit of Cast node.

            ...

            Parameters
            ----------
                node : Node
                    The Cast node.

        """
        # visit expression
        self.visit(node.expression)
        # visit new type
        self.visit(node.to_type)
        # add type to node
        node.type = Type(node.to_type.names, node.coord)


    def visit_Compound(self, node):
        """
            A method used to represent a visit of Compound node.

            ...

            Parameters
            ----------
                node : Node
                    The Compound node.

        """
        # visit all items from block_items compound
        for block_item in node.block_items:
            self.visit(block_item)


    def visit_Constant(self, node):
        """
            A method used to represent a visit of Constant node.

            ...

            Parameters
            ----------
                node : Node
                    The Constant node.

        """
        if not isinstance(node.type, uCType):
            _type = self.__typemap(node.type)
            node.rawtype = Type(names=[_type], coord=node.coord)

            if _type.typename == 'int':
                node.value = int(node.value)
            elif _type.typename == 'float':
                node.value = float(node.value)
            # the [1:-1] is used because the sting
            # come as '"asdsd"'
            elif _type.typename == 'string':
                node.value = str(node.value[1:-1])


    def visit_Decl(self, node):
        """
            A method used to represent a visit of Decl node.

            ...

            Parameters
            ----------
                node : Node
                    The Decl node.

        """
        # first visit declaration type
        self.visit(node.type)

        # add bind
        node.name.bind = node.type

        # get var and var line
        var = node.name.name
        line_var = self.__getline(node.name)

        # if pointer, get the type of the pointer
        _type = node.type
        if isinstance(_type, PtrDecl):
            while isinstance(_type, PtrDecl):
                _type = _type.type

        # threat if the declarations is a function declaration
        if isinstance(_type, FuncDecl):
            assert self.environment.lookup(var), line_var + f"{var} isnt defined!"
        else:
            assert self.environment.find(var), line_var + f"{var} isnt defined!"

            if node.init:
                self.__check_init(_type, node.init, var, line_var)


    def visit_DeclList(self, node):
        """
            A method used to represent a visit of DeclList node.

            ...

            Parameters
            ----------
                node : Node
                    The DeclList node.

        """
        # just visit all declarations
        for decl in node.decls:
            self.visit(decl)
            self.environment.func_def.decls.append(decl)


    def visit_EmptyStatement(self, node):
        """
            A method used to represent a visit of EmptyStatement node.

            If EmptyStatement do nothing!
            ...

            Parameters
            ----------
                node : Node
                    The EmptyStatement node.

        """
        pass


    def visit_ExprList(self, node):
        """
            A method used to represent a visit of ExprList node.

            ...

            Parameters
            ----------
                node : Node
                    The ExprList node.

        """
        # just visit all expressions
        for expr in node.exprs:
            self.visit(expr)
            if isinstance(expr, ID):
                assert expr.scope is not None, f'{self.__getline(node)} {expr.name} isnt defined.'


    def visit_For(self, node):
        """
            A method used to represent a visit of For node.

            ...

            Parameters
            ----------
                node : Node
                    The For node.

        """
        # add current loop to env
        self.environment.cur_loop.append(node)

        # add node to the stack
        if isinstance(node.for_init, DeclList):
            self.environment.push(node)

        # visit all nodes attrs
        self.visit(node.for_init)
        self.visit(node.for_cond)
        self.visit(node.for_next)
        self.visit(node.for_statement)

        # take node back from the stack
        if isinstance(node.for_init, DeclList):
            self.environment.pop()

        #  pop current loop
        self.environment.cur_loop.pop()


    def visit_FuncCall(self, node):
        """
            A method used to represent a visit of FuncCall node.

            ...

            Parameters
            ----------
                node : Node
                    The FuncCall node.

        """

        # visit the ID - miguezao btw
        self.visit(node.name)

        # get line
        func_line = self.__getline(node)

        # get func label
        func_label = self.environment.lookup(node.name.name)

        # check for func label
        assert func_label.kind == 'func', func_line + f'{func_label.name} isnt a function.'

        # update node type
        node.type = func_label.type

        # check func args
        if node.args:
            if isinstance(func_label.bind, PtrDecl):
                assert func_label.bind.type.args is not None, func_line + f'Illegal argument to function {func_label.name}.'
            else:
                assert func_label.bind.args is not None, func_line + f'Illegal argument to function {func_label.name}.'

            # get id bind
            sig = func_label.bind

            if isinstance(node.args, ExprList):
                # deal if args is a list of expressions

                # check if number of args matchs
                if isinstance(sig, PtrDecl):
                    assert len(sig.type.args.params) == len(node.args.exprs), func_line + f'num of args on {func_label.name} mismatch.'
                    sig_args = sig.type.args.params
                else:
                    assert len(sig.args.params) == len(node.args.exprs), func_line + f'num of args on {func_label.name} mismatch.'
                    sig_args = sig.args.params

                for arg, fpar in zip(node.args.exprs, sig_args):
                    # get arg line
                    arg_line = self.__getline(arg)

                    # visit arg
                    self.visit(arg)

                    # deal if arg is an ID
                    if isinstance(arg, ID):
                        assert self.environment.find(arg.name), arg_line + f"{arg.name} is already used."

                    # assert if types are equal
                    if isinstance(arg, Constant):
                        assert arg.rawtype.names == fpar.type.type.names,\
                            arg_line + f"{fpar.type.declname.name} mismatch type."
                    else:
                        assert arg.type.names == fpar.type.type.names,\
                            arg_line + f"{fpar.type.declname.name} mismatch type."
            else:
                # deal if arg is a single expression
                # visit the arg
                self.visit(node.args)

                # check if number of args matchs
                assert len(sig.args.params) == 1, func_line + f'num of args on {func_label.name} mismatch.'

                # get type
                sig_arg_type = sig.args.params[0].type

                # get vardecl obj
                while not isinstance(sig_arg_type, VarDecl):
                    sig_arg_type = sig_arg_type.type

                # assert if types are equal
                # need to deal if Constant because
                # they have a diff class attrs names
                if isinstance(node.args, Constant):
                    assert node.args.rawtype.names == sig_arg_type.type.names, func_line + f"{sig.args.params[0].name.name} mismatch type."
                else:
                    assert node.args.type.names == sig_arg_type.type.names, func_line + f"{sig.args.params[0].name.name} mismatch type."
        else:
            assert func_label.bind.args is None, func_line + f"{func_label.name} receives an empty values as argument."


    def visit_FuncDecl(self, node):
        """
            A method used to represent a visit of FuncDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The FuncDecl node.

        """
        # first we visit the type
        self.visit(node.type)

        # get func from env, modify and push back to stack
        func_decl = self.environment.lookup(node.type.declname.name)
        func_decl.kind = "func"

        func_decl.bind = node.args
        self.environment.push(node)

        # check for func args
        for arg in node.args or []:
            self.visit(arg)


    def visit_FuncDef(self, node):
        """
            A method used to represent a visit of FuncDef node.

            ...

            Parameters
            ----------
                node : Node
                    The FuncDef node.

        """
        # control declarations inside a function
        node.decls = []
        # save func ref on enviroment
        self.environment.func_def = node

        # first visit the func return
        self.visit(node.spec)

        # then visit the func declaration
        self.visit(node.decl)

        # after we visit all the function parameters
        for param in node.param_decls or []:
            self.visit(param)

        # then visit the func body
        for body in node.body or []:
            self.visit(body)

        # pop func from env stack
        self.environment.pop()

        # correct func modifiers
        node.spec = (self.environment.lookup(node.decl.name.name)).type


    def visit_GlobalDecl(self, node):
        """
            A method used to represent a visit of GlobalDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The GlobalDecl node.

        """
        # visit all declarations
        for decl in node.decls:
            self.visit(decl)


    def visit_ID(self, node):
        """
            A method used to represent a visit of ID node.

            ...

            Parameters
            ----------
                node : Node
                    The ID node.

        """
        # look for node in enviroment
        id_node = self.environment.lookup(node.name)

        # if id node exists
        if id_node:
            # add type
            node.type = id_node.type
            # add kind
            node.kind = id_node.kind
            # add scope
            node.scope = id_node.scope
            # add bind
            node.bind = id_node.bind


    def visit_If(self, node):
        """
            A method used to represent a visit of If node.

            ...

            Parameters
            ----------
                node : Node
                    The If node.

        """
        # visit conditional
        self.visit(node.if_cond)

        # check if cond is bool
        self.__check_type(func_name="If", type_name="bool", node=node.if_cond)

        # visit true node
        self.visit(node.if_true)

        # visit false node
        if node.if_false:
            self.visit(node.if_false)


    def visit_InitList(self, node):
        """
            A method used to represent a visit of InitList node.

            ...

            Parameters
            ----------
                node : Node
                    The InitList node.

        """
        # visit all expressions
        for expression in node.expressions:
            self.visit(expression)


    def visit_ParamList(self, node):
        """
            A method used to represent a visit of ParamList node.

            ...

            Parameters
            ----------
                node : Node
                    The ParamList node.

        """
        # visit all the parameters
        for param in node.params:
            self.visit(param)


    def visit_Print(self, node):
        """
            A method used to represent a visit of Print node.

            ...

            Parameters
            ----------
                node : Node
                    The Print node.

        """
        # check expressions exist and the visit it

        if isinstance(node.expr, ExprList):
            aux = node.expr
        elif node.expr:
            aux = [node.expr]
        else:
            aux = []

        for expr in aux:
            self.visit(expr)
            # check if var is declared
            if isinstance(expr, (ArrayRef, ID)):
                self.__check_scope(expr, self.__getline(node))


    def visit_Program(self,node):
        """
            A method used to represent a visit of Program node.

            1. Visit all of the global declarations
            2. Record the associated symbol table
            ...

            Parameters
            ----------
                node : Node
                    The Program node.

        """
        node.environment = self.environment
        node.symble_table = self.environment.peek()
        # 1. Visit all of the statements
        for gdecl in node.gdecls:
            self.visit(gdecl)

        # add check for see if main exists
        if self.environment.find('main') == False:
            assert False, self.__getline(node) + f'uC code must have a main function.'


    def visit_PtrDecl(self, node):
        """
            A method used to represent a visit of PtrDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The PtrDecl node.

        """
        # visit the node type first
        self.visit(node.type)

        # gets type
        _type = node.type

        # loop to make type be a VarDecl
        while not isinstance(_type, VarDecl):
            _type = _type.type

        # insert type
        _type.type.names.insert(0, self.__typemap("ptr"))


    def visit_Read(self, node):
        """
            A method used to represent a visit of Read node.

            ...

            Parameters
            ----------
                node : Node
                    The Read node.

        """
        if isinstance(node.names, ExprList):
            aux = node.names.exprs
        else:
            aux = [node.names]

        for name in aux:
            self.visit(name)
            if isinstance(name, (ID, ArrayRef)):
                self.__check_location(var=name)
            else:
                assert False, self.__getline(name) + f"Constant is not a variable."


    def visit_Return(self, node):
        """
            A method used to represent a visit of Return node.

            ...

            Parameters
            ----------
                node : Node
                    The Return node.

        """
        if node.expression:
            self.visit(node.expression)
            # need to deal if Constant because
            # they have a diff class attrs names
            if isinstance(node.expression, Constant):
                _type = node.expression.rawtype.names
            else:
                _type = node.expression.type.names
        else:
            _type = [self.__typemap('void')]

        cur_rtype = self.environment.cur_rtype
        line = self.__getline(node)

        assert _type == cur_rtype, line + f"return {_type[0].typename} is incompatible with {cur_rtype[0].typename}."


    def visit_Type(self, node):
        """
            A method used to represent a visit of Type node.

            ...

            Parameters
            ----------
                node : Node
                    The Type node.

        """
        # iterate over names convert str
        # to uctype obj
        for i, name in enumerate(node.names or []):
            if not isinstance(name, uCType):
                # gets a uCType object
                node.names[i] = self.__typemap(name)


    def visit_VarDecl(self, node):
        """
            A method used to represent a visit of VarDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The VarDecl node.

        """
        # firs we adjust the type
        self.visit(node.type)

        # get var name and visit it
        self.visit(node.declname)

        if isinstance(node.declname, ID):
            # check the location
            declname_line = self.__getline(node.declname)
            # assert the declaration dont exist
            assert not self.environment.find(node.declname.name), declname_line + f"{node.declname.name} already defined."

            # add the var to the symbol table
            self.environment.add_local(identifier=node.declname, kind='var')

            # copy the type to the id
            node.declname.type = node.type


    def visit_UnaryOp(self, node):
        """
            A method used to represent a visit of UnaryOp node.

            ...

            Parameters
            ----------
                node : Node
                    The UnaryOp node.

        """
        # get line
        line = self.__getline(node)

        # visit expression
        self.visit(node.expr)

        # check if the expression had been defined
        self.__check_scope(node=node.expr, line=self.__getline(node.expr))

        # get expression type
        expression_type = node.expr.type.names[-1]

        # check if operand is valid
        self.__check_operand_match(operator=node.op, node=expression_type, operand_type='unary_ops', line=line, func_name='Unary')

        # update node type
        node.type = Type(names=list(node.expr.type.names), coord=node.coord)

        # special check for operand
        if node.op == '*':
            node.type.names.pop(0)
        elif node.op == '&':
            node.type.names.insert(0, self.__typemap('ptr'))


    def visit_While(self, node):
        """
            A method used to represent a visit of While node.

            ...

            Parameters
            ----------
                node : Node
                    The While node.

        """
        # add current loop to env
        self.environment.cur_loop.append(node)
        self.visit(node.while_cond)
        cond_type = node.while_cond.type.names[-1]

        line = self.__getline(node)

        assert cond_type == BoolType, line + "While conditional type isnt a BoolType"

        if node.while_stmt:
            self.visit(node.while_stmt)

        #  pop current loop
        self.environment.cur_loop.pop()
