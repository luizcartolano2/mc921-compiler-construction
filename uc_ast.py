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
    #   ArrayDecl - Done           #
    #------------------------------#
    #   ArrayRef  - Done           #
    #------------------------------#
    #   Assert                     #
    #------------------------------#
    #   Assignment                 #
    #------------------------------#
    #   BinaryOp                   #
    #------------------------------#
    #   Break                      #
    #------------------------------#
    #   Cast                       #
    #------------------------------#
    #   Compound                   #
    #------------------------------#
    #   Constant                   #
    #------------------------------#
    #   Decl                       #
    #------------------------------#
    #   DeclList                   #
    #------------------------------#
    #   EmptyStatement             #
    #------------------------------#
    #   ExprList                   #
    #------------------------------#
    #   For                        #
    #------------------------------#
    #   FuncCall                   #
    #------------------------------#
    #   FuncDecl                   #
    #------------------------------#
    #   FuncDef                    #
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
            self.type = type
            self.dimension = dimension
            self.dimension_quals = dimension_quals
            self.coord = coord


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
            self.array_name = array_name
            self.array_subscript = array_subscript
            self.coord = coord


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






















