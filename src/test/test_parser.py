import io
import pytest

from src.parser.parser import Parser
from src.parser.syntax import *
from src.lexer.lexer import Lexer
from src.lexer.token_type import TokenType
from src.source.source import FileSource
from src.exceptions.exceptions import *


def new_parser(source_string):
    return Parser(Lexer(FileSource(io.StringIO(source_string))))

def test_parse_comment():
    comment_str = '#comment'
    parser = new_parser(comment_str)
    parser.parse_program()
    assert isinstance(parser.program, Program)
    assert parser.program.comments[0].value == comment_str