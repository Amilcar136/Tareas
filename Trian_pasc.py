import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_triangle():

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glVertex2f(-0.5, -0.5)    # Vértice inferior izquierdo
    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex2f(0.5, -0.5)     # Vértice inferior derecho
    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex2f(0.0, 0.5)      # Vértice superior
    glEnd()
    

def main():
    # Inicializar GLFW
    if not glfw.init():
        return

    # Crear la ventana
    window = glfw.create_window(500, 500, "OpenGL con GLFW", None, None)
    if not window:
        glfw.terminate()
        return

    # Hacer el contexto de OpenGL actual
    glfw.make_context_current(window)

    # Establecer el color de fondo
    glClearColor(0.0, 0.0, 0.0, 1.0)

    #Proyeccion
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-5, 5, -5, 5) #Rango de vista

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        positions = [
        (-2, 0, 0),  #Triangulo 1
        (2, -2, 0),   #Triangulo 2
        ]

        for pos in positions:
            glPushMatrix()
            glTranslatef(*pos)
            draw_triangle()
            glPopMatrix()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()