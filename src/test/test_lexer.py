import io
import pytest

from src.lexer.lexer import Lexer
from src.lexer.token_types import TokenTypes
from src.lexer.token_map import TokenMap
from src.source.source import FileSource
from src.exceptions.exceptions import *


def new_lexer(source_string):
    return Lexer(FileSource(io.StringIO(source_string)))


def test_is_eof():
    lexer = new_lexer('')
    token = lexer.get_next_token()
    assert token.type == TokenTypes.EOT


def test_build_id():
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
    assert token.type == TokenTypes.ID
    assert token.value == expected


def test_skip_whitespaces():
    lexer = new_lexer('     a')
    token = lexer.get_next_token()
    assert token.type == TokenTypes.ID
    assert token.value == 'a'


def test_build_keyword():
    keyword_list = TokenMap.keywords.keys()
    keyword_file = ' '.join(keyword_list)
    lexer = new_lexer(keyword_file)
    for keyword in keyword_list:
        token = lexer.get_next_token()
        assert token.type == TokenMap.keywords[keyword]


def test_build_number():
    value = 123456
    file_text = str(value) + ' 05'
    lexer = new_lexer(file_text)

    token = lexer.get_next_token()
    assert token.type == TokenTypes.NUMBER
    assert token.value == value

    token = lexer.get_next_token()
    assert token.type == TokenTypes.NUMBER
    assert token.value == 0


def test_build_comment():
    file_text = '# this is a comment 478 #11 !@""'
    lexer = new_lexer(file_text + '\n')
    token = lexer.get_next_token()
    assert token.type == TokenTypes.COMMENT
    assert token.value == file_text


def test_build_operator():
    operator_list = TokenMap.operators.keys()
    compound_operator_list = TokenMap.compound_operators
    operator_file = ' '.join(operator_list) + ' ' + ' '.join(compound_operator_list)
    lexer = new_lexer(operator_file)

    for operator in operator_list:
        token = lexer.get_next_token()
        assert token.type == TokenMap.operators[operator]

    for operator in compound_operator_list:
        token = lexer.get_next_token()
        assert token.type == TokenMap.compound_operators[operator]


def test_expression():
    file_text = 'a + 2 > 3*b'
    lexer = new_lexer(file_text)

    token = lexer.get_next_token()
    assert token.type == TokenTypes.ID
    assert token.value == 'a'

    token = lexer.get_next_token()
    assert token.type == TokenTypes.ADD

    token = lexer.get_next_token()
    assert token.type == TokenTypes.NUMBER
    assert token.value == 2

    token = lexer.get_next_token()
    assert token.type == TokenTypes.GREATER_THAN

    token = lexer.get_next_token()
    assert token.type == TokenTypes.NUMBER
    assert token.value == 3

    token = lexer.get_next_token()
    assert token.type == TokenTypes.MULTIPLY

    token = lexer.get_next_token()
    assert token.type == TokenTypes.ID
    assert token.value == 'b'


def test_statement():
    file_text = 'm=matrix(3,5);'
    lexer = new_lexer(file_text)

    token = lexer.get_next_token()
    assert token.type == TokenTypes.ID
    assert token.value == 'm'

    token = lexer.get_next_token()
    assert token.type == TokenTypes.ASSIGN

    token = lexer.get_next_token()
    assert token.type == TokenTypes.MATRIX

    token = lexer.get_next_token()
    assert token.type == TokenTypes.L_PARENTHESIS

    token = lexer.get_next_token()
    assert token.type == TokenTypes.NUMBER
    assert token.value == 3

    token = lexer.get_next_token()
    assert token.type == TokenTypes.COMMA

    token = lexer.get_next_token()
    assert token.type == TokenTypes.NUMBER
    assert token.value == 5

    token = lexer.get_next_token()
    assert token.type == TokenTypes.R_PARENTHESIS

    token = lexer.get_next_token()
    assert token.type == TokenTypes.SEMICOLON


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
