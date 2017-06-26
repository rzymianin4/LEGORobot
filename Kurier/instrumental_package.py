import math
import time
from ev3.ev3dev import Key
from ev3.ev3dev import Lcd
from PIL import ImageFont
from angle import angle

global key
key = Key()
global lcd
lcd = Lcd()
global fi
fi = math.pi/2.25
global BEFORE
BEFORE = 32.0


from math import pi

"""class angle(object):
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
"""

def count_right():
    lcd.reset()
    n = 0
    pressed = False
    time.sleep(0.1)
    while True:
        # time.sleep(0.1)
        if key.right:
            if not pressed:
                n += 1
                pressed = True
        else:
            pressed = False
        if key.enter:
            return n

def display(pos1, pos2=['', ''], pos3=['', '']):
    font = ImageFont.load_default()
    lcd.reset()
    lcd.update()
    lcd.draw.text((10, 10), str(pos1), font=font)
    lcd.draw.text((10, 20), str(pos2), font=font)
    lcd.draw.text((10, 30), str(pos3), font=font)
    lcd.update()

def field_to_cm(pos):
    """pos_cm is a LIST,
        return cm coordinates of field """
    return [pos[0]*32+15.0, pos[1]*32+15.0]

def count_rad(point1, point2):
    """return angle(in radians) form OX to (point1, point2)
        return values from (-pi, pi>"""
    del_x = point2[0]-point1[0]
    del_y = point2[1]-point1[1]
    return angle(math.atan2(del_y, del_x))

def target(point, ang, dist):
    return [point[0] + dist*math.cos(ang), point[1] + dist*math.sin(ang)]

def nearest_field_cm(pos):
    x = pos[0]
    y = pos[1]
    x -= x%32 - 15
    y -= y%32 - 15
    return [x, y]

def count_cm(point1, point2):
    return math.hypot(point2[0]-point1[0], point2[1]-point1[1])

def scenario(permutacja):
    X1 = permutacja[0]
    X2 = permutacja[1]
    X3 = permutacja[2]
    P1 = 'P' + str(X1)
    P2 = 'P' + str(X2)
    P3 = 'P' + str(X3)
    A1 = 'A' + str(X1)
    A2 = 'A' + str(X2)
    A3 = 'A' + str(X3)
    s1 = [P1, A1, P2, P3, A3, A2]
    s2 = [P1, A1, P2, A2, P3, A3]
    s3 = [P1, P2, A2, A1, P3, A3]
    s4 = [P1, P2, P3, A3, A2, A1]
    s5 = [P1, P2, A2, P3, A3, A1]
    return [s1, s2, s3, s4, s5]
