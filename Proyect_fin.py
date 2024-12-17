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

#parametros flujo
lkparm = dict(winSize=(15,15), maxLevel=2,
              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

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

def update_transformations(delta):
    global translation, rotation

    mean_delta = np.mean(delta, axis=0)

    #Actualizar traslación
    translation[0] += mean_delta[0] * 0.01 #Escalar factor para suavizar
    translation[1] -= mean_delta[1] * 0.01

    #Actualizar rotacion
    rotation[1] += mean_delta[0] * 0.05 #rotacion alrededor de y
    rotation[0] -= mean_delta[1] * 0.05 #rotacion alrededor de x

def draw_points(frame, p1, p0):
    for i in range(len(p1) - 1):
        a, b = (int(x) for x in p1[i].ravel())
        c, d = (int(x) for x in p1[i + 1].ravel())
        frame = cv2.line(frame, (a, b), (c, d), (0, 255, 0), 2)

    for i in range(0, len(p1), 5):
            for j in range(5):
                if i + j < len(p1):
                    a, b = (int(x) for x in p1[i+j].ravel())
                    if i + j + 5 < len(p1):
                        c, d = (int(x) for x in p1[i+j+5].ravel())
                        frame = cv2.line(frame, (a,b), (c,d), (0,0,255), 2)
    
    for nv in p0:
        a, b = (int(x) for x in nv.ravel())
        frame = cv2.circle(frame, (a, b), 3, (0, 0, 255), -1)
    return frame

# Bucle principal
def main():
    global window, rotation, translation

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
    _, vframe = cap.read()
    vgris = cv2.cvtColor(vframe, cv2.COLOR_BGR2GRAY)

    #puntos iniciales para flujo optico
    p0 = np.float32([(50, 50), (150, 50), (250, 50),
                   (50, 150), (150, 150), (250, 150),
                   (50, 250), (150, 250), (250, 250)]).reshape(-1, 1, 2)

    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret:
            break
        fgris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #calcular flujo optico
        p1, st, err = cv2.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

        if p1 is not None:
            bp1, bp0 = p1[st == 1], p0[st == 1]
            update_transformations(bp1 - bp0)
            frame = draw_points(frame, bp1, bp0)
            p0 = p1.copy()
        else:
            #p0 = np.float32([(50, 50), (150, 50), (250, 50),
            #                 (50, 150), (150, 150), (250, 150)]).reshape(-1, 1, 2)
            pass

        #Mostrar video
        cv2.imshow('Video', frame)

        # Renderizar escena
        render()

        vgris = fgris.copy()

        #Salir con tecla ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

        glfw.poll_events()

    glfw.terminate()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
