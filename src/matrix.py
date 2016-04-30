import operator


class Matrix(object):
    def __init__(self, elements):
        self.row_count = self.check_positive_length(elements)
        self.col_count = self.check_positive_length(elements[0])
        self.elements = []
        for row in elements:
            self.elements.append(self.check_equal_length(row, self.row_count))

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

    def transpose(self):
        for i in range(self.row_count):
            for j in range(i+1, self.col_count):
                self.elements[i][j], self.elements[j][i] = self.elements[j][i], self.elements[i][j]
        return self

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
        return self.cofactor_matrix().transpose()

    def inverse(self):
        assert not self.is_singular()
        return self.adjugate().scalar_muliplication(1.0/self.determinant())

    def get_non_zero_element(self, elements):
        for i, element in enumerate(elements):
            if element != 0:
                return i, element
        return None, None

    # def row_echelon_form(self):
    #     for i in range(self.row_count):
    #         column = self.get_col(i)
    #         zero_index, zero_element = self.get_non_zero_element(column[i:])
    #         if zero_element is None:
    #             continue
    #         else:
    #             for j in range()
    #             self.elementwise_binary_operator(operator)





A = Matrix([[1,2,3],[3,4,5],[6,7,9]])
B = Matrix([[4,3],[2,1]])
print A
print
print A.scalar_muliplication(2)
print
print A.transpose()
print
print A*A.adjugate()
print
print A.inverse()
print
print A.inverse()*A

