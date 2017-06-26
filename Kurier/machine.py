# -*- coding: utf-8 -*-
import time
import signal
import random
import sys
import os

from math import radians, pi, degrees


from ev3.lego import GyroSensor
from ev3.lego import ColorSensor
from ev3.lego import UltrasonicSensor
from ev3.lego import InfraredSensor
from ev3.lego import LargeMotor as LMotor
from ev3.lego import MediumMotor as MMotor
from ev3.ev3dev import LED
from ev3.ev3dev import Tone
from ev3.ev3dev import Key
from ev3.ev3dev import Lcd
from ev3.ev3dev import NoSuchSensorError
from ev3.ev3dev import NoSuchMotorError



def say(text='Nie mam nic do powiedzenia', lang='pl', speed=120):
    """run espeak -s speed -a 200 -g 1 -v lang text --stdout | aplay"""
    os.system('espeak -s ' + str(speed) + ' -a 200 -g 1 -v ' +
              str(lang) + ' "' + str(text) + '" --stdout | aplay')


class Machine(object):

    def __init__(self):
        self.key = Key()
        self.led = LED()
        self.lcd = Lcd()
        self.tone = Tone()
        self.speed = 600                 # speed. 900 is max
        self.slow = 300
        self.turn_speed = 600
        self.turn_slow = 200
        self.loader_speed = 1000
        # self.turn_callibrate = 260
        # self.half_turn_callibrate = 300
        # self.neg_half_turn_callibrate = 300
        self.dist_callibrate = 20
        self.dyspersion = [1,1]  # [0.99, 0.99]   # difference between motor speeds for running [0] front, [1] back

        try:
            self.R = LMotor(port=LMotor.PORT.B)    # Rigth motor
            self.L = LMotor(port=LMotor.PORT.D)    # Left motor
            self.C = MMotor(port=MMotor.PORT.A)  # Central motor

        except NoSuchMotorError:
            self.led.left.color = LED.COLOR.RED
            say("Brak silnika")

        try:
            self.gyro = GyroSensor()
            self.gyro.ang_and_rate
        except NoSuchSensorError:
            self.led.left.color = LED.COLOR.RED
            say("Brak żyrosensora", speed=200)
        try:
            self.color = ColorSensor()
        except NoSuchSensorError:
            self.led.left.color = LED.COLOR.RED
            say("Brak sensora koloru", speed=200)
        self.sonar = None
        try:
            self.ir = InfraredSensor()
            self.ir.mode = "IR-REMOTE"
        except:
            self.L.left.color = LED.COLOR.RED
            say("Brak sensora podczerwieni", speed=200)

        self.R.reset()
        self.L.reset()
        self.C.reset()
        self.R.stop_mode = 'coast' 
        self.L.stop_mode = 'coast'
        self.C.stop_mode = 'coast'
        self.R.ramp_up_sp = 1000
        self.L.ramp_up_sp = 1000
        self.R.regulation_mode = True
        self.L.regulation_mode = True
        self.C.regulation_mode = True
        self.R.position_mode = 'relative'
        self.L.position_mode = 'relative'
        self.C.position_mode = 'absolute'
        self.led.left.color = LED.COLOR.GREEN
        self.led.right.color = LED.COLOR.GREEN
        signal.signal(signal.SIGINT, self.sigint_handler)
        # sets handler for keyboard interrupt( CTRL + C)

    def run(self, speed1=600, speed2=600):
        """run forever R and L with given speed (600 dafault, 900 max)
            non time-blocking"""
        self.R.run_forever(speed1)
        self.L.run_forever(speed2)

    def sigint_handler(self, *args):    # define interrupt handler
        self.shutdown()

    def stop(self):
        """stop all motors"""
        self.R.stop()
        self.L.stop()
        self.C.stop()

    def start(self):
        """set left led to green"""
        self.led.left.color = LED.COLOR.GREEN
        self.led.left.on()
        # self.run()

    def shutdown(self):
        """stop, change motor stop mode,
        play sound, set leds to green etc."""
        self.stop()
        self.R.stop_mode = 'coast'     # free motor
        self.L.stop_mode = 'coast'     # free motor
        self.C.stop_mode = 'coast'
        self.led.left.color = LED.COLOR.AMBER
        self.led.left.on()
        self.tone.play(440)
        time.sleep(0.1)
        self.led.left.color = LED.COLOR.GREEN
        self.led.left.on()
        self.tone.stop()
        sys.exit(0)

    @property
    def still(self):
        """return True if R and L are stopped"""
        return (self.R.pulses_per_second == 0) and (self.L.pulses_per_second == 0)

    def turn_right(self):
        """turn right forever
            non time-blocking"""
        self.L.run_forever(self.turn_speed, stop_mode=LMotor.STOP_MODE.HOLD)
        self.R.run_forever(-self.turn_speed, stop_mode=LMotor.STOP_MODE.HOLD)

    def turn_left(self):
        """turn left forever
            non time-blocking"""
        self.L.run_forever(-self.turn_speed, stop_mode=LMotor.STOP_MODE.HOLD)
        self.R.run_forever(self.turn_speed, stop_mode=LMotor.STOP_MODE.HOLD)

    def turn_deg(self, value):
        """turn given angle (in degrees)
            non time-blocking"""
        starting = self.gyro.ang
        if value > 0:
            self.turn_right()
            value -= 10
            while True:
                if self.gyro.ang - starting >= value:
                    self.stop()
                    return
        else:
            self.turn_left()
            value += 10
            while True:
                if self.gyro.ang - starting <= value:
                    self.stop()
                    return
    def turn_rad(self, value):
        self.turn_deg(degrees(value))

    def slow_right(self):
        """turn right forever
            non time-blocking"""
        self.L.run_forever(self.turn_slow, stop_mode=LMotor.STOP_MODE.HOLD)
        self.R.run_forever(-self.turn_slow, stop_mode=LMotor.STOP_MODE.HOLD)

    def slow_left(self):
        """turn left forever
            non time-blocking"""
        self.L.run_forever(-self.turn_slow, stop_mode=LMotor.STOP_MODE.HOLD)
        self.R.run_forever(self.turn_slow, stop_mode=LMotor.STOP_MODE.HOLD)

    def turn_deg_slow(self, value):
        """turn given angle (in degrees)
            non time-blocking"""
        starting = self.gyro.ang
        if value > 0:
            self.slow_right()
            value -= 3
            while True:
                if self.gyro.ang - starting >= value:
                    self.stop()
                    return
        else:
            self.slow_left()
            value += 3
            while True:
                if self.gyro.ang - starting <= value:
                    self.stop()
                    return

    def turn_rad_slow(self, value):
        self.turn_deg_slow(degrees(value))

    def run_dist_cm(self, value=1, callibrate=None):
        """run R value*callibrate and L value*callibrate
            none time-blocking"""
        if callibrate is None:
            callibrate = self.dist_callibrate
        # self.R.run_position_limited(callibrate*value, speed_sp=speed * self.dyspersion[value < 0], stop_mode=LMotor.STOP_MODE.COAST)
        # self.L.run_position_limited(callibrate*value, speed_sp=speed, stop_mode=LMotor.STOP_MODE.COAST)
        if value > 0:
            self.R.run_time_limited(1000*value/callibrate, speed_sp=self.speed*self.dyspersion[0], stop_mode=LMotor.STOP_MODE.COAST)
            self.L.run_time_limited(1000*value/callibrate, speed_sp=self.speed, stop_mode=LMotor.STOP_MODE.COAST)
        else:
            self.R.run_time_limited(-1000*value/callibrate, speed_sp=-self.speed*self.dyspersion[1], stop_mode=LMotor.STOP_MODE.COAST)
            self.L.run_time_limited(-1000*value/callibrate, speed_sp=-self.speed, stop_mode=LMotor.STOP_MODE.COAST)

    def run_slow(self, value=1, dyspersion=[0.97,0.98]):
        if value > 0:
            self.R.run_time_limited(1000*value/10.0, speed_sp=self.slow*dyspersion[0], stop_mode=LMotor.STOP_MODE.COAST)
            self.L.run_time_limited(1000*value/10.0, speed_sp=self.slow, stop_mode=LMotor.STOP_MODE.COAST)
        else:
            self.R.run_time_limited(-1000*value/10.0, speed_sp=-self.slow*dyspersion[1], stop_mode=LMotor.STOP_MODE.COAST)
            self.L.run_time_limited(-1000*value/10.0, speed_sp=-self.slow, stop_mode=LMotor.STOP_MODE.COAST)

    def left_dist(self):
        """return tuple containing how many steps A and L still have to go"""
        return (self.R.position - self.R.position_sp,
                self.L.position - self.L.position_sp)

    def set_speed(self, val=600):
        """set self.speed (max 900) to val"""
        if val > 900:
            print 'Can\'t go so fast!'
            val = 900
        self.speed = val

    def load(self, steps=20):
        """load brick
            non time-blocking"""
        self.C.run_time_limited(100*steps, self.loader_speed, stop_mode=MMotor.STOP_MODE.COAST)
        # time.sleep(steps/10.0)
        # self.C.run_position_limited(self.C.position + 3*360 - self.C.position % (360*3),
        #                        self.loader_speed, stop_mode=MMotor.STOP_MODE.HOLD)

    def unload(self, steps=5):
        """unload brick
            TIME-BLOCKING"""
        self.C.run_time_limited(100*steps, -self.loader_speed, stop_mode=MMotor.STOP_MODE.COAST)
        time.sleep(steps/10.0)
        self.C.run_time_limited(100*3, self.loader_speed, stop_mode=MMotor.STOP_MODE.COAST)
        # self.C.run_position_limited(self.C.position + 3*360 - self.C.position % (360*3),
        #                           self.loader_speed, stop_mode=MMotor.STOP_MODE.HOLD)

    def look_up(self):
        """set sonar to top position
            non time blocking"""
        self.C.run_position_limited(self.C.position + 1.5*360 - self.C.position % (360*3),
                                    self.loader_speed)

    def look_down(self):
        """set sonar to bottom position
            none time-blocking"""
        self.C.run_position_limited(self.C.position + 3*360 - self.C.position % (360*3),
                                    self.loader_speed)

    def ang_rad(self):
        ang = self.gyro.ang % 360
        if ang > 180:
            ang = ang - 360
        return radians(ang)

    def call(self, n):
        time.sleep(3)
        tab = []
        for i in range(n):
            fi = self.gyro.ang
            ran = (random.random()*2-1)*180
            self.turn_deg(ran)
            time.sleep(3)
            tab.append((ran, self.gyro.ang-fi))
            self.run_dist_cm(-5)
            time.sleep(1)
            self.run_dist_cm(5)
            time.sleep(1)
        return tab

    def bee(self):
        self.tone.play(698.46)
        time.sleep(0.01)
        self.tone.stop()

    def BEE(self):
        self.tone.play(100,100)

    def beep(self):
        self.tone.play(698.46)
        time.sleep(0.1)
        self.tone.stop()
        time.sleep(0.02)
        self.tone.play(523.25)
        time.sleep(0.1)
        self.tone.stop()

    def finish(self):
        """stop, change motor stop mode,
        play sound, set leds to green etc."""
        self.stop()
        self.R.stop_mode = 'coast'     # free motor
        self.L.stop_mode = 'coast'     # free motor
        self.C.stop_mode = 'coast'
        self.led.left.color = LED.COLOR.AMBER
        self.led.left.on()
        self.beep()
        self.led.left.color = LED.COLOR.GREEN
        self.led.left.on()
        sys.exit(0)
