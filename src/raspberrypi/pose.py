
import smbus
import math
from time import sleep
import cv2
import numpy as np
import face

class Pose():
    def __init__(self):
        try:
            self.bus = smbus.SMBus(1)
            self.power_mgmt_1 = 0x6b
            self.power_mgmt_2 = 0x6c
            self.address = 0x68
            self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
        except :
            print("Error")
        
    def read_byte(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def read_word(self, reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        value = (h << 8) + l
        return value

    def read_word_2c(self, reg):
        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        #print("radiany :", radians)
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        #print("radianx :",radians)
        return -math.degrees(radians)
    
    def get_z_rotation(self, x,y,z):
        radians = math.atan2(z, self.dist(x,y))
        #print("radianx :",radians)
        return -math.degrees(radians)

    def get_pose(self):
        try:
            gyroskop_xout = self.read_word_2c(0x43)
            gyroskop_yout = self.read_word_2c(0x45)
            gyroskop_zout = self.read_word_2c(0x47)
            #print("Gyro:", gyroskop_xout/138, gyroskop_yout/138, gyroskop_zout/138)
            beschleunigung_xout = self.read_word_2c(0x3b)
            beschleunigung_yout =self.read_word_2c(0x3d)
            beschleunigung_zout = self.read_word_2c(0x3f)
            beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
            beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
            beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0

            anglex = self.get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
            angley = self.get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
            anglez = self.get_z_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
            return {"x":round(anglex,2), "y":round(angley,2), "z":round(anglez)}
        except:
            print("I/O Error")
            return {"x":int(0), "y":int(0), "z:":int(0)}
        

        #gyroskop_xout = pose.read_word_2c(0x43)
        #gyroskop_yout = pose.read_word_2c(0x45)
        #gyroskop_zout = pose.read_word_2c(0x47)

        #print ("gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
        #print ("gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
        #print ("gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))
        #print ("Beschleunigungssensor")
        #print ("---------------------")


        #beschleunigung_xout = pose.read_word_2c(0x3b)
        #beschleunigung_yout = pose.read_word_2c(0x3d)
        #beschleunigung_zout = pose.read_word_2c(0x3f)

        #beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
        #beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
        #beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0

        #print ("beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skaliert)
        #print ("beschleunigung_yout: ", ("%6d" % beschleunigung_yout), " skaliert: ", beschleunigung_yout_skaliert)
        #print ("beschleunigung_zout: ", ("%6d" % beschleunigung_zout), " skaliert: ", beschleunigung_zout_skaliert)
        #print ("X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
        #print ("Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
        
