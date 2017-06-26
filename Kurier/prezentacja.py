# -*- coding: utf-8 -*-
from ev3.lego import InfraredSensor
import os
from robot import Robot


r = Robot([[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]],[0,0])
r.load_dist = 20
IR = InfraredSensor()

def say(text='Nie mam nic do powiedzenia', lang='pl', speed=130):
    """runs espeak -s speed -a 200 -g 1 -v lang text --stdout | aplay"""
    os.system('espeak -s ' + str(speed) + ' -a 200 -g 1 -v ' +
              str(lang) + ' "' + str(text) + '" --stdout | aplay')

def read():
    return IR.value0
    
def wait():
    while not read():
        pass
    
tab = [
    ",, A ja Endriaga.",
    ",, Mnie trochę krócej",
    ", Gotowi!",
    ", Żeby móc wiedzieć na czym stoję",
    ", Żeby Cię móc lepiej widzieć",
    ", Żeby znać swoją orientację, , w przestrzeni", 
    ", Żeby móc cię zjeść!)",
    ", Nic mnie nie zatrzyma!!",
    ", Kłaniam się!"
    
    ] # tablica rzeczy do gadania

for text in tab:
    wait()
    if '!!' in text:
        say(text, speed = 180)
    elif ')' in text:
        say(text)
        r.load([30,0])

    else:
        say(text)
 
