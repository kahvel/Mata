

class Solver(object):
    def __init__(self, derivative, initial_x, initial_y, delta_x, steps):
        self.derivative = derivative
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.delta_x = delta_x  # h
        self.matrix = None  # a
        self.weights = None  # b
        self.nodes = None  # c
        self.steps = steps

    def k(self, stage, x, y):
        if stage == 1:
            return self.derivative(x, y)
        else:
            delta_multiplier = sum(map(lambda a: a[1]*self.k(a[0]+1, x, y), enumerate(self.matrix[stage-1][:-1])))
            return self.derivative(x+self.nodes[stage-1]*self.delta_x, y+self.delta_x*delta_multiplier)

    def run(self):
        y_values = [self.initial_y]
        x_values = [self.initial_x]
        y = self.initial_y
        x = self.initial_x
        for i in range(self.steps):
            y += self.delta_x*sum(self.weights[j]*self.k(j+1, x, y) for j in range(len(self.weights)))
            x += self.delta_x
            y_values.append(y)
            x_values.append(x)
        return x_values, y_values


class EulerMethod(Solver):
    def __init__(self, derivative, initial_x, initial_y, delta_x, steps):
        Solver.__init__(self, derivative, initial_x, initial_y, delta_x, steps)
        self.matrix = [[0]]
        self.weights = [1]
        self.nodes = [0]

    def simple_run(self):
        y_values = [self.initial_y]
        x_values = [self.initial_x]
        y = self.initial_y
        x = self.initial_x
        for i in range(self.steps):
            y += self.delta_x*self.derivative(x, y)
            x += self.delta_x
            y_values.append(y)
            x_values.append(x)
        return x_values, y_values


class RungeKuttaFourth(Solver):
    def __init__(self, derivative, initial_x, initial_y, delta_x, steps):
        Solver.__init__(self, derivative, initial_x, initial_y, delta_x, steps)
        self.matrix = [[0], [0.5, 0], [0, 0.5, 0], [0, 0, 1, 0]]
        self.weights = [1.0/6, 1.0/3, 1.0/3, 1.0/6]
        self.nodes = [0, 0.5, 0.5, 1]

    def simple_run(self):
        y_values = [self.initial_y]
        x_values = [self.initial_x]
        y = self.initial_y
        x = self.initial_x
        for i in range(self.steps):
            k1 = self.derivative(x, y)
            k2 = self.derivative(x+self.delta_x/2.0, y+self.delta_x/2.0*k1)
            k3 = self.derivative(x+self.delta_x/2.0, y+self.delta_x/2.0*k2)
            k4 = self.derivative(x+self.delta_x, y+self.delta_x*k3)
            y += self.delta_x/6.0*(k1+2*k2+2*k3+k4)
            x += self.delta_x
            y_values.append(y)
            x_values.append(x)
        return x_values, y_values


class RungeKuttaFourth38(Solver):
    def __init__(self, derivative, initial_x, initial_y, delta_x, steps):
        Solver.__init__(self, derivative, initial_x, initial_y, delta_x, steps)
        self.matrix = [[0], [1.0/3, 0], [-1.0/3, 1, 0], [1, -1, 1, 0]]
        self.weights = [1.0/8, 3.0/8, 3.0/8, 1.0/8]
        self.nodes = [0, 1.0/3, 2.0/3, 1]


class Midpoint(Solver):
    def __init__(self, derivative, initial_x, initial_y, delta_x, steps, alpha=0.5):
        Solver.__init__(self, derivative, initial_x, initial_y, delta_x, steps)
        self.matrix = [[0], [alpha, 0]]
        self.weights = [(1-1.0/(2*alpha)), 1/(2*alpha)]
        self.nodes = [0, alpha]


class Heun(Midpoint):
    def __init__(self, derivative, initial_x, initial_y, delta_x, steps):
        Midpoint.__init__(self, derivative, initial_x, initial_y, delta_x, steps, alpha=1.0)


class Ralston(Midpoint):
    def __init__(self, derivative, initial_x, initial_y, delta_x, steps):
        Midpoint.__init__(self, derivative, initial_x, initial_y, delta_x, steps, alpha=2.0/3)


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    euler_method = EulerMethod(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
    euler_result = euler_method.run()

    runge_kutta_fourth = RungeKuttaFourth(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
    runge_kutta_result = runge_kutta_fourth.run()

    runge_kutta_fourth_38 = RungeKuttaFourth38(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
    runge_kutta_38_result =  runge_kutta_fourth_38.run()

    midpoint = Midpoint(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
    midpoint_result = midpoint.run()

    heun = Heun(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
    heun_result = heun.run()

    ralston = Ralston(lambda x, y: 1+x**2+y**2, 1, 0, 0.1, 9)
    ralston_result = ralston.run()

    n_digits = 3
    print "x                  ", map(lambda x: round(x, 1), euler_result[0])
    print "y"
    print "Euler method       ", map(lambda x: round(x, n_digits), euler_result[1])
    print "Runge-Kutta 4th    ", map(lambda x: round(x, n_digits), runge_kutta_result[1])
    print "Runge-Kutta 4th 3/8", map(lambda x: round(x, n_digits), runge_kutta_38_result[1])
    print "Midpoint           ", map(lambda x: round(x, n_digits), midpoint_result[1])
    print "Heun               ", map(lambda x: round(x, n_digits), heun_result[1])
    print "Ralston            ", map(lambda x: round(x, n_digits), ralston_result[1])

    plt.plot(euler_result[0], euler_result[1], label="Euler")
    plt.plot(runge_kutta_result[0], runge_kutta_result[1], label="Runge-Kutta 4th")
    # plt.plot(runge_kutta_38_result[0], runge_kutta_38_result[1])
    plt.plot(midpoint_result[0], midpoint_result[1], label="Midpoint")
    plt.plot(heun_result[0], heun_result[1], label="Heun")
    plt.plot(ralston_result[0], ralston_result[1], label="Ralston")
    plt.legend(loc=2)
    # plt.savefig("vordlus.png")
    plt.show()


