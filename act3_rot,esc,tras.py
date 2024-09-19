#rotar 70°, trasladar 20px, escalar 2
import cv2 as cv
import numpy as np
import math

#cargar imagen
img = cv.imread ('Rama_flor.png', 0)

#obtener tamaño de la imagen
x, y =img.shape

#Crear imagen vacía para almacenar el resultado
resultimg = np.zeros((int(x * 2), int(y * 2)), dtype=np.uint8)

#definir ángulo de rotacion
angle = 70
theta = math.radians(angle)

#definir desplazamiento
dx, dy = 20, 20

#definir escala
scale = 2

#rotar imagen
for i in range(int(x * scale)):
    for j in range(int(y * scale)):
        #coords originales
        orig_x = int(i / scale)
        orig_y = int(j / scale)
        #rotar
        rot_x = int((orig_x - x // 2) * math.cos(theta) - (orig_y - y // 2) * math.sin(theta) + x // 2)
        rot_y = int((orig_x - x // 2) * math.sin(theta) + (orig_y - y // 2) * math.cos(theta) + y // 2)
        #confirmar coords
        if 0 <= rot_x < x and 0 <= rot_y < y:
            resultimg[i, j] = img[rot_x, rot_y]

#mostrar imagenes
cv.imshow('imagen original', img)
cv.imshow('imagen resultante', resultimg)
cv.waitKey(0)
cv.destroyAllWindows