import linear_programming
import matrix
import unittest


class MyTestCase(unittest.TestCase):
    def test_success(self):
        A = matrix.Matrix([
            [2, -1],
            [1, 2],
            [-1, 2]
        ])
        b = [4, 9, 3]
        c = [2, 5]
        lp = linear_programming.LinearProgramming(c, A, b)
        result = lp.run()
        self.assertAlmostEqual(result.value, 21)
        self.assertAlmostEqual(result.x_values[0]*c[0]+result.x_values[1]*c[1], 21)
        self.assertEqual(result.status, "SUCCESSFUL")
        for i in range(len(b)):
            self.assertLessEqual(round(result.x_values[0]*A.elements[i][0]+result.x_values[1]*A.elements[i][1], 7), b[i])

    def test_degenerate(self):
        A = matrix.Matrix([
            [3, 1],
            [1, -1],
            [0, 1]
        ])
        b = [6, 2, 3]
        c = [2, 1]
        lp = linear_programming.LinearProgramming(c, A, b)
        result = lp.run()
        self.assertAlmostEqual(result.value, 4)
        self.assertAlmostEqual(result.x_values[0]*c[0]+result.x_values[1]*c[1], 4)
        self.assertEqual(result.status, "SUCCESSFUL")
        for i in range(len(b)):
            self.assertLessEqual(result.x_values[0]*A.elements[i][0]+result.x_values[1]*A.elements[i][1], b[i])

    def test_unbounded(self):
        A = matrix.Matrix([
            [-1, 1],
            [1, -2]
        ])
        b = [1, 2]
        c = [2, 1]
        lp = linear_programming.LinearProgramming(c, A, b)
        result = lp.run()
        self.assertAlmostEqual(result.value, 4)
        self.assertAlmostEqual(result.x_values[0]*c[0]+result.x_values[1]*c[1], 4)
        self.assertEqual(result.status, "UNBOUNDED")
        for i in range(len(b)):
            self.assertLessEqual(result.x_values[0]*A.elements[i][0]+result.x_values[1]*A.elements[i][1], b[i])


if __name__ == '__main__':
    unittest.main()
