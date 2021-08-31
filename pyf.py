
import os, sys, re, time
import datetime as dt

class Object:
    def __init__(self, V):
        self.value = V
        self.nest = []

    ## Python types wrapper
    def box(self, that):
        if isinstance(that, Object): return that
        raise TypeError(['box', type(that), that])

    ## @name text dump

    def __repr__(self): return self.dump()

    def dump(self, cycle=[], depth=0, prefix=''):
        def pad(depth): return '\n' + '\t' * depth
        ret = pad(depth) + self.head(prefix)
        return ret

    def head(self, prefix=''):
        gid = f' {id(self):x}'
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    def tag(self): return self.__class__.__name__.lower()
    def val(self): return f'{self.value}'

    ## @name operator

    def __iter__(self): return iter(self.nest)

    def __floordiv__(self, that):
        that = self.box(that)
        self.nest.append(that); return self

class IO(Object):
    def __init__(self, V):
        super().__init__(V)
        self.path = V

class Dir(IO):

    def __floordiv__(self, that):
        assert isinstance(that, IO)
        that.path = f'{self.path}/{that.path}'
        return super().__floordiv__(that)

    def sync(self):
        try: os.mkdir(self.path)
        except FileExistsError: pass
        for i in self: i.sync()

class File(IO):
    def __init__(self, V, ext, tab='\t', comment='#'):
        super().__init__(V + ext)
        self.ext = ext
        self.tab = tab
        self.comment = comment

    def sync(self):
        with open(self.path, 'w') as F:
            pass

class Meta(Object): pass

class jsonFile(File):
    def __init__(self, V, ext='.json'):
        super().__init__(V, ext)

class Project(Meta):
    def __init__(self, V=None):
        if not V: V = os.getcwd().split('/')[-1]
        super().__init__(V)
        self.g_dir()
        self.g_vscode()

    def g_dir(self):
        self.d = Dir(self.value)

    def g_vscode(self):
        self.vscode = Dir('.vscode'); self.d // self.vscode
        self.settings = jsonFile('settings'); self.vscode // self.settings

    def sync(self):
        self.d.sync()

if __name__ == '__main__':
    if sys.argv[1] == 'meta':
        p = Project()
        p.sync()

# for i in [
# './.vscode/settings.json', \
# './.vscode/tasks.json', \
# './.vscode/extensions.json', \
# './bin/.gitignore', \
# './doc/.gitignore', \
# './lib/.gitignore', \
# './src/.gitignore', \
# './tmp/.gitignore', \
# './gitignore', \
# './pyf.py', \
# './README.md', \
# './Makefile', \
# './apt.txt', \
# './apt.dev', \
# './requirements.txt', \
# ]: os.system(f'touch {i}')

# 'python3 -m venv .'

# settings \
# {
#     "multiCommand.commands": [
#         {
#             "command": "multiCommand.f12",
#             "sequence": [
#                 "workbench.action.files.saveAll",
#                 {"command": "workbench.action.terminal.sendSequence",
#                     "args": {"text": "\u000D clear ; make meta \u000D"}}
#                 ]
#         },
#     ]
# }


# mk \
# MODULE = $(notdir $(CURDIR))

# PY  = bin/python3
# PIP = bin/pip3
# PEP = bin/autopep8

# meta: $(PY) $(MODULE).py
# 	$^

# install:
# 	python3 -m venv .
# 	bin/pip3 install -U autopep8 pytest
# 	bin/pip3 install -U -r requirements.txt
