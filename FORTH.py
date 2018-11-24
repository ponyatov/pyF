#!/usr/bin/env python2.7
# tiny object FORTH in Python

# object system

## base object (universal data container)
class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
    def __repr__(self):
        return self.dump()
    def dump(self):
        return self.head()
    def head(self):
        return '<%s:%s>' % (self.type,self.value)

class Primitive(Object): pass
class Symbol(Primitive): pass
class String(Primitive): pass
class Number(Primitive): pass

class Container(Object): pass
class Stack(Container): pass
class Map(Container): pass

## active object has execution semantics
class Active(Object): pass

## function
class Fn(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def __call__(self):
        self.fn()

# data stack
S = Stack('data')

# vocabulary
W = Map('FORTH')

# ? ( -- ) print data stack
def q(): print S
W['?'] = Fn(q)

# syntax parser using PLY library
import ply.lex as lex   # FORTH has no syntax: lexer only

tokens = ['symbol','number','string']

t_ignore = ' \t\r\n'

states = (('str','exclusive'),)

t_str_ignore = ''

def t_string(t):
    r'\''
    t.lexer.string = '' ; t.lexer.push_state('str')
def t_str_string(t):
    r'\''
    t.lexer.pop_state()
    return String(t.lexer.string)
def t_str_any(t):
    r'.'
    t.lexer.string += t.value

def t_number(t):
    r'[0-9]+'
    return Number(t.value)

def t_symbol(t):
    r'[a-zA-Z0-9_]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

# WORD ( -- token ) get next literal object from source code stream
def WORD():
    token = lexer.token()
    if not token: return False
    S.push(token) ; return True

# INTERPRET ( string:src -- ... ) interpret given string
def INTERPRET():
    lexer.input(pop())
    while True:
        if not WORD(): break
        q()

while True:
    S.push(raw_input('ok> ')) ; INTERPRET()

