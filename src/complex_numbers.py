

class ComplexNumber(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return str(self.a) + "+" + str(self.b) + "i"

    def __add__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.a+other.a, self.b+other.b)
        else:
            return ComplexNumber(self.a+other, self.b)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.a-other.a, self.b-other.b)
        else:
            return ComplexNumber(self.a-other, self.b)

    def __rsub__(self, other):
        return (ComplexNumber(-self.a, -self.b)).__add__(other)

    def __mul__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.a*other.a-self.b*other.b, self.a*other.b+other.a*self.b)
        else:
            return ComplexNumber(self.a*other, self.b*other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        if isinstance(other, ComplexNumber):
            return self.a == other.a and self.b == other.b
        else:
            return self.a == other and self.b == 0

    def conjugate(self):
        return ComplexNumber(self.a, -self.b)

    def __abs__(self):
        return (self.a**2 + self.b**2)**0.5

    def __div__(self, other):
        if isinstance(other, ComplexNumber):
            return self*other.reciprocal()
        else:
            return ComplexNumber(float(self.a)/other, float(self.b)/other)

    def __rdiv__(self, other):
        return self.reciprocal()*other

    def reciprocal(self):
        assert not (self.a == 0 and self.b == 0)
        denominator = self.a**2+self.b**2
        return ComplexNumber(float(self.a)/denominator, -float(self.b)/denominator)
