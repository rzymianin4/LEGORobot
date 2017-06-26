#-*- coding: utf-8 -*-
from instrumental_package import *

class Map(object):

    def __init__(self, pack, address):
        self.table = [[None for x in range(5)] for y in range(5)]
        self.left_obstacles = 3 # - len(obstacle)
        for n, it in enumerate(pack):
            self.table[it[0]][it[1]] = "P"+str(n+1)
        for n, it in enumerate(address):
            self.table[it[0]][it[1]] = "A"+str(n+1)

    def erease(self, coord):
        self.table[coord[0]][coord[1]] = None

    def add_obstacle(self, obstacle):
        for it in obstacle:
            if self.left_obstacles <= 0:
                print "ERR: too many obstacles"
                break
            self.left_obstacles -= 1
            self.table[it[0]][it[1]] = "X"+str(3 - self.left_obstacles)


    def list_packs(self):
        tab = [None for i in range(3)]
        for x, it_x in enumerate(self.table):
            for y, it_y in enumerate(it_x):
                if "P" in it_y:
                    tab[it_y[1]] = [x, y]
        return tab

    def list_addresses(self):
        tab = [None for i in range(3)]
        for x, it_x in enumerate(self.table):
            for y, it_y in enumerate(it_x):
                if "A" in it_y:
                    tab[it_y[1]] = [x, y]
        return tab

    def list_obstacles(self):
        tab = [None for i in range(3)]
        for x, it_x in enumerate(self.table):
            for y, it_y in enumerate(it_x):
                if "X" in it_y:
                    tab[it_y[1]] = [x, y]
        return tab

    def list_bricks(self):
        return self.list_packs() + self.list_obstacles()

    def search(self, elements):
        """take 'P1', return ['P1',[x,y]]"""
        tab = []
        for it in elements:
            for x, it_x in enumerate(self.table):
                for y, it_y in enumerate(it_x):
                    if it == it_y:
                        tab.append([it, field_to_cm([x, y])])
        return tab
