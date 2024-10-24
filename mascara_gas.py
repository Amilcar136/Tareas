import cv2
import numpy as np

# Cargar las máscaras que deseas agregar (asegúrate de que sean PNG con transparencia)
mascaras = [
    cv2.imread('jason.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('diablo.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('mascarapug.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('mistert.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('spider.png', cv2.IMREAD_UNCHANGED)
]

# Verificar que todas las imágenes tienen un canal alfa
for i, mascara in enumerate(mascaras):
    if mascara.shape[2] != 4:
        print(f"Error: La máscara {i + 1} no tiene canal alfa.")
        exit()

# Cargar el clasificador preentrenado de rostros
face_cascade = cv2.CascadeClassifier('C:\\Users\\amilc\\Desktop\\Python\\Grafi\\haarcascade_frontalface_alt2.xml')

# Capturar video desde la cámara
video = cv2.VideoCapture(0)

# Definir un desplazamiento para mover la máscara
desplazamiento_x = 0  # Mover 0 píxeles hacia la derecha
desplazamiento_y = 60  # Mover 60 píxeles hacia arriba

# Mostrar el menú de selección de máscara
print("Opcion 1: mascara de jason")
print("Opcion 2: mascara de diablo")
print("Opcion 3: mascara de pug")
print("Opcion 4: mascara de Mister T")
print("Opcion 5: mascara de spiderman")
opc = int(input("Ingresa la opcion que quieras (1-5): "))

# Seleccionar la máscara usando if
if opc == 1:
    mascara_seleccionada = mascaras[0]
elif opc == 2:
    mascara_seleccionada = mascaras[1]
elif opc == 3:
    mascara_seleccionada = mascaras[2]
elif opc == 4:
    mascara_seleccionada = mascaras[3]
elif opc == 5:
    mascara_seleccionada = mascaras[4]
else:
    print("Opción no válida, se usará la máscara 1 por defecto.")
    mascara_seleccionada = mascaras[0]

while True:
    # Leer cada frame del video
    ret, frame = video.read()

    if not ret:
        break

    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar los rostros en el frame
    rostros = face_cascade.detectMultiScale(frame_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Procesar cada rostro detectado
    for (x, y, w, h) in rostros:
        # Redimensionar la máscara seleccionada para que coincida con el tamaño del rostro detectado
        mascara_redimensionada = cv2.resize(mascara_seleccionada, (w, h))

        # Separar los canales de la máscara: color y alfa (transparencia)
        mascara_rgb = mascara_redimensionada[:, :, :3]
        mascara_alpha = mascara_redimensionada[:, :, 3]

        # Asegurarse de que la máscara alfa sea de tipo uint8
        mascara_alpha = cv2.convertScaleAbs(mascara_alpha)

        # Aplicar el desplazamiento a las coordenadas x e y
        x_nuevo = x + desplazamiento_x
        y_nuevo = y + desplazamiento_y

        # Evitar que la máscara salga del borde de la imagen
        if x_nuevo < 0: x_nuevo = 0
        if y_nuevo < 0: y_nuevo = 0
        if x_nuevo + w > frame.shape[1]: x_nuevo = frame.shape[1] - w
        if y_nuevo + h > frame.shape[0]: y_nuevo = frame.shape[0] - h

        # Crear una región de interés (ROI) en el frame donde colocaremos la máscara
        roi = frame[y_nuevo:y_nuevo+h, x_nuevo:x_nuevo+w]

        # Asegurarse de que la ROI y la máscara tengan el mismo tamaño
        if roi.shape [:2] == mascara_alpha.shape[:2]:
            # Invertir la máscara alfa para obtener la parte del rostro donde se aplicará la máscara
            mascara_alpha_inv = cv2.bitwise_not(mascara_alpha)

            # Enmascarar la región del rostro en la imagen original
            fondo = cv2.bitwise_and(roi, roi, mask=mascara_alpha_inv)

            # Enmascarar la máscara RGB
            mascara_fg = cv2.bitwise_and(mascara_rgb, mascara_rgb, mask=mascara_alpha)

            # Combinar el fondo (parte del rostro sin máscara) y la parte con la máscara
            resultado = cv2.add(fondo, mascara_fg)

            # Reemplazar la región del rostro con la imagen combinada
            frame[y_nuevo:y_nuevo+h, x_nuevo:x_nuevo+w] = resultado

        else:
            print("Error: El tamaño de la ROI no coincide con la máscara.")

    # Mostrar el frame con la máscara aplicada
    cv2.imshow('Video con mascara', frame)

    # Presionar 'q' para salir del loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar las ventanas
video.release()
cv2.destroyAllWindows()