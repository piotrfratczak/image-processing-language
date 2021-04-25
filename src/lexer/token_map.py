from .token_types import TokenTypes


class TokenMap:
    keywords = {
        'and':    TokenTypes.AND,
        'or':     TokenTypes.OR,
        'while':  TokenTypes.WHILE,
        'for':    TokenTypes.FOR,
        'in':     TokenTypes.IN,
        'if':     TokenTypes.IF,
        'of':     TokenTypes.OF,
        'newop':  TokenTypes.NEW_OPERATOR,
        'else':   TokenTypes.ELSE,
        'return': TokenTypes.RETURN,
        'number': TokenTypes.NUMBER,
        'pixel':  TokenTypes.PIXEL,
        'matrix': TokenTypes.MATRIX
    }

    operators = {
        '!': TokenTypes.NOT,
        '<': TokenTypes.LESS_THAN,
        '>': TokenTypes.GREATER_THAN,
        '=': TokenTypes.ASSIGN,
        '+': TokenTypes.ADD,
        '-': TokenTypes.SUBTRACT,
        '*': TokenTypes.MULTIPLY,
        '/': TokenTypes.DIVIDE,
        '@': TokenTypes.SPECIAL_MULTIPLY,
        '%': TokenTypes.MODULO,
        '.': TokenTypes.DOT,
        ',': TokenTypes.COMMA,
        ';': TokenTypes.SEMICOLON,
        '(': TokenTypes.L_PARENTHESIS,
        ')': TokenTypes.R_PARENTHESIS,
        '{': TokenTypes.L_BRACE,
        '}': TokenTypes.R_BRACE,
        '[': TokenTypes.L_BRACKET,
        ']': TokenTypes.R_BRACKET 
    }

    compound_operators = {
        '==': TokenTypes.EQUAL,
        '!=': TokenTypes.NOT_EQUAL,
        '>=': TokenTypes.GREATER_OR_EQUAL,
        '<=': TokenTypes.LESS_OR_EQUAL 
    }
