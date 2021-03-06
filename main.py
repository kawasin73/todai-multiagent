import random
import math
import copy
import time
import functools
import matplotlib.pyplot as plt


# Particle Swarm Optimization
class PSOCalc:
    NAME = "Particle Swarm Optimization Algorithm"

    def __init__(self, dimension, w=1.0, c1=1.0, c2=1.0):
        self.dimension = dimension
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def initialize(self, func, n):
        self.func = func
        self.samples = [
            self.Individual(
                self.func,
                self.dimension,
                self.w, self.c1, self.c2
            )
            for _ in range(n)
        ]
        self.best_value = math.inf
        self.best_point = [0] * self.dimension

    def next_step(self):
        for sample in self.samples:
            v = sample.current_value()
            if v < self.best_value:
                self.best_value = v
                self.best_point = sample.point

        for sample in self.samples:
            sample.next_step(self.best_point)

    def best_set(self):
        return (self.best_value, self.best_point)

    class Individual:
        def __init__(self, func, dimension, w, c1, c2):
            self.func = func
            self.point = func.initial_value(dimension)
            self.velocity = [0] * len(self.point)

            self.w = w
            self.c1 = c1
            self.c2 = c2
            self.best_point = self.point
            self.best_value = math.inf

        def current_value(self):
            value = self.func.call(self.point)
            if value < self.best_value:
                self.best_value = value
                self.best_point = self.point
            return value

        def next_step(self, global_best_point):
            r1 = random.random()
            r2 = random.random()
            self.velocity = [
                self.w * v + self.c1 * r1 * (b - x) + self.c2 * r2 * (g - x)
                for v, x, b, g in zip(self.velocity, self.point, self.best_point, global_best_point)
            ]
            self.point = [
                self.func.check_range(x + v)
                for v, x in zip(self.velocity, self.point)
            ]


# Artificial Bee Colony Algorithm
# URL: https://www.jstage.jst.go.jp/article/iscie/24/4/24_4_97/_pdf
class ABCCalc:
    NAME = "Artificial Bee Colony Algorithm"

    def __init__(self, dimension, trial_limit=10):
        self.dimension = dimension
        self.trial_limit = trial_limit

    def initialize(self, func, n):
        self.func = func
        self.n = n
        self.samples = [
            func.initial_value(self.dimension)
            for _ in range(n)
        ]
        self.trial_counter = [0] * n
        self.values = [func.call(v) for v in self.samples]
        self.fits = [self._fit(v) for v in self.values]

    def next_step(self):
        self._employed_bees()
        self._onlooker_bees()
        self._scout_bees()

    def best_set(self):
        min_idx = min(zip(self.values, range(self.n)))[1]
        return self.values[min_idx], self.samples[min_idx]

    def _fit(self, v):
        try:
            return math.exp(-v)
        except OverflowError:
            return 0

    def _employed_bees(self):
        next_samples = copy.copy(self.samples)
        for i, sample in enumerate(self.samples):
            idx = random.randrange(0, self.n - 1)
            if idx >= i:
                # not select self
                idx += 1
            x = self.samples[idx]
            j = random.randrange(0, self.dimension)
            new_sample = copy.copy(sample)
            new_sample[j] = self.func.check_range(sample[j] + random.uniform(-1, 1) * (sample[j] - x[j]))
            v = self.func.call(new_sample)
            if v < self.values[i]:
                next_samples[i] = new_sample
                self.trial_counter[i] = 0
                self.values[i] = v
                self.fits[i] = self._fit(v)
            else:
                self.trial_counter[i] += 1
        self.samples = next_samples

    def _onlooker_bees(self):
        next_samples = copy.copy(self.samples)
        next_fits = copy.copy(self.fits)
        for i, sample in enumerate(self.samples):
            x = random.choices(self.samples, self.fits)[0]
            j = random.randrange(0, self.dimension)
            new_sample = copy.copy(sample)
            new_sample[j] = self.func.check_range(sample[j] + random.uniform(-1, 1) * (sample[j] - x[j]))
            v = self.func.call(new_sample)
            if v < self.values[i]:
                next_samples[i] = new_sample
                self.trial_counter[i] = 0
                self.values[i] = v
                next_fits[i] = self._fit(v)
            else:
                self.trial_counter[i] += 1
        self.samples = next_samples
        self.fits = next_fits

    def _scout_bees(self):
        for i in range(self.n):
            if self.trial_counter[i] >= self.trial_limit:
                self.samples[i] = self.func.initial_value(self.dimension)
                self.values[i] = self.func.call(self.samples[i])
                self.fits[i] = self._fit(self.values[i])
                self.trial_counter[i] = 0


