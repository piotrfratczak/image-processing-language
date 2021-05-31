from typing import List


class Variable:
    def evaluate_to_bool(self):
        if self:
            return True
        return False


class NumberVariable(Variable):
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

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


class PixelVariable(Variable):
    def __init__(self, name: str, r: int = 0, g: int = 0, b: int = 0):
        self.name = name
        self.r = self.__pixelize(r)
        self.g = self.__pixelize(g)
        self.b = self.__pixelize(b)

        self.__MIN_VALUE = 0
        self.__MAX_VALUE = 255

    def __pixelize(self, number):
        return min(max(number, self.__MIN_VALUE), self.__MAX_VALUE)

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


class MatrixVariable(Variable):
    def __init__(self, name: str, rows: List[List[int]] = None):
        self.name = name
        self.rows = rows
        self.xdim = len(rows[0])
        self.ydim = len(rows)

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


class Matrix3dVariable(Variable):
    def __init__(self, name: str, matrices: List[MatrixVariable]):
        self.name = name
        self.matrices = matrices
        self.zdim = len(matrices)

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
