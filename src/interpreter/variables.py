from typing import List
from copy import deepcopy
from ..exceptions.exceptions import MatrixDimensionsException


class Variable:
    def __init__(self, name: str):
        self.name = name

    def evaluate_to_bool(self):
        pass

    def add_value(self, value: int):
        pass

    def multiply_by_value(self, value: int):
        pass

    def has_zero(self):
        pass


class NumberVariable(Variable):
    def __init__(self, name: str, value: int):
        super().__init__(name)
        self.value = value

    def has_zero(self):
        return self.value == 0

    def __add__(self, other):
        if not isinstance(other, Variable):
            return None

        if isinstance(other, NumberVariable):
            return NumberVariable(self.name + '+' + other.name,
                                  self.value + other.value)

        new_variable = deepcopy(other)
        new_variable.name = other.name + '+' + self.name
        new_variable.add_value(self.value)
        return new_variable

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if not isinstance(other, Variable):
            return None

        if isinstance(other, NumberVariable):
            return NumberVariable(self.name + '*' + other.name,
                                  self.value * other.value)

        new_variable = deepcopy(other)
        new_variable.name = other.name + '*' + self.name
        new_variable.multiply_by_value(self.value)
        return new_variable

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        if not isinstance(other, NumberVariable):
            return None

        return NumberVariable(self.name + '-' + other.name,
                              self.value - other.value)

    def __truediv__(self, other):
        if not isinstance(other, NumberVariable):
            return None

        return NumberVariable(self.name + '/' + other.name,
                              self.value // other.value)

    def __mod__(self, other):
        if not isinstance(other, NumberVariable):
            return None

        return NumberVariable(self.name + '%' + other.name,
                              self.value % other.value)

    def __bool__(self):
        return self.value > 0

    def __eq__(self, other):
        if isinstance(other, NumberVariable):
            return self.value == other.value
        return False

    def __ne__(self, other):
        if isinstance(other, NumberVariable):
            return self.value != other.value
        return False

    def __gt__(self, other):
        if isinstance(other, NumberVariable):
            return self.value > other.value
        return False

    def __ge__(self, other):
        if isinstance(other, NumberVariable):
            return self.value >= other.value
        return False

    def __lt__(self, other):
        if isinstance(other, NumberVariable):
            return self.value < other.value
        return False

    def __le__(self, other):
        if isinstance(other, NumberVariable):
            return self.value <= other.value
        return False

    def __str__(self):
        return 'number \'' + self.name + '\' = ' + str(self.value)


class PixelVariable(Variable):
    def __init__(self, name: str, r: int = 0, g: int = 0, b: int = 0):
        super().__init__(name)
        self.__MIN_VALUE = 0
        self.__MAX_VALUE = 255
        self.r = self.__pixelize(r)
        self.g = self.__pixelize(g)
        self.b = self.__pixelize(b)

    def __pixelize(self, number):
        return int(min(max(number, self.__MIN_VALUE), self.__MAX_VALUE))

    def set_r(self, value):
        self.r = self.__pixelize(value)

    def set_g(self, value):
        self.g = self.__pixelize(value)

    def set_b(self, value):
        self.b = self.__pixelize(value)

    def has_zero(self):
        return self.r == 0 or self.g == 0 or self.b == 0

    def add_value(self, value):
        self.set_r(self.r + value)
        self.set_g(self.g + value)
        self.set_b(self.b + value)

    def multiply_by_value(self, value):
        self.set_r(self.r * value)
        self.set_g(self.g * value)
        self.set_b(self.b * value)

    def divide_by_value(self, value):
        self.set_r(self.r / value)
        self.set_g(self.g / value)
        self.set_b(self.b / value)

    def modulo_with_value(self, value):
        self.set_r(self.r % value)
        self.set_g(self.g % value)
        self.set_b(self.b % value)

    def __add__(self, other):
        if isinstance(other, NumberVariable):
            return other + self
        if not isinstance(other, PixelVariable):
            return None

        new_pixel = deepcopy(other)
        new_pixel.name = other.name + '+' + self.name
        new_pixel.set_r(other.r + self.r)
        new_pixel.set_g(other.g + self.g)
        new_pixel.set_b(other.b + self.b)
        return new_pixel

    def __sub__(self, other):
        if isinstance(other, NumberVariable):
            new_pixel = deepcopy(self)
            new_pixel.add_value(-other.value)
            return new_pixel
        if not isinstance(other, PixelVariable):
            return None

        new_pixel = deepcopy(other)
        new_pixel.name = self.name + '-' + other.name
        new_pixel.set_r(self.r - other.r)
        new_pixel.set_g(self.g - other.g)
        new_pixel.set_b(self.b - other.b)
        return new_pixel

    def __mul__(self, other):
        if isinstance(other, NumberVariable):
            return other * self
        if not isinstance(other, PixelVariable):
            return None

        new_pixel = deepcopy(other)
        new_pixel.name = other.name + '*' + self.name
        new_pixel.set_r(other.r * self.r)
        new_pixel.set_g(other.g * self.g)
        new_pixel.set_b(other.b * self.b)
        return new_pixel

    def __truediv__(self, other):
        if isinstance(other, NumberVariable):
            new_pixel = deepcopy(self)
            new_pixel.name = self.name + '/' + other.name
            new_pixel.divide_by_value(other.value)
            return new_pixel

        if not isinstance(other, PixelVariable):
            return None

        new_pixel = deepcopy(other)
        new_pixel.name = self.name + '/' + other.name
        new_pixel.set_r(self.r / other.r)
        new_pixel.set_g(self.g / other.g)
        new_pixel.set_b(self.b / other.b)
        return new_pixel

    def __mod__(self, other):
        if isinstance(other, NumberVariable):
            new_pixel = deepcopy(self)
            new_pixel.name = self.name + '%' + other.name
            new_pixel.modulo_with_value(other.value)
            return new_pixel

        if not isinstance(other, PixelVariable):
            return None

        new_pixel = deepcopy(other)
        new_pixel.name = self.name + '%' + other.name
        new_pixel.set_r(self.r % other.r)
        new_pixel.set_g(self.g % other.g)
        new_pixel.set_b(self.b % other.b)
        return new_pixel

    def __bool__(self):
        return self.r > 0 and self.g > 0 and self.b > 0

    def __eq__(self, other):
        if isinstance(other, PixelVariable):
            return self.r == other.r and self.g == other.g and self.b == other.b
        return False

    def __ne__(self, other):
        if isinstance(other, PixelVariable):
            return self.r != other.r or self.g != other.g or self.b != other.b
        return False

    def __gt__(self, other):
        if isinstance(other, PixelVariable):
            return self.r > other.r and self.g > other.g and self.b > other.b
        return False

    def __ge__(self, other):
        if isinstance(other, PixelVariable):
            return self.r >= other.r and self.g >= other.g and self.b >= other.b
        return False

    def __lt__(self, other):
        if isinstance(other, PixelVariable):
            return self.r < other.r and self.g < other.g and self.b < other.b
        return False

    def __le__(self, other):
        if isinstance(other, PixelVariable):
            return self.r <= other.r and self.g <= other.g and self.b <= other.b
        return False

    def __str__(self):
        return 'pixel \'' + self.name + '\' = pixel(r=' + str(self.r) + \
               ', g=' + str(self.g) + ', b=' + str(self.b) + ')'


class MatrixVariable(Variable):
    def __init__(self, name: str, rows: List[List[int]] = None):
        super().__init__(name)
        self.rows = rows
        self.xdim = len(rows[0])
        self.ydim = len(rows)

    def has_zero(self):
        for row in self.rows:
            for number in row:
                if number == 0:
                    return True
        return False

    def add_value(self, value: int):
        for i in range(self.ydim):
            self.rows[i] = [x + value for x in self.rows[i]]

    def multiply_by_value(self, value: int):
        for i in range(self.ydim):
            self.rows[i] = [x * value for x in self.rows[i]]

    def divide_by_value(self, value: int):
        for i in range(self.ydim):
            self.rows[i] = [x // value for x in self.rows[i]]

    def modulo_with_value(self, value: int):
        for i in range(self.ydim):
            self.rows[i] = [x % value for x in self.rows[i]]

    def special_multiply(self, other):
        if isinstance(other, Matrix3dVariable):
            return other.special_multiply(self)

        if not isinstance(other, MatrixVariable):
            return None

        if other.xdim != self.xdim or other.ydim != self.ydim:
            raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                            str(other.xdim) + ' by ' + str(other.ydim))
        new_rows = []
        for row, o_row in zip(self.rows, other.rows):
            new_row = []
            for field, o_field in zip(row, o_row):
                new_row.append(field * o_field)
            new_rows.append(new_row)
        return MatrixVariable('', new_rows)

    def __add__(self, other):
        if isinstance(other, NumberVariable):
            return other + self

        if isinstance(other, Matrix3dVariable):
            if self.xdim != other.xdim or self.ydim != other.ydim:
                raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                                str(other.xdim) + ' by ' + str(other.ydim))
            new_matrix = deepcopy(other)
            new_matrix.name = self.name + '+' + other.name
            for i in range(new_matrix.zdim):
                new_matrix.matrices[i] += self
            return new_matrix

        if not isinstance(other, MatrixVariable):
            return None

        if self.xdim != other.xdim or self.ydim != other.ydim:
            raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                            str(other.xdim) + ' by ' + str(other.ydim))
        new_rows = []
        for row, o_row in zip(self.rows, other.rows):
            new_row = []
            for field, o_field in zip(row, o_row):
                new_row.append(field + o_field)
            new_rows.append(new_row)
        return MatrixVariable(self.name + '+' + other.name, new_rows)

    def __sub__(self, other):
        if isinstance(other, NumberVariable):
            number = deepcopy(other)
            number.value = -number.value
            return number + self

        if isinstance(other, Matrix3dVariable):
            if self.xdim != other.xdim or self.ydim != other.ydim:
                raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                                str(other.xdim) + ' by ' + str(other.ydim))
            new_matrix = deepcopy(other)
            new_matrix.name = self.name + '-' + other.name
            for i in range(new_matrix.zdim):
                new_matrix.matrices[i] -= self
            return new_matrix

        if not isinstance(other, MatrixVariable):
            return None

        if self.xdim != other.xdim or self.ydim != other.ydim:
            raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                            str(other.xdim) + ' by ' + str(other.ydim))
        new_rows = []
        for row, o_row in zip(self.rows, other.rows):
            new_row = []
            for field, o_field in zip(row, o_row):
                new_row.append(field - o_field)
            new_rows.append(new_row)
        return MatrixVariable(self.name + '-' + other.name, new_rows)

    def __mul__(self, other):
        if isinstance(other, NumberVariable):
            return other * self

        if not isinstance(other, MatrixVariable):
            return None

        if self.xdim != other.ydim:
            raise MatrixDimensionsException(str(other.ydim), str(self.xdim))

        rows = []
        for i in range(self.ydim):
            rows.append([0] * other.xdim)
        # iterating by row by self
        for i in range(self.ydim):
            # iterating by coloum by other
            for j in range(other.xdim):
                # iterating by rows of other
                for k in range(other.ydim):
                    rows[i][j] += self.rows[i][k] * other.rows[k][j]

        return MatrixVariable(self.name + '*' + other.name, rows)

    def __truediv__(self, other):
        if isinstance(other, NumberVariable):
            new_matrix = deepcopy(self)
            new_matrix.name = self.name + '/' + other.name
            new_matrix.divide_by_value(other.value)
            return new_matrix
        return None

    def __mod__(self, other):
        if isinstance(other, NumberVariable):
            new_matrix = deepcopy(self)
            new_matrix.name = self.name + '%' + other.name
            new_matrix.modulo_with_value(other.value)
            return new_matrix
        return None

    def __bool__(self):
        for row in self.rows:
            for number in row:
                if number <= 0:
                    return False
        return True

    def __eq__(self, other):
        if isinstance(other, MatrixVariable):
            return self.rows == other.rows
        return False

    def __ne__(self, other):
        if isinstance(other, MatrixVariable):
            return self.rows != other.rows
        return False

    def __gt__(self, other):
        if isinstance(other, MatrixVariable):
            return self.rows > other.rows
        return False

    def __ge__(self, other):
        if isinstance(other, MatrixVariable):
            return self.rows >= other.rows
        return False

    def __lt__(self, other):
        if isinstance(other, MatrixVariable):
            return self.rows < other.rows
        return False

    def __le__(self, other):
        if isinstance(other, MatrixVariable):
            return self.rows <= other.rows
        return False

    def __str__(self):
        return 'matrix \'' + self.name + '\' = ' + str(self.rows)


