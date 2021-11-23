# import the necessary packages
import numpy as np
import argparse
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])

hsvcolor = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

boundaries = [
	([136,87,111],[180,255,255]),
	([22,93,0],[45,255,255]),
	([100,100,100],[125,255,255])
]

for(lower,upper) in boundaries:
	lower=np.array(lower,dtype="uint8")
	upper=np.array(upper,dtype="uint8")

	mask=cv2.inRange(hsvcolor,lower,upper)

	output=cv2.bitwise_and(image,image,mask=mask)

	cv2.imshow("image",np.hstack([image,output]))
	cv2.waitKey(0)
