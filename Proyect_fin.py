import cv2
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Variables globales
window = None
angle = 0 # Ángulo de rotación del cubo
x_opengl = 0.0
y_opengl = 0.0
scale = 0.1

# Capturar video desde la cámara
video = cv2.VideoCapture(0)

#Textura pra fondo
texture_id = None

def init():
    global texture_id

    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0) # Color de fondo
    glEnable(GL_DEPTH_TEST) # Activar prueba de profundidad para 3D

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
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, frame.shape[1], frame.shape[0], 0, GL_BGR, GL_UNSIGNED_BYTE, frame)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Dibujar un cuadrado que cubre toda la ventana
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -5)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, -5)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, -5)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, -5)
    glEnd()
    
def draw_cube(x, y, scale):
    global angle
    glPushMatrix()
    glTranslatef(x, y, -5.0) # Posición basada en los movimientos
    glScalef(scale, scale, scale) # Escalar el cubo en función de la distancia
    glRotatef(angle, 1, 1, 1) # Rotar el cubo en todos los ejes
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
    global x_opengl, y_opengl, scale
    ret, frame = video.read()
    if not ret:
        return

    # Convertir el frame a escala de grises
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque para suavizar
    frame_blur = cv2.GaussianBlur(frame_gray, (15, 15), 0)

    # Detectar los contornos
    _, thresh = cv2.threshold(frame_blur, 60, 255,
    cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

