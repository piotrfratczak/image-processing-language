from .token import Token
from .keywords import *
from .token_type import TokenType
from ..exceptions.exceptions import *


class Lexer:
    def __init__(self, source, max_id_length=128, max_comment_length=512, max_number=pow(2, 128)):
        self.__source = source
        self.__source.next_char()

        self.token = None
        self.token_start_position = None
        self.token_start_byte = None

        self.__max_id_length = max_id_length
        self.__max_comment_length = max_comment_length
        self.__max_number = max_number

    def get_next_token(self):
        self.skip_whitespaces()
        self.set_next_start_position()

        if self.is_eof():
            return self.construct_token(TokenType.EOT)

        if self.build_number():
            return self.token
        if self.build_keyword_or_id():
            return self.token
        if self.build_comment():
            return self.token
        if self.build_operator():
            return self.token

        self.token = self.construct_token(TokenType.UNKNOWN)
        return self.token

    def build_number(self):
        if not self.__source.char.isdigit():
            return False

        value = 0
        if self.__source.char != '0':
            value = int(self.__source.char)
            while self.get_next_char().isdigit():
                if value > self.__max_number:
                    raise NumberTooLargeException(self.__source.position, value)
                value = value*10 + int(self.__source.char)
        else:
            self.get_next_char()

        self.token = self.construct_token(TokenType.NUMBER, value)
        return True

    def build_keyword_or_id(self):
        if not self.__source.char.isalpha():
            return False

        token_chars = [self.__source.char]
        cur_char = self.get_next_char()
        while cur_char.isalpha() or cur_char.isdigit() or cur_char == '_':
            if len(token_chars) == self.__max_id_length:
                raise IdTooLongException(self.__source.position)
            token_chars.append(cur_char)
            cur_char = self.get_next_char()
        token_str = ''.join(token_chars)

        token_keyword = get_keyword(token_str)
        if token_keyword:  # keyword
            self.token = self.construct_token(token_keyword)
        else:  # id
            self.token = self.construct_token(TokenType.ID, token_str)
        return True

    def build_comment(self):
        if self.__source.char != '#':
            return False

        comment_chars = ['#']
        while self.get_next_char() != '\n' and not self.is_eof():
            if len(comment_chars) > self.__max_comment_length:
                raise CommentTooLongException(self.__source.position, self.token_start_position)
            comment_chars.append(self.__source.char)
        comment_str = ''.join(comment_chars)

        self.token = self.construct_token(TokenType.COMMENT, comment_str)
        return True

    def build_operator(self):
        first_char = self.__source.char
        two_chars = first_char + self.get_next_char()

        simple_operator = get_operator(first_char)
        if simple_operator:
            self.token = self.construct_token(simple_operator)
            return True

        compound_operator = get_compound_operator(two_chars)
        if compound_operator:
            self.token = self.construct_token(compound_operator)
            self.get_next_char()
            return True

        simple_comparison_operator = get_compound_operator(first_char)
        if simple_comparison_operator:
            self.token = self.construct_token(simple_comparison_operator)
            return True

        return False

    def skip_whitespaces(self):
        while self.__source.char.isspace():
            self.__source.next_char()

    def set_next_start_position(self):
        self.token_start_position = self.__source.position
        self.token_start_byte = self.__source.byte

    def construct_token(self, token_type, value=None):
        return Token(token_type, self.token_start_position, self.token_start_byte, value)

    def get_next_char(self):
        self.__source.next_char()
        return self.__source.char

    def is_eof(self):
        return self.__source.is_eof or self.__source.char is None
