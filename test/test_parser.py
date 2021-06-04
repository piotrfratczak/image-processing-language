import io
import pytest

from src.parser.parser import Parser
from src.parser.syntax import *
from src.lexer.lexer import Lexer
from src.lexer.token_type import TokenType
from src.source.source import FileSource
from src.exceptions.exceptions import *


def new_parser(source_string):
    source = FileSource(io.StringIO(source_string))
    lexer = Lexer(source)
    return Parser(lexer)


def test_parse_next_token():
    parser = new_parser('id')
    id_token = parser.parse_next_token(TokenType.ID)
    assert id_token.type == TokenType.ID
    assert id_token.value == 'id'


def test_parse_type_pixel():
    parser = new_parser('pixel')
    pixel_type = parser.parse_type()
    assert pixel_type == TokenType.PIXEL


def test_parse_type_number():
    parser = new_parser('number')
    number_type = parser.parse_type()
    assert number_type == TokenType.NUMBER_TYPE


def test_parse_type_matrix():
    parser = new_parser('matrix')
    matrix_type = parser.parse_type()
    assert matrix_type == TokenType.MATRIX


def test_parse_type_none():
    parser = new_parser('id')
    _type = parser.parse_type()
    assert _type is None


def test_try_or_exception_token():
    parser = new_parser('id')
    id_token = parser.try_or_exception(TokenType.ID, 'Exception')
    assert id_token.type == TokenType.ID
    assert id_token.value == 'id'


def test_try_or_exception_base_expression():
    parser = new_parser('')
    expression = BaseExpression(expression=5)
    result = parser.try_or_exception(expression, 'Exception')
    assert result
    assert result == expression


def test_try_or_exception_condition():
    parser = new_parser('')
    result = parser.try_or_exception(2 > 1, 'Exception')
    assert result


def test_try_or_exception_token_exception():
    parser = new_parser('id')
    with pytest.raises(SyntaxException):
        parser.try_or_exception(TokenType.L_PARENTHESIS, 'No left parenthesis')


def test_try_or_exception_base_expression_exception():
    parser = new_parser('=')
    expression = parser.parse_base_expression()
    assert expression is None
    with pytest.raises(SyntaxException):
        parser.try_or_exception(expression, 'No expression')


def test_try_or_exception_condition_exception():
    parser = new_parser('')
    with pytest.raises(SyntaxException):
        parser.try_or_exception(2 < 1, '2 is greater than 1')


def test_parse_next_token_none():
    parser = new_parser('id')
    id_token = parser.parse_next_token(TokenType.L_PARENTHESIS)
    assert id_token is None


def test_program():
    parser = new_parser('main() {'
                        'a = 2;'
                        '# comment\n'
                        'return 0;'
                        '}')
    parser.parse_program()
    assert isinstance(parser.program, Program)
    assert len(parser.program.function_definitions) == 1
    assert len(parser.program.operator_definitions) == 0
    assert len(parser.program.comments) == 1


def test_program_init():
    parser = new_parser('main() {'
                        'a = number(2);'
                        '# comment\n'
                        'return 0;'
                        '}')
    parser.parse_program()
    assert isinstance(parser.program, Program)
    assert len(parser.program.function_definitions) == 1
    assert len(parser.program.operator_definitions) == 0
    assert len(parser.program.comments) == 1


def test_comment():
    comment_str = '#comment'
    parser = new_parser(comment_str)
    parser.parse_program()
    assert isinstance(parser.program, Program)
    assert parser.program.comments[0] == comment_str


def test_multiple_comments():
    comment1 = '# comment 1'
    comment2 = '# comment 2'
    parser = new_parser(comment1 + '\n' + comment2)
    parser.parse_program()
    assert isinstance(parser.program, Program)
    assert parser.program.comments[0] == comment1
    assert parser.program.comments[1] == comment2


