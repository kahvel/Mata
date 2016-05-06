import operator


def get_unit_matrix(n):
    elements = []
    for i in range(n):
        elements.append(list(map(int, (j == i for j in range(n)))))
    return Matrix(elements)


def get_row_matrix(element, n):
    return Matrix([[element]*n])


def get_col_matrix(element, n):
    return get_row_matrix(element, n).transposed()


class IndexElementPair(object):
    def __init__(self, index, element):
        self.index = index
        self.element = element

    def is_none(self):
        return self.index is None

    def __repr__(self):
        return str(self.element) + " index: " + str(self.index)


class Matrix(object):
    def __init__(self, elements):
        self.row_count = self.check_positive_length(elements)
        self.col_count = self.check_positive_length(elements[0])
        self.elements = []
        for row in elements:
            self.elements.append(self.check_equal_length(row[:], self.col_count))

    def check_positive_length(self, elements):
        assert len(elements) > 0
        return len(elements)

    def check_equal_length(self, elements, length):
        assert len(elements) == length
        return list(elements)

    def check_matrix_size(self, other):
        assert self.row_count == other.row_count
        assert self.col_count == other.col_count

    def elementwise_binary_operator(self, op, this, other):
        return Matrix([[op(a, b) for a, b in zip(row, other_row)] for row, other_row in zip(this, other)])

    def elementwise_unary_operator(self, op, elements):
        return Matrix([[op(a) for a in row] for row in elements])

    def __add__(self, other):
        self.check_matrix_size(other)
        return self.elementwise_binary_operator(operator.add, self.elements, other.elements)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self.check_matrix_size(other)
        return self.elementwise_binary_operator(operator.sub, self.elements, other.elements)

    def __rsub__(self, other):
        self.check_matrix_size(other)
        return self.elementwise_binary_operator(operator.isub, self.elements, other.elements)

    def __repr__(self):
        return "\n".join(map(str, self.elements))

    def transposed(self):
        new_elements = [[None for _ in range(self.row_count)] for _ in range(self.col_count)]
        for i in range(self.row_count):
            for j in range(self.col_count):
                new_elements[j][i] = self.elements[i][j]
        return Matrix(new_elements)

    def get_row(self, i):
        return self.elements[i][:]

    def get_col(self, j):
        return list(map(operator.itemgetter(j), self.elements))

    def set_row(self, i, elements):
        assert len(elements) == self.col_count
        self.elements[i] = list(elements)

    def set_col(self, i, elements):
        assert len(elements) == self.row_count
        for j in range(self.row_count):
            self.elements[j][i] = elements[j]

    def delete_row(self, i):
        del self.elements[i]
        self.row_count -= 1

    def delete_col(self, i):
        for j in range(self.row_count):
            del self.elements[j][i]
        self.col_count -= 1

    def __mul__(self, other):
        assert self.col_count == other.row_count
        result = []
        for i in range(self.row_count):
            result.append([])
            for j in range(other.col_count):
                result[i].append(sum(map(lambda x: x[0]*x[1], zip(self.get_row(i), other.get_col(j)))))
        return Matrix(result)

    def __rmul__(self, other):
        return other.__mul__(self)

    def scalar_muliplication(self, scalar):
        return self.elementwise_unary_operator(lambda x: x*scalar, self.elements)

    def determinant(self):
        assert self.row_count == self.col_count
        if self.row_count == 1:
            return self.elements[0][0]
        else:
            return sum(self.elements[0][i]*self.cofactor(0, i) for i in range(self.col_count))

    def cofactor(self, row, col):
        return (-1)**(row+col)*self.minor(row, col)

    def cofactor_matrix(self):
        return Matrix([[self.cofactor(i, j) for j in range(self.col_count)] for i in range(self.row_count)])

    def minor(self, row, col):
        new_matrix = Matrix([r[:col]+r[col+1:] for r in self.elements[:row]+self.elements[row+1:]])
        return new_matrix.determinant()

    def is_singular(self):
        return self.determinant() == 0

    def adjugate(self):
        return self.cofactor_matrix().transposed()

    def inverse(self):
        assert not self.is_singular()
        return self.adjugate().scalar_muliplication(1.0/self.determinant())

    def merge_horisontal(self, other):
        assert self.row_count == other.row_count
        new_elements = []
        for i in range(self.row_count):
            new_elements.append(self.get_row(i) + other.get_row(i))
        return Matrix(new_elements)

    def merge_vertical(self, other):
        assert self.col_count == other.col_count
        new_elements = []
        for i in range(self.col_count):
            new_elements.append(self.get_col(i) + other.get_col(i))
        return Matrix(new_elements).transposed()

    def __eq__(self, other):
        return self.elements == other.elements

    def is_symmetric(self):
        return self == self.transposed()

    def get_row_with_non_zero_element_row_op(self, start_row, col):
        non_zero_element = self.get_first_non_zero_element_in_col(col, start_row)
        if non_zero_element.index == start_row:
            return self.get_row(start_row)
        else:
            current_row = self.get_row(start_row)
            non_zero_row = self.get_row(non_zero_element.index)
            return map(operator.add, current_row, non_zero_row)

    def make_element_non_zero_using_row(self, row, col):
        self.set_row(row, self.get_row_with_non_zero_element_row_op(row, col))

    def get_first_non_zero_element_in_col(self, col, start_row=0):
        for i, element in enumerate(self.get_col(col)[start_row:]):
            if element != 0:
                return IndexElementPair(i+start_row, element)

    def all_elements_zero_in_row(self, i, start_col=0):
        return self.all_elements_zero(self.get_row(i)[start_col:])

    def all_elements_zero_in_col(self, i, start_row=0):
        return self.all_elements_zero(self.get_col(i)[start_row:])

    def all_elements_zero(self, elements):
        return all(map(lambda e: e == 0, elements))

    def get_first_rows(self, number_of_rows):
        return [row for row in self.elements[:number_of_rows]]

    def get_zeroed_row_using_row(self, i, row_index, col_index, rows_to_zero):
        if i in rows_to_zero:
            row = self.get_row(i)
            multiplier = row[col_index]
            return list(map(lambda x, y: x-multiplier*y, row, self.get_row(row_index)))
        else:
            return self.get_row(i)

    def get_zeroed_elements_using_row(self, row_index, col_index, rows_to_zero):
        new_rows = []
        for i in range(self.row_count):
            new_rows.append(self.get_zeroed_row_using_row(i, row_index, col_index, rows_to_zero))
        return new_rows

    def make_elements_zero_using_row(self, row_index, col_index, rows_to_zero=None):
        if rows_to_zero is None:
            rows_to_zero = tuple(i for i in range(self.row_count) if i != row_index)
        for i, new_row in enumerate(self.get_zeroed_elements_using_row(row_index, col_index, rows_to_zero)):
            self.set_row(i, new_row)

    def get_scaled_row(self, factor, row_index):
        return map(lambda x: x/float(factor), self.get_row(row_index))

    def scale_row(self, factor, row_index):
        self.set_row(row_index, self.get_scaled_row(factor, row_index))

    def col_to_row_echelon_form(self, col_index, row_index=0):
        self.make_element_non_zero_using_row(row_index, col_index)
        non_zero_element = self.get_first_non_zero_element_in_col(col_index, row_index)
        self.scale_row(non_zero_element.element, row_index)
        self.make_elements_zero_using_row(row_index, col_index, range(row_index+1, self.row_count))
        return self

    def row_echelon_form_step(self, matrix, col_index, start_row):
        if not matrix.all_elements_zero_in_col(col_index, start_row):
            return matrix.col_to_row_echelon_form(col_index, start_row), start_row+1
        else:
            return matrix, start_row

    def row_echelon_form(self):
        rank = 0
        matrix = Matrix(self.elements)
        for col_index in range(matrix.col_count):
            matrix, rank = self.row_echelon_form_step(matrix, col_index, rank)
        return matrix


if __name__ == '__main__':
    A = Matrix([[1,2,3],[3,4,5],[6,7,9]])
    B = Matrix([[4,2,2],[2,1,1]])
    C = Matrix([[4,3],[2,1]])
    print B.row_echelon_form()
    print
    print Matrix([[0]]).row_echelon_form()
    print
    print A
    print
    print A.scalar_muliplication(2)
    print
    print A.transposed()
    print
    print A*A.adjugate()
    print
    print A.inverse()
    print
    print A.inverse()*A

