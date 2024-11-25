import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_triangle(x, y, color):

    glBegin(GL_TRIANGLES)
    glColor3f(color[0], color[1], color[2])  # Rojo
    glVertex2f(x - 0.25, y - 0.25)    # Vértice inferior izquierdo
    glVertex2f(x + 0.25, y + 0.5)     # Vértice inferior derecho
    glVertex2f(x, y + 0.25)      # Vértice superior
    glEnd()
    
def triang_Pasc(rows):
    triangle = []
    for i in range (rows):
        for j in range (i + 1):
            #Calcular posicion (x, y)
            x = (j - i / 2) * 0.5
            y = -i * 0.5

            color_value = (j / (i + 1), 0.5, 1.0 - (j / (i+1)))
            triangle.append((x, y, color_value))
    return triangle

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

    triangulos = triang_Pasc(5)


    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        for (x, y, color) in triangulos:
            draw_triangle(x, y, color)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()