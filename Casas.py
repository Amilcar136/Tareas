import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Atrás
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)

    # Arriba
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para el techo
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

def draw_roof():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1)  # Rojo brillante

    # Frente
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)

    # Atrás
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(0, 2, 0)

    # Izquierda
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(0, 2, 0)

    # Derecha
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)
    glEnd()

def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()

def draw_ground2():
    """Dibuja un plano para representar la calle"""
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-7, 0.001, 2.5)
    glVertex3f(7, 0.001, 2.5)
    glVertex3f(7, 0, -2.5)
    glVertex3f(-7, 0, -2.5)
    glEnd()

def draw_edif():
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.44, 0.52)

    # Piso 1
    glVertex3f(-1, 0, -3)
    glVertex3f(1, 0, -3)
    glVertex3f(1, 3, -3)
    glVertex3f(-1, 3, -3)

    # Piso 2
    glVertex3f(-1, 3, -3)
    glVertex3f(1, 3, -3)
    glVertex3f(1, 6, -3)
    glVertex3f(-1, 6, -3)

    # Piso 3
    glVertex3f(-1, 6, -3)
    glVertex3f(1, 6, -3)
    glVertex3f(1, 9, -3)
    glVertex3f(-1, 9, -3)

    # Lados
    glVertex3f(-1, 0, -3)
    glVertex3f(-1, 9, -3)
    glVertex3f(-1, 9, -5)
    glVertex3f(-1, 0, -5)

    glColor3f(0.62, 0.71, 0.9)  # Color más oscuro para los lados
    glVertex3f(1, 0, -3)
    glVertex3f(1, 9, -3)
    glVertex3f(1, 9, -5)
    glVertex3f(1, 0, -5)

    glEnd()


def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techo

    
def draw_scene():
    """Dibuja toda la escena con 4 casas"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(10, 8, 15,  # Posición de la cámara
              0, 0, 0,    # Punto al que mira
              0, 1, 0)    # Vector hacia arriba

    # Dibujar el suelo
    draw_ground()
    draw_ground2()

    # Dibujar las casas en diferentes posiciones
    positions = [
        (-4, 0, -5),  # Casa 1
        (5, 0, -5),   # Casa 2
        (-4, 0, 5),   # Casa 3
        (5, 0, 5),    # Casa 4
        (-1, 0, -5),  # Casa 5
        (2, 0, -5),   # Casa 6
        (2, 0, 5),    # Casa 7
        (-1, 0, 5)    # Casa 8

    ]

    positions_edif = [
        (-8, 0, 3), #Edif 1
        (-8, 0, 6)
    ]


    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual 
        draw_house()        # Dibujar la casa
        glPopMatrix()


    for pos in positions_edif:
        glPushMatrix()
        glTranslatef(*pos)
        draw_edif()
        glPopMatrix()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con 4 casas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()