class Function:
    NAME = "invalid function"
    MAX = 0
    MIN = 0

    def initial_value(self, dimension):
        return [random.uniform(self.MIN, self.MAX) for _ in range(dimension)]

    def check_range(self, v):
        if v > self.MAX:
            return v
        elif v < self.MIN:
            return v
        else:
            return v

    def call(self, sample):
        raise NotImplementedError("unimplemented Function call")


class SphereFunction(Function):
    NAME = "SphereFunction"
    MAX = 5.0
    MIN = -5.0

    def call(self, x):
        return sum([v * v for v in x])


class RastriginFunction(Function):
    NAME = "RastriginFunction"
    MAX = 5.0
    MIN = -5.0

    def call(self, x):
        return 10 * len(x) + sum([(v * v) - (10 * math.cos(2 * math.pi * v)) for v in x])


class RosenbrockFunction(Function):
    NAME = "RosenbrockFunction"
    MAX = 10.0
    MIN = -5.0

    def call(self, x):
        result = 0.0
        for i in range(len(x) - 1):
            v1 = (x[i + 1] - x[i] * x[i])
            v2 = (1.0 - x[i])
            result += (100 * v1 * v1 + v2 * v2)
        return result


class GriewankFunction(Function):
    NAME = "GriewankFunction"
    MAX = 600.0
    MIN = -600.0

    def call(self, x):
        return 1.0 + sum([v * v for v in x]) / 4000.0 - functools.reduce(
            lambda v, y: v * y,
            [math.cos(xi / math.sqrt(i + 1.0)) for i, xi in enumerate(x)]
        )


class AlpineFunction(Function):
    NAME = "AlpineFunction"
    MAX = 10.0
    MIN = -10.0

    def call(self, x):
        return sum([math.fabs(v * math.sin(v) + 0.1 * v) for v in x])


class TwoNMinimaFunction(Function):
    NAME = "2n MinimaFunction"
    MAX = 5.0
    MIN = -5.0

    def call(self, x):
        return sum([math.pow(v, 4) - 16.0 * math.pow(v, 2) + 5 * v for v in x])


class Executer:
    DIMENSION = 10
    SAMPLES = 500
    STEPS = 5000

    CALCS = [
        PSOCalc(DIMENSION, w=0.3, c1=0.3, c2=0.4),
        ABCCalc(DIMENSION, trial_limit=10),
    ]
    FUNCS = [
        SphereFunction(),
        RastriginFunction(),
        RosenbrockFunction(),
        GriewankFunction(),
        AlpineFunction(),
        TwoNMinimaFunction(),
    ]

    def exec(self):
        for calc in self.CALCS:
            for func in self.FUNCS:
                self._exec(calc, func)

    def _exec(self, calc, func):
        logs = []
        start = time.time()
        calc.initialize(func, self.SAMPLES)
        for i in range(self.STEPS):
            calc.next_step()
            if i % 100 == 0:
                value, _ = calc.best_set()
                logs.append([i, value])
        end = time.time()
        value, point = calc.best_set()
        logs.append([self.STEPS, value])

        print(calc.NAME, '[', func.NAME, ']')
        print(value, point)
        print("time {0} sec".format(end - start))
        print('')
        self._save_image(logs, calc.NAME, func.NAME, value)

    def _save_image(self, logs, calc_name, func_name, value):
        idx, values = list(zip(*logs))
        plt.plot(idx, values)
        plt.xlabel('steps')
        if value > 0:
            plt.yscale('log')
        plt.grid(which='both')
        plt.suptitle(calc_name + ' + ' + func_name)
        plt.savefig(calc_name + '_' + func_name + '.png')
        plt.clf()


if __name__ == '__main__':
    e = Executer()
    e.exec()
