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
cap = cv2.VideoCapture(0)

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

# Función para actualizar transformaciones en base a la nariz
def detect_and_update():
    global rotation, translation, scale
    ret, frame = cap.read()
    if not ret:
        return
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))
    if len(faces) > 0:
        x, y, w, h = faces[0]  # Primer rostro detectado
        height, width = gray.shape[:2]

        x, y, w, h = max(0, x), max(0, y), min(w, width - x), min(h, height - y)  # Primer rostro detectado
        if w > 0 and h > 0:  # Validar que el ROI es válido
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
        else:
            return  # Salir si no hay ROI válido

        # Detectar puntos faciales
        _, landmarks = landmark_model.fit(roi_gray, np.array([faces]))
        nose = landmarks[0][0][30]  # Punto de la nariz (landmark 30)

        # Ajustar transformaciones
        nose_x = nose[0] + x
        nose_y = nose[1] + y
        rotation[0] = (nose_y / window_height) * 360 - 180
        rotation[1] = (nose_x / window_width) * 360 - 180
        scale = 1 + (w / window_width)

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

    # Dibujar fondo (cámara)
    ret, frame = cap.read()
    if not ret:
        return
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (window_width, window_height))
    glDrawPixels(window_width, window_height, GL_RGB, GL_UNSIGNED_BYTE, frame)

    # Transformaciones y dibujo del tetraedro
    glPushMatrix()
    glTranslatef(translation[0], translation[1], translation[2])
    glScalef(scale, scale, scale)
    glRotatef(rotation[0], 1, 0, 0)
    glRotatef(rotation[1], 0, 1, 0)
    glRotatef(rotation[2], 0, 0, 1)
    draw_tetrahedron()
    glPopMatrix()

# Bucle principal
def main():
    if not glfw.init():
        print("No se pudo inicializar GLFW")
        return

    window = glfw.create_window(window_width, window_height, "Figura 3D con GLFW", None, None)
    if not window:
        glfw.terminate()
        print("No se pudo crear la ventana GLFW")
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        detect_and_update()  # Detección facial y ajustes
        render()  # Renderizar la escena
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
