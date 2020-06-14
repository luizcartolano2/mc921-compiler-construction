"""
#################################################
# uc_codegen.py                                 #
#                                               #
# Code for uC Code Generator                    #
#                                               #
# Authors: Luiz Cartolano && Erico Faustino     #
#################################################
"""
import uc_sema
from uc_ast import *
from uc_type import *

class GenerateCode(NodeVisitor):
    """
        A Code Generator for the uC language.

        ...

        Methods
        -------
            __new_temp(self)
                A method used to allocate local spaces
                on the interpreter.

            __new_global_codes(self)
                A method used to allocate global spaces
                on the interpreter.

            __load_location(self, node)
                A method used to load an ID or Array
                from mem to registers.

            visit_*(self, node)
                The methods that implements visit to all
                AST nodes
    """
    def __init__(self):
        super(GenerateCode, self).__init__()

        # all the other attrs are private
        # version dictionary for temporaries
        self.__fname = '_glob_'  # We use the function name as a key
        self.__versions = {self.__fname:0}

        # attributes to manage function state
        self.__func_alloc_phase = None
        self.__func_ret_location = None
        self.__func_ret_label = None

        # The generated code (list of tuples)
        # code needs to be public for the uc mod
        # access it
        self.code = []
        self.global_codes = []
        self.queue = []

        # binary opcodes table
        self.__binary_opcodes = {
            "+" : "add",
            "-" : "sub",
            "*" : "mul",
            "/" : "div",
            "%" : "mod",
            "&&": "and",
            "||": "or",
            "==": "eq",
            "!=": "ne",
            ">" : "gt",
            "<" : "lt",
            ">=": "ge",
            "<=": "le",
        }

        # unary operators
        self.__unary_opcodes = {
            '+'  : '',
            '-'  : 'sub',
            '++' : 'add',
            '--' : 'sub',
            'p++': 'add',
            'p--': 'sub',
            '*'  : 'pointer',
            '&'  : 'address',
        }

        # assign ops
        self.__assing_opcodes = {
            "+=" : "add",
            "-=" : "sub",
            "*=" : "mul",
            "/=" : "div",
            "%=" : "mod",
        }


    def __new_temp(self, temp_name=None):
        """
            A method used to allocate local spaces
            on the interpreter.

            ...

            Parameters
            ----------
                None
        """
        # check if __fname is already been defined
        # if not create it
        if self.__fname not in self.__versions:
            self.__versions[self.__fname] = 0

        if temp_name is not None:
            name = f"%{temp_name}"
        else:
            # create register name and add one to counter
            name = "%" + "%d" % (self.__versions[self.__fname])
            self.__versions[self.__fname] += 1

        # return the name
        return name


    def __new_global_codes(self):
        """
            A method used to allocate global spaces
            on the interpreter.

            ...

            Parameters
            ----------
                None
        """
        # create global name and add one to counter
        name = f'@.str.{self.__versions["_glob_"]}'
        self.__versions["_glob_"] += 1

        # return the name
        return name


    def __load_location(self, node):
        """
            A method used to load an ID or Array
            from mem to registers.

            ...

            Parameters
            ----------
                node : Node
                    Can be any Node obj.
        """
        # get new register to load the
        # variable
        # import pdb; pdb.set_trace()
        varname = self.__new_temp()

        # get the type for load
        typename = node.type.names[-1].typename

        # if referencing an array we need to
        # append the _* to end of type to reproduce
        # professor behavior
        if isinstance(node, ArrayRef):
            typename += '_*'
        elif isinstance(node, ArrayDecl):
            # Same happens if deals with arrays
            # of arrays, on that case we must
            # add the index of assignment to
            # reproduce prof behavior
            if hasattr(node.bin, 'dimension'):
                typename += f'_{node.bin.dimension.value}'
            else:
                typename += f'_{node.bin.dim.value}'

        # load the variable to the register
        self.code.append((f'load_{typename}', node.location, varname))

        # update node location
        node.location = varname


    # You must implement visit_Nodename methods for all of the other
    # AST nodes.  In your code, you will need to make instructions
    # and append them to the self.code list.
    #
    # A few sample methods follow.  You may have to adjust depending
    # on the names of the AST nodes you've defined.
    def visit_ArrayDecl(self, node, decl, dim=""):
        """
            A method used to represent a visit of ArrayDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The ArrayDecl node.

                decl : Node
                    The Decl node.

                dim : str
                    The array dimension.
        """
        # first get a copy of the node reference
        node_type = node

        # update the dimension value
        dim += f'_{node.dimension.value}'

        # iterate over node type until we get
        # in a VarDecl type
        while not isinstance(node_type, VarDecl):
            # get the type of the type
            node_type = node_type.type

            # if we have an array of arrays
            # something like a[3][2] we add the
            # new dimension
            if isinstance(node_type, ArrayDecl):
                dim += f'_{node_type.dimension.value}'

        # force visit to the VarDecl function
        self.visit_VarDecl(node_type, decl, dim)


    def visit_ArrayRef(self, node):
        """
            A method used to represent a visit of ArrayRef node.

            ...

            Parameters
            ----------
                node : Node
                    The ArrayRef node.
        """
        # first we visit the associated
        # subscription for the ArrayRef
        node_subs_i = node.subscript
        self.visit(node_subs_i)

        # if the node.name is an ArrayRef it means
        # we are dealing with arrays of arrays like
        # a[][], otherwise, its a single dimension
        # array, like a[]
        if isinstance(node.name, ArrayRef):
            # if arrays of arrays we need to get
            # the other subscription
            node_subs_j = node.name.subscript
            self.visit(node_subs_j)

            # gets array dimension and visit it
            dim = node.name.name.bind.type.dimension
            self.visit(dim)

            # if we are dealing with an ID or referencing
            # an Array we need to load it on memory first
            if isinstance(node_subs_j, (ID, ArrayRef)):
                self.__load_location(node_subs_j)

            # create a label to allocate
            # the array
            target = self.__new_temp()

            # get array type
            typename = node.type.names[-1].typename

            # get the position to access on memory
            self.code.append((f'mul_{typename}', dim.location, node_subs_j.location, target))

            # if we are dealing with an ID or referencing
            # an Array we need to load it on memory first
            if isinstance(node_subs_i, (ID, ArrayRef)):
                self.__load_location(node_subs_i)

            # create a label to allocate
            # the index pos of the array
            index = self.__new_temp()
            self.code.append((f'add_{typename}', target, node_subs_i.location, index))

            # gets the element and update
            # location on node attr
            var = node.name.name.bind.type.type.declname.location
            node.location = self.__new_temp()
            self.code.append((f'elem_{typename}', var, index, node.location))

        else:
            # if we are dealing with an ID or referencing
            # an Array we need to load it on memory first
            if isinstance(node_subs_i, (ID, ArrayRef)):
                self.__load_location(node_subs_i)

            # gets array loc
            var = node.name.bind.type.declname.location

            # get index to access on array
            index = node_subs_i.location

            # gets the element and update
            # location on node attr
            target = self.__new_temp()
            node.location = target
            self.code.append((f'elem_{node.type.names[-1].typename}', var, index, target))


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

        # create labels on register for the
        # true, false and exit branches
        true_label = self.__new_temp()
        false_label = self.__new_temp()
        exit_label = self.__new_temp()

        # creates the branchs for conditions
        # it has the label of the assert expression and
        # where to jumps either if assertation fails or succeed
        self.code.append(('cbranch', node.expr.location, true_label, false_label))

        # deal if the assert is true
        self.code.append((true_label[1:], ))
        self.code.append(('jump', exit_label))

        # deal if the assert is false
        # create false label
        self.code.append((false_label[1:], ))

        # create sting to print on false label
        target = self.__new_global_codes()
        self.global_codes.append(('global_string', target, f'assertion_fail on {node.coord.line}:{node.coord.column}'))

        # add print string command
        self.code.append(('print_string', target))

        # assert breaks exec if fails
        self.code.append(('jump', '%1'))

        # create exit label on interpreter
        self.code.append((exit_label[1:], ))


    def visit_Assignment(self, node):
        """
            A method used to represent a visit of Assignment node.

            ...

            Parameters
            ----------
                node : Node
                    The Assignment node.

        """
        # visit right side first
        self.visit(node.right_value)

        # if we are dealing with an ID or referencing
        # an Array we need to load it on memory first.
        if isinstance(node.right_value, (ID, ArrayRef)):
            self.__load_location(node.right_value)

        # visit the left side of assignment
        left_node = node.left_value
        self.visit(left_node)

        # check if operation is an assign one
        # like += / -= / *= / /= or %= if yes
        # a special treatment is given
        if node.op in self.__assing_opcodes:
            # get type of left node
            left_node_type = left_node.type.names[-1].typename

            left_value = self.__new_temp()
            target = self.__new_temp()

            # need to deal if Constant because
            # they have a diff class attrs names
            if isinstance(left_node, Constant):
                typename = left_node.rawtype.typename
            else:
                typename = left_node.type.names[-1].typename

            # if referencing an array we need to
            # append the _* to end of type to reproduce
            # professor behavior
            if isinstance(node.right_value, ArrayRef):
                typename += '_*'

            # before doing the operation we must
            # load the value to a register in order
            # to be able to perform the operation
            # like on x *= i + 1
            self.code.append((f'load_{typename}', left_node.location, left_value))

            # gets the operation opcode
            # and create instruction to
            # the register performs it
            opcode = f'{self.__assing_opcodes[node.op]}_{left_node_type}'
            self.code.append((opcode, node.right_value.location, left_value, target))

            # store the operation result
            # on the created target
            self.code.append((f'store_{left_node_type}', target, left_node.location))

        else:
            if isinstance(left_node, (ID, ArrayRef)):
                typename = left_node.type.names[-1].typename

                # if referencing an array we need to
                # append the _* to end of type to reproduce
                # professor behavior. Same happens if deals
                # with arrays of arrays, on that case we must
                # add the index of assignment
                if isinstance(left_node, ArrayRef):
                    typename += '_*'
                elif isinstance(left_node.bind, ArrayDecl):
                    typename += f'_{left_node.bind.dimension.value}'

                # if the left value is a function
                # we also need to make a special
                # treat in order to load the right
                # locations to the interpreter
                if hasattr(left_node, 'kind'):
                    if left_node.kind == 'func':
                        left_value_loc = left_node.location
                    else:
                        left_value_loc = left_node.location
                else:
                    left_value_loc = left_node.location
                # get locations
                right_value_loc = node.right_value.location

            else:
                # if not deals with special classes
                # just get the var type
                typename = left_node.type.names[-1].typename
                right_value_loc = node.right_value.location
                left_value_loc = left_node.location

            # store the operation result
            # on the created target
            self.code.append((f'store_{typename}', right_value_loc, left_value_loc))


    def visit_BinaryOp(self, node):
        """
            A method used to represent a visit of BinaryOp node.

            ...

            Parameters
            ----------
                node : Node
                    The BinaryOp node.

        """
        # visit the left side of the operation
        self.visit(node.left_value)
        # visit the left side of the operation
        self.visit(node.right_value)

        # if we are dealing with an ID or referencing an Array
        # we need to load it on memory first. This is valid for
        # both sides of operation, so we repeat it twice
        if isinstance(node.left_value, (ID, ArrayRef)):
            self.__load_location(node.left_value)

        if isinstance(node.right_value, (ID, ArrayRef)):
            self.__load_location(node.right_value)

        # allocate the target register to
        # store the operation result
        target = self.__new_temp()

        # create the opcode of instruction, need to deal if Constant
        # because they have a diff classes attr name
        if isinstance(node.left_value, Constant):
            opcode = f'{self.__binary_opcodes[node.op]}_{node.left_value.rawtype.names[-1].typename}'
        else:
            opcode = f'{self.__binary_opcodes[node.op]}_{node.left_value.type.names[-1].typename}'

        # create the instruct to the binary operation
        self.code.append((opcode, node.left_value.location, node.right_value.location, target))

        # update node location
        node.location = target


    def visit_Break(self, node):
        """
            A method used to represent a visit of Break node.

            ...

            Parameters
            ----------
                node : Node
                    The Break node.

        """
        # break generates a pretty simple
        # instruction, that just indicates
        # to jump to the exit label of the
        # associated loop
        self.code.append(('jump', node.bind.for_exit))


    def visit_Cast(self, node):
        """
            A method used to represent a visit of Cast node.

            ...

            Parameters
            ----------
                node : Node
                    The Cast node.

        """
        # visit the expression
        self.visit(node.expression)

        # if we are dealing with an ID or referencing an Array
        # we need to load it on memory first
        if isinstance(node.expression, (ID, ArrayRef)):
            self.__load_location(node.expression)

        # allocate a new register to make the cast
        temp = self.__new_temp()

        # check if the cast is a int
        # to float or a float to int
        if node.to_type.names[-1].typename == uc_sema.IntType.typename:
            cast_op = 'fptosi'
        else:
            cast_op = 'sitofp'

        # create the cast instruction
        self.code.append((cast_op, node.expression.location, temp))

        # update node information about
        # the cast operation location
        node.location = temp


    def visit_Compound(self, node):
        """
            A method used to represent a visit of Compound node.

            ...

            Parameters
            ----------
                node : Node
                    The Compound node.

        """
        # visit all blocks
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
        # in order to reproduce the professor behavior
        # we are going to make all strings to be declared
        # as global definitions, because of it, strings
        # are going to receive a special treatment
        if node.type == "string":
            # here we check if string already
            # exists in the memory, if yes we
            # dont realocate it just getting the
            # previous value
            temp = [item for item in self.global_codes if item[-1] == node.value]
            if len(temp) == 0:
                # generates the label to a new global declaration
                target = self.__new_global_codes()

                # creates the instruction to the global string
                self.global_codes.append(('global_string', target, node.value))
            else:
                target = temp[0][1]

        else:
            # generates the label to a new local declaration
            target = self.__new_temp()

            # creates the instruction to the literal
            self.code.append((f'literal_{node.type}', node.value, target))

        # update the constant node location
        node.location = target


    def visit_Decl(self, node):
        """
            A method used to represent a visit of Decl node.

            ...

            Parameters
            ----------
                node : Node
                    The Decl node.

        """
        # the Decl visit will identify the type of the
        # declaration and make a force visit to the node
        # that handles it
        if isinstance(node.type, ArrayDecl):
            self.visit_ArrayDecl(node.type, node)
        elif isinstance(node.type, FuncDecl):
            self.visit(node.type)
        elif isinstance(node.type, PtrDecl):
            raise NotImplementedError
        elif isinstance(node.type, VarDecl):
            self.visit_VarDecl(node.type, node)


    def visit_DeclList(self, node):
        """
            A method used to represent a visit of DeclList node.

            ...

            Parameters
            ----------
                node : Node
                    The DeclList node.

        """
        # visit all declaraions
        for decl in node.decls:
            self.visit(decl)


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
            If ExprList do nothing!

            ...

            Parameters
            ----------
                node : Node
                    The ExprList node.
        """
        pass


    def visit_For(self, node):
        """
            A method used to represent a visit of For node.

            ...

            Parameters
            ----------
                node : Node
                    The For node.

        """
        # create labels on register for the
        # entry, true and exit branches
        entry_label = self.__new_temp()
        true_label = self.__new_temp()
        exit_label = self.__new_temp()
        node.for_exit = exit_label

        # visit init and start it on interpreter
        self.visit(node.for_init)
        self.code.append((entry_label[1:], ))

        # branch to for condition, keeps on the loop while
        # while true and branch out of the loop when cond fails

        # first visit the cond
        self.visit(node.for_cond)

        # create the loop branch
        self.code.append(('cbranch', node.for_cond.location, true_label, exit_label))

        # add to register pos to jump while label is true
        self.code.append((true_label[1:], ))

        # visit for statement
        self.visit(node.for_statement)

        # visit gor iterator
        self.visit(node.for_next)

        # jump back to the loop
        self.code.append(('jump', entry_label))

        # create exit label on register for cbranch works
        self.code.append((exit_label[1:], ))


    def visit_FuncCall(self, node):
        """
            A method used to represent a visit of FuncCall node.

            ...

            Parameters
            ----------
                node : Node
                    The FuncCall node.
        """
        # first check if function has
        # args to avoid errors
        if node.args is not None:
            # if the args come as list of expressions
            # we do a special treatment
            if isinstance(node.args, ExprList):
                # iterate over func arguments
                for arg in node.args.exprs:
                    # visit the argument
                    self.visit(arg)
                    # if we are dealing with an ID or referencing an Array
                    # we need to load it on memory first.
                    if isinstance(arg, (ID, ArrayRef)):
                        self.__load_location(arg)

                    # create the instruct to the parameter
                    if isinstance(arg, Constant):
                        self.code.append((f'param_{arg.rawtype.names[-1].typename}', arg.location))
                    else:
                        self.code.append((f'param_{arg.type.names[-1].typename}', arg.location))
            else:
                self.visit(node.args)

                # if we are dealing with an ID or referencing an Array
                # we need to load it on memory first.
                if isinstance(node.args, (ID, ArrayRef)):
                    self.__load_location(node.args)

                # need to deal if Constant because
                # they have a diff classes attr name
                if isinstance(node.args, Constant):
                    typename = node.args.rawtype.names[-1].typename
                else:
                    typename = node.args.type.names[-1].typename

                # create the instruct to the parameter
                self.code.append((f'param_{typename}', node.args.location))

        # update node location with a IR target
        node.location = self.__new_temp()

        # visit func name
        self.visit(node.name)
        # create the instruct to the function call
        self.code.append(('call', node.name.location, node.location))


    def visit_FuncDecl(self, node):
        """
            A method used to represent a visit of FuncDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The FuncDecl node.
        """
        # get func name and set it to an class attr
        # we do this way because that is an important
        # info to know in other moments of the visiting
        self.__fname = f'@{node.type.declname.name}'

        # add intruct to define the function
        self.code.append(('define', self.__fname))
        # update function loc
        node.type.declname.location = self.__fname

        # visit the function arguments
        if node.args is not None:
            # makes sure the quere of args is empty
            self.queue = []

            # iterate over the args alloc registers
            # for them, we put them on a stack (LIFO)
            # so we can pop this registers location when
            # initializing the function args
            for _ in node.args.params:
                self.queue.insert(0, self.__new_temp())

        # create label/location to where function returns
        # we do this way (a class attr) because that
        # is an important info to know in other moments
        # of the visiting like on Breaks
        self.__func_ret_location = self.__new_temp()
        self.__func_ret_label = self.__new_temp()

        # now we do two works while declaring
        # the function first, we iterate over
        # all arguments declaring then
        self.__func_alloc_phase = 'arg_decl'
        for arg in node.args or []:
            self.visit(arg)

        # after, we iterate over
        # all arguments initalizing then
        self.__func_alloc_phase = 'arg_init'
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
        # visit declaration
        self.__func_alloc_phase = None
        self.visit(node.decl)

        # iterate over params
        for par in node.param_decls or []:
            self.visit(par)

        # if the function has a body we need
        # to iterate over ir, declaring/initializing
        # variables and others
        if node.body is not None:
            # now we do two works while defining
            # the function, first, we iterate over
            # all body visiting the declarations
            self.__func_alloc_phase = 'var_decl'
            for body in node.body:
                if isinstance(body, Decl):
                    self.visit(body)

            # then, we iterate over all
            # declarations visiting them
            for decl in node.decls:
                self.visit(decl)

            # after, we iterate over
            # all body initalizing then
            self.__func_alloc_phase = 'var_init'
            for body in node.body:
                self.visit(body)

        # append the label/location to where
        # function returns to the list of
        # opcodes
        self.code.append((self.__func_ret_label[1:], ))

        # deal with the function return
        # void functions deserves a special
        # treatment
        if node.spec.names[-1].typename == 'void':
            self.code.append(('return_void', ))
        else:
            # if function isnt void then
            # we must create a new label to
            # the return value and get the type
            return_value = self.__new_temp()
            typename = node.spec.names[-1].typename

            # add instructions to load the
            # return value and then return it
            self.code.append((f'load_{typename}', self.__func_ret_location, return_value))
            self.code.append((f'return_{typename}', return_value))


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
            # makes sure its not a FuncDecl
            if not isinstance(decl.type, FuncDecl):
                self.visit(decl)
            # if it is a FuncDecl we will
            # make a special treat if the
            # body of the function is empty
            # in order to assignment works
            elif decl.init is None:
                self.global_codes.append((f'global_{decl.name.type.names[-1].typename}', f'@{decl.name.name}'))
                decl.name.location = f'@{decl.name.name}'


    def visit_ID(self, node):
        """
            A method used to represent a visit of ID node.

            ...

            Parameters
            ----------
                node : Node
                    The ID node.
        """
        # if the node location had already been setted
        # we dont need to make it again
        if not node.location:
            # first we get ID connection
            bind_type = node.bind

            # in order to update the ID location we must
            # get the VarDecl connection he has, so we
            # iterate deeper on the bind type
            while not isinstance(bind_type, VarDecl):
                bind_type = bind_type.type

            # once we get a VarDecl bind type we make the
            # ID location the same of the VarDecl
            node.location = bind_type.declname.location


    def visit_If(self, node):
        """
            A method used to represent a visit of If node.

            ...

            Parameters
            ----------
                node : Node
                    The If node.
        """
        # create labels on register for the
        # true, false and exit branches
        true_label = self.__new_temp()
        false_label = self.__new_temp()
        exit_label = self.__new_temp()

        # visit if conditional
        self.visit(node.if_cond)

        # creates the branchs for conditions
        # it has the label of the condition and where
        # to jumps either if conditions fails or succeed
        self.code.append(('cbranch', node.if_cond.location, true_label, false_label))

        # informs the register the existence of
        # the true label
        self.code.append((true_label[1:], ))

        # visit the true statement
        self.visit(node.if_true)

        # make sure the false statement (else)
        # exists
        if node.if_false:
            # if there is an else create the
            # instruct to jump out of the if/else
            self.code.append(('jump', exit_label))
            # informs the register the existence of
            # the false label
            self.code.append((false_label[1:], ))

            # visit the false statement
            self.visit(node.if_false)

            # informs the register the existence of
            # the exit label
            self.code.append((exit_label[1:], ))
        else:
            # informs the register the existence of
            # the false label that is going to be used
            # as the exit_label
            self.code.append((false_label[1:], ))


    def visit_InitList(self, node):
        """
            A method used to represent a visit of InitList node.

            ...

            Parameters
            ----------
                node : Node
                    The InitList node.
        """
        # first make sure the list of values on InitList is empty
        node.list_values = []

        # go over expressions appending values to the list_values
        # attr of InitList node
        for expr in node.expressions:
            # if we have a list of list a special treatment
            # is required due to diff on attr names
            if isinstance(expr, InitList):
                self.visit(expr)
                node.list_values.append(expr.list_values)
            elif isinstance(expr, Constant):
                node.list_values.append(expr.value)
            else:
                raise NotImplementedError


    def visit_ParamList(self, node):
        """
            A method used to represent a visit of ParamList node.

            ...

            Parameters
            ----------
                node : Node
                    The ParamList node.

        """
        # visit all parameters
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
        # convert all the expressions to a list in order to be
        # able to iterate over then
        if isinstance(node.expr, ExprList):
            aux = node.expr
        elif node.expr:
            aux = [node.expr]
        else:
            # if None is given print void
            self.global_codes.append('print_void', )
            return

        for expr in aux:
            # visit the expr
            self.visit(expr)

            # deal with the name (either an ID or ArrayRef)
            # create a place to load the name
            if isinstance(expr, (ID, ArrayRef)):
                self.__load_location(expr)

            # special treat for Constants because their attr have diff name
            if isinstance(expr, Constant):
                typename = expr.rawtype.names[-1].typename
            else:
                typename = expr.type.names[-1].typename

            # add a print inst
            self.code.append(('print_' + typename, expr.location))


    def visit_Program(self, node):
        """
            A method used to represent a visit of Program node.

            ...

            Parameters
            ----------
                node : Node
                    The Program node.

        """
        # visit all global declarations
        for _decl in node.gdecls:
            self.visit(_decl)

        # append globals to the start of the list, in order to
        # be equals to professor examples of IR
        self.code = self.global_codes + self.code


    def visit_PtrDecl(self, node):
        """
            A method used to represent a visit of PtrDecl node.
            Wasnt implemented.
            ...

            Parameters
            ----------
                node : Node
                    The PtrDecl node.
        """
        raise NotImplementedError


    def visit_Read(self, node):
        """
            A method used to represent a visit of Read node.

            ...

            Parameters
            ----------
                node : Node
                    The Read node.

        """
        # convert all the expressions to a list in order to be
        # able to iterate over then
        if isinstance(node.names, ExprList):
            aux = node.names
        elif node.names:
            aux = [node.names]

        # iterate over Read names
        for name in aux:
            # first we visit the name
            self.visit(name)

            # allocate register to store the read value
            target = self.__new_temp()

            # get the type
            typename = name.type.names[-1].typename

            # add a read inst
            self.code.append(('read_' + typename, target))

            # deal if is an ArrayRef
            if isinstance(name, ArrayRef):
                typename += '_*'

            # add a store inst
            self.code.append(('store_' + typename, target, name.location))


    def visit_Return(self, node):
        """
            A method used to represent a visit of Return node.

            ...

            Parameters
            ----------
                node : Node
                    The Return node.

        """
        # makes sure the expression exists to avoid errors
        if node.expression:
            # visit the expression
            self.visit(node.expression)

            # if we are dealing with an ID or referencing an Array
            # we need to load it on memory first
            if isinstance(node.expression, (ID, ArrayRef)):
                self.__load_location(node.expression)

            # create the store instruction, need to deal if Constant
            # because they have a diff class attrs names
            if isinstance(node.expression, Constant):
                self.code.append(('store_' + node.expression.rawtype.names[-1].typename, node.expression.location, self.__func_ret_location))
            else:
                self.code.append(('store_' + node.expression.type.names[-1].typename, node.expression.location, self.__func_ret_location))

        # create the jump instruction to function label return
        self.code.append(('jump', self.__func_ret_label))


    def visit_Type(self, node):
        """
            A method used to represent a visit of Type node.
            If Type do nothing!

            ...

            Parameters
            ----------
                node : Node
                    The Type node.

        """
        pass


    def visit_VarDecl(self, node, decl, dim=""):
        """
            A method used to represent a visit of VarDecl node.

            ...

            Parameters
            ----------
                node : Node
                    The VarDecl node.
                decl : Node
                    The Decl node.
                dim : str
                    The array dimension.

        """
        if node.declname.scope == 0:
            # get typename
            typename = node.type.names[-1].typename

            # add dim to the typename
            typename += dim

            # add '@' to the varname to indicate is global
            varname = f'@{node.declname.name}'

            # if declaration doesnt come with a init just annouce it exists
            if decl.init is None:
                self.global_codes.append((f'global_{typename}', varname))
            else:
                # if the declaration comes with a list we visit it to get the
                # list of values initialized else just get the value
                if isinstance(decl.init, InitList):
                    self.visit(decl.init)
                    init_val = decl.init.list_values
                elif isinstance(decl.init, Constant):
                    init_val = decl.init.value

                # create the intruct to the global var with the value
                self.global_codes.append((f'global_{typename}', varname, init_val))

            # update the id location with the created spot on registers
            node.declname.location = varname

        else:
            # isnt a global declaration, but a
            # local one get the var type
            typename = node.type.names[-1].typename + dim

            # get var location
            location = node.declname.location

            # we act according to the allocation phase of funtion visit
            if self.__func_alloc_phase in ['arg_decl', 'var_decl']:
                # if declaring an arg or var
                # first we create the register spot
                varname = self.__new_temp(temp_name=node.declname.name)

                # create the instruction to the local declaration
                self.code.append((f'alloc_{typename}', varname))

                # update the id location with the created spot on registers
                node.declname.location = varname

            elif self.__func_alloc_phase == 'arg_init':
                # deal with arg initialization
                # first we get the last arg that was put on queue
                arg = self.queue.pop()

                # create the instruction to the local declaration
                self.code.append((f'store_{typename}', arg, location))

            elif self.__func_alloc_phase == 'var_init':
                # deal with an variable initialization
                # first we make sure the init exist to avoid errors
                if decl.init is not None:
                    # first visit the declaration init
                    self.visit(decl.init)

                    # make a special treatment if we init var with a list
                    if isinstance(decl.init, InitList):
                        # to make the IR looks like to professors (and make sure)
                        # it will work with the uc_interpretor he gave us, we make
                        # the array declaration as global
                        # first create the register alocation
                        target = self.__new_global_codes()

                        # create the instruct for the global array decl
                        self.global_codes.append((f'global_{typename}', target, decl.init.list_values))
                        self.code.append((f'store_{typename}', target, location))
                    else:
                        # deal if init is a single value
                        # if we initiate the var with an ID or Array (previous declared)
                        # we first had to load it to a register
                        if isinstance(decl.init, (ID, ArrayRef)):
                            self.__load_location(decl.init)
                        elif isinstance(decl.init, ArrayDecl):
                            # now, if we are declaring a new array to initiate
                            # we first allocate the register space and then load it
                            decl.init.location = self.__new_temp()
                            self.code.append((f'load_{decl.init.expr.type.names[-1].typename}_*', decl.init.expr.location, decl.init.location))

                        # at least we store the value of initialization to the id node
                        # the code doesnt work with pointers for lack of time
                        self.code.append((f'store_{typename}', decl.init.location, location))


    def visit_UnaryOp(self, node):
        """
            A method used to represent a visit of UnaryOp node.

            ...

            Parameters
            ----------
                node : Node
                    The UnaryOp node.

        """
        # first visit the expression
        self.visit(node.expr)

        # original expr location
        orig_loc = node.expr.location

        # if we are dealing with an ID or referencing an Array
        # we need to load it on memory first
        if isinstance(node.expr, (ID, ArrayRef)):
            self.__load_location(node.expr)

        # make special treatment according to the operator
        if node.op == '!':
            # first we take care of the negation operator
            # if we are dealing with an ID or referencing an Array
            # we need to load it on memory first
            node.location = self.__new_temp()
            # append the not_bool instruc to the list of instructions
            self.code.append(('not_bool', node.expr.location, node.location))
        elif node.op == '+':
            # if the unary oper is an '+', like in '+x' or '+5'
            # it just indicate a positive number, so we just update node
            # location
            node.location = node.expr.location

        # for the next possible operations there are some common attrs that will be used
        # now, we get intruct opcode for further use
        opcode = f'{self.__unary_opcodes[node.op]}_{node.expr.type.names[-1].typename}'

        # allocate two new registers
        aux = self.__new_temp()
        node.location = self.__new_temp()
        # check the remaining operators
        if node.op == '-':
            # if the unary oper is an '-', like in '-x' or '-5'
            # it just indicate a negative number, so we update node
            # location and indicate the literal value

            # create the intruct to the literal number
            self.code.append(('literal_int', 0, aux))

            # create the intruct to the operation
            self.code.append((opcode, 0, node.expr.location, node.location))
        elif node.op in ['++', 'p++', '--', 'p--']:
            # if we deal with  postfix ++ or prefix ++ operators
            # first we get the associated val (if we are adding)
            # like on x++ or ++x, or we are dealing with a subtraction
            # like on --x or x--
            if node.op in ['++', 'p++']:
                val = 1
            else:
                val = -1

            # create the intruct to the literal number to be addedd(1) or subtracted(-1)
            self.code.append(('literal_int', val, aux))

            # create the instruction to the operation
            self.code.append((opcode, node.expr.location, aux, node.location))

            # create a store instruction
            self.code.append((f'store_{node.expr.type.names[-1].typename}', node.location, orig_loc))

            # makes a special location att. if we deal with postfix unary ops
            if node.op in ["p++", "p--"]:
                node.location = node.expr.location


    def visit_While(self, node):
        """
            A method used to represent a visit of While node.

            ...

            Parameters
            ----------
                node : Node
                    The While node.

        """
        # create labels on register for the
        # entry, true and exit branches
        entry_label = self.__new_temp()
        true_label = self.__new_temp()
        exit_label = self.__new_temp()
        node.while_exit = exit_label

        # visit cond and start the loop on interpreter
        self.code.append((entry_label[1:], ))
        self.visit(node.while_cond)

        # branch to for condition, keeps on the loop while
        # while true and branch out of the loop when cond fails
        # create the loop branch
        self.code.append(('cbranch', node.while_cond.location, true_label, exit_label))

        # add to register pos to jump while label is true
        self.code.append((true_label[1:], ))

        # visit for statement
        if node.while_stmt:
            self.visit(node.while_stmt)

        # jump back to the loop
        self.code.append(('jump', entry_label))

        # create exit label on register for cbranch works
        self.code.append((exit_label[1:], ))
