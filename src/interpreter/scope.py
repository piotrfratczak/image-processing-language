from typing import Optional
from collections import deque
from .variables import *
from ..exceptions.exceptions import *


class Scope:
    def __init__(self, name: str):
        self.name = name
        self.symbols = {}

    def add_symbol(self, name: str, value):
        if name in self.symbols.keys():
            raise OverwriteException(name)
        self.symbols[name] = value

    def get_symbol(self, name: str):
        if name not in self.symbols.keys():
            raise UndeclaredSymbolException(name)
        return self.symbols[name]

    def has_symbol(self, name: str):
        return name in self.symbols.keys()

    def update_symbol(self, name: str, value):
        if name not in self.symbols.keys():
            raise UndeclaredSymbolException(name)
        if not isinstance(value, type(self.symbols[name])):
            raise TypeMismatchError(type(self.symbols[name]), type(value))
        self.symbols[name] = value

    def copy_symbols(self, source):
        self.symbols.update(source)


class ScopeManager:
    def __init__(self):
        self.__global_scope = Scope('global')
        self.__scope_stack = deque()
        self.__scope_stack.append(Scope('main'))

        self.last_result: Optional[int, PixelVariable, MatrixVariable, List[MatrixVariable]] = None
        self.return_result: Optional[int, PixelVariable, MatrixVariable, List[MatrixVariable]] = None

    def add_variable(self, name: str, value):
        if len(self.__scope_stack) == 0:
            raise OutOfScopeError()
        self.__scope_stack[-1].add_symbol(name, value)

    def add_update_variable(self, name: str, value):
        for scope in reversed(self.__scope_stack):
            if scope.has_symbol(name):
                scope.update_symbol(name, value)
                return
        if len(self.__scope_stack) > 0:
            self.__scope_stack[-1].add_symbol(name, value)

    def get_variable(self, name: str):
        for scope in reversed(self.__scope_stack):
            if scope.has_symbol(name):
                return scope.get_symbol(name)
        raise UndeclaredSymbolException(name)

    def add_function(self, name: str, function):
        self.__global_scope.add_symbol(name, function)

    def get_function(self, name: str):
        return self.__global_scope.get_symbol(name)

    def switch_to_new_scope(self, name: str):
        self.__scope_stack.append(Scope(name))

    def switch_to_previous_scope(self):
        if len(self.__scope_stack) <= 1:
            raise NoParentScopeError(self.__scope_stack[-1].name)
        self.__scope_stack.pop()
        self.last_result = self.return_result
        self.return_result = None
