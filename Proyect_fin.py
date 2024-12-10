import cv2
import cv2.data
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys


# Variables globales
window = None
#angle = 0  Ángulo de rotación del cubo
x_rotation = 0.0
y_rotation = 0.0
scale = 0.1
prev_center = None

# Capturar video desde la cámara
video = cv2.VideoCapture(0)

#Textura para fondo
texture_id = None

def init():
    global texture_id

    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0) # Color de fondo
    glEnable(GL_DEPTH_TEST) # Activar prueba de profundidad para 3D
    glEnable(GL_TEXTURE_2D)

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 1.0, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

    #Generar textura
    texture_id = glGenTextures(1)

def video_background(frame):
    global texture_id

    #Cargar textura
    frame = cv2.flip(frame, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, frame.shape[1], frame.shape[0], 0, GL_BGR, GL_UNSIGNED_BYTE, frame)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Dibujar un cuadrado que cubre toda la ventana
    glDisable(GL_DEPTH_TEST)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, -1)
    glEnd()
    glEnable(GL_DEPTH_TEST)
    
def draw_cube():
    glPushMatrix()
    glTranslatef(0.0, 0.0, -5.0) # Posición basada en los movimientos
    glScalef(scale, scale, scale) # Escalar el cubo en función de la distancia
    glRotatef(x_rotation, 1, 0, 0) # Rotar el cubo en todos los ejes
    glRotatef(y_rotation, 0, 1, 0)
    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0) # Rojo
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)

    glColor3f(0.0, 1.0, 0.0) # Verde
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)

    glColor3f(0.0, 0.0, 1.0) # Azul
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)

    glColor3f(1.0, 1.0, 0.0) # Amarillo
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)

    glColor3f(1.0, 0.0, 1.0) # Magenta
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)

    glColor3f(0.0, 1.0, 1.0) # Cyan
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)

    glEnd()
    glPopMatrix()

def process_frame():
    global x_rotation, y_rotation, prev_center
    ret, frame = video.read()
    if not ret:
        return None, False

    # Convertir el frame a escala de grises
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque para suavizar
    frame_blur = cv2.GaussianBlur(frame_gray, (15, 15), 0)

    # Detectar los contornos
    _, thresh = cv2.threshold(frame_blur, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Encontrar el contorno más grande
        max_contour = max(contours, key=cv2.contourArea)
        #Calcular el centroide del contorno
        M = cv2.moments(max_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            #Comparar con el centroide anterior para determinar el movimiento
            if prev_center is not None:
                dx = cx -prev_center[0]
                dy = cy - prev_center[1]
                x_rotation += (cy- frame.shape[0] / 2) / 100.00
                y_rotation += (cx - frame.shape[1] / 2) / 100.00

            prev_center = (cx, cy)

        #Dibujar el contorno en el frame
        cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)

        return frame, True
    
    #return frame, False

def main():
    global window 

    # Inicializar GLFW7
    if not glfw.init():
        sys.exit()
        
    # Crear ventana de GLFW
    width, height = 640, 480
    window = glfw.create_window(width, height, "Cubo 3D con Control por Mano", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)

    # Configuración de viewport y OpenGL
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpiar pantalla y buffer de profundidad
        glLoadIdentity()

        # Procesar el frame para actualizar la posición y escala
        frame, valid = process_frame()
        if valid:
            video_background(frame)

        # Dibujar el cubo
        draw_cube()
        
        glfw.swap_buffers(window) # Intercambiar buffers para animación suave
        #angle += 0.1 # Incrementar el ángulo para rotación
        glfw.poll_events()

    glfw.terminate() # Cerrar GLFW al salir
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()