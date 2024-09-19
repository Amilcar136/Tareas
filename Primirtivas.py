import cv2 as cv
import numpy as np

img = np.ones((500,500, 3), dtype=np.uint8)*255
                #centro #radio #colores   #tamaño
'''cv.circle(img, (250,250), 50, (0,234,21), -1)#lienzo, centro del circulo, radio, (colores rgb), tamaño de linea
cv.circle(img, (250,250), 40, (255,255,255), -1)
cv.circle(img, (250,250), 20, (0, 0, 0), -1)
cv.circle(img, (250, 250), 10, (255, 255, 255), -1)
cv.line(img,(1,1), (230,240), (0,234,21), 3)#linea
cv.rectangle(img, (20, 20), (50, 60), (0,0,0), 3)#rectangulo
pts = np.array([[10,5], [20, 30], [70, 20], [50, 10]], )'''
#Dibujar la cara
cv.ellipse(img, (250, 250), (100, 100), 0, 0, 360, 255, -1)
cv.circle(img, (50,50), 60, (0,255,255),-1)
#Dibujar los ojos
img [200:250, 200:250] = 0
img [200:250, 280:320] = 0
#Dibujar la boca
cv.ellipse(img, (260, 290), (40, 20), 0, 0, 180, 0, -1)


cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows