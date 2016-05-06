
from matrix import Matrix, get_unit_matrix, get_row_matrix, IndexElementPair


def coefficients_to_formula(coefficients, variable):
    return "+".join(map(lambda x: "(" + str(x[1]) + "*" + variable + str(x[0]) + ")", enumerate(coefficients)))


def get_formula(objective, c, A, b, variable, inequality):
    result = objective + " " + coefficients_to_formula(c, variable) + "\n"
    result += "\n".join(coefficients_to_formula(coefficients, variable) + " " + inequality + "= " + str(elem) for coefficients, elem in zip(A, b)) + "\n"
    result += ", ".join(map(lambda x: variable + str(x), range(len(c)))) + " >= 0"
    return result


class LinearProgrammingResult(object):
    def __init__(self, objective_function_value, x_values, c):
        self.value = objective_function_value
        self.x_values = x_values
        self.status = "SUCCESSFUL"
        self.c = c

    def set_status(self, status):
        self.status = status

    def __repr__(self):
        result = ", ".join(map(lambda x: "x" + str(x[0]) + "=" + str(x[1]), enumerate(self.x_values)))
        result += "\nmax" + coefficients_to_formula(self.c, "x") + " = " + str(self.value)
        result += "\nStatus: " + str(self.status)
        return result


class LinearProgramming(object):
    def __init__(self, c, A, b):
        assert isinstance(A, Matrix)
        assert A.row_count == len(b)
        assert A.col_count == len(c)
        self.A = A
        self.b = b
        self.c = c

    def __repr__(self):
        return get_formula("max", self.c, self.A.elements, self.b, "x", "<")

    def dual(self):
        return get_formula("min", self.b, self.A.transposed().elements, self.c, "y", ">")

    def pick_first_positive(self, elements):
        for i, element in enumerate(elements):
            if element > 0:
                return i
        return None

    def build_matrix(self):
        A_and_unit = self.A.merge_horisontal(get_unit_matrix(self.A.row_count)).merge_horisontal(Matrix([self.b]).transposed())
        c_and_zero = Matrix([self.c]).merge_horisontal(get_row_matrix(0, self.A.row_count+1))
        return A_and_unit.merge_vertical(c_and_zero)

    def all_zeros_except_one_one(self, elements):
        i = None
        for j, element in enumerate(elements):
            if i is None and element == 1:
                i = j
            elif i is not None and element == 1:
                return None
            elif element != 0 and element != 1:
                return None
        return i

    def update_x_values(self, matrix, one_index, x_values):
        if one_index is None:
            x_values.append(0)
        else:
            x_values.append(matrix.elements[one_index][-1])

    def get_result(self, matrix, variable_locations, coefficients):
        x_values = []
        for i in variable_locations:
            col = matrix.get_col(i)
            one_index = self.all_zeros_except_one_one(col)
            self.update_x_values(matrix, one_index, x_values)
        return LinearProgrammingResult(-matrix.elements[-1][-1], x_values, coefficients)

    def calculate_ratio(self, chosen, last):
        if chosen > 0:
            return last/chosen
        else:
            return float("inf")

    def first_smallest_ratio(self, chosen_col, last_col):
        minimum_ratio = float("inf")
        index = None
        element = None
        for i, chosen, last in zip(range(len(chosen_col)-1), chosen_col[:-1], last_col[:-1]):
            ratio = self.calculate_ratio(chosen, last)
            if ratio < minimum_ratio:
                element = chosen
                minimum_ratio = ratio
                index = i
        return IndexElementPair(index, element)

    def build_phase_one_matrix(self):
        A_and_unit = self.A.merge_horisontal(get_unit_matrix(self.A.row_count)).merge_horisontal(Matrix([self.b]).transposed())
        c_and_zero = Matrix([self.c]).merge_horisontal(get_row_matrix(0, self.A.row_count+1))
        new_objective = get_row_matrix(0, self.A.col_count).merge_horisontal(get_row_matrix(-1, self.A.row_count)).merge_horisontal(Matrix([[0]]))
        return A_and_unit.merge_vertical(c_and_zero).merge_vertical(new_objective)#.merge_horisontal(Matrix([([0]*(self.A.row_count+1))+[1]]).transposed())

    def build_phase_one_matrix2(self):
        A_and_unit = []
        for row_index in range(self.A.row_count):
            row = self.A.get_row(row_index)
            if self.b[row_index] < 0:
                A_elements = list(map(lambda x: -1*x, row))
                b_element = -self.b[row_index]
                identity_matrix_row = [0] * row_index + [-1] + [0] * (self.A.row_count - 1 - row_index)
            else:
                A_elements = row
                b_element = self.b[row_index]
                identity_matrix_row = [0] * row_index + [1] + [0] * (self.A.row_count - 1 - row_index)
            # identity_matrix_row2 = [0] * row_index + [1] + [0] * (self.A.row_count - 1 - row_index)
            new_row = A_elements + identity_matrix_row + identity_matrix_row + [b_element]
            A_and_unit.append(new_row)
        new_objective = get_row_matrix(0, self.A.col_count+self.A.row_count).merge_horisontal(get_row_matrix(-1, self.A.row_count)).merge_horisontal(Matrix([[0]]))
        return Matrix(A_and_unit).merge_vertical(new_objective)

    def price_out(self, matrix, indices):
        for row, col in enumerate(indices):
            matrix.make_elements_zero_using_row(row, col)

    def run(self):
        matrix = self.build_phase_one_matrix2()
        basic_variable_locations = range(self.A.col_count+self.A.row_count, self.A.col_count+self.A.row_count*2)
        self.price_out(matrix, basic_variable_locations)
        basic_variable_count = self.A.row_count
        result, matrix = self.optimise(matrix, basic_variable_locations, [-1]*basic_variable_count)
        if not all(map(lambda x: x == 0, result.x_values)) or round(result.value,7) != 0:
            result.set_status("UNFEASIBLE")
            return result
        else:
            matrix.delete_row(-1)
            for i in range(self.A.col_count+self.A.row_count-1, self.A.col_count-1, -1):
                matrix.delete_col(i)
            matrix = matrix.merge_vertical(Matrix([self.c]).merge_horisontal(get_row_matrix(0, self.A.row_count+1)))
            for i in range(self.A.col_count+self.A.row_count):
                col = matrix.get_col(i)[:-1]
                if sum(map(lambda x: x == 1, col)) == 1 and sum(map(lambda x: x == 0, col)) == matrix.row_count - 2:
                    matrix.make_elements_zero_using_row(col.index(1), i, [matrix.row_count-1])
            result = self.optimise(matrix, range(self.A.col_count), self.c)
            return result[0]

    def optimise(self, matrix, variable_locations, coefficients):
        max_result = LinearProgrammingResult(-float("inf"), [], [])
        while True:
            last_row = matrix.get_row(-1)[:-1]
            chosen_col = self.pick_first_positive(last_row)
            if chosen_col is None:
                return self.get_result(matrix, variable_locations, coefficients), matrix
            else:
                smallest_ratio = self.first_smallest_ratio(matrix.get_col(chosen_col), matrix.get_col(-1))
                if smallest_ratio.is_none():
                    max_result.set_status("UNBOUNDED")
                    return max_result, matrix
                matrix.scale_row(smallest_ratio.element, smallest_ratio.index)
                matrix.make_elements_zero_using_row(smallest_ratio.index, chosen_col)
                result = self.get_result(matrix, variable_locations, coefficients)
                if result.value >= max_result.value:
                    max_result = result
                # else:
                #     max_result.set_status("UNBOUNDED")
                #     return max_result, matrix


if __name__ == '__main__':
    # A = Matrix([
    #     [1,0,0,1,-1],
    #     [0,1,0,-1,0],
    #     [1,0,0,0,0],
    #     [0,1,0,0,0],
    #     [0,0,1,0,0],
    #     [0,0,0,1,0],
    #     [0,0,0,0,1]
    # ])
    # b = [0,0,3,4,7,2,5]
    # c = [1,1,1,0,0]
    # lp = LinearProgramming(c, A, b)
    # result = lp.run()
    # print lp
    # print
    # print lp.dual()
    # print

    A = Matrix([
        [1,1,0],
        [0,2,1],
        [1,0,1]
    ])
    b = [3,4,2]
    c = [1,7,1]
    lp = LinearProgramming(c, A, b)
    result = lp.run()
    print lp
    print
    print result

