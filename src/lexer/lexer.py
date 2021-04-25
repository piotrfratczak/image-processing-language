from .token import Token
from .token_map import TokenMap
from .token_types import TokenTypes
from ..exceptions.exceptions import *


class Lexer:
    def __init__(self, source):
        self.__source = source
        self.__source.next_char()
        self.token = None
        self.__ID_MAX_LENGTH = 128
        self.__COMMENT_MAX_LENGTH = 512
        self.__MAX_NUMBER = pow(2, 128)

    def get_next_token(self):
        self.skip_whitespaces()

        if self.is_eof():
            return Token(TokenTypes.EOT, self.__source.position)

        if self.build_number():
            return self.token
        if self.build_keyword_or_id():
            return self.token
        if self.build_comment():
            return self.token
        if self.build_operator():
            return self.token

        self.token = Token(TokenTypes.UNKNOWN, self.__source.position)
        return self.token

    def build_number(self):
        if self.__source.char.isdigit():
            value = 0
            if self.__source.char != '0':
                value = int(self.__source.char)
                while self.get_next_char().isdigit():
                    value = value*10 + int(self.__source.char)
                    if value > self.__MAX_NUMBER:
                        raise NumberTooLargeException(self.__source.position, value)

            self.token = Token(TokenTypes.NUMBER, self.__source.position, value)
            return True
        return False

    def build_keyword_or_id(self):
        if self.__source.char.isalpha():
            token_str = self.__source.char
            cur_char = self.get_next_char()
            while cur_char.isalpha() or cur_char.isdigit() or cur_char == '_':
                token_str += cur_char
                if len(token_str) > self.__ID_MAX_LENGTH:
                    raise IdTooLongException(self.__source.position)
                cur_char = self.get_next_char()

            if token_str in TokenMap.keywords:
                self.token = Token(TokenMap.keywords[token_str], self.__source.position)
            else:  # id
                self.token = Token(TokenTypes.ID, self.__source.position, token_str)
            return True
        return False

    def build_comment(self):
        if self.__source.char == '#':
            comment_position = self.__source.position
            comment_str = '#'
            while self.get_next_char() != '\n':
                comment_str += self.__source.char
                if len(comment_str) > self.__COMMENT_MAX_LENGTH:
                    raise CommentTooLongException(self.__source.position, comment_position)

            self.token = Token(TokenTypes.COMMENT, self.__source.position, comment_str)
            return True
        return False

    def build_operator(self):
        if self.__source.char in TokenMap.operators.keys():
            operator_str = self.__source.char
            self.token = Token(TokenMap.operators[operator_str], self.__source.position)

            operator_str += self.get_next_char()
            if operator_str in TokenMap.compound_operators.keys():
                self.token = Token(TokenMap.compound_operators[operator_str], self.__source.position)
                self.get_next_char()
            return True
        return False

    def skip_whitespaces(self):
        while self.__source.char.isspace():
            self.__source.next_char()

    def get_next_char(self):
        self.__source.next_char()
        return self.__source.char

    def is_eof(self):
        return self.__source.char == '' or self.__source.char is None
