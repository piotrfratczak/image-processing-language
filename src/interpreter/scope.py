from typing import Optional
from ..exceptions.exceptions import *
from .variables import *


class Scope:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, name: str, value):
        self.symbols[name] = value

    def get_symbol(self, name: str):
        if name not in self.symbols.keys():
            raise UndeclaredSymbolError(name)
        return self.symbols[name]

    def copy_symbols(self, source):
        self.symbols.update(source)


class ScopeManager:
    def __init__(self):
        self.global_scope = Scope('global')
        self.local_scope = Scope('main')
        self.last_result: Optional[int, PixelVariable, MatrixVariable, List[MatrixVariable]] = None
        self.return_result: Optional[int, PixelVariable, MatrixVariable, List[MatrixVariable]] = None

    def add_variable(self, name: str, value):
        if name in self.local_scope.symbols.keys():
            raise OverwriteError(name)
        self.local_scope.add_symbol(name, value)

    def update_variable(self, name: str, value):
        if name not in self.local_scope.symbols.keys():
            raise UndeclaredSymbolError(name)
        if not isinstance(value, type(self.local_scope.symbols[name])):
            raise TypeMismatchError(name)
        self.local_scope.symbols[name] = value

    def get_variable(self, name: str):
        return self.local_scope.get_symbol(name)

    def add_function(self, name: str, function):
        self.global_scope.add_symbol(name, function)

    def get_function(self, name: str):
        return self.global_scope.get_symbol(name)

    def switch_to_new_scope(self, function):
        self.local_scope = Scope(function.id, self.local_scope)

    def switch_to_parent_scope(self):
        if not self.local_scope.parent:
            raise NoParentScopeError(self.local_scope.name)
        self.last_result = self.return_result
        self.local_scope = self.local_scope.parent
        self.return_result = None
