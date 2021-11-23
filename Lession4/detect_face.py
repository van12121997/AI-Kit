import cv2
import numpy as np

img = cv2.imread('/home/ai/Desktop/AI-KIT/Lession4/examples/hocsinh.jpg')

classifier = cv2.CascadeClassifier('/home/ai/Desktop/AI-KIT/Lession4/models/haarcascade_frontalface_default.xml')

boxes = classifier.detectMultiScale(img)

for box in boxes:
	x,y,width,height = box
	x2,y2 = x + width, y + height
	cv2.rectangle(img,(x,y),(x2,y2), (0,255,255), 1)
cv2.imshow('face detection',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
