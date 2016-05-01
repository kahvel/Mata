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
        return self.elements[i]

    def get_col(self, j):
        return list(map(operator.itemgetter(j), self.elements))

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

    def row_echelon_form(self):
        echelon_form = EchelonForm(self)
        return echelon_form.row_echelon_form()


class EchelonForm(object):
    def __init__(self, matrix):
        assert isinstance(matrix, Matrix)
        self.matrix = matrix
        self.rank = 0

    def get_new_row(self, non_zero_index):
        if non_zero_index == self.rank:
            return self.matrix.get_row(self.rank)
        else:
            current_row = self.matrix.get_row(self.rank)
            non_zero_row = self.matrix.get_row(non_zero_index)
            return map(operator.add, current_row, non_zero_row)

    def get_non_zero_element(self, elements):
        for i, element in enumerate(elements[self.rank:]):
            if element != 0:
                return IndexElementPair(i+self.rank, element)
        return IndexElementPair(None, None)

    def get_initial_rows(self):
        return [row for row in self.matrix.elements[:self.rank]]

    def zero_rows(self, i, rows_to_zero, scaled_current_row):
        new_rows = []
        print
        for j in rows_to_zero:
            row = self.matrix.get_row(j)
            multiplier = row[i]
            new_rows.append(list(map(lambda x,y: x-multiplier*y, row, scaled_current_row)))
        return new_rows

    def scale_row(self, factor, row):
        return map(lambda x: x/float(factor), row)

    def get_new_elements(self, non_zero_element, i):
        scaled_current_row = self.scale_row(non_zero_element.element, self.get_new_row(non_zero_element.index))
        new_elements = self.get_initial_rows()
        new_elements.append(scaled_current_row)
        new_elements.extend(self.zero_rows(i, range(self.rank+1, self.matrix.row_count), scaled_current_row))
        return new_elements

    def update_rank_and_matrix(self, non_zero_element, i):
        if not non_zero_element.is_none():
            self.matrix = Matrix(self.get_new_elements(non_zero_element, i))
            self.rank += 1

    def row_echelon_form(self):
        self.rank = 0
        for i in range(self.matrix.col_count):
            non_zero_element = self.get_non_zero_element(self.matrix.get_col(i))
            self.update_rank_and_matrix(non_zero_element, i)
        return self.matrix


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

