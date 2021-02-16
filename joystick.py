from bluepy import btle
import time

import sys
sys.path.append('sources/')


from Control import *
from Servo import *
from Ultrasonic import *
from Action import *

"""
    Controle robot chien avec un joystick
"""
class Joystick:
    
    def __init__(self):
        #init les classes pour controler le robot
        self.servo=Servo()
        self.control=Control()
        self.sonic=Ultrasonic()
        self.action=Action()

        # init bluetooth low energy
        self.dev = btle.Peripheral()

        # init UUID
        self.service_uuid = btle.UUID("2A9F")

        self.char_uuid_x = btle.UUID("2AAE")
        self.char_uuid_y = btle.UUID("2AAF")
        self.char_uuid_z = btle.UUID("2AB3")

    # Se connecter à la manette
    def connect(self):
        print ("Connecting...")
        self.dev.connect("B8:F0:09:CC:88:92")
        print ("Done")

    # Récupère les valeures de la manette et execute
    def run(self):

        print ("Get value...")

        x = 121
        y = 121
        z = 1

        

        while True:

            try:

                result = []

                # récupère le service
                for i in self.dev.getServices():
                    if i.uuid == self.service_uuid:
                        result = i.getCharacteristics()
                        break


                # récupère la valeur de x, y et z
                for i in result:
                    if i.uuid == self.char_uuid_x:
                        x = int(i.read().hex(), 16)
                    elif i.uuid == self.char_uuid_y:
                        y = int(i.read().hex(), 16)
                    elif i.uuid == self.char_uuid_z:
                        z = int(i.read().hex(), 16)
                    else: 
                        print ("error uuid")

                print (x)
                print (y)
                print (z)

                # Quand le joystick est enclenché
                if z == 0:
                    if (x > 180):
                        print ("push up")
                        self.action.push_ups()
                    elif (x < 70):
                        print ("swim")
                        self.action.swim()
                    elif (y > 180):
                        print ("yoga")
                        self.action.yoga()
                    elif (y < 70):
                        print ("coquettish")
                        self.action.coquettish()
                    else:
                        print ("helloOne")
                        self.action.helloOne()
                # utilisation simple
                else:
                    if (x > 180 and y > 180):
                        print ("turnRight")
                        self.control.turnRight()
                    elif (x > 180 and y < 70): 
                        print ("turnLeft")
                        self.control.turnLeft()
                    elif (x > 180):
                        print ("forWard")
                        self.control.forWard()
                    elif (y > 180):
                        print ("stepRight")
                        self.control.setpRight()
                    elif (y < 70):
                        print ("stepLeft")
                        self.control.setpLeft()
                    elif (x < 70):
                        print ("backWard")
                        self.control.backWard()
                    else:
                        print ("Relax")
                        self.control.relax(True)

            # pour arreter le programme
            except KeyboardInterrupt:
                print ("Stop")
                self.control.relax(True) 
                self.dev.disconnect()
                sys.exit()
            except Exception as ex:
                # reconnecte si besoin
                if type(ex).__name__ == "BTLEDisconnectError":
                    print ("connect to device")
                    self.dev.connect("B8:F0:09:CC:88:92")
                    self.control.relax(True)
                else:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print (message)
                    self.control.relax(True)


if __name__=='__main__':
    joy=Joystick()  
    time.sleep(1) 
    joy.connect()
    time.sleep(1)
    joy.run()
    time.sleep(1)




