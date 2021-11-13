#import smbus
import math
from time import sleep
import cv2
import numpy as np

class Face():
    def __init__(self):            
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.ori_height = 0
        self.ori_width = 0
    def grapPicture(self):
        if self.cap.isOpened():
            _,frame = self.cap.read()        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.ori_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.ori_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return gray
        else:
            return None
    
    def detect(self, picture):
        mx = my = mw = mh = 0
        #if picture != None:
        faces = self.face_cascade.detectMultiScale(picture, 1.3, 5) # scalefactor, minneighbors
        max = 0
        if len(faces) > 0:
            for(x,y,w,h) in faces:
                if (w * h) > max :
                    max = w* h
                    mx = x
                    my = y
                    mw = w
                    mh = h         
        #picture = cv2.rectangle(picture, (mx,my), (mx+mw,my+mh), (0,0,255), 2)
        #cv2.imshow("cam",picture)
        #cv2.waitKey(100)
        #print("w:",self.ori_width,",h:",self.ori_height, mx,my,mw,mh)
        return {"status":False, "width":self.ori_width, "height":self.ori_height, "x":mx,"y":my,"w":mw,"h":mh}
        #else:
        #    return {"status":True, "width":self.ori_width, "height":self.ori_height, "x":mx,"y":my,"w":mw,"h":mh}
