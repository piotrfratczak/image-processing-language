import io
import pytest

from src.lexer.lexer import Lexer
from src.lexer.token_type import TokenType
from src.source.source import FileSource
from src.exceptions.exceptions import *


def test_source():
    source = FileSource(io.StringIO('a'))
    source.next_char()
    source.next_char()
    assert source.position.line == 1
    assert source.position.column == 1
    assert source.byte == 1


def new_lexer(source_string):
    return Lexer(FileSource(io.StringIO(source_string)))

# TODO 1 znak != 1 bajt + test
def test_is_eof():
    lexer = new_lexer('')
    token = lexer.get_next_token()
    assert token.type == TokenType.EOT


def test_build_id(): # TODO rozbić testy
    id_test_helper('i')
    id_test_helper('id')
    id_test_helper('id_')
    id_test_helper('id_compound')
    id_test_helper('id4')
    id_test_helper('id5ab')
    id_test_helper('id6_o2')
    
    id_test_helper('id7 decoy', 'id7')
    id_test_helper('id8^decoy', 'id8')
    id_test_helper('id9-decoy', 'id9')
    id_test_helper('id10.decoy', 'id10')


def id_test_helper(tested_id, expected=None):
    if expected is None:
        expected = tested_id
    lexer = new_lexer(tested_id)
    token = lexer.get_next_token()
    assert token.type == TokenType.ID
    assert token.value == expected


def test_skip_whitespaces():
    lexer = new_lexer('     a')
    token = lexer.get_next_token()
    assert token.type == TokenType.ID
    assert token.value == 'a'


# def test_build_keyword():   # TODO zrobic listę dla testów do sprawdzenia
#     keyword_list = Tokens.keywords.keys()
#     keyword_file = ' '.join(keyword_list)
#     lexer = new_lexer(keyword_file)
#     for keyword in keyword_list:
#         token = lexer.get_next_token()
#         assert token.type == Tokens.keywords[keyword]


def test_build_number():
    value = 123456
    file_text = str(value) + ' 05'
    lexer = new_lexer(file_text)

    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER
    assert token.value == value

    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER
    assert token.value == 0


def test_build_comment():
    file_text = '# this is a comment 478 #11 !@""'
    lexer = new_lexer(file_text + '\n')
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMENT
    assert token.value == file_text


# def test_build_operator():
#     operator_list = Tokens.operators.keys()
#     compound_operator_list = Tokens.compound_operators
#     operator_file = ' '.join(operator_list) + ' ' + ' '.join(compound_operator_list)
#     lexer = new_lexer(operator_file)

#     for operator in operator_list:
#         token = lexer.get_next_token()
#         assert token.type == Tokens.operators[operator]

#     for operator in compound_operator_list:
#         token = lexer.get_next_token()
#         assert token.type == Tokens.compound_operators[operator]


def test_expression():
    file_text = 'a + 2 > 3*b'
    lexer = new_lexer(file_text)

    token = lexer.get_next_token()
    assert token.type == TokenType.ID
    assert token.value == 'a'

    token = lexer.get_next_token()
    assert token.type == TokenType.ADD

    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER
    assert token.value == 2

    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER_THAN

    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER
    assert token.value == 3

    token = lexer.get_next_token()
    assert token.type == TokenType.MULTIPLY

    token = lexer.get_next_token()
    assert token.type == TokenType.ID
    assert token.value == 'b'


def test_statement():
    file_text = 'm=matrix(3,5);'
    lexer = new_lexer(file_text)

    token = lexer.get_next_token()
    assert token.type == TokenType.ID
    assert token.value == 'm'

    token = lexer.get_next_token()
    assert token.type == TokenType.ASSIGN

    token = lexer.get_next_token()
    assert token.type == TokenType.MATRIX

    token = lexer.get_next_token()
    assert token.type == TokenType.L_PARENTHESIS

    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER
    assert token.value == 3

    token = lexer.get_next_token()
    assert token.type == TokenType.COMMA

    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER
    assert token.value == 5

    token = lexer.get_next_token()
    assert token.type == TokenType.R_PARENTHESIS

    token = lexer.get_next_token()
    assert token.type == TokenType.SEMICOLON


def test_id_too_long():
    file_text = 'a' * 129
    lexer = new_lexer(file_text)
    with pytest.raises(IdTooLongException):
        lexer.get_next_token()


def test_comment_too_long():
    file_text = '#' + 'a' * 512
    lexer = new_lexer(file_text)
    with pytest.raises(CommentTooLongException):
        lexer.get_next_token()


def test_number_too_large():
    value = pow(2, 128) + 1
    file_text = str(value)
    lexer = new_lexer(file_text)
    with pytest.raises(NumberTooLargeException):
        lexer.get_next_token()
