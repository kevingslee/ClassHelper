import cv2
import numpy as np

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
while(1):
	_,frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if len(faces) > 0:
		for(x,y,w,h) in faces:
			frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			#eyes = eye_cascade.detectMultiScale(roi_gray)
			#for (ex,ey,ew,eh) in eyes:
			#	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		print("w:",width,",h:",height,faces)

	cv2.imshow("cam",frame)
	cv2.waitKey(10)

cv2.destroyAllWindow()