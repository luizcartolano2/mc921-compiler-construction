##################################################
# uc_ast.py                                      #
#                                                #
# AST Node classes.                              #
#                                                #
# Code for the AST Node Classes for the uC BNF.  #
#                                                #
# Authors: Luiz Cartolano && Erico Faustino      #
##################################################


import sys


def _repr(obj):
    """
        Get the representation of an object, with dedicated pprint-like format for lists.
    """
    if isinstance(obj, list):
        return '[' + (',\n '.join((_repr(e).replace('\n', '\n ') for e in obj))) + '\n]'
    else:
        return repr(obj)


class Node(object):
    __slots__ = ()
    """
        Abstract base class for AST nodes.
    """

    def __repr__(self):
        """ Generates a python representation of the current node
        """
        result = self.__class__.__name__ + '('
        indent = ''
        separator = ''

        if self.__class__ == ID:
            result += separator
            result += indent
            result += 'name' + (
                _repr(getattr(self, 'name')).replace('\n', '\n  ' + (' ' * (1 + len(self.__class__.__name__)))))
            separator = ','
            indent = ' ' * len(self.__class__.__name__)
        else:
            for name in self.__slots__[:-1]:
                result += separator
                result += indent
                result += name + '=' + (_repr(getattr(self, name)).replace('\n', '\n  ' + (
                            ' ' * (len(name) + len(self.__class__.__name__)))))
                separator = ','
                indent = ' ' * len(self.__class__.__name__)

        result += indent + ')'

        return result

    def children(self):
        """
            A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and children (recursively) to a buffer.
            buf:
                Open IO buffer into which the Node is printed.
            offset:
                Initial offset (amount of leading spaces)
            attrnames:
                True if you want to see the attribute names in name=value pairs. False to only see the values.
            nodenames:
                True if you want to see the actual node names within their parents.
            showcoord:
                Do you want the coordinates of each Node to be displayed.
        """
        lead = ' ' * offset

        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__ + ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__ + ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self, n)) for n in self.attr_names if getattr(self, n) is not None]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            if self.coord:
                buf.write('%s' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(buf, offset + 4, attrnames, nodenames, showcoord, child_name)


class Coord(object):
    """
        Coordinates of a syntactic element. Consists of:
            - Line number
            - (optional) column number, for the Lexer
    """
    __slots__ = ('line', 'column')

    def __init__(self, line, column=None):
        self.line = line
        self.column = column

    def __str__(self):
        if self.line:
            coord_str = "   @ %s:%s" % (self.line, self.column)
        else:
            coord_str = ""
        return coord_str


class NodeVisitor(object):
    """
        A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.
        For example:
        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []
            def visit_Constant(self, node):
                self.values.append(node.value)
        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:
        cv = ConstantVisitor()
        cv.visit(node)
        Notes:
        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """

    _method_cache = None

    def visit(self, node):
        """ Visit a node.
        """

        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c in node:
            self.visit(c)


class ArrayDecl(Node):
    """
        A class used to represent an array declaration

        ...

        Attributes
        ----------
            type :
                the type (int/float/...) of the array
            dimension :
                the number of elements in the array
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('type', 'dimension', 'coord', 'location')

    def __init__(self, type, dimension, coord=None, location=None):
        self.type = type
        self.dimension = dimension
        self.coord = coord

    def children(self):
        nodelist = []

        if self.type is not None:
            nodelist.append(("type", self.type))

        if self.dimension is not None:
            nodelist.append(("dimension", self.dimension))

        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

        if self.dimension is not None:
            yield self.dimension

    attr_names = ()


class ArrayRef(Node):
    """
        A class used to represent an array reference

        ...

        Attributes
        ----------
            name : 
                the name of the array
            subscript : 
                the subscript reference for the array
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """
    __slots__ = ('name', 'subscript', 'coord', 'type', 'location')

    def __init__(self, name, subscript, coord=None, type=None, location=None):
        self.name = name
        self.subscript = subscript
        self.coord = coord
        self.type = type
        self.location = location

    def children(self):
        nodelist = []

        if self.name is not None:
            nodelist.append(("name", self.name))

        if self.subscript is not None:
            nodelist.append(("subscript", self.subscript))

        return tuple(nodelist)

    def __iter__(self):
        if self.name is not None:
            yield self.name

        if self.subscript is not None:
            yield self.subscript

    attr_names = ()


class Assert(Node):
    """
        A class used to represent an Assert operation

        ...

        Attributes
        ----------
            expr : 
                the expression associated to the assert statement
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('expr', 'coord')

    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):

        nodelist = []

        if self.expr is not None:
            nodelist.append(("expr", self.expr))

        return tuple(nodelist)

    def __iter__(self):

        if self.expr is not None:
            yield self.expr

    attr_names = ()


