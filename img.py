import cv2

img = cv2.imread('a.png')

img = cv2.resize(img, (0, 0), fx=0.5, fy= 0.5)

cv2.imshow('img', img)

cv2.waitKey(0)