#!/usr/bin/env python2.7

## @file
## @brief tiny object FORTH in Python

## @defgroup pyf pyFORTH
## @brief tiny object FORTH in Python
## @{

## @defgroup sym symbolic object system
## @brief computation on universal data containers
## @{

## @defgroup object base Object
## @brief universal data container
## @{

## base object
class Object:
    ## construct object with given primitive value
    def __init__(self,V):
        ## class/type tag
        self.type = self.__class__.__name__.lower()
        ## single primitive value (in implementation language: Python)
        self.value = V
        ## **ordered**: `nest[]`ed elements = stack = vector = array
        self.nest = []
        ## **associative array**: object slots = map elements (string keyed)
        self.attr = {}

    ## @name dump
    ## @{

    ## print object
    def __repr__(self):
        return self.dump()
    ## full dump in tree form
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    ## short dump: header only
    def head(self,prefix=''):
        return '%s<%s:%s>' % (prefix,self.type,self.value)
    def pad(self,N):
        return '\n' + '\t'*N
    ## @}

    ## @name associative array
    ## @{

    ## store `=` operator `self[key] = obj`
    def __setitem__(self,key,obj):
        self.attr[key] = obj ; return self
    ## fetch operator `self[key]`
    def __getitem__(self,key):
        return self.attr[key]
    ## @}
    
    ## @name stack
    ## @{
    def push(self,obj):
        self.nest.append(obj) ; return self
    def pop(self):
        return self.nest.pop()
    ## @}

## @}

## @defgroup Primitives
## @{

class Primitive(Object): pass

## @defgroup symbol Symbol
## @{
class Symbol(Primitive): pass
## @}

## @defgroup string String
## @{
class String(Primitive): pass
## @}

## @defgroup number Numbers
## @{
class Number(Primitive): pass
class Integer(Number): pass
class Hex(Integer): pass
class Bin(Integer): pass
## @}

## @}

## @defgroup cont Data containers
## @{

class Container(Object): pass
class Stack(Container): pass
class Map(Container): pass

## @}

## @defgroup active Active objects
## @brief has execution semantics
## @{

class Active(Object): pass

## function
class Fn(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def __call__(self):
        self.fn()

## @}

## @}

## data stack
S = Stack('data')

## vocabulary
W = Map('FORTH')

## `? ( -- )` print data stack
def q(): print S
W['?'] = Fn(q)

## @defgroup interp interpreter
## @{

## @defgroup ply syntax parser using PLY library
## @brief FORTH has no syntax: lexer only
## @{

import ply.lex as lex

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

def t_ANY_error(t): raise SyntaxError(t)

lexer = lex.lex()

## @}

# WORD ( -- token ) get next literal object from source code stream
def WORD():
    token = lexer.token()
    if not token: return False
    S.push(token) ; return True

# INTERPRET ( string:src -- ... ) interpret given string
def INTERPRET():
    lexer.input(S.pop())
    while True:
        if not WORD(): break
        q()

# startup: run command line console
while True:
    S.push(raw_input('ok> ')) ; INTERPRET()

## @}

## @}

