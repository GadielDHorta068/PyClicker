import pyautogui
import cv2
import numpy as np
import time
import keyboard  # Para manejar la entrada del teclado
import setproctitle  # Para establecer el nombre del proceso

# Establece el nombre del proceso
setproctitle.setproctitle("word.exe")

# Función para encontrar el objeto de mayor tamaño en movimiento en la pantalla
def encontrar_objeto_mayor_movimiento():
    tiempo_inicio = time.time()

    while True:
        # Captura una imagen de la pantalla
        imagen = pyautogui.screenshot()

        # Convierte la imagen a formato OpenCV (BGR)
        frame_actual = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)

        # Convierte a escala de grises
        frame_actual_gris = cv2.cvtColor(frame_actual, cv2.COLOR_BGR2GRAY)

        # Calcula la diferencia entre frames
        if 'frame_previo_gris' not in locals():
            frame_previo_gris = frame_actual_gris.copy()

        diferencia = cv2.absdiff(frame_previo_gris, frame_actual_gris)
        _, umbral = cv2.threshold(diferencia, 30, 255, cv2.THRESH_BINARY)

        # Encuentra contornos de objetos en movimiento
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Busca el contorno del objeto más grande en movimiento
        mayor_contorno = max(contornos, key=cv2.contourArea, default=None)

        # Si se encontró un contorno válido, devuelve sus coordenadas y tamaño
        if mayor_contorno is not None:
            x, y, w, h = cv2.boundingRect(mayor_contorno)
            return x, y, w, h

        frame_previo_gris = frame_actual_gris

        # Si pasa más de 10 segundos sin encontrar ningún objeto, detiene la búsqueda
        if time.time() - tiempo_inicio > 10:
            return None

        # Espera para reducir la carga de la CPU
        time.sleep(0.1)

# Función para hacer clic en la pantalla en las coordenadas dadas
def hacer_click(x, y):
    pyautogui.click(x, y)

# Función para esperar hasta que se presione una tecla específica
def esperar_tecla(tecla):
    while True:
        if keyboard.is_pressed(tecla):
            return True
        time.sleep(0.1)

# Función para ejecutar el programa en pantalla completa
def ejecutar_en_pantalla_completa():
    # Obtiene las dimensiones de la pantalla
    ancho, alto = pyautogui.size()

    # Configura la pantalla completa
    pyautogui.FAILSAFE = False  # Desactiva la función de seguridad de PyAutoGUI
    pyautogui.PAUSE = 0.1  # Breve pausa entre operaciones de PyAutoGUI

    try:
        # Mientras no se presione la tecla 'q', sigue ejecutando
        while not keyboard.is_pressed('q'):
            coordenadas = encontrar_objeto_mayor_movimiento()
            if coordenadas:
                x, y, w, h = coordenadas
                centro_x = x + w // 2
                centro_y = y + h // 2
                hacer_click(centro_x, centro_y)
                print(f"Se hizo clic en las coordenadas ({centro_x}, {centro_y})")
            else:
                print("No se encontró ningún objeto en movimiento después de 10 segundos.")

            # Espera 1 segundo antes de buscar de nuevo
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass  # Captura la excepción de interrupción de teclado (Ctrl+C)

    print("Programa detenido.")

# Ejemplo de uso
if __name__ == "__main__":
    # Espera hasta que se presione la tecla 's' para comenzar
    print("Presiona 's' para comenzar...")
    esperar_tecla('s')

    # Ejecuta en pantalla completa
    ejecutar_en_pantalla_completa()
