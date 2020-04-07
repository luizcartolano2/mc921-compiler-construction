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
    #   ID                         #
    #------------------------------#
    #   If                         #
    #------------------------------#
    #   InitList                   #
    #------------------------------#
    #   ParamList                  #
    #------------------------------#
    #   Print                      #
    #------------------------------#
    #   Program                    #
    #------------------------------#
    #   PtrDecl                    #
    #------------------------------#
    #   Read                       #
    #------------------------------#
    #   Return                     #
    #------------------------------#
    #   Type                       #
    #------------------------------#
    #   VarDecl                    #
    #------------------------------#
    #   UnaryOp                    #
    #------------------------------#
    #   While                      #
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
        __slots__ = ('operation', 'left_value', 'right_value', 'coord')


        def __init__(self, operation, left_value, right_value, coord=None):
            self.operation      = operation
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


        attr_names = ('operation')


    class BinaryOp(Node):
        __slots__ = ('operation', 'left_value', 'right_value', 'coord')


        def __init__(self, operation, left_value, right_value, coord=None):
            self.operation      = operation
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


        attr_names = ('operation')


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
        __slots__ = ('decl_name', 'decl_quals', 'decl_storage', 'decl_func_spec', 'decl_type', 'decl_init', 'decl_bitsize', 'coord')


        def __init__(self, decl_name, decl_quals, decl_storage, decl_func_spec, decl_type, decl_init, decl_bitsize, coord=None):
            self.decl_name      = decl_name
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


        attr_names = ('decl_name', 'decl_quals', 'decl_storage', 'decl_func_spec')


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




























