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
            s = 0
            for j in range(len(result.x_values)):
                s += result.x_values[j]*A.elements[i][j]
            self.assertLessEqual(round(s,7), b[i])

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
        self.assertAlmostEqual(result.value, 5)
        self.assertAlmostEqual(result.x_values[0]*c[0]+result.x_values[1]*c[1], 5)
        self.assertEqual(result.status, "SUCCESSFUL")
        for i in range(len(b)):
            s = 0
            for j in range(len(result.x_values)):
                s += result.x_values[j]*A.elements[i][j]
            self.assertLessEqual(s, b[i])

    def test_unbounded(self):
        A = matrix.Matrix([
            [-1, 1],
            [1, -2]
        ])
        b = [1, 2]
        c = [2, 1]
        lp = linear_programming.LinearProgramming(c, A, b)
        result = lp.run()
        # self.assertAlmostEqual(result.value, 4)
        # self.assertAlmostEqual(result.x_values[0]*c[0]+result.x_values[1]*c[1], 4)
        self.assertEqual(result.status, "UNBOUNDED")
        # for i in range(len(b)):
        #     self.assertLessEqual(result.x_values[0]*A.elements[i][0]+result.x_values[1]*A.elements[i][1], b[i])

    def test_repr(self):
        primal = """max (-1*x0)+(2*x1)+(-2*x2)
(1*x0)+(1*x1)+(-1*x2) <= 5
(-1*x0)+(-1*x1)+(1*x2) <= -5
x0, x1, x2 >= 0"""
        dual = """min (5*y0)+(-5*y1)
(1*y0)+(-1*y1) >= -1
(1*y0)+(-1*y1) >= 2
(-1*y0)+(1*y1) >= -2
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

    def test_negative_b(self):
        A = matrix.Matrix([
            [-1,0,-1,0,0],
            [-1,0,0,-1,0],
            [-1,-1,0,0,-1],
            [0,-1,0,0,0],
            [0,-1,0,0,0]
        ]).transposed()
        b = [-1,-1,-1,-1,-1]
        c = [-1,-1,-1,-1,-1]
        lp = linear_programming.LinearProgramming(c, A, b)
        result = lp.run()
        self.assertAlmostEqual(result.value, -3)
        s = 0
        for j in range(len(result.x_values)):
            s += result.x_values[j]*c[0]
        self.assertAlmostEqual(s, -3)
        self.assertEqual(result.status, "SUCCESSFUL")
        for i in range(len(b)):
            s = 0
            for j in range(len(result.x_values)):
                s += result.x_values[j]*A.elements[i][j]
            self.assertLessEqual(s, b[i])

    def test_unfeasible(self):
        A = matrix.Matrix([
            [1, 1, 1],
            [-1, -1, 1]
        ])
        b = [-5, -5]
        c = [-1, 2, -2]
        lp = linear_programming.LinearProgramming(c, A, b)
        result = lp.run()
        self.assertEqual(result.status, "UNFEASIBLE")


class WikipediaTestCase(unittest.TestCase):
    def setUp(self):
        self.A1 = matrix.Matrix([
            [3, 2, 1],
            [2, 5, 3]
        ])
        self.b1 = [10, 15]
        self.c1 = [2, 3, 4]
        self.lp1 = linear_programming.LinearProgramming(self.c1, self.A1, self.b1)

    def test_build_phase_one_matrix(self):
        phase_one_matrix = [
            [3, 2, 1, 1, 0, 10, 0],
            [2, 5, 3, 0, 1, 15, 0],
            [2, 3, 4, 0, 0, 0, 0],
            [0, 0, 0, -1, -1, 0, 1]
        ]
        result = self.lp1.build_phase_one_matrix()
        for row1, row2 in zip(phase_one_matrix, result.elements):
            for element1, element2 in zip(row1, row2):
                self.assertAlmostEqual(element1, element2)

    def test_price_out(self):
        expected = [
            [3, 2, 1, 1, 0, 10, 0],
            [2, 5, 3, 0, 1, 15, 0],
            [2, 3, 4, 0, 0, 0, 0],
            [5, 7, 4, 0, 0, 25, 1]
        ]
        result = self.lp1.build_phase_one_matrix()
        self.lp1.price_out(result, [3,4])
        for row1, row2 in zip(expected, result.elements):
            for element1, element2 in zip(row1, row2):
                self.assertAlmostEqual(element1, element2)

    def test(self):
        phase_one_matrix = [
            [1,   1/7, 0,  3/7,  -1/7,   15/7, 0, 0],
            [0,  11/7, 1, -2/7,   3/7,   25/7, 0, 0],
            [0, -25/7, 0,  2/7, -10/7, -130/7, 1, 0],
            [0,     0, 0,   -1,    -1,      0, 0, 1]
        ]
        result = self.lp1.run()
        self.assertAlmostEqual(result.value, 20)
        self.assertAlmostEqual(result.x_values[0]*self.c1[0]+result.x_values[1]*self.c1[1]+result.x_values[2]*self.c1[2], 20)
        self.assertEqual(result.status, "SUCCESSFUL")
        for i in range(len(self.b1)):
            s = 0
            for j in range(len(result.x_values)):
                s += result.x_values[j]*self.A1.elements[i][j]
            self.assertLessEqual(s, self.b1[i])


if __name__ == '__main__':
    unittest.main()
