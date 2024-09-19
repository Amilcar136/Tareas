#rotar 60°, trasladar 10px, escalar 1/5
import cv2 as cv
import numpy as np
import math

#cargar imagen
img = cv.imread ('Rama_flor.png', 0)

#obtener tamaño de la imagen
x, y =img.shape

#Crear imagen vacía para almacenar el resultado
resultimg = np.zeros((int(x * 1/5), int(y * 1/5)), dtype=np.uint8)

#definir el ángulo de rotacion (en grados) y convertirlo a radianes
angle = 60
theta = math.radians (angle)

#Definir desplazamiento 
dx, dy = 10, 10

#Definir escala
scale = 1/5

#rotar la imagen
for i in range (int(x * scale)):
    for j in range (int(y* scale)):
        #coord orig
        orig_x = int(i / scale)
        orig_y = int(j / scale)
        #rotar
        rot_x = int((orig_x - x // 2)* math.cos(theta) - (((orig_y - y // 2)*math.sin(theta) + x //2)))
        rot_y = int((orig_x - x // 2)* math.sin(theta) + (((orig_y - y // 2)*math.cos(theta) + y // 2)))
        #transladar
        transx = rot_x + dx
        transy = rot_y + dy
        if 0 <= transx < x and 0 <= transy < y:
            resultimg[i, j] = img[transx, transy]

#Mostrar la imagen original y la rotada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen rotada, escalada y trasladada (modo raw)', resultimg)
cv.waitKey(0)
cv.destroyAllWindows