from uc_ast import FuncDecl

class SymbolTable(dict):
    """
        Class representing a symbol table.  It should provide functionality
        for adding and looking up nodes associated with identifiers.

        ...

        Methods
        -------
            add(self, name, value)
                Add new symbol with value.

            lookup(self, name)
                Lookup for symbol.
    """
    def __init__(self, decl=None):
        super().__init__()
        self.decl = decl


    def add(self, name, value):
        """
            Add new symbol with value.
        """
        self[name] = value


    def lookup(self, name):
        """
            Lookup for symbol.
        """
        return self.get(name, None)


class Environment():
    """
        A Environment class to keep code state.

        ...

        Methods
        -------
            push(self, closure)
                Add symbol to the stack.

            pop(self)
                Pop symbol from the stack.

            peek(self)
                Peek symbol from the stack.

            peek_root(self)
                Peek root symbol from the stack.

            scope_level(self)
                Gets scope level.

            add_local(self, identifier, kind)
                Add local definition.

            add_root(self, name, value)
                Add root definition.

            lookup(self, name)
                Search and return a symbol.

            find(self, name)
                Find if symbol exists.
    """
    def __init__(self):
        # define a root
        self.root = SymbolTable()

        # define a stack and append the root for it
        self.stack = []
        self.stack.append(self.root)

        # define types
        self.stack_types = []
        self.cur_rtype = []
        self.cur_loop = []

        # add a attr to deal with func definitions
        self.func_def = None

        # update root with types
        self.root.update({
            "int"   : IntType,
            "float" : FloatType,
            "char"  : CharType,
            "array" : ArrayType,
            "ptr"   : PtrType,
            "void"  : VoidType,
        })


    def push(self, closure):
        """
            Add symbol to the stack.
        """
        # append to stack
        self.stack.append(SymbolTable(decl=closure))
        # append type
        self.stack_types.append(self.cur_rtype)

        if isinstance(closure, FuncDecl):
            # aqui sepa vai dar merda
            self.cur_rtype = closure.type.type.names
        else:
            self.cur_rtype = [VoidType]


    def pop(self):
        """
            Pop symbol from the stack.
        """
        # pop stack
        self.stack.pop()
        # pop type_stack
        self.cur_rtype = self.stack_types.pop()


    def peek(self):
        """
            Peek root symbol from the stack.
        """
        return self.stack[-1]


    def peek_root(self):
        """
            Peek root symbol from the stack.
        """
        return  self.stack[0]


    def scope_level(self):
        """
            Gets scope level.
        """
        return len(self.stack) - 1


    def add_local(self, identifier, kind):
        """
            Add local definition.
        """
        self.peek().add(identifier.name, identifier)
        identifier.kind = kind
        identifier.scope = self.scope_level()


    def add_root(self, name, value):
        """
            Add root definition.
        """
        self.root.add(name, value)


    def lookup(self, name):
        """
            Search and return a symbol.
        """
        for scope in reversed(self.stack):
            hit = scope.lookup(name)
            if hit:
                return hit
        return None


    def find(self, name):
        """
            Find if symbol exists.
        """
        cur_symtable = self.stack[-1]

        return name in cur_symtable


class uCType(object):
    """
        Class that represents a type in the uC language.  Types
        are declared as singleton instances of this type.
    """

    def __init__(self, typename, binary_ops=None, unary_ops=None, rel_ops=None, assign_ops=None):
        """
            You must implement yourself and figure out what to store.
        """
        self.typename = typename
        self.unary_ops = unary_ops or set()
        self.binary_ops = binary_ops or set()
        self.rel_ops = rel_ops or set()
        self.assign_ops = assign_ops or set()

    def __repr__(self):
        return "type[{}]".format(self.typename)


IntType = uCType(
    typename="int",
    binary_ops={"+", "-", "*", "/", "%"},
    unary_ops={"-", "+", "--", "++", "p--", "p++", "*", "&"},
    rel_ops={"==", "!=", "<", ">", "<=", ">="},
    assign_ops={"=", "+=", "-=", "*=", "/=", "%="},
)
FloatType = uCType(
    typename="float",
    binary_ops={"+", "-", "*", "/", "%"},
    unary_ops={"-", "+", "*", "&"},
    rel_ops={"==", "!=", "<", ">", "<=", ">="},
    assign_ops={"=", "+=", "-=", "*=", "/=", "%="},
)
CharType = uCType(
    typename="char",
    binary_ops=None,
    unary_ops={"*", "&"},
    rel_ops={"==", "!=", "&&", "||"},
    assign_ops={"=", "+=", "-=", "*=", "/=", "%="},
)
ArrayType = uCType(
    typename="array",
    binary_ops=None,
    unary_ops={"*", "&"},
    rel_ops={"==", "!="},
    assign_ops={"="},
)
PtrType = uCType(
    typename="ptr",
    binary_ops=None,
    unary_ops={"*", "&"},
    rel_ops={"==", "!="},
    assign_ops={"="},
)
VoidType = uCType(
    typename="void",
    binary_ops=None,
    unary_ops={"*", "&"},
    rel_ops={"==", "!="},
    assign_ops=None,
)
StringType = uCType(
    typename="string",
    binary_ops=None,
    unary_ops=None,
    rel_ops={'==', '!='},
    assign_ops=None,
)
BoolType = uCType(
    typename="bool",
    binary_ops=None,
    unary_ops={"!", "*", "&"},
    rel_ops={"==", "!=", "&&", "||"},
    assign_ops={"="},
)