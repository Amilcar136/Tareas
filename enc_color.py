import cv2 as cv
import numpy as np

img = cv.imread('colores.png', 1)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#rango de colores rojos
bajo_rojo1 = np.array([0, 100, 100])
alto_rojo1 = np.array([10, 255, 255])
bajo_rojo2 = np.array([160, 40, 40])
alto_rojo2 = np.array([180, 255, 255])

#rango de colores amarillo
bajo_ama = np.array([20, 100, 100])
alto_ama = np.array([40, 255, 255])

#rango colores azul
bajo_azul = np.array([100, 100, 100])
alto_azul = np.array([140, 255, 255])

#rango colores verde
bajo_verde = np.array([50, 100, 100])
alto_verde = np.array([80, 255, 255])

#mascara de rojo
mask_rojo1 = cv.inRange(hsv, bajo_rojo1, alto_rojo1)
mask_rojo2 = cv.inRange(hsv, bajo_rojo2, alto_rojo2)
mask_rojo = cv.add(mask_rojo1, mask_rojo2)

#mascara amarillo
mask_ama = cv.inRange(hsv, bajo_ama, alto_ama)
#mascara azul
mask_azul = cv.inRange(hsv, bajo_azul, alto_azul)
#mascara verde
mask_verde = cv.inRange(hsv, bajo_verde, alto_verde)

res_rojo = cv.bitwise_and(img, img, mask=mask_rojo)
res_ama = cv.bitwise_and(img, img, mask=mask_ama)
res_azul = cv.bitwise_and(img, img, mask=mask_azul)
res_verde = cv.bitwise_and(img, img, mask=mask_verde)

#imprimir imagen
cv.imshow('imagen', hsv)
cv.imshow('rojo', res_rojo)
cv.imshow('amarillo', res_ama)
cv.imshow('azul', res_azul)
cv.imshow('verde', res_verde)
cv.waitKey(0)
cv.destroyAllWindows