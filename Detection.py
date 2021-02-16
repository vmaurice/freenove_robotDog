import math
import time

from Control import *
from Servo import *
from Ultrasonic import *

class Detection:
    
    def __init__(self):
        self.servo=Servo()
        self.control=Control()
        self.sonic=Ultrasonic()

    def getDistance(self):

        t = []

        t2 = []

        n = 50

        median = int(n / 2)

        for i in range (n):
            t.append(self.sonic.getDistance())
            time.sleep(0.01)


        t.sort()
        print(t[median])
        return t[median]
    
    def runTable(self):

        self.servo.setServoAngle(15,0)

        t = time.time()
        
        while time.time() - t < (60 * 3):
            if self.getDistance() > 20:
                for i in range(10):
                    self.control.turnLeft()
            else:
                self.control.forWard()
        
        self.servo.setServoAngle(15,90)
        self.control.relax(True)

    def obstable(self):

        self.control.relax(True)

        self.servo.setServoAngle(15,90)
            
        
        t = time.time()
        
        while time.time() - t < (60 * 3): # 3 minutes
            #self.servo.setServoAngle(15,90)
            #time.sleep(1)
            if self.getDistance() < 10: # mur
                for i in range(10):
                    self.servo.setServoAngle(15,90)
                    self.control.turnLeft()
            else:
                self.servo.setServoAngle(15,45) # livre, objet plat
                time.sleep(0.5)
                if self.getDistance() < 150:
                    for i in range(10):
                        self.servo.setServoAngle(15,90)
                        self.control.turnLeft()
                else:
                    self.servo.setServoAngle(15,0)
                    time.sleep(0.5)
                    if self.getDistance() > 15: # vide (ex : table)
                        for i in range(10):
                            self.servo.setServoAngle(15,90)
                            self.control.turnLeft()
                    else:
                        self.servo.setServoAngle(15,90)
                        self.control.forWard()
            
            
        
        self.servo.setServoAngle(15,90)
        self.control.relax(True)
        
    def is_in_front_of_obstacle(self):

        self.servo.setServoAngle(15,90)
        time.sleep(0.5)
        if self.getDistance() < 10: # mur
            print("mur")
            return True
        else:
            self.servo.setServoAngle(15,45) # livre, objet plat
            time.sleep(0.5)
            if self.getDistance() < 10:
                print("plat")
                self.servo.setServoAngle(15,90)
                return True
            else:
                self.servo.setServoAngle(15,25)
                time.sleep(0.5)
                if self.getDistance() > 15: # vide (ex : table)
                    print("table")
                    self.servo.setServoAngle(15,90)
                    return True
                else:
                    print("rien")
                    self.servo.setServoAngle(15,90)
                    return False

  
        
if __name__=='__main__':
    action=Action()  
    time.sleep(2) 
    #action.runTable() # ne verifie que la vide
    action.obstable() # obstacle
    time.sleep(3)
    
    
        

