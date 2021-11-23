import cv2

img = cv2.imread('/home/ai/Desktop/AI-KIT/image/color.jpg')
(h,w,d) = img.shape
(B,G,R) = img[230,420]
print("weight={}, height={}. depth={}".format(w,h,d))
print("B={}, G={}, R={}".format(B,G,R))
cv2.imshow('Image',img)
cv2.waitKey(0)
