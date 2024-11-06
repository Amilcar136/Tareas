import numpy as np
import cv2

def draw_isometric_triangle_prism(image, position, size):
    # Definimos los puntos del prisma triangular en coordenadas isométricas
    x, y = position
    h = size * np.sqrt(3) / 2  # Altura del triángulo

    # Puntos del prisma
    points = np.array([
        [x, y],  # Punto A (base del triángulo)
        [x + size, y],  # Punto B (base del triángulo)
        [x + size / 2, y - h],  # Punto C (cima del triángulo)
        [x, y + size],  # Punto D (base inferior)
        [x + size, y + size],  # Punto E (base inferior)
        [x + size / 2, y - h + size]  # Punto F (cima del triángulo inferior)
    ], dtype=np.int32)

    # Definimos las líneas que forman el prisma
    lines = [
        (0, 1), (1, 2), (2, 0),  # cara frontal
        (3, 4), (4, 5), (5, 3),  # cara trasera
        (0, 3), (1, 4), (2, 5)   # conexiones verticales
    ]

    # Dibujamos las líneas en la imagen
    for line in lines:
        cv2.line(image, tuple(points[line[0]]), tuple(points[line[1]]), (255, 255, 255), 2)

# Crear una imagen en negro
height, width = 600, 800
image = np.zeros((height, width, 3), dtype=np.uint8)

# Dibujar un prisma triangular isométrico en la imagen
draw_isometric_triangle_prism(image, (300, 300), 100)

# Mostrar la imagen
cv2.imshow('Res', image)
cv2.waitKey(0)
cv2.destroyAllWindows()