from math import pi

class angle(object):
    def __init__(self, number):
        self.value = float(number)
        self.calibrate()

    def calibrate(self):
        if self.value >= pi:
            self.value = self.value - 2*pi
            self.calibrate()
        if self.value < -pi:
            self.value = self.value + 2*pi
            self.calibrate()

    def __float__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __invert__(self):
        self += pi
        return self

    def __abs__(self):
        return abs(self.value)

    def __cmp__(self, other):
        return cmp(float(self), float(other))

    def __iadd__(self, number):
        self.value = self.value + number
        self.calibrate()
        return self

    def __isub__(self, number):
        self.value = self.value - number
        self.calibrate()
        return self

    def __imul__(self, number):
        self.value = self.value * number
        self.calibrate()
        return self

    def __idiv__(self, number):
        self.value = self.value / number
        self.calibrate()
        return self

    def __add__(self, other):
        self.value = float(self) + float(other)
        self.calibrate()
        return self

    def __sub__(self, other):
        self.value = float(self) - float(other)
        self.calibrate()
        return self

    def __mul__(self, other):
        self.value = float(self) * float(other)
        self.calibrate()
        return self

    def __div__(self, other):
        self.value = float(self) / float(other)
        self.calibrate()
        return self
