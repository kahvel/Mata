import differential_equations
import unittest


class MyTestCase(unittest.TestCase):
    def test_euler_method(self):
        expected_result = ([0, 0.5, 1.0, 1.5], [1, 1.5, 2.25, 3.375])
        euler_method = differential_equations.EulerMethod(lambda x, y: y, 0, 1, 0.5, 3)
        self.assertAlmostEqual(euler_method.run(), expected_result)
        self.assertAlmostEqual(euler_method.simple_run(), expected_result)

    def test_runge_kutta_fourth(self):
        expected_result = ([0, 0.5, 1.0, 1.5], [1, 1.6484375, 2.71734619140625, 4.47937536239624])
        runge_kutta = differential_equations.RungeKuttaFourth(lambda x, y: y, 0, 1, 0.5, 3)
        self.assertAlmostEqual(runge_kutta.run(), expected_result)
        self.assertAlmostEqual(runge_kutta.simple_run(), expected_result)

    def test_runge_kutta_fourth38(self):
        expected_result = ([0, 0.5, 1.0, 1.5], [1.0, 1.6484375, 2.71734619140625, 4.47937536239624])
        runge_kutta = differential_equations.RungeKuttaFourth38(lambda x, y: y, 0, 1, 0.5, 3)
        self.assertEqual(map(lambda x: round(x, 16), runge_kutta.run()[1]), expected_result[1])

    def test_midpoint(self):
        expected_result = ([0, 0.5, 1.0, 1.5], [1, 1.625, 2.640625, 4.291015625])
        midpoint = differential_equations.Midpoint(lambda x, y: y, 0, 1, 0.5, 3)
        self.assertAlmostEqual(midpoint.run(), expected_result)

    def test_heun(self):
        expected_result = ([0, 0.5, 1.0, 1.5], [1, 1.625, 2.640625, 4.291015625])
        heun = differential_equations.Heun(lambda x, y: y, 0, 1, 0.5, 3)
        self.assertAlmostEqual(heun.run(), expected_result)

    def test_ralston(self):
        expected_result = ([0, 0.5, 1.0, 1.5], [1, 1.625, 2.640625, 4.291015625])
        ralston = differential_equations.Ralston(lambda x, y: y, 0, 1, 0.5, 3)
        self.assertAlmostEqual(ralston.run(), expected_result)

    def test_runge_kutta_fourth_2(self):
        runge_kutta_fourth = differential_equations.RungeKuttaFourth(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
        runge_kutta_result = runge_kutta_fourth.run()
        runge_kutta_result_simple = runge_kutta_fourth.simple_run()
        self.assertEqual(map(lambda x: round(x, 7), runge_kutta_result[1]), map(lambda x: round(x, 7), runge_kutta_result_simple[1]))

    def test_euler_method_2(self):
        runge_kutta_fourth = differential_equations.EulerMethod(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
        runge_kutta_result = runge_kutta_fourth.run()
        runge_kutta_result_simple = runge_kutta_fourth.simple_run()
        self.assertAlmostEqual(runge_kutta_result, runge_kutta_result_simple)


if __name__ == '__main__':
    unittest.main()
