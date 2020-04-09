import ply.lex as lex
import sys


class UCLexer():
    """ A lexer for the uC language. After building it, set the
        input text with input(), and call token() to get new
        tokens.
    """
    def __init__(self, error_func):
        """ Create a new Lexer.
            An error function. Will be called with an error
            message, line and column as arguments, in case of
            an error during lexing.
        """
        self.error_func = error_func
        self.filename = ''

        # Keeps track of the last token returned from self.token()
        self.last_token = None


    def build(self, **kwargs):
        """ Builds the lexer from the specification. Must be
            called after the lexer object is created.

            This method exists separately, because the PLY
            manual warns against calling lex.lex inside __init__
        """
        self.lexer = lex.lex(object=self, **kwargs)


    def reset_lineno(self):
        """ Resets the internal line number counter of the lexer.
        """
        self.lexer.lineno = 1


    def input(self, text):
        self.lexer.input(text)


    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token


    def find_tok_column(self, token):
        """ Find the column of the token in its line.
        """
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr


    # Internal auxiliary methods
    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)


    def _make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))


    # Reserved keywords
    keywords = (
        'ASSERT', 'BREAK', 'CHAR', 'ELSE', 'FLOAT', 'FOR', 'IF', 'INT', 'PRINT', 'READ', 'RETURN', 'VOID', 'WHILE',
    )

    keyword_map = {}
    for keyword in keywords:
        keyword_map[keyword.lower()] = keyword


    #
    # All the tokens recognized by the lexer
    #
    tokens = keywords + (
        # Identifiers
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'SEMI',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
        'INT_CONST',
        'CHAR_CONST',
        'FLOAT_CONST',
        'STRING_LITERAL',
        'ID',
        'EQ',
        'EQUALS',
        'COMMA',
        'ADDRESS',
        'PLUSPLUS',
        'MINUSMINUS',
        'NOT',
        'GT',
        'GE',
        'LT',
        'LE',
        'NE',
        'MOD',
        'PLUSEQUAL',
        'MINUSEQUAL',
        'TIMESEQUAL',
        'DIVIDEEQUAL',
        'MODEQUAL',
        'AND',
        'OR',
    )        


    #
    # Rules
    #
    t_EQ          = r'=='
    t_PLUSPLUS    = r'\+\+'
    t_MINUSMINUS  = r'\-\-'
    T_GE          = r'\>\=' 
    T_LE          = r'\<\='
    T_NE          = r'\!\='
    T_PLUSEQUAL   = r'\+\='
    T_MINUSEQUAL  = r'\-\='
    T_TIMESEQUAL  = r'\*\='
    T_DIVIDEEQUAL = r'\/\='
    T_MODEQUAL    = r'\%\='
    T_AND         = r'\&\&'
    T_OR          = r'\|\|'
    
    t_PLUS        = r'\+'
    t_CHAR_CONST  = r"""'.'"""
    t_MINUS       = r'-'
    t_TIMES       = r'\*'
    t_DIVIDE      = r'/'
    t_EQUALS      = r'='
    t_LPAREN      = r'\('
    t_RPAREN      = r'\)'
    t_LBRACE      = r'\{'
    t_RBRACE      = r'\}'
    t_LBRACKET    = r'\['
    t_RBRACKET    = r'\]'
    t_SEMI        = r';'
    t_COMMA       = r'\,'
    t_ADDRESS     = r'\&'
    t_NOT         = r'\!'
    t_GT          = r'\>'
    t_LT          = r'\<'
    t_MOD         = r'\%'
    # A string containing ignored characters (spaces and tabs)
    t_ignore      = ' \t'

    
    # Newlines
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")


    def t_ID(self, t):
        r'[a-zA-Z_][0-9a-zA-Z_]*'
        t.type = self.keyword_map.get(t.value, "ID")
        return t


    def t_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        pass


    def t_error_comment(self, t):
        r'/\*(.|\n)*$'
        msg = "{}: Unterminated comment".format(t.lexer.lineno)
        self._error(msg, t)


    # define a comment //
    def t_COMMENT_2(self, t):
        r'//.*'
        pass


    def t_FLOAT_CONST(self, t):
        r'([0-9]*\.[0-9]+)|([0-9]+\.)'
        t.value = float(t.value)
            
        return t


    def t_INT_CONST(self, t):
        r'0|[1-9][0-9]*'
        t.value = int(t.value)
   
        return t


    def t_STRING_LITERAL(self, t):
        r'".*?"'
        t.value = str(t.value)
    
        return t


    def t_error_string(self, t):
        r'".*$'
        msg = "{}: Unterminated string".format(t.lexer.lineno)
        self._error(msg, t)
        pass


    def t_error(self, t):
        msg = "Illegal character %s" % repr(t.value[0])
        self._error(msg, t)

    # Scanner (used only for test)
    def scan(self, data):
        # output = ""

        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
            # output += str(tok) + '\n'

        # return output


if __name__ == '__main__':

    def print_error(msg, x, y):
        print("Lexical error: %s at %d:%d" % (msg, x, y))

    m = UCLexer(print_error)
    m.build()  # Build the lexer
    print(m.scan(open(sys.argv[1]).read()) )
