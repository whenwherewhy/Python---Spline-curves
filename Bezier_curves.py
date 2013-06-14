from collections import deque


class BezierCurves:
    RANGE_STEP = 1000

    def __init__(self, degree):
        self._degree = degree
        self.control_points = []
        self.curve = []
        self.derivative_control_points = []
        self.derivative = dict()
        self.subdivision_left = dict()
        self.subdivision_right = dict()

    def append_point(self, point):
        if len(self.control_points) == self._degree + 1:
            raise IndexError

        self.control_points.append(point)

    def deCasteljau_algorithm(self, param, points):
        algr_step = []
        algr_step.append([point for point in points])
        degree = len(points)
        subdiv_last = []
        self.subdivision_left[param] = []
        self.subdivision_right[param] = deque()

        for step in range(1, degree):
            algr_step.append([(1 - param) * algr_step[step - 1][point] +
                             param * algr_step[step - 1][point + 1]
                             for point in range(len(algr_step[step - 1]) - 1)])

            self.subdivision_left[param].append(algr_step[step - 1][0])
            self.subdivision_right[param].appendleft(algr_step[step - 1]
                                                              [degree - step])

        algorithm_result = algr_step[degree - 1][0]
        self.subdivision_left[param].append(algorithm_result)
        self.subdivision_right[param].appendleft(algorithm_result)

        return algorithm_result

    def finite_difference(self, degree):
        algr_step = []
        algr_step.append([point for point in self.control_points])
        for step in range(1, degree + 1):
            algr_step.append([algr_step[step - 1][point + 1] -
                             algr_step[step - 1][point]
                             for point in range(len(algr_step[step - 1]) - 1)])

        return algr_step[degree]

    def _curve_calculation(self, control_points, derivative=None):
        key = self._degree - len(control_points) + 1
        self.derivative[key] = []

        for t in range(self.RANGE_STEP + 1):
            parameter = t / self.RANGE_STEP
            if derivative:
                self.derivative[key].append(self.deCasteljau_algorithm(
                                            parameter,
                                            control_points))
            else:
                self.curve.append(self.deCasteljau_algorithm(parameter,
                                  control_points))

    def _derivative_calculation(self, degree):
        derivative_control_points = self.finite_difference(degree)
        self._curve_calculation(derivative_control_points, True)

    def degree_elevation(self):
        elevation = []
        elevation.append(self.control_points[0])

        for i in range(1, self._degree):
            point = ((i * self.control_points[i - 1] + (self._degree + 1 - i) *
                     self.control_points[i]) * (1 / (self._degree + 1)))
            elevation.append(point)

        elevation.append(self.control_points[self._degree])

        return elevation

    def draw_curve(self):
        self._curve_calculation(self.control_points)
        return self.curve

    def draw_derivative(self):
        self._derivative_calculation(self.derivative_control_points, True)
        return self.derivative
