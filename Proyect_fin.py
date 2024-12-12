import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

# Variables globales
window_width, window_height = 800, 600
rotation = [0, 0, 0]  # Rotación (x, y, z)
translation = [0, 0, -5]  # Traslación inicial
scale = 1.0  # Escalamiento

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, window_width / window_height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Función para dibujar el tetraedro
def draw_tetrahedron():
    glBegin(GL_TRIANGLES)
    vertices = [
        (0, 1, 0),
        (-1, -1, -1),
        (1, -1, -1),
        (0, -1, 1)
    ]
    faces = [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3)
    ]
    colors = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0)
    ]
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()


# Renderizar la escena
def render():
    global translation, rotation, scale
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Aplicar transformaciones
    glTranslatef(*translation)
    glScalef(scale, scale, scale)
    glRotatef(rotation[0], 1.0, 0.0, 0.0)
    glRotatef(rotation[1], 0.0, 1.0, 0.0)
    glRotatef(rotation[2], 0.0, 0.0, 1.0)

    draw_tetrahedron()
    glfw.swap_buffers(window)

def update_transformations(contour, width, height):
    global translation, rotation, scale

    #Calcular momentos del contorno
    moments = cv2.moments(contour)
    if moments['m00'] == 0:
        return
    
    # Centroide del contorno
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])

    # Calcular traslación
    translation[0] = (cx / width - 0.5) * 10  # Mapea el rango [0, ancho] a [-5, 5]
    translation[1] = -(cy / height - 0.5) * 10 # Invertir para OpenGL

    # Calcular escala basada en el área del contorno
    area = cv2.contourArea(contour)
    scale = 1 + (area / (width * height)) * 5

    # Calcular rotación basada en el ángulo del contorno
    rect = cv2.minAreaRect(contour)
    angle = rect[-1]
    rotation[2] = angle

# Bucle principal
def main():
    global window

    #Iniciar glfw
    if not glfw.init():
        raise Exception("No se pudo inicializar GLFW")

    window = glfw.create_window(window_width, window_height, "Figura 3D con GLFW", None, None)
    if not window:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")

    glfw.make_context_current(window)
    init_gl()

    #iniciar camara con opencv
    cap = cv2.VideoCapture(0)

    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret:
            break

        # Procesar imagen
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definir rango de color de piel en HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # Máscara para aislar la piel
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Filtrar ruido
        mask = cv2.medianBlur(mask, 5)

        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Tomar el contorno más grande
            largest_contour = max(contours, key=cv2.contourArea)
            update_transformations(largest_contour, frame.shape[1], frame.shape[0])

        # Renderizar escena
        render()

        # Mostrar video en una ventana
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        glfw.poll_events()

    glfw.terminate()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
