#rotar 30 grados en sentido horario, 60 en antihorario y escalar en 2
import cv2 as cv
import numpy as np
import math

#cargar imagen
img = cv.imread ('Rama_flor.png', 0)

#obtener tamaño de la imagen
x, y =img.shape

#Crear imagen vacía para almacenar el resultado
resultimg = np.zeros((int(x * 2), int(y * 2)), dtype=np.uint8)

#definir el ángulo de rotacion (en grados) y convertirlo a radianes
angle1 = -30
theta1 = math.radians (angle1)

#definir segundo angulo
angle2 = 60
theta2 = math.radians (angle2)

#definir escalado
scale = 2

for i in range (int(x * scale)):
    for j in range (int(y * scale)):
        #coord orig
        orig_x = int(i / scale)
        orig_y = int(j / scale)
        #rotacion1
        rot_x1 = int((orig_x - x // 2) * math.cos(theta1) - (orig_y - y // 2) *math.sin(theta1) + x // 2)
        rot_y1 = int((orig_x - x // 2) * math.sin(theta1) + (orig_y - y // 2) *math.cos(theta1) + y // 2)
        #rotacion2
        rot_x2 = int((rot_x1 - x // 2) * math.cos(theta2) - (rot_y1 - y // 2) *math.sin(theta2) + x // 2)
        rot_y2 = int((rot_x1 - x // 2) * math.sin(theta2) + (rot_y1 - y // 2) *math.cos(theta2) + y // 2)
        #checar si las coordenadas estan dentro de la imagen
        if 0 <= rot_x2 < x and 0 <= rot_y2 < y:
            resultimg[i, j] = img[rot_x2, rot_y2]

#mostrar imagen original y resultado
cv.imshow('imagen original', img)
cv.imshow('imagen rotada y escalada', resultimg)
cv.waitKey(0)
cv.destroyAllWindows