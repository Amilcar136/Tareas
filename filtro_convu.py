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

mat_convu = np.ones((3,3), np.float32) / 9
img_convu = np.zeros(scaled_img.shape, dtype=np.uint8)

for i in range(1, scaled_img.shape[0] - 1):
    for j in range(1, scaled_img.shape[1] - 1):
        for c in range(1):
            suma = 0
            # Aplicar la matriz de convolución
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    suma += scaled_img[i + ki, j + kj] * mat_convu[ki + 1, kj + 1]
                    img_convu[i, j] = np.clip(suma, 0, 255) 

cv.imshow ("img original", img)
cv.imshow ("img escalada", scaled_img)
cv.imshow ("imagen 1/9", img_convu)
cv.waitKey(0)
cv.destroyAllWindows