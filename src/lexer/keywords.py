from .token_type import TokenType


def get_keyword(token_str):
    keywords = {
        'and': TokenType.AND,
        'or': TokenType.OR,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'if': TokenType.IF,
        'of': TokenType.OF,
        'newop': TokenType.NEW_OPERATOR,
        'else': TokenType.ELSE,
        'return': TokenType.RETURN,
        'number': TokenType.NUMBER_TYPE,
        'pixel': TokenType.PIXEL,
        'matrix': TokenType.MATRIX
    }
    if token_str in keywords:
        return keywords[token_str]
    else:
        return None


def get_operator(token_str):
    operators = {
        '+': TokenType.ADD,
        '-': TokenType.SUBTRACT,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '@': TokenType.SPECIAL_MULTIPLY,
        '%': TokenType.MODULO,
        '.': TokenType.DOT,
        ',': TokenType.COMMA,
        ';': TokenType.SEMICOLON,
        '(': TokenType.L_PARENTHESIS,
        ')': TokenType.R_PARENTHESIS,
        '{': TokenType.L_BRACE,
        '}': TokenType.R_BRACE,
        '[': TokenType.L_BRACKET,
        ']': TokenType.R_BRACKET
    }
    if token_str in operators:
        return operators[token_str]
    else:
        return None


def get_compound_operator(token_str):
    if token_str == '!':
        return TokenType.NOT
    elif token_str == '<':
        return TokenType.LESS_THAN
    elif token_str == '>':
        return TokenType.GREATER_THAN
    elif token_str == '=':
        return TokenType.ASSIGN
    elif token_str == '==':
        return TokenType.EQUAL
    elif token_str == '!=':
        return TokenType.NOT_EQUAL
    elif token_str == '>=':
        return TokenType.GREATER_OR_EQUAL
    elif token_str == '<=':
        return TokenType.LESS_OR_EQUAL
    else:
        return None
