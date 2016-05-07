import complex_numbers
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.c1 = complex_numbers.ComplexNumber(4, 5)
        self.c2 = complex_numbers.ComplexNumber(4, 5)

    def test_add(self):
        self.assertEqual(self.c1 + self.c2, complex_numbers.ComplexNumber(8, 10))
        self.assertEqual(self.c1 + 1, complex_numbers.ComplexNumber(5, 5))
        self.assertEqual(1 + self.c1, complex_numbers.ComplexNumber(5, 5))

    def test_sub(self):
        self.assertEqual(self.c1 - self.c2, complex_numbers.ComplexNumber(0, 0))
        self.assertEqual(self.c1 - 1, complex_numbers.ComplexNumber(3, 5))
        self.assertEqual(1 - self.c1, complex_numbers.ComplexNumber(-3, -5))

    def test_mul(self):
        self.assertEqual(self.c1 * self.c2, complex_numbers.ComplexNumber(-9, 40))
        self.assertEqual(self.c1 * 3, complex_numbers.ComplexNumber(12, 15))
        self.assertEqual(4 * self.c1, complex_numbers.ComplexNumber(16, 20))

    def test_div(self):
        self.assertEqual(self.c1 / self.c2, complex_numbers.ComplexNumber(1, 0))
        self.assertEqual(self.c1 / 5, complex_numbers.ComplexNumber(0.8, 1))
        self.assertEqual(5 / self.c1, complex_numbers.ComplexNumber(20.0/41, -25.0/41))
    
    def test_reciprocal(self):
        self.assertEqual(self.c1.reciprocal(), complex_numbers.ComplexNumber(4.0/41, -5.0/41))

if __name__ == '__main__':
    unittest.main()
