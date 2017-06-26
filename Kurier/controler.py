# -*- coding: utf-8 -*-

from robot import Robot
from robot import Obstacle
from map import Map
from math import pi
from instrumental_package import *
from copy import deepcopy

class Nobel_z_matmy_Error(Exception):
    """Hasn't found smallest value in finite set"""

class Controler(object):
    def __init__(self, pack, address):
        self.endrega = Robot(pack, address, [5.5, 15])

    def timer(self, list_of_actions):
        time = 0
        curr_ang = 0
        for n, iterator in enumerate(list_of_actions):
            if iterator[0]:
                time = time + self.endrega.time_of_action
            else:
                time = time + count_cm(list_of_actions[n-1][1] if n else self.endrega.pos_cm, list_of_actions[n][1])/self.endrega.speed_cm
            """if iterator[0] != "U":
                alpha = count_rad(list_of_actions[n-1][1] if n else self.endrega.pos_cm, list_of_actions[n][1]) - curr_ang
                time = time + float(alpha)/self.endrega.speed_rad
                curr_ang = alpha + curr_ang
                """
        return time

    def router(self, list_of_points):
        tab = []
        for n, iterator in enumerate(list_of_points):
            if "P" in iterator[0]:
                tab.append([None, target(iterator[1], count_rad(iterator[1], list_of_points[n-1][1] if n else self.endrega.pos_cm), BEFORE)])
                tab.append(["L", iterator[1]])
            elif "A" in iterator[0]:
                tab.append([None, target(iterator[1], count_rad(iterator[1], list_of_points[n-1][1] if n else self.endrega.pos_cm), BEFORE/2.0)])
                tab.append(["U", target(iterator[1], count_rad(iterator[1], list_of_points[n-1][1] if n else self.endrega.pos_cm), BEFORE)])
            else:
                tab.append([None, iterator[1]])
        return tab

    def pather(self):
        permutations = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        shortest_time = 1e10
        shortest_path = None
        for p in permutations:
            for s in scenario(p):
                route = self.router(self.endrega.board.search(s))
                time = self.timer(route)
                if time < shortest_time:
                    shortest_time = time
                    shortest_path = route
        if shortest_path is None:
            raise Nobel_z_matmy_Error('no shortest_path')
        return shortest_path

    def RUN(self, list_of_actions):
        self.endrega.reset_dir()
        actions = deepcopy(list_of_actions)
        while len(actions):
            print 'jestem', self.endrega.pos_cm, 'jade', actions[0]
            if actions[0][0] is None:
                try:
                    if count_cm(self.endrega.pos_cm, actions[0][1]) > 45:
                        trg = target(self.endrega.pos_cm, count_rad(self.endrega.pos_cm, actions[0][1]), 45)
                        self.endrega.goto_cm(trg, T=actions[0][1])
                        print 'tymczasowo jade na', trg
                    elif actions[1][0] == "L" and count_cm(self.endrega.pos_cm, actions[1][1]) < 45:
                            actions.pop(0)
                            continue
                    else:
                        self.endrega.goto_cm(actions[0][1])
                        actions.pop(0)
                except Obstacle as new:
                    # self.endrega.body.bee()
                    # self.endrega.body.bee()
                    self.endrega.goto_cm(new.point, obst=True)
                continue
            elif actions[0][0] == "L":
                self.endrega.load(actions[0][1])
                actions.pop(0)
            elif actions[0][0] == "U":
                self.endrega.unload()
                actions.pop(0)
            else:
                print("ERR: action unknown!", actions[0], '.')
                actions.pop(0)
        else:
            self.endrega.finish()