def test_base_expression_id():
    parser = new_parser('a')
    expression = parser.parse_expression()
    assert isinstance(expression, BaseExpression)
    assert expression.expression == 'a'


def test_base_expression_minus_id():
    parser = new_parser('-a')
    expression = parser.parse_expression()
    assert isinstance(expression, BaseExpression)
    assert expression.expression == 'a'
    assert expression.subtract_operator


def test_base_expression_number():
    parser = new_parser('5')
    expression = parser.parse_expression()
    assert isinstance(expression, BaseExpression)
    assert expression.expression == 5


def test_base_expression_matrix():
    parser = new_parser('[1, 2, 4;]')
    expression = parser.parse_expression()
    assert isinstance(expression, BaseExpression)
    assert isinstance(expression.expression, Matrix)


def test_expression_in_parenthesis():
    parser = new_parser('(a+b)')
    expression = parser.parse_expression_in_parenthesis()
    assert isinstance(expression, ExpressionInParenthesis)
    assert isinstance(expression.expression, LogicalExpression)


def test_simple_matrix():
    parser = new_parser('[1;]')
    matrix = parser.parse_matrix()
    assert isinstance(matrix, Matrix)
    assert len(matrix.rows) == 1
    assert len(matrix.rows[0].expressions) == 1
    assert matrix.rows[0].expressions[0].expression == 1


def test_one_row_matrix():
    parser = new_parser('[1, 3, 4;]')
    matrix = parser.parse_matrix()
    assert isinstance(matrix, Matrix)
    assert len(matrix.rows) == 1
    assert len(matrix.rows[0].expressions) == 3
    assert matrix.rows[0].expressions[0].expression == 1
    assert matrix.rows[0].expressions[1].expression == 3
    assert matrix.rows[0].expressions[2].expression == 4


def test_multiple_rows_matrix():
    parser = new_parser('[1, 2, 3;'
                        ' 5, 6, 7;]')
    matrix = parser.parse_matrix()
    assert isinstance(matrix, Matrix)
    assert len(matrix.rows) == 2
    assert len(matrix.rows[0].expressions) == 3
    assert matrix.rows[0].expressions[0].expression == 1
    assert matrix.rows[0].expressions[1].expression == 2
    assert matrix.rows[0].expressions[2].expression == 3
    assert len(matrix.rows[1].expressions) == 3
    assert matrix.rows[1].expressions[0].expression == 5
    assert matrix.rows[1].expressions[1].expression == 6
    assert matrix.rows[1].expressions[2].expression == 7
    
    
def test_simple_3dmatrix():
    parser = new_parser('{ [1,2,3;] }')
    matrix = parser.parse_matrix3d()
    assert isinstance(matrix, Matrix3d)
    assert len(matrix.matrices) == 1
    assert isinstance(matrix.matrices[0], Matrix)


def test_multiple_matrices_3dmatrix():
    parser = new_parser('{'
                        '[1,2,3;],'
                        '[4,5,6;],'
                        '[7,8,9;]'
                        '}')
    matrix = parser.parse_matrix3d()
    assert isinstance(matrix, Matrix3d)
    assert len(matrix.matrices) == 3
    assert isinstance(matrix.matrices[0], Matrix)
    assert isinstance(matrix.matrices[1], Matrix)
    assert isinstance(matrix.matrices[2], Matrix)


def test_expression():
    parser = new_parser(' a * b + c ')
    expression = parser.parse_expression()
    assert isinstance(expression, AdditiveExpression)
    assert len(expression.additive_operators) == 1
    assert expression.additive_operators[0] == TokenType.ADD
    assert len(expression.multiplicative_expressions) == 2


def test_simple_block():
    parser = new_parser('a = 3;')
    block = parser.parse_block()
    assert isinstance(block, Block)
    assert len(block.statements) == 1
    assert isinstance(block.statements[0], Assignment)


