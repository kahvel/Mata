
from matrix import Matrix, get_unit_matrix, get_row_matrix, EchelonForm, IndexElementPair


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
        result += "\nmax" + coefficients_to_formula(self.c) + " = " + str(self.value)
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

    def get_result(self, matrix):
        x_values = []
        for i in range(self.A.col_count):
            col = matrix.get_col(i)
            one_index = self.all_zeros_except_one_one(col)
            self.update_x_values(matrix, one_index, x_values)
        return LinearProgrammingResult(-matrix.elements[-1][-1], x_values, self.c)

    def calculate_ratio(self, chosen, last):
        if chosen > 0:
            return last/chosen
        else:
            return float("inf")

    def first_smallest_ratio(self, chosen_col, last_col):
        minimum_ratio = float("inf")
        ratio_index = None
        for i, chosen, last in zip(range(len(chosen_col)-1), chosen_col[:-1], last_col[:-1]):
            ratio = self.calculate_ratio(chosen, last)
            if ratio < minimum_ratio:
                minimum_ratio = ratio
                ratio_index = i
        return IndexElementPair(ratio_index, minimum_ratio)

    def run(self):
        matrix = self.build_matrix()
        max_result = LinearProgrammingResult(-float("inf"), [], [])
        while True:
            last_row = matrix.get_row(-1)
            chosen_col = self.pick_first_positive(last_row)
            if chosen_col is None:
                return self.get_result(matrix)
            else:
                echelon_form = EchelonForm(matrix)
                smallest_ratio = self.first_smallest_ratio(matrix.get_col(chosen_col), matrix.get_col(-1))
                if smallest_ratio.is_none():
                    max_result.set_status("UNBOUNDED")
                    return max_result
                current_row = matrix.get_row(smallest_ratio.index)
                scaled_current_row = echelon_form.scale_row(current_row[chosen_col], current_row)
                new_elements = echelon_form.zero_rows(chosen_col, range(smallest_ratio.index), scaled_current_row)
                new_elements.append(scaled_current_row)
                new_elements.extend(echelon_form.zero_rows(chosen_col, range(smallest_ratio.index+1, matrix.row_count), scaled_current_row))
                matrix = Matrix(new_elements)
                result = self.get_result(matrix)
                if result.value >= max_result.value:
                    max_result = result
                else:
                    max_result.set_status("UNBOUNDED")
                    return max_result


if __name__ == '__main__':
    A = Matrix([
        [1,0,0,1,-1],
        [0,1,0,-1,0],
        [1,0,0,0,0],
        [0,1,0,0,0],
        [0,0,1,0,0],
        [0,0,0,1,0],
        [0,0,0,0,1]
    ])
    b = [0,0,3,4,7,2,5]
    c = [1,1,1,0,0]
    lp = LinearProgramming(c, A, b)
    result = lp.run()
    print lp
    print
    print lp.dual()
