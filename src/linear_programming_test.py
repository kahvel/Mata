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

    def test_repr(self):
        primal = """max (-1*x0)+(2*x1)+(-2*x2)
(1*x0)+(1*x1)+(-1*x2) <= 5
(-1*x0)+(-1*x1)+(1*x2) <= -5
x0, x1, x2 >= 0"""
        dual = """min (5*y0)+(-5*y1)
(1*y0)+(-1*y1) <= -1
(1*y0)+(-1*y1) <= 2
(-1*y0)+(1*y1) <= -2
y0, y1 >= 0"""
        A = matrix.Matrix([
            [1, 1, -1],
            [-1, -1, 1]
        ])
        b = [5, -5]
        c = [-1, 2, -2]
        lp = linear_programming.LinearProgramming(c, A, b)
        self.assertEqual(str(lp), primal)
        self.assertEqual(lp.dual(), dual)


if __name__ == '__main__':
    unittest.main()
