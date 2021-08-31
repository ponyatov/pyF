## Object HyperGraph node
class Object:

    ## @name constructor

    def __init__(self, V):
        self.value = V # scalar
        self.nest = [] # ordered container = vector = nested AST

    def box(self, that):
        if isinstance(that, Object): return that
        else: raise TypeError(['box', type(that), that])

    ## @name dump

    def test(self): return self.dump(test=True)

    def dump(self, cycle=[], depth=0, prefix='', test=False):
        # head
        def pad(depth): return '\n' + '\t' * depth
        ret = pad(depth) + self.head(prefix, test)
        # slot{}s
        # nest[]ed
        for j, k in enumerate(self):
            ret += k.dump(cycle, depth + 1, f'{j}: ', test)
        # subtree
        return ret

    def head(self, prefix='', test=False):
        gid = '' if test else f' {id(self):x}'
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    def tag(self): return self.__class__.__name__.lower()

    def val(self): return f'{self.value}'

    ## @name operator

    def __iter__(self): return iter(self.nest)

    def __floordiv__(self, that):
        that = self.box(that)
        self.nest.append(that); return self