class Matrix3dVariable(Variable):
    def __init__(self, name: str, matrices: List[MatrixVariable]):
        super().__init__(name)
        self.matrices = matrices
        self.xdim = matrices[0].xdim
        self.ydim = matrices[0].ydim
        self.zdim = len(matrices)

    def has_zero(self):
        for matrix in self.matrices:
            if matrix.has_zero():
                return True
        return False

    def add_value(self, value: int):
        for i in range(len(self.matrices)):
            self.matrices[i].add_value(value)

    def multiply_by_value(self, value: int):
        for i in range(len(self.matrices)):
            self.matrices[i].multiply_by_value(value)

    def special_multiply(self, other):
        if isinstance(other, Matrix3dVariable):
            if other.xdim != self.xdim or other.ydim != self.ydim or other.zdim != self.zdim:
                raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim) + ' by ' + str(self.zdim),
                                                str(other.xdim) + ' by ' + str(other.ydim) + ' by ' + str(other.zdim))
            new_matrices = []
            for matrix, o_matrix in zip(self.matrices, other.matrices):
                new_matrices.append(matrix.special_multiply(o_matrix))
            return Matrix3dVariable('', new_matrices)

        elif isinstance(other, MatrixVariable):
            if other.xdim != self.xdim or other.ydim != self.ydim:
                raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                                str(other.xdim) + ' by ' + str(other.ydim))
            new_matrices = []
            for matrix in self.matrices:
                new_matrices.append(matrix.special_multiply(other))
            return Matrix3dVariable('', new_matrices)
        return None

    def __add__(self, other):
        if isinstance(other, NumberVariable):
            return other + self

        if isinstance(other, MatrixVariable):
            new_matrix = deepcopy(self)
            new_matrix.name = self.name + '+' + other.name
            for m in range(self.zdim):
                new_matrix.matrices[m] += other
            return new_matrix

        if not isinstance(other, Matrix3dVariable):
            return None

        if self.xdim != other.xdim or self.ydim != other.ydim or self.zdim != other.zdim:
            raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                            str(other.xdim) + ' by ' + str(other.ydim),)
        new_matrix = deepcopy(self)
        new_matrix.name = self.name + '+' + other.name
        for m in range(self.zdim):
            new_matrix.matrices[m] += other.matrices[m]
        return new_matrix

    def __sub__(self, other):
        if isinstance(other, MatrixVariable) or isinstance(other, NumberVariable):
            new_matrix = deepcopy(self)
            new_matrix.name = self.name + '-' + other.name
            for m in range(self.zdim):
                new_matrix.matrices[m] -= other
            return new_matrix

        if not isinstance(other, Matrix3dVariable):
            return None

        if self.xdim != other.xdim or self.ydim != other.ydim or self.zdim != other.zdim:
            raise MatrixDimensionsException(str(self.xdim) + ' by ' + str(self.ydim),
                                            str(other.xdim) + ' by ' + str(other.ydim),)
        new_matrix = deepcopy(self)
        new_matrix.name = self.name + '-' + other.name
        for m in range(self.zdim):
            new_matrix.matrices[m] -= other.matrices[m]
        return new_matrix

    def __mul__(self, other):
        if isinstance(other, MatrixVariable) or isinstance(other, NumberVariable):
            new_matrix = deepcopy(self)
            new_matrix.name = self.name + '*' + other.name
            for m in range(self.zdim):
                new_matrix.matrices[m] *= other
            return new_matrix

        if not isinstance(other, Matrix3dVariable):
            return None

        if self.zdim != other.zdim:
            raise MatrixDimensionsException(str(other.zdim), str(self.zdim))
        new_matrix = deepcopy(self)
        new_matrix.name = self.name + '*' + other.name
        for m in range(self.zdim):
            new_matrix.matrices[m] *= other.matrices[m]
        return new_matrix

    def __truediv__(self, other):
        if not isinstance(other, NumberVariable):
            return None

        new_matrix = deepcopy(self)
        new_matrix.name = self.name + '/' + other.name
        for m in range(new_matrix.zdim):
            new_matrix.matrices[m] /= other
        return new_matrix

    def __mod__(self, other):
        if not isinstance(other, NumberVariable):
            return None

        new_matrix = deepcopy(self)
        new_matrix.name = self.name + '%' + other.name
        for m in range(new_matrix.zdim):
            new_matrix.matrices[m] %= other
        return new_matrix

    def __bool__(self):
        for matrix in self.matrices:
            if not matrix:
                return False
        return True

    def __eq__(self, other):
        if isinstance(other, Matrix3dVariable):
            return self.matrices == other.matrices
        return False

    def __ne__(self, other):
        if isinstance(other, Matrix3dVariable):
            return self.matrices != other.matrices
        return False

    def __gt__(self, other):
        if isinstance(other, Matrix3dVariable):
            return self.matrices > other.matrices
        return False

    def __ge__(self, other):
        if isinstance(other, Matrix3dVariable):
            return self.matrices >= other.matrices
        return False

    def __lt__(self, other):
        if isinstance(other, Matrix3dVariable):
            return self.matrices < other.matrices
        return False

    def __le__(self, other):
        if isinstance(other, Matrix3dVariable):
            return self.matrices <= other.matrices
        return False

    def __str__(self):
        matrices_str = str(self.matrices[0].rows)
        for matrix in self.matrices[1:]:
            matrices_str += ',\n' + str(matrix.rows)
        return 'matrix \'' + self.name + '\' = {' + matrices_str + '}'
