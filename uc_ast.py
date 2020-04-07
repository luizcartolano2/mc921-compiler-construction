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
        """ 
            Generates a python representation of the current node
        """
        result = self.__class__.__name__ + '('
        
        indent = ''
        separator = ''

        for name in self.__slots__[:-2]:
            result += separator
            result += indent
            result += name + '=' + (_repr(getattr(self, name)).replace('\n', '\n  ' + (' ' * (len(name) + len(self.__class__.__name__)))))
            
            separator = ','
            indent = '\n ' + (' ' * len(self.__class__.__name__))
        
        result += indent + ')'
        
        return result


    def children(self):
        """ 
            A sequence of all children that are Nodes
        """
        pass


    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ 
            Pretty print the Node and all its attributes and
            children (recursively) to a buffer.
            buf:
                Open IO buffer into which the Node is printed.
            offset:
                Initial offset (amount of leading spaces)
            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.
            nodenames:
                True if you want to see the actual node names
                within their parents.
            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """

        lead = ' ' * offset
        
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)


    ################################
    #   Classes representadas      #
    #------------------------------#
    #   ArrayDecl       - Done     #
    #------------------------------#
    #   ArrayRef        - Done     #
    #------------------------------#
    #   Assert                     #
    #------------------------------#
    #   Assignment      - Done     #
    #------------------------------#
    #   BinaryOp        - Done     #
    #------------------------------#
    #   Break           - Done     #
    #------------------------------#
    #   Cast            - Done     #
    #------------------------------#
    #   Compound        - Done     #
    #------------------------------#
    #   Constant        - Done     #
    #------------------------------#
    #   Decl            - Done     #
    #------------------------------#
    #   DeclList        - Done     #
    #------------------------------#
    #   EmptyStatement  - Done     #
    #------------------------------#
    #   ExprList        - Done     #
    #------------------------------#
    #   For             - Done     #
    #------------------------------#
    #   FuncCall        - Done     #
    #------------------------------#
    #   FuncDecl        - Done     #
    #------------------------------#
    #   FuncDef         - Done     #
    #------------------------------#
    #   GlobalDecl                 #
    #------------------------------# 
    #   ID              - Done     #
    #------------------------------#
    #   If              - Done     #
    #------------------------------#
    #   InitList        - Done     #
    #------------------------------#
    #   ParamList       - Done     #
    #------------------------------#
    #   Print                      #
    #------------------------------#
    #   Program         - Done     #
    #------------------------------#
    #   PtrDecl         - Done     #
    #------------------------------#
    #   Read                       #
    #------------------------------#
    #   Return          - Done     #
    #------------------------------#
    #   Type            - Done     #
    #------------------------------#
    #   VarDecl                    #
    #------------------------------#
    #   UnaryOp         - Done     #
    #------------------------------#
    #   While           - Done     #
    ################################


    class ArrayDecl(Node):
        __slots__ = ('type', 'dimension', 'dimension_quals', 'coord')


        def __init__(self, type, dimension, dimension_quals, coord=None):
            self.type            = type
            self.dimension       = dimension
            self.dimension_quals = dimension_quals
            self.coord           = coord


        def children(self):
            nodelist = []

            if self.type is not None: 
                nodelist.append(("type", self.type))

            if self.dim is not None: 
                nodelist.append(("dimension", self.dimension))

            return tuple(nodelist)


        def __iter__(self):
            if self.type is not None:
                yield self.type

            if self.dimension is not None:
                yield self.dimension


        attr_names = ('dimension_quals')


    class ArrayRef(Node):
        __slots__ = ('name', 'subscript', 'coord')


        def __init__(self, array_name, array_subscript, coord=None):
            self.array_name      = array_name
            self.array_subscript = array_subscript
            self.coord           = coord


        def children(self):
            nodelist = []

            if self.array_name is not None: 
                nodelist.append(("array_name", self.array_name))

            if self.array_subscript is not None: 
                nodelist.append(("array_subscript", self.array_subscript))

            return tuple(nodelist)


        def __iter__(self):
            if self.array_name is not None:
                yield self.array_name

            if self.array_subscript is not None:
                yield self.array_subscript


        attr_names = ()


    class Assignment(Node):
        __slots__ = ('op', 'left_value', 'right_value', 'coord')


        def __init__(self, op, left_value, right_value, coord=None):
            self.op      = op
            self.left_value     = left_value
            self.right_value    = right_value
            self.coord          = coord


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


        attr_names = ('op')


    class BinaryOp(Node):
        __slots__ = ('op', 'left_value', 'right_value', 'coord')


        def __init__(self, op, left_value, right_value, coord=None):
            self.op      = op
            self.left_value     = left_value
            self.right_value    = right_value
            self.coord          = coord


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


        attr_names = ('op')


    class Break(Node):
        __slots__ = ('coord')


        def __init__(self, coord=None):
            self.coord = coord


        def children(self):
            return tuple()


        def __iter__(self):
            return
            yield


        attr_names = ()


    class Cast(Node):
        __slots__ = ('to_type', 'expression', 'coord')


        def __init__(self, to_type, expression, coord=None):
            self.to_type    = to_type
            self.expression = expression
            self.coord      = coord


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
        __slots__ = ('block_items', 'coord')


        def __init__(self, block_items, coord=None):
            self.block_items = block_items
            self.coord       = coord


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
        __slots__ = ('type', 'value', 'coord')


        def __init__(self, type, value, coord=None):
            self.type  = type
            self.value = value
            self.coord = coord


        def children(self):

            return tuple([])


        def __iter__(self):
            return
            yield


        attr_names = ('type', 'value')


    class Decl(Node):
        __slots__ = ('name', 'decl_quals', 'decl_storage', 'decl_func_spec', 'decl_type', 'decl_init', 'decl_bitsize', 'coord')


        def __init__(self, name, decl_quals, decl_storage, decl_func_spec, decl_type, decl_init, decl_bitsize, coord=None):
            self.name           = name
            self.decl_quals     = decl_quals
            self.decl_storage   = decl_storage
            self.decl_func_spec = decl_func_spec
            self.decl_type      = decl_type
            self.decl_init      = decl_init
            self.decl_bitsize   = decl_bitsize
            self.coord          = coord


        def children(self):
            nodelist = []

            if self.decl_init is not None: 
                nodelist.append(("decl_init", self.decl_init))

            if self.decl_type is not None: 
                nodelist.append(("decl_type", self.decl_type))

            if self.decl_bitsize is not None: 
                nodelist.append(("decl_bitsize", self.decl_bitsize))

            return tuple(nodelist)


        def __iter__(self):
            if self.decl_type is not None:
                yield self.decl_type

            if self.decl_init is not None:
                yield self.decl_init

            if self.decl_bitsize is not None:
                yield self.decl_bitsize


        attr_names = ('name', 'decl_quals', 'decl_storage', 'decl_func_spec')


    class DeclList(Node):
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
        __slots__ = ('for_init', 'for_cond', 'for_next', 'for_statement', 'coord')


        def __init__(self, for_init, for_cond, for_next, for_statement, coord=None):
            self.for_init      = for_init
            self.for_cond      = for_cond
            self.for_next      = for_next
            self.for_statement = for_statement
            self.coord         = coord


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
        __slots__ = ('func_name', 'func_args', 'coord')


        def __init__(self, func_name, func_args, coord=None):
            self.func_name = func_name
            self.func_args = func_args
            self.coord     = coord


        def children(self):
            nodelist = []

            if self.func_name is not None: 
                nodelist.append(("func_name", self.func_name))

            if self.func_args is not None: 
                nodelist.append(("func_args", self.func_args))

            return tuple(nodelist)


        def __iter__(self):
            if self.func_name is not None:
                yield self.func_name

            if self.func_args is not None:
                yield self.func_args


        attr_names = ()


    class FuncDecl(Node):
        __slots__ = ('func_args', 'func_type', 'coord')


        def __init__(self, func_args, func_type, coord=None):
            self.func_args = func_args
            self.func_type = func_type
            self.coord     = coord


        def children(self):
            nodelist = []

            if self.func_args is not None: 
                nodelist.append(("func_args", self.func_args))

            if self.func_type is not None: 
                nodelist.append(("func_type", self.func_type))

            return tuple(nodelist)


        def __iter__(self):

            if self.func_args is not None:
                yield self.func_args

            if self.func_type is not None:
                yield self.func_type


        attr_names = ()


    class FuncDef(Node):
        __slots__ = ('func_decl', 'func_param_decls', 'func_body', 'coord')


        def __init__(self, func_decl, func_param_decls, func_body, coord=None):
            self.func_decl        = func_decl
            self.func_param_decls = func_param_decls
            self.func_body        = func_body
            self.coord            = coord


        def children(self):
            nodelist = []

            if self.func_decl is not None: 
                nodelist.append(("func_decl", self.func_decl))

            if self.func_body is not None: 
                nodelist.append(("func_body", self.func_body))

            for i, child in enumerate(self.func_param_decls or []):
                nodelist.append(("func_param_decls[%d]" % i, child))

            return tuple(nodelist)


        def __iter__(self):

            if self.func_decl is not None:
                yield self.func_decl

            if self.func_body is not None:
                yield self.func_body

            for child in (self.func_param_decls or []):
                yield child


        attr_names = ()


    class ID(Node):
        __slots__ = ('name', 'coord')


        def __init__(self):
            self.name = name


        def children(self):
            return tuple([])


        def __iter__(self):
            return
            yield


        attr_names = ('name')


    class If(Node):
        __slots__ = ('if_cond', 'if_true', 'if_false', 'coord')


        def __init__(self, if_cond, if_true, if_false, coord=None):
            self.if_cond   = if_cond
            self.if_true   = if_true
            self.if_false  = if_false
            self.coord     = coord


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
        __slots__ = ('expressions', 'coord')


        def __init__(self, expressions, coord=None):
            self.expressions = expressions
            self.coord       = coord


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
        __slots__ = ('params', 'coord')


        def __init__(self, params, coord=None):
            self.params = params
            self.coord  = coord


        def children(self):
            nodelist = []

            for i, child in enumerate(self.params or []):
                nodelist.append(("params[%d]" % i, child))

            return tuple(nodelist)


        def __iter__(self):

            for child in (self.params or []):
                yield child


        attr_names = ()


    class Program(Node):
        __slots__ = ('gdecls', 'coord')


        def __init__(self, gdecls, coord=None):
            self.gdecls = gdecls
            self.coord  = coord


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
        __slots__ = ('ptr_quals', 'ptr_type', 'coord')


        def __init__(self, ptr_quals, ptr_type, coord=None):
            self.ptr_quals = ptr_quals
            self.ptr_type  = ptr_type
            self.coord     = coord


        def children(self):
            
            nodelist = []

            if self.ptr_type is not None:
                nodelist.append(("ptr_type", self.ptr_type))

            return tuple(nodelist)


        def __iter__(self):
            
            if self.ptr_type is not None:
                yield self.ptr_type


        attr_names = ('ptr_quals')


    class Return(Node):
        __slots__ = ('expression', 'coord')


        def __init__(self, expression, coord=None):
            self.expression = expression
            self.coord      = coord


        def children(self):
            if self.expression is not None:
                nodelist.append(("expression", self.expression))

            return tuple(nodelist)


        def __iter__(self):
            if self.expression is not None:
                yield self.expression


        attr_names = ()


    class Type(Node):
        __slots__ = ('name', 'type_quals', 'type', 'coord')


        def __init__(self, name, type_quals, type, coord=None):
            self.name       = name
            self.type_quals = type_quals
            self.type       = type
            self.coord      = coord


        def children(self):

            nodelist = []

            if self.type is not None:
                nodelist.append(("type", self.type))

            return tuple(nodelist)


        def __iter__(self):

            if self.type is not None:
                yield self.type


        attr_names = ('name', 'type_quals')


    class UnaryOp(Node):
        __slots__  = ('op', 'expr', 'coord')


        def __init__(self, op, expr, coord=None):
            self.op    = op
            self.expr  = expr
            self.coord = coord


        def children(self):
            nodelist = []

            if self.expr is not None:
                nodelist.append(("expr", self.expr))

            return tuple(nodelist)


        def __iter__(self):
            if self.expr is not None:
                yield self.expr


        attr_names = ('op')


    class While(Node):
        __slots__ = ('while_cond', 'while_stmt', 'coord')


        def __init__(self, while_cond, while_stmt, coord=None):
            self.while_cond = while_cond
            self.while_stmt = while_stmt
            self.coord      = coord


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




















