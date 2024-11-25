import glfw
import cv2 as cv
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

if not glfw.init():
    raise Exception("GLFW no pudo inicializarse")

window = glfw.create_window(800, 800, "Ventana", None, None)
glfw.make_context_current(window)

gluPerspective(45, (800/800), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)