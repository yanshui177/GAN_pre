import numpy as np
import cv2
img = np.zeros((512, 512, 3), np.uint8)
cv2.circle(img, (447, 63), 10, (0, 0, 255), -1)

img = cv2.copyMakeBorder(img, 50, 50, 50, 50,
                       cv2.BORDER_CONSTANT, value=[0, 255, 0])
cv2.imshow("shiyan", img)
cv2.waitKey(0)
cv2.destroyAllWindows()




