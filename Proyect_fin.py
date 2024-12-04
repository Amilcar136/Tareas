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

def init():

    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0) # Color de fondo
    glEnable(GL_DEPTH_TEST) # Activar prueba de profundidad para 3D

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 1.0, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

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

