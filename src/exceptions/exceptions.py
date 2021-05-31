class NumberTooLargeException(Exception):
    def __init__(self, position, value):
        self.__position = position
        self.__value = value
        self.__message = "Number too large ({}) at: {}, {}.".format(self.__value,
                                                                    self.__position.line,
                                                                    self.__position.column)
        super().__init__(self.__message)


class IdTooLongException(Exception):
    def __init__(self, position):
        self.__position = position
        self.__message = "Identifier too long at: {}, {}.".format(self.__position.line,
                                                                  self.__position.column)
        super().__init__(self.__message)


class CommentTooLongException(Exception):
    def __init__(self, position, start_position):
        self.__position = position
        self.__start_position = start_position
        self.__message = "Comment starting at: {}, {}; too long at: {}, {}.".format(self.__start_position.line,
                                                                                    self.__start_position.column,
                                                                                    self.__position.line,
                                                                                    self.__position.column)
        super().__init__(self.__message)


class SyntaxException(Exception):
    def __init__(self, position, byte, message="Exception"):
        self.__position = position
        self.__byte = byte
        self.__message = "Syntax Exception. {} at: {}, {}.".format(message,
                                                                   self.__position.line,
                                                                   self.__position.column)


class UndeclaredSymbolError(Exception):
    def __init__(self, name: str):
        self.__name = name


class OverwriteError(Exception):
    def __init__(self, name: str):
        self.__name = name


class TypeMismatchError(Exception):
    def __init__(self, name: str):
        self.__name = name


class NoParentScopeError(Exception):
    def __init__(self, name: str):
        self.__name = name


class NoMainFunctionException(Exception):
    pass


class ArgumentTypeException(Exception):
    pass


class InvalidVariableTypeException(Exception):
    pass


class IllicitOperatorException(Exception):
    pass


class InvalidArgumentsNumberException(Exception):
    pass


class MatrixDimensionsException(Exception):
    pass
