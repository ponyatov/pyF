from pyf import *

def test_any(): assert True

def hello(): return Object("Hello")
def world(): return Object('World')

def test_hello():
    assert hello().test() == \
        '\n<object:Hello>'

def test_world():
    assert (hello() // world()).test() == \
        '\n<object:Hello>\n\t0: <object:World>'
