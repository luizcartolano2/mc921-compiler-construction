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