def test_block_in_braces():
    parser = new_parser('{'
                        'a = 1;'
                        'return a;'
                        '}')
    block = parser.parse_block()
    assert isinstance(block, Block)
    assert len(block.statements) == 2
    assert isinstance(block.statements[0], Assignment)
    assert isinstance(block.statements[1], ReturnStatement)


def test_simple_condition():
    parser = new_parser('2 < 6')
    condition = parser.parse_condition()
    assert isinstance(condition, Condition)


def test_elaborate_condition():
    parser = new_parser('a+5 >= 2+b')
    condition = parser.parse_condition()
    assert isinstance(condition, Condition)
    
    
def test_condition_in_parenthesis():
    parser = new_parser('(a > b)')
    condition = parser.parse_expression_in_parenthesis()
    assert isinstance(condition, ExpressionInParenthesis)
    assert isinstance(condition.expression, Condition)


def test_function_definition():
    parser = new_parser('add(a, b) { return a+b; }')
    function_definition = parser.parse_function_definition()
    assert isinstance(function_definition, FunctionDefinition)
    assert function_definition.id == 'add'
    assert len(function_definition.parameter_list) == 2
    assert function_definition.parameter_list[0] == 'a'
    assert function_definition.parameter_list[1] == 'b'
    assert function_definition.block
    assert isinstance(function_definition.block.statements[0], ReturnStatement)
    assert function_definition.block.statements[0].expression
    assert len(function_definition.block.statements[0].expression.multiplicative_expressions) == 2
    assert function_definition.block.statements[0].expression.multiplicative_expressions[0].expression == 'a'
    assert function_definition.block.statements[0].expression.additive_operators[0] == TokenType.ADD
    assert function_definition.block.statements[0].expression.multiplicative_expressions[1].expression == 'b'


def test_while_loop():
    parser = new_parser('while (a > 5) {'
                        '   b = b+1;'
                        '}')
    while_loop = parser.parse_while_loop()
    assert isinstance(while_loop, WhileLoop)
    assert while_loop.condition
    assert while_loop.block
    
    
def test_for_loop():
    parser = new_parser('for (a in 5) {'
                        '   b = a + 2;'
                        '   # this is a loop\n'
                        '}')
    for_loop = parser.parse_for_loop()
    assert isinstance(for_loop, ForLoop)
    assert for_loop.iterator == 'a'
    assert isinstance(for_loop.expression, BaseExpression)
    assert isinstance(for_loop.block, Block)


def test_operator_definition():
    parser = new_parser('newop (avg, a of number, b of number) {'
                        '   return (a + b) / 2;'
                        '}')
    operator_definition = parser.parse_operator_definition()
    assert isinstance(operator_definition, OperatorDefinition)
    assert operator_definition.operator == 'avg'
    assert operator_definition.id1 == 'a'
    assert operator_definition.type1 == TokenType.NUMBER_TYPE
    assert operator_definition.id2 == 'b'
    assert operator_definition.type2 == TokenType.NUMBER_TYPE
    assert operator_definition.block
    
    
def test_empty_argument_list():
    parser = new_parser('')
    argument_list = parser.parse_argument_list()
    assert isinstance(argument_list, ArgumentList)
    assert len(argument_list.expressions) == 0


def test_argument_list():
    parser = new_parser('1, a, 2-4')
    argument_list = parser.parse_argument_list()
    assert isinstance(argument_list, ArgumentList)
    assert len(argument_list.expressions) == 3


def test_init_statement():
    parser = new_parser('matrix(2, 3);')
    init_statement = parser.parse_init_statement()
    assert isinstance(init_statement, InitStatement)
    assert isinstance(init_statement.argument_list, ArgumentList)
    assert len(init_statement.argument_list.expressions) == 2


def test_matrix_lookup():
    parser = new_parser('mat[2,4]')
    matrix_lookup = parser.parse_reference_or_call()
    assert isinstance(matrix_lookup, MatrixLookup)
    assert len(matrix_lookup.indices) == 2
    assert matrix_lookup.indices[0].expression == 2
    assert matrix_lookup.indices[1].expression == 4