class Assignment(Node):
    """
        A class used to represent an assignment expression

        ...

        Attributes
        ----------
            op : 
                the assignment operator
            left_value : 
                the left value of the assignment
            right_value : 
                the right value of the assignment
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('op', 'left_value', 'right_value', 'coord')

    def __init__(self, op, left_value, right_value, coord=None):
        self.op = op
        self.left_value = left_value
        self.right_value = right_value
        self.coord = coord

    def children(self):
        nodelist = []

        if self.left_value is not None:
            nodelist.append(("left_value", self.left_value))

        if self.right_value is not None:
            nodelist.append(("right_value", self.right_value))

        return tuple(nodelist)

    def __iter__(self):
        if self.left_value is not None:
            yield self.left_value

        if self.right_value is not None:
            yield self.right_value

    attr_names = ('op',)


class BinaryOp(Node):
    """
        A class used to represent a binary expression

        ...

        Attributes
        ----------
            op : 
                the binary operator
            left_value : 
                the left value of the expression
            right_value : 
                the right value of the expression
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """
    __slots__ = ('op', 'left_value', 'right_value', 'coord', 'type', 'location')

    def __init__(self, op, left_value, right_value, coord=None, type=None, location=None):
        self.op = op
        self.left_value = left_value
        self.right_value = right_value
        self.coord = coord
        self.type = type
        self.location = location

    def children(self):
        nodelist = []

        if self.left_value is not None:
            nodelist.append(("left_value", self.left_value))

        if self.right_value is not None:
            nodelist.append(("right_value", self.right_value))

        return tuple(nodelist)

    def __iter__(self):
        if self.left_value is not None:
            yield self.left_value

        if self.right_value is not None:
            yield self.right_value

    attr_names = ('op',)


class Break(Node):
    """
        A class used to represent a break expression

        ...

        Attributes
        ----------
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """
    __slots__ = ('coord', 'bind')

    def __init__(self, coord=None, bind=None):
        self.coord = coord
        self.bind = bind

    def children(self):
        return tuple()

    def __iter__(self):
        return
        yield

    attr_names = ()


class Cast(Node):
    """
        A class used to represent a binary expression

        ...

        Attributes
        ----------
            to_type : 
                the type expression will have
            expression : 
                the expression to be casted
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    # TODO add type e gen_location

    __slots__ = ('to_type', 'expression', 'coord', 'type', 'location')

    def __init__(self, to_type, expression, coord=None, type=None, location=None):
        self.to_type = to_type
        self.expression = expression
        self.coord = coord
        self.type = type
        self.location = location

    def children(self):
        nodelist = []

        if self.to_type is not None:
            nodelist.append(("to_type", self.to_type))

        if self.expression is not None:
            nodelist.append(("expression", self.expression))

        return tuple(nodelist)

    def __iter__(self):
        if self.to_type is not None:
            yield self.to_type

        if self.expression is not None:
            yield self.expression

    attr_names = ()


class Compound(Node):
    """
        A class used to represent a compound expression

        ...

        Attributes
        ----------
            block_items : 
                a block of assignments/expressions that make part of a compound object
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('block_items', 'coord')

    def __init__(self, block_items, coord=None):
        self.block_items = block_items
        self.coord = coord

    def children(self):
        nodelist = []

        for i, child in enumerate(self.block_items or []):
            nodelist.append(("block_items[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):
        for child in (self.block_items or []):
            yield child

    attr_names = ()


class Constant(Node):
    """
        A class used to represent a constant

        ...

        Attributes
        ----------
            type : 
                the constant type (int/float/string)
            valu : 
                the constant value
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    # TODO: tem --> rawtype/gen_location

    __slots__ = ('type', 'value', 'coord', 'rawtype', 'location')

    def __init__(self, type, value, coord=None, rawtype=None, location=None):
        self.type = type
        self.value = value
        self.coord = coord
        self.rawtype = rawtype
        self.location = location

    def children(self):
        return tuple([])

    def __iter__(self):
        return
        yield

    attr_names = ('type', 'value',)


