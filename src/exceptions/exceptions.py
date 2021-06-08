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
        super().__init__(self.__message)


class UndeclaredSymbolException(Exception):
    def __init__(self, name: str):
        self.__name = name
        self.__message = "Semantic Exception. Undeclared symbol {}.".format(self.__name)

        super().__init__(self.__message)


class OverwriteException(Exception):
    def __init__(self, name: str):
        self.__name = name
        self.__message = "Semantic Exception. Symbol {} must not be overwritten.".format(self.__name)

        super().__init__(self.__message)


class TypeMismatchError(Exception):
    def __init__(self, variable, expected, actual):
        self.__variable = variable
        self.__expected = expected
        self.__actual = actual
        self.__message = "Semantic Exception. Type mismatch of {} - expected {} but received {}." \
            .format(self.__variable, self.__expected, self.__actual)

        super().__init__(self.__message)


class NoParentScopeError(Exception):
    def __init__(self, name: str):
        self.__name = name
        self.__message = "Error. {} has no parent scope.".format(self.__name)

        super().__init__(self.__message)


class NoMainFunctionException(Exception):
    def __init__(self):
        self.__message = "Exception. No main function was found."

        super().__init__(self.__message)


class ArgumentTypeException(Exception):
    def __init__(self, variable, expected, actual):
        self.__variable = variable
        self.__expected = expected
        self.__actual = actual
        self.__message = "Semantic Exception. Argument type of {} is {} but {} was expected." \
            .format(self.__variable, self.__actual, self.__expected)

        super().__init__(self.__message)


class InvalidVariableTypeException(Exception):
    def __init__(self, name: str):
        self.__name = name
        self.__message = "Exception. {} is not a valid variable type.".format(self.__name)

        super().__init__(self.__message)


class IllicitOperatorException(Exception):
    def __init__(self, operator, type1, type2):
        self.__operator = operator
        self.__type1 = type1
        self.__type2 = type2
        self.__message = "Semantic Exception. Operator {} must not be used for types {} and {}.".format(self.__operator,
                                                                                                        self.__type1,
                                                                                                        self.__type2)
        super().__init__(self.__message)


class InvalidArgumentsNumberException(Exception):
    def __init__(self, initial_message, actual):
        self.__initial_message = initial_message
        self.__actual = actual
        self.__message = "Invalid Arguments Number Exception. {} Received {} arguments.".format(self.__initial_message,
                                                                                                self.__actual)
        super().__init__(self.__message)


class MatrixDimensionsException(Exception):
    def __init__(self, expected, actual):
        self.__expected = expected
        self.__actual = actual
        self.__message = "Invalid Matrix dimensions Exception. Expected {} but received {}.".format(self.__expected,
                                                                                                    self.__actual)
        super().__init__(self.__message)


class ComparisonTypeMismatchException(Exception):
    def __init__(self, expected, actual, comparison):
        self.__expected = expected
        self.__actual = actual
        self.__comparison = comparison
        self.__message = "Compared Types Mismatch Exception. {} and {} must not be compared with {}." \
            .format(self.__expected, self.__actual, self.__comparison)

        super().__init__(self.__message)


class OutOfScopeError(Exception):
    def __init__(self):
        self.__message = "Out of Scope Error."

        super().__init__(self.__message)


class IndexOutOfRangeError(Exception):
    def __init__(self):
        self.__message = "Index out of range."

        super().__init__(self.__message)


class UndefinedReferenceException(Exception):
    def __init__(self, _id):
        self.__id = _id
        self.__message = "Undefined Reference Exception to unknown {}.".format(self.__id)

        super().__init__(self.__message)


class ZeroDivisionException(Exception):
    def __init__(self):
        self.__message = "Division by 0 is illegal!"

        super().__init__(self.__message)
