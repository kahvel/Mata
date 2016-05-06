import matrix
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.elements1 = [
            [1,2,3],
            [4,5,6]
        ]
        self.matrix1 = matrix.Matrix(self.elements1)
        self.elements2 = [
            [0,0,0],
            [4,0,6],
            [1,0,0]
        ]
        self.matrix2 = matrix.Matrix(self.elements2)
        self.elements3 = [
            [4,2,6],
            [1,11,5],
            [3,12,9]
        ]
        self.matrix3 = matrix.Matrix(self.elements3)
        self.elements4 = [
            [0,2,6],
            [4,0,0],
            [1,11,5],
            [3,12,9]
        ]
        self.matrix4 = matrix.Matrix(self.elements4)
        self.elements5 = [
            [0,0,0,0,2,6],
            [0,4,0,4,0,0],
            [0,0,0,1,11,5],
            [0,0,0,3,12,9]
        ]
        self.matrix5 = matrix.Matrix(self.elements5)

    def test_get(self):
        self.assertEqual(self.matrix1.get_row(0), self.elements1[0])
        self.assertEqual(self.matrix1.get_col(1), list(map(lambda x: x[1], self.elements1)))

    def test_set_row(self):
        new_row = [1,2,3]
        expected_result = [1,2,3]
        self.matrix1.set_row(0, new_row)
        new_row[0] = 0
        self.assertEqual(self.matrix1.get_row(0), expected_result)

    def test_set_col(self):
        new_col = [1,2]
        expected_result = [1,2]
        self.matrix1.set_col(0, new_col)
        new_col[0] = 0
        self.assertEqual(self.matrix1.get_col(0), expected_result)

    def test_all_elements_zero(self):
        self.assertTrue(self.matrix2.all_elements_zero_in_row(0))
        self.assertTrue(self.matrix2.all_elements_zero_in_row(2,1))
        self.assertTrue(self.matrix2.all_elements_zero_in_col(1))
        self.assertFalse(self.matrix2.all_elements_zero_in_row(1))
        self.assertFalse(self.matrix2.all_elements_zero_in_col(0))

    def test_first_non_zero_element(self):
        non_zero_element = self.matrix2.get_first_non_zero_element_in_col(0)
        self.assertEqual(non_zero_element.index, 1)
        self.assertEqual(non_zero_element.element, 4)
        non_zero_element = self.matrix2.get_first_non_zero_element_in_col(0, 2)
        self.assertEqual(non_zero_element.index, 2)
        self.assertEqual(non_zero_element.element, 1)
        non_zero_element = self.matrix2.get_first_non_zero_element_in_col(1)
        self.assertIsNone(non_zero_element)

    def test_make_element_non_zero(self):
        row = self.matrix2.get_row_with_non_zero_element_row_op(0, 0)
        self.assertEqual(row, self.elements2[1])
        row = self.matrix2.get_row_with_non_zero_element_row_op(1, 0)
        self.assertEqual(row, self.elements2[1])
        self.matrix2.make_element_non_zero_using_row(0, 0)
        self.assertEqual(self.matrix2.get_row(0), self.elements2[1])

    def test_delete_row(self):
        self.matrix2.delete_row(0)
        self.assertEqual(self.matrix2.elements, self.elements2[1:])

    def test_delete_col(self):
        self.matrix2.delete_col(-1)
        self.assertEqual(self.matrix2.elements, [[0,0],[4,0],[1,0]])

    def test_row_echelon_form_1(self):
        expected_result = [
            [1.0, 0.5, 1.5],
            [0.0, 1.0, 0.3333333333],
            [0.0, 0.0, 1.0]
        ]
        for row1, row2 in zip(self.matrix3.row_echelon_form().elements, expected_result):
            for element1, element2 in zip(row1, row2):
                self.assertAlmostEqual(element1, element2)

    def test_row_echelon_form_2(self):
        expected_result = [
            [1.0, 0.5, 1.5],
            [-0.0, 1.0, 3.0],
            [-0.0, -0.0, 1.0],
            [0.0, 0.0, 0.0]
        ]
        for row1, row2 in zip(self.matrix4.row_echelon_form().elements, expected_result):
            for element1, element2 in zip(row1, row2):
                self.assertAlmostEqual(element1, element2)

    def test_row_echelon_form_3(self):
        expected_result = [
            [0.0, 1.0, 0.0, 1.0, 0.5, 1.5],
            [0.0, 0.0, 0.0, 1.0, 9.0, -1.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 3.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        ]
        for row1, row2 in zip(self.matrix5.row_echelon_form().elements, expected_result):
            for element1, element2 in zip(row1, row2):
                self.assertAlmostEqual(element1, element2)


if __name__ == '__main__':
    unittest.main()
