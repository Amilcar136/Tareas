import numpy as np
import cv2 as cv

img = cv.imread("mascarapug.png", 0)

x, y = img.shape

scale_x, scale_y = 2, 2

scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)


#aplicar escalado
for i in range(x):
    for j in range (y):
        #orig_x = int(i * scale_y)
        #orig_y = int(j * scale_x)
        scaled_img[i*2, j*2] = img[i, j]


cv.imshow ("img original", img)
cv.imshow ("img escalada", scaled_img)
#cv.imshow ("imagen 1/9", img_convu)
cv.waitKey(0)
cv.destroyAllWindows