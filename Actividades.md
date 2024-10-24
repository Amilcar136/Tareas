# Actividades Graficación
## Fernando Amilcar Rodriguez Ramirez
## No. de control: 22121370

### Actividad 1: - Generar una imagen tipo pixel art utilizando una matriz de enteros en el rango de 0 a 255.
codigo:
```
import cv2 as cv
import numpy as np

mat = np.ones((480, 480), dtype=np.uint8) * 240

mat[0:16, 96:176] = 1
mat[16:32, 64:208] = 1
mat[32:48, 48:224] = 1
mat[48:64, 32:96] = 1
mat[48:64, 144:192] = 1
mat[48:80, 224:240] = 1
mat[64:80, 144:192] = 1
mat[64:80, 32:96] = 1
mat[80:96, 16:192] = 1
mat[80:176, 240:256] = 1
mat[96:112, 16:176] = 1
mat[112:128, 16:160] = 1
mat[128:144, 16:144] = 1
mat[144:160, 16:80] = 1
mat[160:176, 16:64] = 1
mat[176:208, 32:64] = 1
mat[176:208, 144:176] = 1
mat[176:208, 224:240:] = 1
mat[208:224, 48:80] = 1
mat[208:224, 208:224] = 1
mat[224:240, 64:112] = 1
mat[224:240, 192:208] = 1
mat[240:256, 96:192] = 1

cv.imshow ('imagen', mat)
cv.waitKey(0)
cv.destroyAllWindows
```

Resultado:

![resultado act1](resAct1.png)

### Actividad 2: - Generar al menos cinco operadores puntuales utilizando la imagen generada o una imagen previamente cargada.
Codigo act 2.1:
```
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
```

codigo act 2.2
```
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
```

Resultados codigo 1:

![res1](image.png)
![res1.1](image-1.png)

Resultados codigo 2:

![res 2](image-2.png)

### Actividad 3: - Aplicar las transformaciones geométricas vistas en clase.

codigo act 3:
```
'''transformaciones geometricas'''
#Escalar imagen
import cv2 as cv
import numpy as np

img =cv.imread('yinyang.png', 0)
x, y = img.shape
im2 = np.zeros((x,y), dtype=np.uint8)
for i in range(x):
    for j in range(y):
        im2[int(i*0.5)+50,int(j*0.5)+70] = img[i,j] #Escalar una imagen (0.5 más chica, *2 mas grande)

cv.imshow('img', img)
cv.imshow ('img2', im2)
cv.waitKey()
cv.destroyAllWindows()
```

Resultado:

![Resact3](image-5.png)

### Actividad 4: Investigar qué son las ecuaciones paramétricas.
#### ¿Qué son las ecuaciones parametricas?
Las ecuaciones paramétricas son un método para describir una curva en un espacio usando uno o más parámetros independientes. 
A diferencia de las ecuaciones cartesianas tradicionales, donde las variables (como X y Y) están relacionadas de forma directa, en las paramétricas se definen ambas variables en función de un parámetro común, generalmente denotado como t.

Por ejemplo, para una circunferencia de radio r centrada en el origen:
+ x(t) = r ⋅ cos(t)
+ y(t) = r ⋅ sen(t)

Aquí, el parámetro t recorre los valores de 0 a 2π, describiendo toda la curva.

#### Aplicaciones 
+ **Movimiento en física:** Se usa para representar trayectorias de objetos en el tiempo.
+ **Gráficos por computadora:** Se utiliza para representar formas y curvas complejas.
+ **Geometría y diseño:** Para la creación de modelos en CAD y animaciones.

#### Fuentes
+ Larson, R., Edwards, B. H. (2013). Cálculo y geometría analítica. McGraw Hill.
+ Stewart, J. (2006). Cálculo de una variable. Thomson.