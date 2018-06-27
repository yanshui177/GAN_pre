import cv2

img = cv2.imread('./data/134212_1.jpg')
cv2.imshow('123', img)
a = cv2.copyMakeBorder(img, 5, 5, 5, 5,
                       cv2.BORDER_CONSTANT, value=[0, 255, 0])
cv2.imshow('a', a)
cv2.waitKey(0)