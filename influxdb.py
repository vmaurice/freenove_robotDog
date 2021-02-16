import time
import smbus2 as smbus
import json
import socket


from datetime import datetime

import sys
sys.path.append('sources/')



from Control import *
from Servo import *
from ADS7830 import *
from Ultrasonic import *
from IMU import *


# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04

"""
    Envoie les informations du robot sous JSON à une interface telegraf qui lui envoie à la bdd influxdb
"""
class Send:
    def __init__(self):
        self.servo = Servo()
        self.control=Control()
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.adc = ADS7830()
        self.sonic = Ultrasonic()
        self.imu=IMU()
        

        # Initialize I2C (SMBus)
        self.I2Cbus = smbus.SMBus(1)

        self.slaveAddress = PCA9685_ADDRESS

        self.servo_angle = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.calibration_angle = [[-10, -2, 13], [-11, -7, 17], [9, -6, 16], [14, -18, 17]]

        # You can generate a Token from the "Tokens Tab" in the UI
        self.bucket = "robotDog"

        self.host = "localhost"
        self.port = 8094

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # value PWM to angle
    def inverse(self, n):
        n += 256.0
        return round(((n * 20000.0 / 4096.0) - 850.0) / 10.0, 0)

    # map value
    def map(self,value,fromLow,fromHigh,toLow,toHigh):
        return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

    # get PWM
    def getPWM(self, num):
        return round(float(self.I2Cbus.read_byte_data(self.slaveAddress, LED0_OFF_L + 4 * num)),3)

    # borne the result
    def restriction(self, n, min, max):
        if n < min:
            return min
        elif n > max:
            return max
        else:
            return n


    # Main
    def main(self):

        

        #self.control.forWard()
        #self.control.relax(True)

        #print ("angle by control file : " + str(self.control.angle))
        #print ("calibration angle : " + str(self.control.calibration_angle))

        #self.servo.setServoAngle(15,130)

        

        while True:

            try:

                # récupère la tension des batteries
                voltage = round(self.adc.power(0), 2)

                # récupère l'angle des moteurs
                for i in range(2):
                    self.servo_angle[i][0] = self.restriction(self.inverse(self.getPWM(4+i*3)) - self.calibration_angle[i][0], 0, 180) 
                    self.servo_angle[i][1] = self.restriction(self.inverse(self.getPWM(3+i*3)) + self.calibration_angle[i][1], 0, 180)
                    self.servo_angle[i][2] = self.restriction(self.inverse(self.getPWM(2+i*3)) - self.calibration_angle[i][2], 0, 180)
                    self.servo_angle[i+2][0] = self.restriction(self.inverse(self.getPWM(8+i*3)) - self.calibration_angle[i+2][0], 0, 180)
                    self.servo_angle[i+2][1] = self.restriction(self.inverse(self.getPWM(9+i*3)) - self.calibration_angle[i+2][1], 0, 180)
                    self.servo_angle[i+2][2] = self.restriction(self.inverse(self.getPWM(10+i*3)) + self.calibration_angle[i+2][2], 0, 180)


                #print ("voltage battery : " + str(voltage))
                #print ("servo angle : " + str(self.servo_angle))
                
                sonic_angle = self.inverse(round(float(self.I2Cbus.read_byte_data(self.slaveAddress, LED0_OFF_L + 4 * 15)),3))

                accel_data, gyro_data = self.imu.average_filter()

                #print (accel_data)
                #print(gyro_data)

                msg = ""

                msg += "{ "


                msg += "\"drive\" : {"

                for i in range(2):
                    msg += "\"" + str(i) + "\" : { "
                    msg += "\"" + str(0) + "\" : " + str(self.servo_angle[i][0]) + ", "
                    msg += "\"" + str(1) + "\" : " + str(self.servo_angle[i][1]) + ", "
                    msg += "\"" + str(2) + "\" : " + str(self.servo_angle[i][2]) + " "
                    msg += " }, "
                    msg += "\"" + str(i+2) + "\" : { "
                    msg += "\"" + str(0) + "\" : " + str(self.servo_angle[i+2][0]) + ", "
                    msg += "\"" + str(1) + "\" : " + str(self.servo_angle[i+2][1]) + ", "
                    msg += "\"" + str(2) + "\" : " + str(self.servo_angle[i+2][2]) + " "
                    msg += " }, "

                msg = msg[0:len(msg)-2]

                msg += " }, "

                msg += "\"sonic\" : {"
                msg += "\"angle\" : " + str(sonic_angle) + ", "
                msg += "\"distance\" : " + str(self.sonic.getDistance())

                msg += "}, "

                msg += "\"voltage\" : " + str(round(self.adc.power(0), 2)) + ", "

                msg += "\"IMU\" : {"

                msg += "\"accel\" : {"
                msg += "\"x\" : " + str(accel_data["x"]) + ", "
                msg += "\"y\" : " + str(accel_data["y"]) + ", "
                msg += "\"z\" : " + str(accel_data["z"])

                msg += "}, "

                msg += "\"gyro\" : {"
                msg += "\"x\" : " + str(gyro_data["x"]) + ", "
                msg += "\"y\" : " + str(gyro_data["y"]) + ", "
                msg += "\"z\" : " + str(gyro_data["z"])

                msg += "}"

                msg += "}"


                msg += "}"

                #print (msg)

                json_msg = json.dumps(json.loads(msg))

                #print(json.dumps(json.loads(msg), sort_keys=True, indent=4))
                    


                

                #print ("Sonic angle : " + str(sonic_angle))

                
                try:
                    self.socket.sendto(json_msg.encode('utf8'), (self.host, self.port))
                    print ("Send")
                except (socket.error, RuntimeError):
                    print ("Error send")


                #print ()

                time.sleep(1)

            except KeyboardInterrupt:
                print ("Stop")
                sys.exit()
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)

        #self.control.relax(True)



def main():
    s = Send()
    time.sleep(2)
    s.main()
    time.sleep(2)
    

if __name__ == '__main__':
    main()