class Decl(Node):
    """
        A class used to represent a declaration

        ...

        Attributes
        ----------
            name : 
                the name of the declaration
            type : 
                the type of the declaration
            init : 
                the "body" of the declaration
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('name', 'type', 'init', 'coord')

    def __init__(self, name, type, init, coord=None):
        self.name = name
        self.type = type
        self.init = init
        self.coord = coord

    def children(self):
        nodelist = []

        if self.type is not None:
            nodelist.append(("type", self.type))

        if self.init is not None:
            nodelist.append(("init", self.init))

        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

        if self.init is not None:
            yield self.init

    attr_names = ('name',)


class DeclList(Node):
    """
        A class used to represent a list of declarations

        ...

        Attributes
        ----------
            decls : 
                a list of declaration (Decl) objects
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """
    __slots__ = ('decls', 'coord')

    def __init__(self, decls, coord=None):
        self.decls = decls
        self.coord = coord

    def children(self):
        nodelist = []

        for i, child in enumerate(self.decls or []):
            nodelist.append(("decls[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):
        for child in (self.decls or []):
            yield child

    attr_names = ()


class EmptyStatement(Node):
    """
        A class used to represent an empty statement

        ...

        Attributes
        ----------
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """
    __slots__ = ('coord')

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return tuple()

    def __iter__(self):
        return
        yield

    attr_names = ()


class ExprList(Node):
    """
        A class used to represent a list of expressions

        ...

        Attributes
        ----------
            expr : 
                an expression object
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """
    __slots__ = ('exprs', 'coord')

    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []

        for i, child in enumerate(self.exprs or []):
            nodelist.append(("exprs[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):
        for child in (self.exprs or []):
            yield child

    attr_names = ()


class For(Node):
    """
        A class used to represent a For statement

        ...

        Attributes
        ----------
            for_init : 
                the loop initial value (eg. i = 0)
            for_cond : 
                the loop condition (eg. i < 4)
            for_next :
                what happens with the iterator value (eg. i++)
            for_statement : 
                the code inside the loop 
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    # todo: add exit_label

    __slots__ = ('for_init', 'for_cond', 'for_next', 'for_statement', 'coord', 'for_exit')

    def __init__(self, for_init, for_cond, for_next, for_statement, coord=None, for_exit=None):
        self.for_init = for_init
        self.for_cond = for_cond
        self.for_next = for_next
        self.for_statement = for_statement
        self.coord = coord
        self.for_exit = for_exit

    def children(self):
        nodelist = []

        if self.for_init is not None:
            nodelist.append(("for_init", self.for_init))

        if self.for_cond is not None:
            nodelist.append(("for_cond", self.for_cond))

        if self.for_next is not None:
            nodelist.append(("for_next", self.for_next))

        if self.for_statement is not None:
            nodelist.append(("for_statement", self.for_statement))

        return tuple(nodelist)

    def __iter__(self):
        if self.for_init is not None:
            yield self.for_init

        if self.for_cond is not None:
            yield self.for_cond

        if self.for_next is not None:
            yield self.for_next

        if self.for_statement is not None:
            yield self.for_statement

    attr_names = ()


class FuncCall(Node):
    """
        A class used to represent a function call

        ...

        Attributes
        ----------
            name : 
                the function name
            args : 
                the arguments of the function
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('name', 'args', 'coord', 'type', 'location')

    def __init__(self, name, args, coord=None, type=None, location=None):
        self.name = name
        self.args = args
        self.coord = coord
        self.type = type
        self.location = location

    def children(self):
        nodelist = []

        if self.name is not None:
            nodelist.append(("name", self.name))

        if self.args is not None:
            nodelist.append(("args", self.args))

        return tuple(nodelist)

    def __iter__(self):
        if self.name is not None:
            yield self.name

        if self.args is not None:
            yield self.args

    attr_names = ()


class FuncDecl(Node):
    """
        A class used to represent a function declaration

        ...

        Attributes
        ----------
            args : 
                the arguments of the function
            type : 
                the type of the function (int/float/void)
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    # add gen_location

    __slots__ = ('args', 'type', 'coord', 'location')

    def __init__(self, args, type, coord=None, location=None):
        self.args = args
        self.type = type
        self.coord = coord
        self.location = location

    def children(self):
        nodelist = []

        if self.args is not None:
            nodelist.append(("args", self.args))

        if self.type is not None:
            nodelist.append(("type", self.type))

        return tuple(nodelist)

    def __iter__(self):

        if self.args is not None:
            yield self.args

        if self.type is not None:
            yield self.type

    attr_names = ()