def test_reference():
    parser = new_parser('.b')
    reference = parser.parse_reference('a')
    assert isinstance(reference, Reference)
    assert reference.id1 == 'a'
    assert reference.id2 == 'b'


def test_simple_assignment():
    parser = new_parser('a = 6;')
    assignment = parser.parse_assignment_or_call()
    assert isinstance(assignment, Assignment)
    assert assignment.id == 'a'
    assert assignment.reference is None


def test_assignment_with_reference():
    parser = new_parser('a.b = 7;')
    assignment = parser.parse_assignment_or_call()
    assert isinstance(assignment, Assignment)
    assert assignment.id == 'a'
    assert isinstance(assignment.reference, Reference)
    assert assignment.reference.id1 == 'a'
    assert assignment.reference.id2 == 'b'


def test_function_call():
    parser = new_parser('foo(1, b, g-2);')
    function_call = parser.parse_reference_or_call()
    assert isinstance(function_call, FunctionCall)
    assert function_call.id == 'foo'
    assert function_call.argument_list
    assert len(function_call.argument_list.expressions) == 3


def test_simple_if_statement():
    parser = new_parser('if (a > b) {'
                        '   b = 100;'
                        '}')
    if_statement = parser.parse_if_statement()
    assert isinstance(if_statement, IfStatement)
    assert isinstance(if_statement.condition, Condition)
    assert isinstance(if_statement.block, Block)
    assert if_statement.else_block is None


def test_if_else_statement():
    parser = new_parser('if (a > b) {'
                        '   b = 100;'
                        '} else {'
                        '   b = 5;'
                        '}')
    if_statement = parser.parse_if_statement()
    assert isinstance(if_statement, IfStatement)
    assert isinstance(if_statement.condition, Condition)
    assert isinstance(if_statement.block, Block)
    assert isinstance(if_statement.else_block, Block)


def test_if_else_statement_no_braces():
    parser = new_parser('if (a > b)'
                        '   b = 100;'
                        'else '
                        '   b = 5;'
                        )
    if_statement = parser.parse_if_statement()
    assert isinstance(if_statement, IfStatement)
    assert isinstance(if_statement.condition, Condition)
    assert isinstance(if_statement.block, Block)
    assert isinstance(if_statement.else_block, Block)


def test_if_else_if_statement():
    parser = new_parser('if (a > b) {'
                        '   b = 100;'
                        '} else if (a == b) {'
                        '   b = 5;'
                        '}')
    if_statement = parser.parse_if_statement()
    assert isinstance(if_statement, IfStatement)
    assert isinstance(if_statement.condition, Condition)
    assert isinstance(if_statement.block, Block)
    assert isinstance(if_statement.else_block, Block)
    assert isinstance(if_statement.else_block.statements[0], IfStatement)


def test_if_else_if_else_statement():
    parser = new_parser('if (a > b) {'
                        '   a = 100;'
                        '} else if (a == b) {'
                        '   b = 5;'
                        '} else {'
                        '   c = 0;'
                        '}')
    if_statement = parser.parse_if_statement()
    assert isinstance(if_statement, IfStatement)
    assert isinstance(if_statement.condition, Condition)
    assert isinstance(if_statement.block, Block)
    assert isinstance(if_statement.else_block, Block)
    assert isinstance(if_statement.else_block.statements[0], IfStatement)
    assert isinstance(if_statement.else_block.statements[0].block, Block)
    assert isinstance(if_statement.else_block.statements[0].else_block, Block)


def test_condition_with_expression_in_parenthesis():
    parser = new_parser('(a+b)<c')
    condition = parser.parse_condition()
    assert isinstance(condition, Condition)
    assert isinstance(condition.and_conditions[0], ComparisonCondition)
