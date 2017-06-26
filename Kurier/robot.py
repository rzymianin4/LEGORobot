# -*- coding: utf-8 -*-

import math
import time
from instrumental_package import *
from machine import Machine
from map import Map

class trunk(object):
    def __init__(self):
        self.l = []

    @property
    def pack(self):
        return self.l

    def load(self, x):
        self.l.append(x)

    def unload(self):
        return self.l.pop(-1)


class Obstacle(Exception):
    def __init__(self, point):
        self.point = point


class Robot(object):

    def __init__(self, pack, address, pos_cm=[15, 15]):
        self.board = Map(pack, address)
        self.pos_cm = pos_cm
        self.body = Machine()
        self.trunk = trunk()
        self.speed_cm = 19
        self.speed_slow = 10
        self.distance_we_see_ir = 65
        self.distance_we_see_sonar = 255
        self.time_of_action = 5
        self.speed_rad = 1.9
        self.load_dist = 45

    def finish(self):
        self.body.finish()

    def ir_cm(self, value):
        return 25.5100881825 + 0.48034070391*value

    def load(self, point):
        target_rad = count_rad(self.pos_cm, point) - self.dir
        target_dist_cm = math.hypot(self.pos_cm[0] - point[0], self.pos_cm[1] - point[1])
        self.body.turn_rad_slow(target_rad)
        self.body.run_slow(target_dist_cm)

        self.body.load(self.load_dist)
        #self.goto_cm(point, slow = True)
        time.sleep(target_dist_cm/self.speed_slow)
        self.pos_cm = target(self.pos_cm, self.dir, target_dist_cm)

    def unload(self):
        direct = ~self.dir
        self.body.run_dist_cm(-32)
        self.body.unload()
        time.sleep(32/20.0)
        self.pos_cm = target(self.pos_cm, direct, 30)

    def black(self):
        return self.body.color.reflect < 20

    @property
    def dir(self):
        return angle(self.body.ang_rad())
    @property
    def scan_ir_points(self):
        return self.body.ir.prox
    @property
    def scan_sonar_cm(self):
        return self.body.sonar.dist_cm()

    def obstacle(self, pos, angle, distance, tar, obst=False):
        """returns coordinates of field, at which there is obstacle"""
        if not obst and distance < 60:
            distance = self.ir_cm(distance)
            point = target(pos, angle, distance)
            field = nearest_field_cm(point)
            distance = math.hypot(pos[0]-field[0], pos[1]-field[1])
            distance_to_target =  math.hypot(pos[0]-tar[0], pos[1]-tar[1])
            if distance_to_target - distance < -5:
                print 'target:', tar, distance_to_target
                print 'obst:  ', field, distance
                return
            self.body.stop
            angle_to_obst = count_rad(pos, field) - angle
            alfa = math.atan2(15,distance)
            h = distance*math.cos(angle_to_obst)
            if angle_to_obst > 0:
                point_to_go = target(pos, count_rad(pos, field) - alfa, distance)
            else:
                point_to_go = target(pos, count_rad(pos, field) + alfa, distance)
            if point_to_go[0] < 15:
                point_to_go[0] = 30 - point_to_go[0]
            if point_to_go[1] < 15:
                point_to_go[1] = 30 - point_to_go[1]
            if point_to_go[0] > 143:
                point_to_go[0] = 2*143 - point_to_go[0]
            if point_to_go[1] < 15:
                point_to_go[1] = 2*143 - point_to_go[1]
            self.pos_cm = pos
            print point_to_go
            raise Obstacle(point_to_go)


    def measure_current_position(self, origin, time_passed):
        return [origin[0] + (time_passed*self.speed_cm)*math.cos(self.dir) , origin[1] + (time_passed*self.speed_cm)*math.sin(self.dir)]

    def align(self, coord_cm):
        global fi
        prev_pos = coord_cm[:]
        if (-fi < self.dir < fi) or (math.pi-fi < self.dir or self.dir < fi-math.pi):                        # forward x
            if 6 < coord_cm[1]%32 < 24:
                if 6 > coord_cm[0]%32 or coord_cm[0]%32 > 24:
                    coord_cm[0] = round(coord_cm[0]/32.0)*32-1 if self.black() else coord_cm[0]
        if ((math.pi/2-fi) < self.dir < (math.pi/2+fi)) or (-fi-math.pi/2 < self.dir < -math.pi/2 + fi):              # forward y
            if 6 < coord_cm[0]%32 < 24:
                if coord_cm[1]%32 < 6 or 24 < coord_cm[1]%32:
                    coord_cm[1] = round(coord_cm[1]/32.0)*32-1 if self.black() else coord_cm[1]
        if prev_pos != coord_cm:
            return True
        else:
            return False

    def do_till_still(self, targ, obst=False, T=None):
        """make 10 scans, then till motors stop:
                scan, align if necessary, react to obstacles etc."""
        origin_pos = self.pos_cm[:]
        curr_pos = self.pos_cm[:]
        for i in range(30):
            self.scan_ir_points
        time_of_start = time.time()
        while not self.body.still:

            if self.black():
                print curr_pos, self.dir
            dist = self.scan_ir_points
            if T is None:
                self.obstacle(curr_pos, self.dir, dist, targ, obst)
            else:
                self.obstacle(curr_pos, self.dir, dist, T, obst)
            if self.align(curr_pos):
                time_of_start = time.time()
                print 'byłem', origin_pos, 'jestem', curr_pos
                origin_pos = curr_pos[:]
                # self.body.BEE()
            else:
                curr_pos = self.measure_current_position(origin_pos, time.time() - time_of_start)
        self.pos_cm = target(curr_pos, ~self.dir, 4)

    def goto_cm(self, target_pos_cm, T=None,obst=False):
        """pos_cm is a LIST
            go to point of coordinates"""
        target_rad = count_rad(self.pos_cm, target_pos_cm) - self.dir
        target_dist_cm = math.hypot(self.pos_cm[0] - target_pos_cm[0], self.pos_cm[1] - target_pos_cm[1])
        if target_dist_cm < 2:
            return
        self.body.turn_rad_slow(target_rad)
        self.body.run_dist_cm(target_dist_cm)
        return self.do_till_still(target_pos_cm, obst, T=T)

    def speed(self, n=100):
        t = time.time()
        self.body.run_dist_cm(n)
        for i in range(40):
            pass
        while not self.body.still:
            pass
        return n/(time.time() - t)

    def reset_dir(self):
        self.body.gyro.ang_and_rate
        self.body.gyro.ang

