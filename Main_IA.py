#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:17:04 2021

@author: blaise
"""
from DaLog import *
from CircleDetection import *
from Detection import *
from Control import *
from Connection import *

control = None

def doInstr(instr):
    if instr == 'F':
        control.forWard()
    elif instr == 'SL':
        control.setpLeft()
    elif instr == 'P':
        control.stop()
        time.sleep(0.1)
    elif instr == 'SR':
        control.setpRight()
    elif instr == 'TL':
        control.turnLeft()
    elif instr == 'TR':
        control.turnRight()
    elif instr == 'END':
        return True
    return False

def execInstructionList(instList):
     for i in instList:
        doInstr(i)

def turnBack():
    inst = ["TR","TR","TR","TR","TR","TR","TR","TR","TR","TR","TR","TR","TR","TR","TR","TR","P","SL","SL","SL","P","F","F"]
    inst.append("END")
    execInstructionList(inst)


'''
def passObstacle():
    
    def reverseOrder(order):
        if order=="TR":
            return "TL"
        else :
            return "TR"
    
    order = "TR"
    inst_size = 3
    inst = ["TR","TR","TR"]
    execInstructionList(inst)
    while detection.is_in_front_of_obstacle():
        order = reverseOrder(order)
        inst_size += 3 
        inst.clear()
        inst = [order for i in range(inst_size)]
        execInstructionList(inst)
'''
def passObstacle():

    def reverseOrder(order):
        if order=="TR":
            return "TL"
        else :
            return "TR"

    order = "TR"
    numberOfLoops = 0 
    inst_size = 3
    inst = ["TR","TR","TR"]
    execInstructionList(inst)
    while detection.is_in_front_of_obstacle():
        order = reverseOrder(order)
        inst_size += 3 
        inst.clear()
        inst = [order for i in range(inst_size)]
        execInstructionList(inst)
        numberOfLoops += 1
    numberOfInstToWriteOnLog = len(inst) - (numberOfLoops//2)*3 
    for i in range (0,numberOfInstToWriteOnLog):
        log.write(order)
        
    

#Da IA in da place 

recognition = CircleDetection()
detection = Detection()
log = Log()
control = Control()
buzzer= Buzzer()

c=Connection("192.168.43.171")

threading.Thread(target=c.server).start()
#threading.Thread(target=c.client).start()

buzzer.run_for(0.1)

while not recognition.findBall() and not c.e.is_set() :
    if detection.is_in_front_of_obstacle():
        #do the obstacle trick
        passObstacle()
    else :
        doInstr("F")
        log.write("F")
        doInstr("F")
        log.write("F")
        

c.send("DETECTED")
buzzer.run_for(0.2)
turnBack()
log.reverse()
while not log.isEmpty:
    doInstr(log.getLastOrder)
    
#Beep