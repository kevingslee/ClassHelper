#!/usr/bin/python
import smbus
import math
from time import sleep
import cv2
import numpy as np
import face
from pose import Pose
from face import Face
import requests
import sys, getopt

BASE = "http://192.168.1.152:5000/"

def main(name, addr):
    #if len() > 0:
    #    BASE = "http://"+addr +":5000/"
    
    # print("server address:" + addr)
    pose = Pose()
    face = Face()

    print("--------")
    #print("Gyroskop")
    #print("--------")
    count = 0
    while True:
        curr_pose = pose.get_pose()
        pic = face.grapPicture()
        data = face.detect(pic)
        if count % 3 == 0:
            response = requests.post(addr + "setstatus/"+name+"/"
                +str(data["width"])+"/"+str(data["height"])+"/"+str(data["x"])+"/"+str(data["y"])+"/"
                +str(data["w"])+"/"+str(data["h"])+"/"+str(curr_pose["x"])+"/"+str(curr_pose["y"])+"/"
                +str(curr_pose["z"]))
        if count == 10:
            count = 0
            print("face data:",data)
            print("pose:",curr_pose)
            #print(response.json())
        else:
            count += 1
        sleep(0.1)

if __name__ == "__main__":
    #print(sys.argv)
    myname = sys.argv[1]
    serveraddr = "http://"+sys.argv[2]+":5000/"
    print("serveraddr",serveraddr)
    if len(sys.argv):
        main(myname, serveraddr)
    else:
        main("Student", "http://"+"192.168.1.176:5000/")