class FuncDef(Node):
    """
        A class used to represent a function definition

        ...

        Attributes
        ----------
            spec : 
                the specifications of the function
            decl : 
                the function declaration
            param_decls : 
                the declaration of the parameters of the function
            body :
                the body of the function
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    # add decls

    __slots__ = ('spec', 'decl', 'param_decls', 'body', 'coord', 'decls')

    def __init__(self, spec, decl, param_decls, body, coord=None, decls=None):
        self.spec = spec
        self.decl = decl
        self.param_decls = param_decls
        self.body = body
        self.coord = coord
        self.decls = decls

    def children(self):
        nodelist = []

        if self.spec is not None:
            nodelist.append(("spec", self.spec))

        if self.decl is not None:
            nodelist.append(("decl", self.decl))

        if self.body is not None:
            nodelist.append(("body", self.body))

        for i, child in enumerate(self.param_decls or []):
            nodelist.append(("param_decls[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):

        if self.spec is not None:
            yield self.spec

        if self.decl is not None:
            yield self.decl

        if self.body is not None:
            yield self.body

        for child in (self.param_decls or []):
            yield child

    attr_names = ()


class GlobalDecl(Node):
    """
        A class used to represent a global declaration

        ...

        Attributes
        ----------
            decls : 
                a list of declarations
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('decls', 'coord')

    def __init__(self, decls, coord=None):
        self.decls = decls
        self.coord = coord

    def children(self):

        nodelist = []

        for i, child in enumerate(self.decls or []):
            nodelist.append(("decls[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):

        for child in (self.decls or []):
            yield child

    attr_names = ()


class ID(Node):
    """
        A class used to represent an identifier

        ...

        Attributes
        ----------
            name : 
                the name associated with the id (eg. var_name)
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    # TODO: add type/scope/kind/bind/gen_location

    __slots__ = ('name', 'coord', 'type', 'scope', 'kind', 'bind', 'location')

    def __init__(self, name, coord=None, type=None, scope=None, kind=None, bind=None, location=None):
        self.name = name
        self.coord = coord
        self.type = type
        self.scope = scope
        self.kind = kind
        self.bind = bind
        self.location = location

    def children(self):
        return ()

    def __iter__(self):
        return
        yield

    attr_names = ('name',)


class If(Node):
    """
        A class used to represent an If expression

        ...

        Attributes
        ----------
            if_cond : 
                the conditional statement (eg. x < 2)
            if_true : 
                what happens if the condition is true
            if_false : 
                what happens if the condition is false
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('if_cond', 'if_true', 'if_false', 'coord')

    def __init__(self, if_cond, if_true, if_false, coord=None):
        self.if_cond = if_cond
        self.if_true = if_true
        self.if_false = if_false
        self.coord = coord

    def children(self):
        nodelist = []

        if self.if_cond is not None:
            nodelist.append(("if_cond", self.if_cond))

        if self.if_true is not None:
            nodelist.append(("if_true", self.if_true))

        if self.if_false is not None:
            nodelist.append(("if_false", self.if_false))

        return tuple(nodelist)

    def __iter__(self):

        if self.if_cond is not None:
            yield self.if_cond

        if self.if_true is not None:
            yield self.if_true

        if self.if_false is not None:
            yield self.if_false

    attr_names = ()


class InitList(Node):
    """
        A class used to represent a list.

        ...

        Attributes
        ----------
            expressions :
                the list of expressions
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('expressions', 'coord', 'list_values')

    def __init__(self, expressions, coord=None, list_values=[]):
        self.expressions = expressions
        self.coord = coord
        self.list_values = list_values

    def children(self):

        nodelist = []

        for i, child in enumerate(self.expressions or []):
            nodelist.append(("expressions[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):

        for child in (self.expressions or []):
            yield child

    attr_names = ()


class ParamList(Node):
    """
        A class used to represent a list of parameters

        ...

        Attributes
        ----------
            params :
                a list of parameters
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('params', 'coord')

    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []

        for i, child in enumerate(self.params or []):
            nodelist.append(("params[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):

        for child in (self.params or []):
            yield child

    attr_names = ()


class Print(Node):
    """
        A class used to represent a print expression

        ...

        Attributes
        ----------
            expr :
                the expression to be printed
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('expr', 'coord')

    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):

        nodelist = []

        if self.expr is not None:
            nodelist.append(("expr", self.expr))

        return tuple(nodelist)

    def __iter__(self):

        if self.expr is not None:
            yield self.expr

    attr_names = ()


class Program(Node):
    """
        A class used to represent a program in the uC language

        ...

        Attributes
        ----------
            gdecls :
                a list of global declarations
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('gdecls', 'coord', 'symble_table', 'environment')

    def __init__(self, gdecls, coord=None, symble_table=None, environment=None):
        self.gdecls = gdecls
        self.coord = coord
        self.symble_table = symble_table
        self.environment = environment

    def children(self):
        nodelist = []

        for i, child in enumerate(self.gdecls or []):
            nodelist.append(("gdecls[%d]" % i, child))

        return tuple(nodelist)

    def __iter__(self):

        for child in (self.gdecls or []):
            yield child

    attr_names = ()


class PtrDecl(Node):
    """
        A class used to represent the declaration of a pointer

        ...

        Attributes
        ----------
            ptr_quals :
                informations about the pointer
            ptr_type :
                the type of the pointer
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('ptr_quals', 'type', 'coord')

    def __init__(self, ptr_quals, type, coord=None):
        self.ptr_quals = ptr_quals
        self.type = type
        self.coord = coord

    def children(self):

        nodelist = []

        if self.type is not None:
            nodelist.append(("type", self.type))

        return tuple(nodelist)

    def __iter__(self):

        if self.type is not None:
            yield self.type

    attr_names = ('ptr_quals',)


class Read(Node):
    """
        A class used to represent a read statement

        ...

        Attributes
        ----------
            names :
                the names to be read
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('names', 'coord')

    def __init__(self, names, coord=None):
        self.names = names
        self.coord = coord

    def children(self):

        nodelist = []

        if self.names is not None:
            nodelist.append(("names", self.names))

        return tuple(nodelist)

    def __iter__(self):

        if self.names is not None:
            yield self.names

    attr_names = ()


class Return(Node):
    """
        A class used to represent a return expression

        ...

        Attributes
        ----------
            expression :
                the expression to be returned
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('expression', 'coord')

    def __init__(self, expression, coord=None):
        self.expression = expression
        self.coord = coord

    def children(self):
        nodelist = []

        if self.expression is not None:
            nodelist.append(("expression", self.expression))

        return tuple(nodelist)

    def __iter__(self):
        if self.expression is not None:
            yield self.expression

    attr_names = ()


class Type(Node):
    """
        A class used to represent a type

        ...

        Attributes
        ----------
            names : 
                the type name (eg. int)
            coord : 
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """
    __slots__ = ('names', 'coord')

    def __init__(self, names, coord=None):
        self.names = names
        self.coord = coord

    def children(self):
        return ()

    def __iter__(self):
        return
        yield

    attr_names = ('names',)


class VarDecl(Node):
    """
        A class used to represent a variable declaration

        ...

        Attributes
        ----------
            declname :
                the name of the declaration
            type :
                the type of the declaration
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('declname', 'type', 'coord')

    def __init__(self, declname, type, coord=None):
        self.declname = declname
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []

        if self.type is not None:
            nodelist.append(("type", self.type))

        return tuple(nodelist)

    def __iter__(self):

        if self.type is not None:
            yield self.type

    attr_names = ('declname',)


class UnaryOp(Node):
    """
        A class used to represent a unary operation

        ...

        Attributes
        ----------
            op :
                the operator
            expr :
                the expression
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('op', 'expr', 'coord', 'type', 'location')

    def __init__(self, op, expr, coord=None, type=None, location=None):
        self.op = op
        self.expr = expr
        self.coord = coord
        self.type = type
        self.location = location

    def children(self):
        nodelist = []

        if self.expr is not None:
            nodelist.append(("expr", self.expr))

        return tuple(nodelist)

    def __iter__(self):
        if self.expr is not None:
            yield self.expr

    attr_names = ('op',)


class While(Node):
    """
        A class used to represent a While

        ...

        Attributes
        ----------
            while_cond :
                the loop condition (eg. i < 3)
            while_stmt :
                the body of the loop
            coord :
                the line/column position of the object

        Methods
        -------
            children(self)
                A sequence of all children that are Nodes
    """

    __slots__ = ('while_cond', 'while_stmt', 'coord', 'while_exit')

    def __init__(self, while_cond, while_stmt, coord=None, while_exit=None):
        self.while_cond = while_cond
        self.while_stmt = while_stmt
        self.coord = coord
        self.while_exit = while_exit

    def children(self):
        nodelist = []

        if self.while_cond is not None:
            nodelist.append(("while_cond", self.while_cond))

        if self.while_stmt is not None:
            nodelist.append(("while_stmt", self.while_stmt))

        return tuple(nodelist)

    def __iter__(self):

        if self.while_cond is not None:
            yield self.while_cond

        if self.while_stmt is not None:
            yield self.while_stmt

    attr_names = ()
