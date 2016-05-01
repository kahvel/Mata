

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
            delta_multiplier = sum(map(lambda a: a*self.k(stage-1, x, y), self.matrix[stage-1]))
            return self.derivative(x*self.nodes[stage-1]*self.delta_x, y+self.delta_x*delta_multiplier)

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


euler_method = EulerMethod(lambda x, y: y, 0, 1, 0.5, 3)
print euler_method.run()
print euler_method.simple_run()

runge_kutta_fourth = RungeKuttaFourth(lambda x, y: y, 0, 1, 0.5, 3)
print runge_kutta_fourth.run()
print runge_kutta_fourth.simple_run()

runge_kutta_fourth_38 = RungeKuttaFourth38(lambda x, y: y, 0, 1, 0.5, 3)
print runge_kutta_fourth_38.run()

midpoint = Midpoint(lambda x, y: y, 0, 1, 0.5, 3)
print midpoint.run()

heun = Heun(lambda x, y: y, 0, 1, 0.5, 3)
print heun.run()

ralston = Ralston(lambda x, y: y, 0, 1, 0.5, 3)
print ralston.run()


