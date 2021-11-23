import cv2

img = cv2.imread('/home/ai/Desktop/AI-KIT/image/color.jpg')
(h, w, d) = img.shape
print("width={}, heiht={}, depth={}".format(w,h,d))

(B,G,R)= img[250,400]
print("R={}, G={}, B={}".format(R,G,B))

catanh = img[100:300,100:250]
cv2.imshow('cat anh',catanh)

dim=(256,256)
resize= cv2.resize(img,dim)
cv2.imshow('resize',resize)

center=(w/2,h/2)
M = cv2.getRotationMatrix2D(center,45,1.0)
rotation = cv2.warpAffine(img,M,(w,h))
cv2.imshow('Rotation',rotation)
cv2.imshow('Display Image', img)
cv2.waitKey(0)
