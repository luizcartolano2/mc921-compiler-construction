#!/usr/bin/env python
# coding: utf-8

# # Dúvidas
# 1. Assign ou Equals?

# list of token names
tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'SEMI',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'INT_CONST',
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
]

# reserved words
reserved = {
    'if'     : 'IF',
    'for'    : 'FOR',
    'void'   : 'VOID',
    'int'    : 'INT',
    'float'  : 'FLOAT',
    'char'   : 'CHAR',
    'assert' : 'ASSERT',
    'else'   : 'ELSE',
    'while'  : 'WHILE',
    'break'  : 'BREAK',
    'print'  : 'PRINT',
    'read'   : 'READ',
    'return' : 'RETURN',
}

tokens += list(reserved.values())

t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_EQUALS      = r'='
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_SEMI        = r';'
t_EQ          = r'=='
t_COMMA       = r'\,'
t_ADDRESS     = r'\&'
t_PLUSPLUS    = r'\+\+'
t_MINUSMINUS  = r'\-\-'
t_NOT         = r'\!'
t_GT          = r'\>'
t_LT          = r'\<'
t_MOD         = r'\%'
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
# A string containing ignored characters (spaces and tabs)
t_ignore  = " \t"


def t_INT_CONST(t):
    r'[0-9]+'
    t.value = str((t.value))
   
    return t


def t_FLOAT_CONST(t):
    r'([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)'
    t.value = str(float(t.value))
        
    return t


def t_STRING_LITERAL(t):
    r'\"(\\.|[^\"\\])*\"'
    t.value = str(t.value)
    
    return t


def t_ID(t):
    r'[a-zA-Z_][0-9a-zA-Z_]*'
    # check for reserved words
    t.type = reserved.get(t.value,'ID')

    return t


# define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# define a comment /**/
def t_COMMENT(t):
    r'\/\*(.|\n)*\*\/'
    pass


# define a comment //
def t_COMMENT_2(t):
    r'\/\/[^\n\r]*?(?:\*\)|[\n\r])'
    pass


def t_error_comment(t):
    r'/\*(.|\n)*$'
    print("{}: Unterminated comment".format(t.lexer.lineno))
    t.lexer.skip(1)
    
    
def t_error_string(t):
    r'\"[^\"]*$'
    print("{}: Unterminated string".format(t.lexer.lineno))
    t.lexer.skip(1)