from copy import deepcopy
from random import random
from ..parser.syntax import Callable
from .variables import NumberVariable, PixelVariable, MatrixVariable


class PrintFunction(Callable):
    def __init__(self):
        self.id = 'print'
        self.parameter_list = []
        self.argument_list = None

    def verify_arguments(self, arguments):
        self.argument_list = deepcopy(arguments)
        return True

    def accept(self, visitor):
        result_string = ''
        for argument in self.argument_list:
            result_string += str(argument)
        print(result_string)


class RandomPixelFunction(Callable):
    def __init__(self):
        self.id = 'random_pixel'
        self.parameter_list = []

    def verify_arguments(self, arguments):
        return len(arguments) == 0

    def accept(self, visitor):
        random_pixel = PixelVariable('')
        random_pixel.set_r(random() * 255)
        random_pixel.set_g(random() * 255)
        random_pixel.set_b(random() * 255)
        visitor.scope_manager.return_result = random_pixel


class DeterminantFunction(Callable):
    def __init__(self):
        self.id = 'det'
        self.parameter_list = ['m']
        self.rows = None

    def verify_arguments(self, arguments):
        if not (len(arguments) == 1 and
                isinstance(arguments[0], MatrixVariable) and
                arguments[0].xdim == arguments[0].ydim):
            return False

        self.rows = arguments[0].rows
        return True

    def accept(self, visitor):
        determinant = self.determinant_recursive(self.rows)
        visitor.scope_manager.return_result = NumberVariable('', determinant)

    def determinant_recursive(self, m, total=0):
        # Section 1: store indices in list for row referencing
        indices = list(range(len(m)))

        # Section 2: when at 2x2 submatrices recursive calls end
        if len(m) == 2 and len(m[0]) == 2:
            val = m[0][0] * m[1][1] - m[1][0] * m[0][1]
            return val

        # Section 3: define submatrix for focus column and
        #      call this function
        for fc in indices:  # m) for each focus column, ...
            # find the submatrix ...
            ms = deepcopy(m)  # B) make a copy, and ...
            ms = ms[1:]  # ... C) remove the first row
            height = len(ms)  # D)

            for i in range(height):
                # E) for each remaining row of submatrix ...
                #     remove the focus column elements
                ms[i] = ms[i][0:fc] + ms[i][fc + 1:]

            sign = (-1) ** (fc % 2)  # F)
            # G) pass submatrix recursively
            sub_det = self.determinant_recursive(ms)
            # H) total all returns from recursion
            total += sign * m[0][fc] * sub_det

        return total
