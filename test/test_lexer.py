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


def test_is_eof():
    lexer = new_lexer('')
    token = lexer.get_next_token()
    assert token.type == TokenType.EOT


def test_build_id():
    id_test_helper('i')


def test_build_id1():
    id_test_helper('id')


def test_build_id2():
    id_test_helper('id_')


def test_build_id3():
    id_test_helper('id_compound')


def test_build_id4():
    id_test_helper('id4')


def test_build_id5():
    id_test_helper('id5ab')


def test_build_id6():
    id_test_helper('id6_o2')


def test_build_id7():
    id_test_helper('id7 decoy', 'id7')


def test_build_id8():
    id_test_helper('id8^decoy', 'id8')


def test_build_id9():
    id_test_helper('id9-decoy', 'id9')


def test_build_id10():
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


def test_build_keyword_id():
    lexer = new_lexer('id')
    token = lexer.get_next_token()
    assert token.type == TokenType.ID


def test_build_keyword_number():
    lexer = new_lexer('22')
    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER


def test_build_keyword_unknown():
    lexer = new_lexer('__22')
    token = lexer.get_next_token()
    assert token.type == TokenType.UNKNOWN


def test_build_keyword_and():
    lexer = new_lexer('and')
    token = lexer.get_next_token()
    assert token.type == TokenType.AND


def test_build_keyword_or():
    lexer = new_lexer('or')
    token = lexer.get_next_token()
    assert token.type == TokenType.OR


def test_build_keyword_while():
    lexer = new_lexer('while')
    token = lexer.get_next_token()
    assert token.type == TokenType.WHILE


def test_build_keyword_for():
    lexer = new_lexer('for')
    token = lexer.get_next_token()
    assert token.type == TokenType.FOR


def test_build_keyword_in():
    lexer = new_lexer('in')
    token = lexer.get_next_token()
    assert token.type == TokenType.IN


def test_build_keyword_if():
    lexer = new_lexer('if')
    token = lexer.get_next_token()
    assert token.type == TokenType.IF


def test_build_keyword_of():
    lexer = new_lexer('of')
    token = lexer.get_next_token()
    assert token.type == TokenType.OF


def test_build_keyword_newop():
    lexer = new_lexer('newop')
    token = lexer.get_next_token()
    assert token.type == TokenType.NEW_OPERATOR


def test_build_keyword_else():
    lexer = new_lexer('else')
    token = lexer.get_next_token()
    assert token.type == TokenType.ELSE


def test_build_keyword_return():
    lexer = new_lexer('return')
    token = lexer.get_next_token()
    assert token.type == TokenType.RETURN


def test_build_keyword_number_type():
    lexer = new_lexer('number')
    token = lexer.get_next_token()
    assert token.type == TokenType.NUMBER_TYPE


def test_build_keyword_pixel():
    lexer = new_lexer('pixel')
    token = lexer.get_next_token()
    assert token.type == TokenType.PIXEL


def test_build_keyword_matrix():
    lexer = new_lexer('matrix')
    token = lexer.get_next_token()
    assert token.type == TokenType.MATRIX


def test_build_operator_not():
    lexer = new_lexer('!')
    token = lexer.get_next_token()
    assert token.type == TokenType.NOT


def test_build_operator_less_than():
    lexer = new_lexer('<')
    token = lexer.get_next_token()
    assert token.type == TokenType.LESS_THAN


def test_build_operator_greater_than():
    lexer = new_lexer('>')
    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER_THAN


def test_build_operator_assign():
    lexer = new_lexer('=')
    token = lexer.get_next_token()
    assert token.type == TokenType.ASSIGN


def test_build_operator_add():
    lexer = new_lexer('+')
    token = lexer.get_next_token()
    assert token.type == TokenType.ADD


def test_build_operator_subtract():
    lexer = new_lexer('-')
    token = lexer.get_next_token()
    assert token.type == TokenType.SUBTRACT


def test_build_operator_multiply():
    lexer = new_lexer('*')
    token = lexer.get_next_token()
    assert token.type == TokenType.MULTIPLY


def test_build_operator_divide():
    lexer = new_lexer('/')
    token = lexer.get_next_token()
    assert token.type == TokenType.DIVIDE


def test_build_operator_special_multiply():
    lexer = new_lexer('@')
    token = lexer.get_next_token()
    assert token.type == TokenType.SPECIAL_MULTIPLY


def test_build_operator_modulo():
    lexer = new_lexer('%')
    token = lexer.get_next_token()
    assert token.type == TokenType.MODULO


def test_build_operator_dot():
    lexer = new_lexer('.')
    token = lexer.get_next_token()
    assert token.type == TokenType.DOT


def test_build_operator_comma():
    lexer = new_lexer(',')
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMA


def test_build_operator_semicolon():
    lexer = new_lexer(';')
    token = lexer.get_next_token()
    assert token.type == TokenType.SEMICOLON


def test_build_operator_left_parenthesis():
    lexer = new_lexer('(')
    token = lexer.get_next_token()
    assert token.type == TokenType.L_PARENTHESIS


def test_build_operator_right_parenthesis():
    lexer = new_lexer(')')
    token = lexer.get_next_token()
    assert token.type == TokenType.R_PARENTHESIS


def test_build_operator_left_brace():
    lexer = new_lexer('{')
    token = lexer.get_next_token()
    assert token.type == TokenType.L_BRACE


def test_build_operator_right_brace():
    lexer = new_lexer('}')
    token = lexer.get_next_token()
    assert token.type == TokenType.R_BRACE


def test_build_operator_left_bracket():
    lexer = new_lexer('[')
    token = lexer.get_next_token()
    assert token.type == TokenType.L_BRACKET


def test_build_operator_right_bracket():
    lexer = new_lexer(']')
    token = lexer.get_next_token()
    assert token.type == TokenType.R_BRACKET


def test_build_operator_equal():
    lexer = new_lexer('==')
    token = lexer.get_next_token()
    assert token.type == TokenType.EQUAL


def test_build_operator_not_equal():
    lexer = new_lexer('!=')
    token = lexer.get_next_token()
    assert token.type == TokenType.NOT_EQUAL


def test_build_operator_greater_or_equal():
    lexer = new_lexer('>=')
    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER_OR_EQUAL


def test_build_operator_less_or_equal():
    lexer = new_lexer('<=')
    token = lexer.get_next_token()
    assert token.type == TokenType.LESS_OR_EQUAL


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
    file_text = '#' + 'a' * 515
    lexer = new_lexer(file_text)
    with pytest.raises(CommentTooLongException):
        lexer.get_next_token()


def test_number_too_large():
    lexer = Lexer(FileSource(io.StringIO('11')), max_number=10)
    with pytest.raises(NumberTooLargeException):
        lexer.get_next_token()
