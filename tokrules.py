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
    #'ASSIGN',
    'SEMI',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'ICONST',
    'FCONST',
    'SCONST',
    'ID',
    'EQ',
    'EQUALS',
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
}

tokens += list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMI    = r';'
t_EQ      = r'=='


def t_ICONST(t):
    r'[0-9]+'
    t.value = int(t.value)
   
    return t


def t_FCONST(t):
    r'([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)'
    t.value = float(t.value)
        
    return t


def t_SCONST(t):
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


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'