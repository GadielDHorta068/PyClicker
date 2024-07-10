import cv2
import numpy as np
import pyautogui
import time


def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot


def detect_board(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    board_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  # Buscamos un contorno cuadrado
            board_contour = approx
            break

    if board_contour is None:
        raise Exception("No se pudo detectar el tablero.")

    return board_contour


def extract_cell_positions(board_contour):
    (x, y, w, h) = cv2.boundingRect(board_contour)
    cell_size = w // 3
    positions = []

    for row in range(3):
        for col in range(3):
            cell_x = x + col * cell_size + cell_size // 2
            cell_y = y + row * cell_size + cell_size // 2
            positions.append((cell_x, cell_y))

    return positions, (x, y, w, h)


def detect_sequence_start(initial_board, board_positions, region=None):
    while True:
        current_board = capture_screen(region)
        hsv_initial = cv2.cvtColor(initial_board, cv2.COLOR_BGR2HSV)
        hsv_current = cv2.cvtColor(current_board, cv2.COLOR_BGR2HSV)

        # Comparar solo celdas con color inicial distinto
        changed_cells = []
        for pos in board_positions:
            if pos[1] < hsv_initial.shape[0] and pos[0] < hsv_initial.shape[1]:
                initial_pixel = hsv_initial[pos[1], pos[0]]
                current_pixel = hsv_current[pos[1], pos[0]]

                if not np.array_equal(initial_pixel, current_pixel):
                    changed_cells.append(pos)

        if changed_cells:
            return current_board

        time.sleep(0.1)


def detect_sequence(board_image, positions, color_ranges):
    sequence = []
    hsv = cv2.cvtColor(board_image, cv2.COLOR_BGR2HSV)

    for pos in positions:
        if pos[1] < hsv.shape[0] and pos[0] < hsv.shape[1]:
            pixel = hsv[pos[1], pos[0]]
            for key, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(pixel, np.array(lower), np.array(upper))
                if mask.any():
                    sequence.append(pos)
                    break

    return sequence


def perform_sequence(sequence, board_origin):
    for pos in sequence:
        pyautogui.click(board_origin[0] + pos[0], board_origin[1] + pos[1])
        time.sleep(1)


def main():
    # Color ranges
    color_ranges = {
        1: ((36, 25, 25), (70, 255, 255)),  # Green
        2: ((0, 50, 50), (10, 255, 255)),  # Red
        3: ((110, 50, 50), (130, 255, 255)),  # Blue
        4: ((25, 50, 50), (35, 255, 255)),  # Yellow
    }

    # Esperar antes de empezar
    time.sleep(3)

    # Capturar la pantalla y detectar el tablero
    screen_image = capture_screen()
    try:
        board_contour = detect_board(screen_image)
    except Exception as e:
        print(f"Error al detectar el tablero: {e}")
        return

    # Extraer posiciones de las celdas
    positions, board_origin = extract_cell_positions(board_contour)

    # Definir la región de captura para el tablero
    board_region = (board_origin[0], board_origin[1], board_origin[2], board_origin[3])

    # Capturar el estado inicial del tablero
    initial_board = capture_screen(region=board_region)

    # Esperar a que comience la secuencia
    sequence_board = detect_sequence_start(initial_board, positions, region=board_region)

    # Detectar la secuencia en el tablero
    sequence = detect_sequence(sequence_board, positions, color_ranges)

    # Ejecutar la secuencia detectada
    perform_sequence(sequence, board_origin)


if __name__ == "__main__":
    main()
