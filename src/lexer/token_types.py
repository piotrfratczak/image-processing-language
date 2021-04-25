from enum import Enum, auto


class TokenTypes(Enum):
    ID = auto()
    COMMENT = auto()
    EOT = auto()
    UNKNOWN = auto()

    AND = auto()
    OR = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    IF = auto()
    OF = auto()
    NEW_OPERATOR = auto()
    ELSE = auto()
    RETURN = auto()

    NUMBER = auto()
    PIXEL = auto()
    MATRIX = auto()

    NOT = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    ASSIGN = auto()
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    SPECIAL_MULTIPLY = auto()
    MODULO = auto()
    HASHTAG = auto()
    DOT = auto()
    COMMA = auto()
    SEMICOLON = auto()
    L_PARENTHESIS = auto()
    R_PARENTHESIS = auto()
    L_BRACE = auto()
    R_BRACE = auto()
    L_BRACKET = auto()
    R_BRACKET = auto()

    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER_OR_EQUAL = auto()
    LESS_OR_EQUAL = auto()
