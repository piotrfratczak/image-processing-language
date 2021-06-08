import io
import pytest

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.source.source import FileSource
from src.exceptions.exceptions import *
from src.interpreter.variables import *


def new_interpreter(source_string):
    source = FileSource(io.StringIO(source_string))
    lexer = Lexer(source)
    parser = Parser(lexer)
    return Interpreter(parser)


def test_program():
    interpreter = new_interpreter('main() {return;}')
    returned = interpreter.interpret()
    assert returned == 0


def test_program_no_return():
    interpreter = new_interpreter('not_main() {return;}')
    with pytest.raises(NoMainFunctionException):
        interpreter.interpret()


def test_program_return_number():
    interpreter = new_interpreter('main() {return 5;}')
    returned = interpreter.interpret()
    assert returned == 5


def test_program_return_negative_number():
    interpreter = new_interpreter('main() {return -5;}')
    returned = interpreter.interpret()
    assert returned == -5


def test_program_return_expression():
    interpreter = new_interpreter('main() {return 1+3;}')
    returned = interpreter.interpret()
    assert returned == 4


def test_program_return_expression_in_parenthesis():
    interpreter = new_interpreter('main() {return (1+3);}')
    returned = interpreter.interpret()
    assert returned == 4


def test_program_return_negative_expression_in_parenthesis():
    interpreter = new_interpreter('main() {return -(1+3);}')
    returned = interpreter.interpret()
    assert returned == -4


def test_program_return_subtraction_expression_in_parenthesis():
    interpreter = new_interpreter('main() {return (-1+3);}')
    returned = interpreter.interpret()
    assert returned == 2


def test_program_return_condition():
    interpreter = new_interpreter('main() {return 5*(1+3);}')
    returned = interpreter.interpret()
    assert returned == 20


