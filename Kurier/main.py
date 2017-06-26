# -*- coding: utf-8 -*-
from machine import Machine
from controler import Controler
from instrumental_package import *

global lcd
global key
lcd.reset()
lcd.update()

while not key.enter:
    if key.backspace:
        exit(0)

target1, target2, target3 = ([count_right(), count_right()], [count_right(), count_right()], [count_right(), count_right()])
display(target1, target2, target3)

#target1=[1,1]
#target2=[1,3]
#target3=[2,2]
LordAndSavior = Controler([target1, target2, target3], [[4, 0], [4, 4], [0, 4]])
shortest = LordAndSavior.pather()
while not key.enter:
    if key.backspace:
        lcd.reset()
        lcd.update()
        exit(0)
LordAndSavior.RUN(shortest)