def test_program_with_assignment():
    interpreter = new_interpreter('main() {'
                                  '     a = 7;'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 7


def test_program_with_init_number_assignment():
    interpreter = new_interpreter('main() {'
                                  '     a = number(7);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 7


def test_program_with_init_number_assignment_by_variable():
    interpreter = new_interpreter('main() {'
                                  '     n = 7;'
                                  '     a = number(n);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 7


def test_program_with_init_number_assignment_zero():
    interpreter = new_interpreter('main() {'
                                  '     a = number();'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0


def test_program_with_init_pixel_assignment():
    interpreter = new_interpreter('main() {'
                                  '     a = pixel(5, 10, 15);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('a', 5, 10, 15)


def test_program_with_init_pixel_assignment_over_limit():
    interpreter = new_interpreter('main() {'
                                  '     a = pixel(5, 10, 1005);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('a', 5, 10, 255)


def test_program_with_init_pixel_assignment_below_limit():
    interpreter = new_interpreter('main() {'
                                  '     a = pixel(5, 10, -2);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('a', 5, 10, 0)


def test_program_with_init_pixel_assignment_by_variables():
    interpreter = new_interpreter('main() {'
                                  '     r = 5;'
                                  '     g = 10;'
                                  '     b = 15;'
                                  '     a = pixel(r, g, b);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('a', 5, 10, 15)


def test_program_with_init_pixel_assignment_zeros():
    interpreter = new_interpreter('main() {'
                                  '     a = pixel();'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('a', 0, 0, 0)


def test_program_with_init_pixel_assignment_same_value():
    interpreter = new_interpreter('main() {'
                                  '     a = pixel(77);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('a', 77, 77, 77)


def test_program_with_init_matrix_assignment_zeros():
    interpreter = new_interpreter('main() {'
                                  '     a = matrix(3);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('a', [[0, 0, 0]])


def test_program_with_init_matrix_assignment_zeros2d():
    interpreter = new_interpreter('main() {'
                                  '     a = matrix(3,2);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('a', [[0, 0],
                                                                         [0, 0],
                                                                         [0, 0]])


def test_program_with_init_matrix_assignment_zeros3d():
    interpreter = new_interpreter('main() {'
                                  '     a = matrix(2,3,2);'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == Matrix3dVariable('a', [
        MatrixVariable('', [[0, 0],
                            [0, 0],
                            [0, 0]]),

        MatrixVariable('', [[0, 0],
                            [0, 0],
                            [0, 0]])
    ])


def test_program_return_variable_expression():
    interpreter = new_interpreter('main() {'
                                  '     a = 7;'
                                  '     b = 5;'
                                  '     return a+b;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 12


def test_program_conditional_return():
    interpreter = new_interpreter('main() {'
                                  '     a = 6;'
                                  '     if (2>1)'
                                  '         a = 2;'
                                  '     else'
                                  '         a = 5;'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 2


def test_program_conditional_return_else():
    interpreter = new_interpreter('main() {'
                                  '     a = 6;'
                                  '     if (2<1)'
                                  '         a = 2;'
                                  '     else'
                                  '         a = 5;'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_direct_conditional_return():
    interpreter = new_interpreter('main() {'
                                  '     if (2>1)'
                                  '         return 2;'
                                  '     else'
                                  '         return 5;'
                                  '     return;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 2


def test_program_direct_conditional_return_else():
    interpreter = new_interpreter('main() {'
                                  '     if (2<1)'
                                  '         return 2;'
                                  '     else'
                                  '         return 5;'
                                  '     return;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_number_as_condition():
    interpreter = new_interpreter('main() {'
                                  '     if (2)'
                                  '         return 2;'
                                  '     else'
                                  '         return 5;'
                                  '     return;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 2


def test_program_number_as_condition_zero():
    interpreter = new_interpreter('main() {'
                                  '     if (0)'
                                  '         return 2;'
                                  '     else'
                                  '         return 5;'
                                  '     return;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_number_as_condition_negation():
    interpreter = new_interpreter('main() {'
                                  '     if (!(2<1))'
                                  '         return 2;'
                                  '     else'
                                  '         return 5;'
                                  '     return;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 2


def test_program_for_loop():
    interpreter = new_interpreter('main() {'
                                  '     a = 0;'
                                  '     for (i in 5) {'
                                  '         a = a+1;'
                                  '     }'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_while_loop():
    interpreter = new_interpreter('main() {'
                                  '     a = 0;'
                                  '     while (a < 5) {'
                                  '         a = a+1;'
                                  '     }'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_with_new_operator():
    interpreter = new_interpreter('newop( avg, n1 of number, n2 of number) {'
                                  '     return (n1 + n2) / 2;'
                                  '}'
                                  'main() {'
                                  '     a = 4;'
                                  '     b = 2;'
                                  '     return a avg b;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 3


def test_program_with_new_operator_after_main():
    interpreter = new_interpreter('main() {'
                                  '     a = 4;'
                                  '     b = 2;'
                                  '     return a avg b;'
                                  '}'
                                  'newop( avg, n1 of number, n2 of number) {'
                                  '     return (n1 + n2) / 2;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 3


def test_program_matrix_lookup():
    interpreter = new_interpreter('main() {'
                                  '     m = matrix(3,2);'
                                  '     a = m[2,1];'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0


def test_program_assign_by_matrix_lookup():
    interpreter = new_interpreter('main() {'
                                  '     m = matrix(3,2);'
                                  '     m[0,0] = 2;'
                                  '     return;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('m', [[2, 0],
                                                                         [0, 0],
                                                                         [0, 0]])


def test_program_assign_matrix_literal():
    interpreter = new_interpreter('main() {'
                                  '     m = [1, 2, 3;];'
                                  '     return;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('m', [[1, 2, 3]])


def test_program_assign_matrix_literal_3d():
    interpreter = new_interpreter('main() {'
                                  '     a = {'
                                  '     [1, 2;'
                                  '      3, 4;'
                                  '      5, 6;],'
                                  ''
                                  '     [7, 8;'
                                  '      9, 10;'
                                  '     11, 12;]'
                                  '     };'
                                  '     return a;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == Matrix3dVariable('a', [
        MatrixVariable('', [[1, 2],
                            [3, 4],
                            [5, 6]]),

        MatrixVariable('', [[7, 8],
                            [9, 10],
                            [11, 12]])
    ])


def test_program_get_pixel_r():
    interpreter = new_interpreter('main() {'
                                  '     p = pixel(100, 200, 50);'
                                  '     red = p.r;'
                                  ''
                                  '     return red;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 100


def test_program_set_pixel_r():
    interpreter = new_interpreter('main() {'
                                  '     p = pixel(100, 200, 50);'
                                  '     p.r = 15;'
                                  ''
                                  '     return p;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('p', 15, 200, 50)


def test_program_set_pixel_b_over_limit():
    interpreter = new_interpreter('main() {'
                                  '     p = pixel(100, 200, 50);'
                                  '     p.b = 1500;'
                                  ''
                                  '     return p;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('p', 100, 200, 255)


def test_program_get_matrix_dims():
    interpreter = new_interpreter('main() {'
                                  '     m = matrix(3,2);'
                                  '     return m.dims;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 2


def test_program_get_matrix_xdim():
    interpreter = new_interpreter('main() {'
                                  '     m = matrix(3,2);'
                                  '     return m.xdim;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 2


def test_program_get_matrix_ydim():
    interpreter = new_interpreter('main() {'
                                  '     m = matrix(3,2);'
                                  '     return m.ydim;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 3


def test_program_get_matrix_zdim():
    interpreter = new_interpreter('main() {'
                                  '     m = matrix(5,2,7);'
                                  '     return m.zdim;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_exception_get_matrix_wdim():
    interpreter = new_interpreter('main() {'
                                  '     m = matrix(5,2,7);'
                                  '     return m.wdim;'
                                  '}'
                                  )
    with pytest.raises(UndefinedReferenceException):
        interpreter.interpret()


def test_program_with_function_call():
    interpreter = new_interpreter('foo() { return 5;}'
                                  'main() {'
                                  '     m = foo();'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_with_function_call_negative():
    interpreter = new_interpreter('foo() { return 5;}'
                                  'main() {'
                                  '     m = -foo();'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == -5


def test_program_with_function_call_with_arguments():
    interpreter = new_interpreter('foo(a, b) { return a*b;}'
                                  'main() {'
                                  '     m = foo(3, 4);'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 12


def test_program_with_function_call_with_expressions_arguments():
    interpreter = new_interpreter('foo(a, b) { return a*b;}'
                                  'main() {'
                                  '     m = foo(foo(3,2), 1+1);'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 12


def test_program_with_function_call_with_expressions_arguments_multiplication():
    interpreter = new_interpreter('foo(a, b) { return a*b;}'
                                  'main() {'
                                  '     m = foo(foo(3,2), 1+2*3);'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 42


def test_program_with_function_call_with_expression3():
    interpreter = new_interpreter('foo(a, b) { return a*b;}'
                                  'main() {'
                                  '     m = foo(foo(3,2), 1+2*3-4);'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 18


def test_program_with_function_call_expression():
    interpreter = new_interpreter('foo() { return 5;}'
                                  'main() {'
                                  '     m = foo() + 3;'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 8


def test_program_with_recursive_function_call():
    interpreter = new_interpreter('foo(a) { '
                                  '     if (a == 1) return 1;'
                                  '     return foo(a-1) + 1;'
                                  '}'
                                  ''
                                  'main() {'
                                  '     m = foo(3);'
                                  '     return m;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 3


def test_program_addition():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 5;'
                                  '     b = 9;'
                                  '     c = a + b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 14


def test_program_subtraction():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 5;'
                                  '     b = 9;'
                                  '     c = a - b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == -4


def test_program_multiplication():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 5;'
                                  '     b = 9;'
                                  '     c = a * b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 45


def test_program_division():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 5;'
                                  '     b = 9;'
                                  '     c = a / b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0


def test_program_division_by_zero():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 5;'
                                  '     b = 0;'
                                  '     c = a / b;'
                                  '     return c;'
                                  '}'
                                  )
    with pytest.raises(ZeroDivisionException):
        interpreter.interpret()


def test_program_whole_division():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 45;'
                                  '     b = 9;'
                                  '     c = a / b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_modulo():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 5;'
                                  '     b = 9;'
                                  '     c = a % b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_program_expression():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = 5;'
                                  '     b = 9;'
                                  '     c = 1;'
                                  '     return a * b + c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 46


def test_program_addition_pixel():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = pixel(1, 2, 3);'
                                  '     b = pixel(2, 2, 2);'
                                  '     c = a + b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('c', 3, 4, 5)


def test_program_subtraction_pixel():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = pixel(1, 2, 3);'
                                  '     b = pixel(2, 2, 2);'
                                  '     c = a - b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('c', 0, 0, 1)


def test_program_multiplication_pixel():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = pixel(1, 2, 3);'
                                  '     b = pixel(2, 2, 3);'
                                  '     c = a * b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('c', 2, 4, 9)


def test_program_multiplication_pixel_by_number():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = pixel(1, 2, 3);'
                                  '     b = 2;'
                                  '     c = a * b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('c', 2, 4, 6)


def test_program_multiplication_pixel_by_number_reversed():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = pixel(1, 2, 3);'
                                  '     b = 2;'
                                  '     c = b * a;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('c', 2, 4, 6)


def test_program_addition_pixel_number():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = pixel(1, 2, 3);'
                                  '     b = 2;'
                                  '     c = a + b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == PixelVariable('c', 3, 4, 5)


def test_program_matrix_addition():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = [1, 2;'
                                  '          1, 2;];'
                                  '     b = [3, 2;'
                                  '          1, 1;];'
                                  '     c = a + b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('c', [[4, 4],
                                                                         [2, 3]])


def test_program_matrix_subtraction():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = [1, 2;'
                                  '          1, 2;];'
                                  '     b = [3, 2;'
                                  '          1, 1;];'
                                  '     c = a - b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('c', [[-2, 0],
                                                                         [0, 1]])


def test_program_matrix_special_multiplication():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = [1, 2;'
                                  '          1, 2;'
                                  '          3, 3;];'
                                  '     b = [3, 2;'
                                  '          1, 1;'
                                  '          2, 1;];'
                                  '     c = a @ b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('c', [[3, 4],
                                                                         [1, 2],
                                                                         [6, 3]])


def test_program_matrix_multiplication():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = [1, 2;'
                                  '          1, 2;'
                                  '          3, 3;];'
                                  '     b = [3, 2, 1;'
                                  '          1, 1, 3;];'
                                  '     c = a * b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('c', [[5, 4, 7],
                                                                         [5, 4, 7],
                                                                         [12, 9, 12]])


def test_program_matrix_addition_number():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = [1, 2;'
                                  '          1, 3;];'
                                  '     b = 2;'
                                  '     c = a + b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('c', [[3, 4],
                                                                         [3, 5]])


def test_program_matrix_subtraction_number():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = [1, 2;'
                                  '          1, 3;];'
                                  '     b = 2;'
                                  '     c = a - b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('c', [[-1, 0],
                                                                         [-1, 1]])


def test_program_matrix_multiplication_number():
    interpreter = new_interpreter(
                                  'main() {'
                                  '     a = [1, 2;'
                                  '          1, 3;];'
                                  '     b = 2;'
                                  '     c = a * b;'
                                  '     return c;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 0
    assert interpreter.scope_manager.last_result == MatrixVariable('c', [[2, 4],
                                                                         [2, 6]])


def test_greater_than_condition_positive():
    interpreter = new_interpreter('a > b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 10))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_greater_than_condition_negative():
    interpreter = new_interpreter('a > b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 2))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_less_than_condition_positive():
    interpreter = new_interpreter('a < b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 1))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_less_than_condition_negative():
    interpreter = new_interpreter('a < b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 23))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_greater_than_or_equal_condition_positive():
    interpreter = new_interpreter('a >= b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 10))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_greater_than_or_equal_condition_equal():
    interpreter = new_interpreter('a >= b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 10))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 10))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_greater_than_or_equal_condition_negative():
    interpreter = new_interpreter('a >= b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 2))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_less_than_or_equal_condition_positive():
    interpreter = new_interpreter('a <= b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 6))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 10))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_less_than_or_equal_condition_equal():
    interpreter = new_interpreter('a <= b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 10))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 10))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_less_than_or_equal_condition_negative():
    interpreter = new_interpreter('a <= b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 7))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_equals_condition_positive():
    interpreter = new_interpreter('a == b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 6))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 6))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_equals_condition_negative():
    interpreter = new_interpreter('a == b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 23))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_not_equals_condition_positive():
    interpreter = new_interpreter('a != b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 7))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 6))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_not_equals_condition_negative():
    interpreter = new_interpreter('a != b')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_equals_and_condition():
    interpreter = new_interpreter('a == b and 1 == 1')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_equals_and_condition_negative_left():
    interpreter = new_interpreter('a == b and 1 == 1')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 6))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_equals_and_condition_negative_right():
    interpreter = new_interpreter('a == b and 1 == 2')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_equals_and_condition_negative():
    interpreter = new_interpreter('a == b and 1 == 2')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 4))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_equals_or_condition_both_true():
    interpreter = new_interpreter('a == b or 1 == 1')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_equals_or_condition_left_true():
    interpreter = new_interpreter('a == b or 1 == 2')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_equals_or_condition_right_true():
    interpreter = new_interpreter('a != b or 1 == 1')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_equals_or_condition_both_false():
    interpreter = new_interpreter('a != b or 1 != 1')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is False


def test_equals_or_condition_both_false_with_negation():
    interpreter = new_interpreter('a != b or !(2 < 1)')
    condition = interpreter.parser.parse_condition()
    interpreter.scope_manager.add_update_variable('a', NumberVariable('a', 5))
    interpreter.scope_manager.add_update_variable('b', NumberVariable('b', 5))
    interpreter.visit_condition(condition)
    assert interpreter.scope_manager.last_result is True


def test_program_builtin_print():
    interpreter = new_interpreter('main() {'
                                  '     a = 5;'
                                  '     print(a);'
                                  '     return;'
                                  '}'
                                  )
    interpreter.interpret()


def test_program_builtin_random_pixel():
    interpreter = new_interpreter('main() {'
                                  '     p = random_pixel();'
                                  '     return;'
                                  '}'
                                  )
    interpreter.interpret()
    assert isinstance(interpreter.scope_manager.last_result, PixelVariable)


def test_program_builtin_det_2by2():
    interpreter = new_interpreter('main() {'
                                  '     m = [1, 2;'
                                  '          3, 4;];'
                                  '     d = det(m);'
                                  '     return d;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == -2


def test_program_builtin_det_3by3():
    interpreter = new_interpreter('main() {'
                                  '     m = [1, 2, 3;'
                                  '          2, 3, 1;'
                                  '          1, 1, 3;];'
                                  '     d = det(m);'
                                  '     return d;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == -5


def test_return_from_if():
    interpreter = new_interpreter('main() {'
                                  '     return foo();'
                                  '}'
                                  ''
                                  'foo() {'
                                  '     if (2 < 1) {'
                                  '         return 3;'
                                  '     } else {'
                                  '         if (2<1){'
                                  '             return 2;'
                                  '         } else {'
                                  '             return 1;'
                                  '         }'
                                  '     }'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 1


def test_return_from_while():
    interpreter = new_interpreter('main() {'
                                  '     return foo(3);'
                                  '}'
                                  ''
                                  'foo(a) {'
                                  '     while (a<2) {'
                                  '         return a;'
                                  '     }'
                                  '     return 5;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 5


def test_return_from_for():
    interpreter = new_interpreter('main() {'
                                  '     return foo(0);'
                                  '}'
                                  ''
                                  'foo(a) {'
                                  '     i = 0;'
                                  '     for (g in 3) {'
                                  '         a = a + 1;'
                                  '         return a;'
                                  '     }'
                                  '     return 10;'
                                  '}'
                                  )
    returned = interpreter.interpret()
    assert returned == 1
